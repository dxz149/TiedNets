import os
import filecmp
import shutil
import cascades_sim as cs
import shared_functions as sf
import networkx as nx

__author__ = 'sturaroa'


def test_choose_random_nodes():
    # given
    G = nx.Graph()
    G.add_nodes_from(range(0, 11, 1))

    # when
    chosen_nodes = cs.choose_random_nodes(G, 3, seed=128)

    # then
    assert chosen_nodes == [5, 8, 9]


# tests for example 1

def test_run_ex_1_realistic():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/run_realistic.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/exp_log_realistic.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/realistic'))


def test_run_ex_1_kngc():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/run_kngc.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/exp_log_kngc.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/run_kngc'))


def test_run_ex_1_sc_th_3():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/run_sc_th_3.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/exp_log_sc_th_3.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/sc_th_3'))


def test_run_ex_1_sc_th_4():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/run_sc_th_4.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/exp_log_sc_th_4.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/sc_th_4'))


def test_run_ex_1_uniform():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_max_matching/run_uniform.ini')
    exp_log_fpath = os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_max_matching/exp_log_uniform.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_max_matching/run_uniform'))


# tests for example 2a

def test_run_ex_2a_realistic():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/run_realistic.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/exp_log_realistic.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/realistic')))


def test_run_ex_2a_kngc():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/run_kngc.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/exp_log_kngc.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/run_kngc')))


def test_run_ex_2a_sc_th_3():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/run_sc_th_3.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/exp_log_sc_th_3.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/sc_th_3')))


def test_run_ex_2a_sc_th_4():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/run_sc_th_4.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/exp_log_sc_th_4.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/sc_th_4')))


def test_run_ex_2a_uniform():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_max_matching/run_uniform.ini')
    exp_log_fpath = os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_max_matching/exp_log_uniform.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_max_matching/run_uniform')))


# tests for example 2b

def test_run_ex_2b_realistic():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/run_realistic.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/exp_log_realistic.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/realistic'))


def test_run_ex_2b_kngc():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/run_kngc.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/exp_log_kngc.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/run_kngc'))


def test_run_ex_2b_sc_th_3():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/run_sc_th_3.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/exp_log_sc_th_3.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/sc_th_3'))


def test_run_ex_2b_sc_th_4():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/run_sc_th_4.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/exp_log_sc_th_4.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_full/sc_th_4'))


def test_run_ex_2b_uniform():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_max_matching/run_uniform.ini')
    exp_log_fpath = os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_max_matching/exp_log_uniform.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2b_max_matching/run_uniform'))


# tests for example 3

def test_run_ex_3_realistic():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/run_realistic.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/exp_log_realistic.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/realistic'))


def test_run_ex_3_kngc():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/run_kngc.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/exp_log_kngc.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/run_kngc'))


def test_run_ex_3_sc_th_3():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/run_sc_th_3.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/exp_log_sc_th_3.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/sc_th_3'))


def test_run_ex_3_sc_th_4():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/run_sc_th_4.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/exp_log_sc_th_4.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_full/sc_th_4'))


def test_run_ex_3_uniform():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_max_matching/run_uniform.ini')
    exp_log_fpath = os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_max_matching/exp_log_uniform.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_3_max_matching/run_uniform'))


# test instabilities

def test_run_ex_unstable_1():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/run_sc_th_5.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/exp_log_sc_th_5.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_2a_full/sc_th_5')))


def test_run_ex_unstable_2():
    # given
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    sim_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_unstable_2/run_uniform.ini')
    exp_log_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_unstable_2/exp_log_uniform.txt')

    # when
    sf.setup_logging(logging_conf_fpath)
    cs.run(sim_conf_fpath)

    # then
    assert filecmp.cmp('log.txt', exp_log_fpath, False)  # assuming UNIX EOLs are used

    # tear down
    shutil.rmtree(os.path.normpath(
        'C:/Users/sturaroa/Documents/Simulations/test_0/ex_unstable_2/run_uniform'))


def test_choose_most_used_distr_subs():
    logging_conf_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/logging_conf.json')
    netw_a_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/A.graphml')
    netw_inter_fpath = os.path.normpath('C:/Users/sturaroa/Documents/Simulations/test_0/ex_1_full/Inter.graphml')

    # when
    sf.setup_logging(logging_conf_fpath)
    A = nx.read_graphml(netw_a_fpath)
    I = nx.read_graphml(netw_inter_fpath)
    chosen_nodes_1 = cs.choose_most_used_distr_subs(A, I, 1)
    chosen_nodes_2 = cs.choose_most_used_distr_subs(A, I, 2)
    chosen_nodes_3 = cs.choose_most_used_distr_subs(A, I, 3)

    # then
    assert chosen_nodes_1 == ['D2']
    assert sorted(chosen_nodes_2) == ['D2', 'D3']
    assert sorted(chosen_nodes_3) == ['D1', 'D2', 'D3']