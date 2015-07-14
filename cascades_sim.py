__author__ = 'sturaroa'

import os
import logging
import networkx as nx
import random
import csv
from collections import OrderedDict
import shared_functions as sf

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


# global variables
logger = None
time = None

# choose node_cnt random nodes
def choose_random_nodes(G, node_cnt, seed=None):
    candidates = G.nodes()
    my_random = random.Random(seed)
    my_random.shuffle(candidates)
    chosen_nodes = list()
    for i in range(0, node_cnt):
        chosen_nodes.append(candidates[i])
    return chosen_nodes


def choose_nodes_by_betweenness_centrality(G, node_cnt, seed=None):
    nodes_with_rank = nx.betweenness_centrality(G, seed=seed)
    # sort the dictionary by value first and then by key (so we have a deterministic sorting)
    nodes_with_rank = OrderedDict(sorted(nodes_with_rank.items(), key=lambda (k, v): (v, k)))
    chosen_nodes = list()
    # choose the first nodes from the ordered dictionary
    for i, node in enumerate(nodes_with_rank):
        if i >= node_cnt:
            break
        chosen_nodes.append(node)
    return chosen_nodes


def choose_most_used_distr_subs(G, I, node_cnt, seed=None):
    # select distribution substations from G
    # get the in-degree of each distribution substation from I
    # make that a list of tuples
    dist_subs_with_rank = list()
    for node in G.nodes():
        role = G.node[node]['role']
        if role == 'distribution_substation':
            rank = I.in_degree()
            dist_subs_with_rank.append((rank, node))

    # sort the data structure by degree and node id
    dist_subs_with_rank.sort()

    # pick the first node_cnt nodes from the data structure
    # put them in a list and return it
    chosen_nodes = list()
    for i, rank_and_node in enumerate(dist_subs_with_rank):
        if i >= node_cnt:
            break
        chosen_nodes.append(rank_and_node[1])
    return chosen_nodes


# find nodes that are not in the giant component, used by the basic models
def find_nodes_not_in_giant_component(G):
    unsupported_nodes = list()
    components = sorted(nx.connected_components(G), key=len, reverse=True)

    for component_idx in range(1, len(components)):
        for node in components[component_idx]:
            unsupported_nodes.append(node)

    return unsupported_nodes


# find nodes that have no inter-link, used by the basic models and by the realistic model
def find_nodes_without_inter_links(G, I):
    unsupported_nodes = list()

    for node in G.nodes():
        if I.has_node(node):
            supporting_nodes = I.neighbors(node)
            if len(supporting_nodes) <= 0:
                unsupported_nodes.append(node)
        else:
            unsupported_nodes.append(node)

    return unsupported_nodes


# find nodes that are in clusters with size smaller than the minimum size
def find_nodes_in_smaller_clusters(G, min_cluster_size):
    unsupported_nodes = list()
    components = sorted(nx.connected_components(G), key=len, reverse=True)

    for component in components:
        if len(component) < min_cluster_size:
            for node in component:
                unsupported_nodes.append(node)

    return unsupported_nodes


# find nodes in small clusters without any inter links, used by the small clusters model
def find_nodes_in_unsupported_clusters(G, I):
    unsupported_nodes = list()
    components = sorted(nx.connected_components(G), key=len, reverse=True)

    for component in components:
        support_found = False
        for node in component:
            if I.has_node(node):
                if len(I.neighbors(node)) > 0:
                    support_found = True
                    break
        if support_found is False:
            for node in component:
                unsupported_nodes.append(node)

    return unsupported_nodes


# find substation nodes in the power network that are not connected to a generator, used by the realistic model
def find_unpowered_substations(G):
    unsupported_nodes = list()

    # divide nodes by role
    generators = list()
    substations = list()
    for node in G.nodes():
        role = G.node[node]['role']
        if role == 'generator':
            generators.append(node)
        elif role in ['transmission_substation', 'distribution_substation']:
            substations.append(node)

    # find out which substations are not powered by a generator
    for substation in substations:
        support_found = False
        for generator in generators:
            if nx.has_path(G, substation, generator):
                support_found = True
                break
        if support_found is False:
            unsupported_nodes.append(substation)

    return unsupported_nodes


# find nodes of the power grid that have no access to a control center, used by the realistic model
def find_uncontrolled_pow_nodes(A, B, I):
    unsupported_nodes = list()

    for node_a in A.nodes():
        support_controllers = list()
        support_relays = list()
        if I.has_node(node_a):
            for node_b in I.neighbors(node_a):
                role = B.node[node_b]['role']
                if role == 'relay':
                    support_relays.append(node_b)
                elif role == 'controller':
                    support_controllers.append(node_b)

        support_found = False
        if len(support_controllers) >= 1:
            if len(support_relays) >= 1:
                for controller in support_controllers:
                    for relay in support_relays:
                        if nx.has_path(B, controller, relay):
                            support_found = True
                            break
                    if support_found is True:
                        break

        if support_found is False:
            unsupported_nodes.append(node_a)

    return unsupported_nodes


def save_state(time, A, B, I, results_dir):
    netw_a_fpath_out = os.path.join(results_dir, str(time) + '_' + A.graph['name'] + '.graphml')
    nx.write_graphml(A, netw_a_fpath_out)
    netw_b_fpath_out = os.path.join(results_dir, str(time) + '_' + B.graph['name'] + '.graphml')
    nx.write_graphml(B, netw_b_fpath_out)
    netw_inter_fpath_out = os.path.join(results_dir, str(time) + '_' + I.graph['name'] + '.graphml')
    nx.write_graphml(I, netw_inter_fpath_out)


# this function will be called from another script, each time with a different configuration fpath
def run(conf_fpath):
    global logger
    logger = logging.getLogger(__name__)
    logger.info('conf_fpath = ' + conf_fpath)

    global time
    time = 0

    if not os.path.isfile(conf_fpath):
        raise ValueError('Invalid value for parameter "conf_fpath", no such file.\nPath: ' + conf_fpath)

    config = ConfigParser()
    config.read(conf_fpath)

    # read graphml files and instantiate network graphs

    seed = config.get('run_opts', 'seed')

    netw_dir = os.path.normpath(config.get('paths', 'netw_dir'))
    netw_a_fname = config.get('paths', 'netw_a_fname')
    netw_a_fpath_in = os.path.join(netw_dir, netw_a_fname)
    A = nx.read_graphml(netw_a_fpath_in, node_type=str)

    netw_b_fname = config.get('paths', 'netw_b_fname')
    netw_b_fpath_in = os.path.join(netw_dir, netw_b_fname)
    B = nx.read_graphml(netw_b_fpath_in, node_type=str)

    netw_inter_fname = config.get('paths', 'netw_inter_fname')
    netw_inter_fpath_in = os.path.join(netw_dir, netw_inter_fname)
    I = nx.read_graphml(netw_inter_fpath_in, node_type=str)

    # read run options

    attacked_netw = config.get('run_opts', 'attacked_netw')
    attack_tactic = config.get('run_opts', 'attack_tactic')
    if attack_tactic not in ['random', 'targeted', 'betweenness_centrality']:
        raise ValueError('Invalid value for parameter "attack_tactic": ' + attack_tactic)
    if attack_tactic in ['random', 'betweenness_centrality']:
        attack_cnt = config.getint('run_opts', 'attacks')
    intra_support_type = config.get('run_opts', 'intra_support_type')
    if intra_support_type not in ['giant_component', 'cluster_size', 'realistic']:
        raise ValueError('Invalid value for parameter "intra_support_type": ' + intra_support_type)
    inter_support_type = config.get('run_opts', 'inter_support_type')
    # if inter_support_type not in ['node_interlink', 'cluster_interlink', 'realistic']:
    if inter_support_type not in ['node_interlink', 'realistic']:
        raise ValueError('Invalid value for parameter "inter_support_type": ' + inter_support_type)

    if intra_support_type == 'cluster_size':
        min_cluster_size = config.getint('run_opts', 'min_cluster_size')

    # read output paths

    results_dir = os.path.normpath(config.get('paths', 'results_dir'))
    run_stats_fname = config.get('paths', 'run_stats_fname')
    run_stats_fpath = os.path.join(results_dir, run_stats_fname)
    end_stats_fpath = os.path.normpath(config.get('paths', 'end_stats_fpath'))

    # ensure output directories exist and are empty
    sf.ensure_dir_exists(results_dir)
    sf.ensure_dir_exists(os.path.dirname(end_stats_fpath))

    # stability check
    unstable_nodes = set()
    if inter_support_type == 'node_interlink':
        unstable_nodes.update(find_nodes_without_inter_links(A, I))
    # elif inter_support_type == 'cluster_interlink':
    #     unstable_nodes.update(find_nodes_in_unsupported_clusters(A, I))
    elif inter_support_type == 'realistic':
        unstable_nodes.update(find_uncontrolled_pow_nodes(A, B, I))

    if intra_support_type == 'giant_component':
        unstable_nodes.update(find_nodes_not_in_giant_component(A))
    elif intra_support_type == 'cluster_size':
        unstable_nodes.update(find_nodes_in_smaller_clusters(A, min_cluster_size))
    elif intra_support_type == 'realistic':
        unstable_nodes.update(find_unpowered_substations(A))

    if inter_support_type == 'node_interlink':
        unstable_nodes.update(find_nodes_without_inter_links(B, I))
    # elif inter_support_type == 'cluster_interlink':
    #     unstable_nodes.update(find_nodes_in_unsupported_clusters(B, I))
    elif inter_support_type == 'realistic':
        unstable_nodes.update(find_nodes_without_inter_links(B, I))

    if intra_support_type == 'giant_component':
        unstable_nodes.update(find_nodes_not_in_giant_component(B))
    elif intra_support_type == 'cluster_size':
        unstable_nodes.update(find_nodes_in_smaller_clusters(B, min_cluster_size))
    # elif intra_support_type == 'realistic':
    #     unstable_nodes.update(list())

    if len(unstable_nodes) > 0:
        logger.debug('Time {}) {} nodes unstable before the initial attack: {}'.format(
            time, len(unstable_nodes), sorted(unstable_nodes, key=sf.natural_sort_key)))

    total_dead_a = 0
    total_dead_b = 0

    # execute simulation of failure propagation
    with open(run_stats_fpath, 'wb') as run_stats_file:

        run_stats = csv.DictWriter(run_stats_file, ['time', 'total_dead_A', 'total_dead_B'], delimiter='\t',
                                   quoting=csv.QUOTE_MINIMAL)
        run_stats.writeheader()
        time += 1

        # perform initial attack
        if attacked_netw == A.graph['name']:
            if attack_tactic == 'random':
                attacked_nodes = choose_random_nodes(A, attack_cnt, seed)
            elif attack_tactic == 'betweenness_centrality':
                attacked_nodes = choose_nodes_by_betweenness_centrality(A, attack_cnt, seed)
            elif attack_tactic == 'targeted':
                target_nodes = config.get('run_opts', 'target_nodes')
                attacked_nodes = [node for node in target_nodes.split()]  # split list on space
            else:
                raise ValueError('Invalid value for parameter "attack_tactic": ' + attack_tactic)
            total_dead_a = len(attacked_nodes)
            logger.info('Time {}) {} nodes of network {} failed because of initial attack: {}'.format(
                time, total_dead_a, A.graph['name'], sorted(attacked_nodes, key=sf.natural_sort_key)))
            A.remove_nodes_from(attacked_nodes)
        elif attacked_netw == B.graph['name']:
            if attack_tactic == 'random':
                attacked_nodes = choose_random_nodes(B, attack_cnt, seed)
            elif attack_tactic == 'betweenness_centrality':
                attacked_nodes = choose_nodes_by_betweenness_centrality(B, attack_cnt, seed)
            elif attack_tactic == 'targeted':
                target_nodes = config.get('run_opts', 'target_nodes')
                attacked_nodes = [node for node in target_nodes.split()]
            else:
                raise ValueError('Invalid value for parameter "attack_tactic": ' + attack_tactic)
            total_dead_b = len(attacked_nodes)
            logger.info('Time {}) {} nodes of network {} failed because of initial attack: {}'.format(
                time, total_dead_b, B.graph['name'], sorted(attacked_nodes, key=sf.natural_sort_key)))
            B.remove_nodes_from(attacked_nodes)
        else:
            raise ValueError('Invalid value for parameter "attacked_netw": ' + attacked_netw)
        I.remove_nodes_from(attacked_nodes)

        # save_state(time, A, B, I, results_dir)
        run_stats.writerow({'time': time, 'total_dead_A': total_dead_a, 'total_dead_B': total_dead_b})
        updated = True
        time += 1

        # phase checks

        while updated is True:
            updated = False

            # inter checks for network A
            if inter_support_type == 'node_interlink':
                unsupported_nodes_a = find_nodes_without_inter_links(A, I)
            # elif inter_support_type == 'cluster_interlink':
            #     unsupported_nodes_a = find_nodes_in_unsupported_clusters(A, I)
            elif inter_support_type == 'realistic':
                unsupported_nodes_a = find_uncontrolled_pow_nodes(A, B, I)
            failed_cnt_a = len(unsupported_nodes_a)
            if failed_cnt_a > 0:
                logger.info('Time {}) {} nodes of network {} failed for lack of inter support: {}'.format(
                    time, failed_cnt_a, A.graph['name'], sorted(unsupported_nodes_a, key=sf.natural_sort_key)))
                total_dead_a += failed_cnt_a
                A.remove_nodes_from(unsupported_nodes_a)
                I.remove_nodes_from(unsupported_nodes_a)
                updated = True
                # save_state(time, A, B, I, results_dir)
                run_stats.writerow({'time': time, 'total_dead_A': total_dead_a, 'total_dead_B': total_dead_b})
            time += 1

            # intra checks for network A
            if intra_support_type == 'giant_component':
                unsupported_nodes_a = find_nodes_not_in_giant_component(A)
            elif intra_support_type == 'cluster_size':
                unsupported_nodes_a = find_nodes_in_smaller_clusters(A, min_cluster_size)
            elif intra_support_type == 'realistic':
                unsupported_nodes_a = find_unpowered_substations(A)
            failed_cnt_a = len(unsupported_nodes_a)
            if failed_cnt_a > 0:
                logger.info('Time {}) {} nodes of network {} failed for lack of intra support: {}'.format(
                    time, failed_cnt_a, A.graph['name'], sorted(unsupported_nodes_a, key=sf.natural_sort_key)))
                total_dead_a += failed_cnt_a
                A.remove_nodes_from(unsupported_nodes_a)
                I.remove_nodes_from(unsupported_nodes_a)
                updated = True
                # save_state(time, A, B, I, results_dir)
                run_stats.writerow({'time': time, 'total_dead_A': total_dead_a, 'total_dead_B': total_dead_b})
            time += 1

            # inter checks for network B
            if inter_support_type == 'node_interlink':
                unsupported_nodes_b = find_nodes_without_inter_links(B, I)
            # elif inter_support_type == 'cluster_interlink':
            #     unsupported_nodes_b = find_nodes_in_unsupported_clusters(B, I)
            elif inter_support_type == 'realistic':
                unsupported_nodes_b = find_nodes_without_inter_links(B, I)
            failed_cnt_b = len(unsupported_nodes_b)
            if failed_cnt_b > 0:
                logger.info('Time {}) {} nodes of network {} failed for lack of inter support: {}'.format(
                    time, failed_cnt_b, B.graph['name'], sorted(unsupported_nodes_b, key=sf.natural_sort_key)))
                total_dead_b += failed_cnt_b
                B.remove_nodes_from(unsupported_nodes_b)
                I.remove_nodes_from(unsupported_nodes_b)
                updated = True
                # save_state(time, A, B, I, results_dir)
                run_stats.writerow({'time': time, 'total_dead_A': total_dead_a, 'total_dead_B': total_dead_b})
            time += 1

            # intra checks for network B
            if intra_support_type == 'giant_component':
                unsupported_nodes_b = find_nodes_not_in_giant_component(B)
            elif intra_support_type == 'cluster_size':
                unsupported_nodes_b = find_nodes_in_smaller_clusters(B, min_cluster_size)
            elif intra_support_type == 'realistic':
                unsupported_nodes_b = list()
            failed_cnt_b = len(unsupported_nodes_b)
            if failed_cnt_b > 0:
                logger.info('Time {}) {} nodes of network {} failed for lack of intra support: {}'.format(
                    time, failed_cnt_b, B.graph['name'], sorted(unsupported_nodes_b, key=sf.natural_sort_key)))
                total_dead_b += failed_cnt_b
                B.remove_nodes_from(unsupported_nodes_b)
                I.remove_nodes_from(unsupported_nodes_b)
                updated = True
                # save_state(time, A, B, I, results_dir)
                run_stats.writerow({'time': time, 'total_dead_A': total_dead_a, 'total_dead_B': total_dead_b})
            time += 1

    save_state('final', A, B, I, results_dir)  # TODO: print time of last mod

    # write statistics about the final result
    with open(end_stats_fpath, 'ab+') as end_stats_file:
        end_stats = csv.writer(end_stats_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        end_stats.writerow([total_dead_a + total_dead_b])