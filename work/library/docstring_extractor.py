# -*- coding: utf-8 -*-
import os
import ast
import glob
import pprint

os.chdir(r'C:\Users\Skufler\PycharmProjects\cb_ru\work\backend\cb_ru')
files = glob.glob('**/*.py', recursive=True)


def print_callable_signature(target: callable):
    args = [a.arg for a in target.args.args]

    print('def ' + target.name + '(' + str(args)[1:-1].replace('\'', '') + '):')
    s = ast.get_docstring(target)
    if s is not None:
        for value in s.split('\n'):
            print('\t', value) 
    print()


for filename in files:
    with open(filename, encoding='utf-8') as fd:
        file_contents = fd.read()

    module = ast.parse(file_contents)
    function_definitions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
    class_definitions = [node for node in module.body if isinstance(node, ast.ClassDef)]

    clss = []
    method_definitions = []

    for class_def in class_definitions:
        clss.append(class_def)
        method_definitions.append([node for node in class_def.body if isinstance(node, ast.FunctionDef)])

    print('Module ' + filename)
    print(ast.get_docstring(module))
    for index, methods in enumerate(method_definitions):
        print('class ' + clss[index].name + ':')
        print(ast.get_docstring(clss[index]))
        for method in methods:
            print_callable_signature(method)

    for function in function_definitions:
        print_callable_signature(function)
