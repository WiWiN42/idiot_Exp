# idiot_ML

## Code Logic

1. Read argument file from command line (format specified)
2. Construct argument suit based on user's and default argument file
3. Run model on every argument suit

## Obstacle

- determine the memory of a round of experiment needed so that we can take advantage of GPU capability

## Argument Format

The arguments should stored in YAML file. There are two kind of argument file:
- default arguments
- user's arguments

run.py will detect whether the user argument file contains 'MODEL' fild, since model file must be specified in user's argument. Then it will check out "COMMAND' fild to figure out what kind of compiler user would like to use to run model script, if there is no 'COMMAND' fild in user's argument file, the program will use defalt, that is 'python3'