"""
Copyright 2020 Chongqing University

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import print_function

import os
import argparse
import subprocess
import multiprocessing as mp
import yaml
import itertools
import wget

parser = argparse.ArgumentParser(description='Experiment runner')
parser.add_argument('--exp_yml', '-a', type=str, default='', help='arguments yaml file')
# parser.add_argument('--exp_name', type=str, default='', help='the name for a round of experiment')
parser.add_argument('--config_yml', '-c', type=str, default='', help='configuration yaml file')
ARGS = parser.parse_args()

def get_field(dic, key, required=True):
    if required:
        assert key in dic, 'expected {} to be defined in experiment'.format(key)
    return dic[key] if key in dic else None

def islist(elem):
    return type(elem) is list or type(elem) is tuple

def alloc_resource(config):
    """Allocate resource based on configuration.

    Args:
        config: configuration file
    """
    pass

def load_arg(arg_path):
    if os.path.exists(arg_path):
        arg = yaml.load(open(arg_path), Loader=yaml.FullLoader)
    else:
        raise Exception("couldn\'t find argument file {}".format(arg_path))
    return arg

def load_config(config_path):
    if os.path.exists(config_path):
        config = yaml.load(open(config_path), Loader=yaml.FullLoader)
    else:
        print("WARNING: couldn\'t find configuration file {}, load default configuration instead".format(config_path))
        try:
            default_config = wget.download('https://raw.githubusercontent.com/aaronyun/idiot_ML/master/example/config.yml', './config.yml')
            config = yaml.load(open(default_config), Loader=yaml.FullLoader)
        except :
            raise Exception("can\'t download configuration file from Github, please check your network connection")
    return config

def nested_dic(dic):
    """Check whether a python dictionary nested more than two layers."""
    state = False
    for top_k, top_v in dic.items():
        if isinstance(top_v, dict):
            for k, v in top_v.item():
                if isinstance(v, dict):
                    state = True
    return state

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
        if islist(elem):
            hparam_values.append(elem)
        else:
            hparam_values.append([elem])

    expanded_hparams = itertools.product(*hparam_values) 

    return expanded_hparams # 2-d tuple

def construct_cmd(keys, value_suits):
    """

    Args:
        keys: list
        value_suits: 2-d tuple
    """
    cmd_suits =[]
    for suit in value_suits:
        cmd = ''
        for i, val in enumerate(suit):
            if type(val) is bool:
                if val is True:
                    cmd += '--{} '.format(keys[i])
            elif val != None:
                cmd += '--{} {} '.format(keys[i], val)
        cmd_suits.append(cmd)
    return cmd_suits

def exec_cmd(cmd):
    """
    Execute a command and print stderr/stdout to the console
    """
    result = subprocess.run(cmd, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        message = result.stderr.decode("utf-8")
        print(message)

def run_experiment(config, cmd, model, cmd_suits):
    """

    Note that model is a plain string not any type of I/O stream, and arg_suits is a list of parameter suit.

    Args:
        model: file path to target model file
        arg_suits: cross product of input argument yaml file

    Exception:

    """
    #TODO allocate resource for this round of experiment
    resource_config = get_field(config, 'RESOURCE')
    pool_config = get_field(config, 'POOL')

    # check model file existence
    if os.path.exists(model):
        pool = mp.Pool(processes=pool_config['worker'])
        for suit in cmd_suits:
            # construct commands
            command= cmd + model + suit
            # execute constructed command
            pool.apply_async(exec_cmd, command)
        pool.close()
        pool.join()
    else:
        raise Exception("couldn\'t find model file {}".format(model))

if __name__ == '__main__':
    # Load argument and configurations
    exp = load_arg(ARGS.exp_yml)
    config = load_config(ARGS.config_yml)

    # Check argument file and load content
    if not nested_dic(exp):
        # get required field from argument file
        cmd = get_field(exp, 'CMD', required=True) # string
        model = get_field(exp, 'MODEL', required=True) # string(path)
        hpara = get_field(exp, 'PARA') # plain dictonary
    else:
        raise Exception("the content of input argument file should\'t nested more than 2 layers")

    # Cross product hyper-parameters
    hpara_keys = hpara.keys()
    hpara_suits = cross_product_hparams(hpara)
    # Construct hyper-parameter suits into command line arguments
    hcmd_suits = construct_cmd(hpara_keys, hpara_suits)

    # Execution
    run_experiment(config, cmd, model, hcmd_suits)