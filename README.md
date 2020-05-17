This is for you idiot who run experiments like a a***. Alright, you are not idoit so that you will use this to make your experiments flow.

## Usage

Follow these rule:
- get down your training script
- prepare your arguments in yaml, let's say-args.yml
- put this into your project folder
- run your experiment: python run.py -a args.yml

## Code Logic

1. Read argument file from command line (format specified)
2. Construct argument suit based on user's and default argument file
3. Run model on every argument suit

## Argument Format

The arguments should stored in YAML file. There are two kind of argument file:
- default arguments
- user's arguments

run.py will detect whether the user argument file contains 'MODEL' fild, since model file must be specified in user's argument. Then it will check out "COMMAND' fild to figure out what kind of compiler user would like to use to run model script, if there is no 'COMMAND' fild in user's argument file, the program will use defalt, that is 'python3'

## Implementation Log

### Todo

### Obstacle

- determine the memory of a round of experiment needed so that we can take advantage of GPU capability
