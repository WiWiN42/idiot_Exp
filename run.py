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
import yaml
import itertools

from .util import nested_dic, get_field

parser = argparse.ArgumentParser(description='Experiment runner')
parser.add_argument('--arg_yml', type=str, help='arguments yaml file')
parser.add_argument('--exp_name', type=str, default='', help='the name for a round of experiment')
ARGS = parser.parse_args()

# Load Argument File and Construct Command

def load_yml(arg_path):
    """Load YAML file and check format.

    Args:
        arg_path: the path of argument file

    Returns:
        raw_args: argument read from given path, of python dictionary

    Exception:
    """
    if os.path.exists(arg_path):
        raw_args = yaml.load(open(arg_path), Loader=yaml.FullLoader)

        # make sure YAML file nested less than 2 layers
        if nested_dic(raw_args):
            raise Exception("Format error, please rearrange you parameters in input YAML file")

    else:
        raise Exception("couldn\'t find argument file {}".format(arg_path))

    return raw_args

def islist(elem):
    return type(elem) is list or type(elem) is tuple

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

    # have to do this in order to know length
    expanded_hparams, dup_expanded = itertools.tee(expanded_hparams, 2)
    expanded_hparams = list(expanded_hparams)
    num_cases = len(list(dup_expanded))

    return expanded_hparams, num_cases

# def assemble_suit(raw_dic):
#     """Get cross product of all parameters and assemble into suits.

#     Args:
#         raw_dic: a python dictionary containing arguments read from yaml file,

#     Returns:
#         suits:

#     Exception:
#     """
#     command = get_field(raw_dic, 'CMD')
#     para = get_field(raw_dic, 'PARA', required=False)

    

    

#     return suits

def construct_cmd(suit):
    cmd = ''
    for key, val in suit.items():
        if type(val) is bool:
            if val is True:
                cmd += '--{} '.format(key)
        elif val != 'None':
            cmd += '--{} {} '.format(key, val)
    return cmd

def exec_cmd(cmd):
    """
    Execute a command and print stderr/stdout to the console
    """
    result = subprocess.run(cmd, stderr=subprocess.PIPE, shell=True)
    if result.stderr:
        message = result.stderr.decode("utf-8")
        print(message)

def run_experiment(model, arg_suits):
    """Run experiment based on given model and argument suits.

    Note that model is a plain string not any type of I/O stream, and arg_suits is a list of parameter suit.

    Args:
        model: file path to target model file
        arg_suits: cross product of input argument yaml file

    Exception:

    """
    # check model file existence
    if os.path.exists(model):
        for suit in arg_suits:
            # construct commands
            cmd = construct_cmd(model, suit)
            # execute constructed command
            exec_cmd(cmd)
    else:
        raise Exception("couldn\'t find model file {}".format(model))

if __name__ == '__main__':

    # Load argument file
    raw_args = load_yml(ARGS.arg_yml)

    # Prepare all possible argument suits
    arg_suits = assemble_suit(raw_args)

    # Run experiment
    run_experiment(arg_suits)