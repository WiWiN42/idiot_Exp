from __future__ import print_function

import os
import argparse
import yaml
import itertools
import subprocess
import multiprocessing as mp

parser = argparse.ArgumentParser(description='Experiment runner')
parser.add_argument('--exp_yml', '-e', type=str, default='', help='arguments yaml file')
ARGS = parser.parse_args()

def load_yml(yml_path):
    if os.path.exists(yml_path):
        arg = yaml.load(open(yml_path), Loader=yaml.FullLoader)
    else:
        raise Exception("couldn\'t find YAML file {}".format(yml_path))
    return arg

def nested_dic(dic):
    """Check whether a python dictionary nested more than two layers."""
    state = False
    for top_k, top_v in dic.items():
        if isinstance(top_v, dict):
            for k, v in top_v.item():
                if isinstance(v, dict):
                    state = True
    return state

def get_field(dic, key, required=True):
    if required:
        assert key in dic, 'expected {} to be defined in experiment'.format(key)
    return dic[key] if key in dic else None

def cross_product_hparams(hparams):
    """Get all possible permutations of hyper-parameter values.

    Args:
        hparams: python dict, where each key is the name of a commandline arg and the value is the target value of the arg. However any arg can also be a list and so this function will calculate the cross product for all combinations of all args.

    Returns:
        expanded_hparams:
        num_cases:
    """
    hparam_values = []

    # turn every hyperparam into a list, to prep for itertools.product
    for elem in hparams.values():
        if type(elem) is list:
            hparam_values.append(elem)
        else:
            hparam_values.append([elem])

    expanded_hparams = itertools.product(*hparam_values) 

    return expanded_hparams #!!!!!!不懂

def construct_cmd(keys, value_sets):
    """
    Args:
        keys: list
        value_sets: 2-d tuple
    """
    cmd_sets =[]
    for _set in value_sets:
        cmd = []
        for i, val in enumerate(_set):
            if type(val) is bool:
                if val is True:
                    cmd.append('--{} '.format(keys[i]))
            elif val != None:
                cmd.append('--{} {} '.format(keys[i], val))
        cmd_sets.append(cmd)
    return cmd_sets

def exec_cmd(cmd):
    """
    Execute a command and print stderr/stdout to the console
    """
    result = subprocess.run(cmd, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        message = result.stderr.decode("utf-8")
        print(message)

def run_experiment(resource, cmd, model, cmd_sets):
    # allocate gpu
    gpu_id = get_field(resource, 'gpu')
    if not gpu_id is None:
        device = 'CUDA_VISIBLE_DEVICESE = {}'.format(gpu_id)
    worker = get_field(resource, 'worker', required=True)

    # check model file existence
    if os.path.exists(model):
        pool = mp.Pool(processes=worker)
        for suit in cmd_sets:
            # construct commands
            command = [device, cmd, model] + suit
            # execute constructed command
            pool.apply_async(exec_cmd, command)
        pool.close()
        pool.join()
    else:
        raise Exception("couldn\'t find model file {}".format(model))

if __name__ == '__main__':
    # load argument and configurations
    exp_config = load_yml(ARGS.exp_yml)

    # check file format
    if nested_dic(exp_config):
        raise Exception("content of {} should\'t nested more than 2 layers".format(ARGS.exp_yml))

    # get required field from experiment configuration file
    resource = get_field(exp_config, 'resource', required=True)
    cmd = get_field(exp_config, 'cmd', required=True) # string
    model = get_field(exp_config, 'model', required=True) # string(path)
    hparas = get_field(exp_config, 'hyperparameter', required=True)

    # cross product hyper-parameters
    hpara_keys = hparas.keys() # <class 'dict_keys'>
    hpara_sets = cross_product_hparams(hparas) #!!!
    # Construct hyper-parameter into python command
    hcmd_sets = construct_cmd(hpara_keys, hpara_sets)

    # Execution
    run_experiment(resource, cmd, model, hcmd_sets)