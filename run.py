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

def construct_cmd(model_file, arg_suit):
    """Insert compiler and model path into arg_suit.

    model_file is a path string and arg_suit should be list.

    Args:
        model_file:
        arg_suit:
    """
    arg_suit.insert(0, COMPILER)
    arg_suit.insert(0, model_file)


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

    COMPILER = 'python3'

    # Read model and argument file
    parser = argparse.ArgumentParser(description='Experiment runner')
    parser.add_argument('model', type=str, help='the file path of model training script')
    parser.add_argument('arg_yml', type=str, help='arguments yaml file')
    args = parser.parse_args()

    #TODO
    # Load argument file

    #TODO
    # Prepare all possible argument suits

    # Run experiment
    run_experiment(model, arg_suits)