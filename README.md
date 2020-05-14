# idiot_ML

## The basic logic of this project:

1. Read model file, argument file (both of which are strings) and result folder from command line
2. Prepare parameter suits based on the given argument file
3. For each parameter suit, we execute the model file with this suit
4. Store the output of each run into specified folder

## todo

- 对于读入的model和argument，以及result的文件路径是否有要求
- 参数文件的格式具体要求，结果保存的具体格式要求
- 如果一次实验的次数很多，总的内存占用超过了指定的gpu数量的总内存，如何确定worker（run次数）数量