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
        yml = yaml.load(open(yml_path), Loader=yaml.FullLoader)
    else:
        raise Exception("couldn\'t find YAML file {}".format(yml_path))
    return yml

def nested_dic(dic):
    """Check whether a python dictionary nested more than two layers."""
    state = False
    for top_k, top_v in dic.items():
        if isinstance(top_v, dict):
            for k, v in top_v.items():
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
        hparams: python dict, where each key is the name of a commandline argument and the value is the target value of the argument. However any argument can also be a list and so this function will calculate the cross product for all combinations of all arguments.

    Returns:

        expanded_hparams: nested tuple, each represens a set of hyper-parameters
    """
    hparam_keys = tuple(hparams.keys())
    hparam_values = []

    # turn every hyperparam into a list, to prepare for itertools.product
    for elem in hparams.values():
        if type(elem) is list:
            hparam_values.append(elem)
        else:
            hparam_values.append([elem])

    expanded_hparams = tuple(itertools.product(*hparam_values))

    return hparam_keys, expanded_hparams

def construct_cmd(keys, value_sets):
    cmd_sets = []
    for _set in value_sets:
        cmd = []
        for idx, val in enumerate(_set):
            if type(val) is bool:
                if val is True:
                    cmd.append('--{}'.format(keys[idx]))
            elif val != None:
                cmd.append('--{}'.format(keys[idx]))
                cmd.append(str(val))
        cmd_sets.append(cmd)
    return cmd_sets

def exec_cmd(cmd):
    """
    Execute a command and print stderr/stdout to the console
    """
    result = subprocess.run(cmd, stderr=subprocess.PIPE)
    if result.stderr:
        message = result.stderr.decode("utf-8")
        print(message)

def err(e):
    print(e)

def run_experiment(resource, cmd, model, hpara_sets):
    """Execute model asynchronously based on assembled hyper-parameter sets.

    Args:
        resource: dict contains resource information
        cmd: command to compile model
        model: model file to execute
        hpara_sets: string list, each string represent a hyper-parameter set
    """
    # allocate gpu
    gpu_id = get_field(resource, 'gpu')
    if not gpu_id is None:
        if gpu_id is list:
            os.environ['CUDA_VISIBLE_DEVICES']=[str(_id) for _id in gpu_id]
        elif gpu_id is int:
            os.environ['CUDA_VISIBLE_DEVICES']=str(gpu_id)
    worker = get_field(resource, 'worker', required=True)

    if os.path.exists(model):
        pool = mp.Pool(processes=worker)
        for suit in hpara_sets:
            # construct commands
            command = [cmd, model]+suit
            # execute constructed command asynchronously
            pool.apply_async(func=exec_cmd, args=(command,), error_callback=err)
        pool.close()
        pool.join()
    else:
        raise Exception("couldn\'t find model file {}".format(model))

if __name__ == '__main__':
    exp_config = load_yml(ARGS.exp_yml)

    if nested_dic(exp_config):
        raise Exception("content of {} should\'t nested more than 2 layers".format(ARGS.exp_yml))

    # get required field from experiment configuration file
    resource = get_field(exp_config, 'resource', required=True)
    cmd = get_field(exp_config, 'command', required=True)
    model = get_field(exp_config, 'model', required=True)
    hparas = get_field(exp_config, 'hyperparameter', required=True)

    # cross product hyper-parameters
    hpara_keys, hpara_sets = cross_product_hparams(hparas)
    # Construct hyper-parameter into python command
    hcmd_sets = construct_cmd(hpara_keys, hpara_sets)

    # Execution
    run_experiment(resource, cmd, model, hcmd_sets)