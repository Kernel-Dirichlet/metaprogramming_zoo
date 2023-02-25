# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 15:23:34 2023

@author: ezw19
"""

import os
import ast
from ast_utils import PythonParser, parse_extension

class DependencyInverter():
    def __init__(self,style='any'):
        self.style = style
        self.ast_parser = PythonParser()
        
    
    def make_interface(self,tokens):
        new_classes = []
        for i in range(len(tokens)):
            #import pdb ; pdb.set_trace()
            interface_dict = {'name': 'class interface{}_{}(ABC)'.format(tokens[i]['class'],tokens[i]['parent']),
                              'docstring': tokens[i]['docstring'],
                              'abstract_methods': []}

            num_methods = len(tokens[i]['methods'])
            for j in range(num_methods):
                func_name = tokens[i]['methods'][j]['name']
                arg_string = ','.join(tokens[i]['methods'][j]['args'])

                #abstract_method = 'abstractmethod name:{} arg_string:{})'.format(func_name,arg_string)
                #interface_dict['abstract_methods'].append(abstract_method)


            new_classes.append(interface_dict)
        return new_classes

    
    def tokenize_file(self,in_file):
        '''
        Tokens are in the form (child,parent)

        use AST to get class names, and then pull methods for those class names

        '''
        f = open(in_file,'r')
        self.lines = f.readlines()
        node = self.ast_parser.get_tree(in_file)

        tokens = []
        classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
        for i in range(len(classes)):
           
            if len(classes[i].bases) != 0:    
                parent = ast.parse(classes[i]).bases[0].id
            else:
                parent = ''
            cls_dict = {'class': classes[i].name,
                        'docstring': '#TODO',
                        'parent': parent,
                        'methods': []}

            methods = [j for j in classes[i].body if isinstance(j,ast.FunctionDef)]
            child_gen = ast.iter_child_nodes(node)
            for k in range(len(methods)):
                #if '__' not in methods[k].name:
                arg_list = []
                num_args = len(methods[k].args.args) #getting number of arguments for a given method
                method_dict = {'name': methods[k].name, 'args': []}

                for n in range(num_args):

                    #import pdb ; pdb.set_trace()
                    arg = methods[k].args.args[n].arg
                    method_dict['args'].append(arg)
                cls_dict['methods'].append(method_dict)
            tokens.append(cls_dict)
        return tokens
    
    def map_files(self,directory): 
        file_paths = os.walk(directory)
        paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file[-3:] == '.py':
                    paths.append('{}/{}'.format(root,file))
                    
        converted_files = 0
        for path in range(len(paths)):
            error_paths = []
            out_file = parse_extension(paths[path],ext='.py')
            out_name = '{}'.format(paths[path])
            try:
                self.map_file(in_file=paths[path],out_file=out_name)
                converted_files += 1
            except:
                error_paths.append(paths[path])
                
            
        print('{}/{} files successfully updated!'.format(converted_files,len(paths)))
        if len(error_paths) > 0: 
            f = open('./mapped_files/error_files.txt','w')
            for i in range(len(error_paths)):
                f.write('{}/n'.format(error_paths[i]))
            f.close()
        
    def map_file(self,in_file,out_file='mapped_file'):
        if not os.path.exists('./mapped_files'):
            os.makedirs('./mapped_files')

        self.tokens = self.tokenize_file(in_file)
        self.interface = self.make_interface(self.tokens)
        if out_file is None:
            name = in_file
        else:
            name = out_file
        f = open('./mapped_files/{}'.format(name),'w')
        f.write('from abc import ABC, abstractmethod\n\n')
        for i in range(len(self.interface)):
            f.write('{}:\n\t\t'.format(self.interface[i]['name']))
            f.write('{}\n\n\t\t'.format(self.tokens[i]['docstring']))
            num_methods = len(self.tokens[i]['methods'])
            for j in range(num_methods): 
                name = self.tokens[i]['methods'][j]['name']
                arg_str = ','.join(self.tokens[i]['methods'][j]['args'])
                f.write('@abstractmethod\n\t\t')
                f.write('def {}({}):\n\t\t'.format(name,arg_str))
                f.write('\tpass\n\n\t\t')
            f.write('\n')
                
        f.close()
            