# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:47:02 2023

@author: ezw19
"""

import subprocess
import ast
import re
import os
from abc import ABC, abstractmethod

parse_extension = lambda file,ext: file.split('/')[-1].split('.{}'.format(ext))[0]

class ASTParser(ABC): 
    def __init__(self,formatter='default'):
        
        self.formatter = formatter 
    
    @abstractmethod
    def get_tree(self): 
        '''
        This method generates an AST for the target language
        each subclass may consider a different language and/or version 
        '''
        pass
    
    def camel_case(self,text): 
        s = text.replace("-", " ").replace("_", " ")
        s = s.split()
        if len(text) == 0:
            return text
        return s[0] + ''.join(i.capitalize() for i in s[1:])
    
    def get_classes(self): 
        '''
        This method retrieves classes for languages with OO support
        '''
        pass
    
    def get_funcs(self):
        '''
        This method retrieves functions for languages with support for functions (outside of classes)
        
        There is nuance to the above, but the idea is there will be a seperate method in general
        for pulling methods out of classes with logic that may be different from standalone functions
        '''
        pass
    
    def get_methods(self):
        '''
        This method retrieves methods for class functions
        '''
        pass
    
class PythonParser(ASTParser):
    
    def get_tree(self,py_file): 
        
        with open(py_file,'r') as f: 
            self.node = ast.parse(f.read())
        return self.node 
    
    def get_funcs(self):
        self.functions = [n for n in self.node.body if isinstance(n, ast.FunctionDef)]
        return self.functions

    def get_classes(self):
        self.classes = [n for n in self.node.body if isinstance(n, ast.ClassDef)]
        return self.classes
    
    def get_docstring(self): 
        import pdb ; pdb.set_trace()
    
class UnitTestGenerator():
    def __init__(self,directory='.'):
        '''
        Pulls all .py files from a directory 
        Auto-generates unit tests for all class methods and functions
        '''
        self.dir = directory
        self.python_parser = PythonParser() #Dependency injection 
    
    def get_ast(self,py_file): 
        with open(py_file,'r') as f: 
             self.node = ast.parse(f.read())
        return self.node #returns python AST object 
    
   
    def script2str(self,file,mode='list'):
        '''
        method to read in script as a string or list of strings (one per line)
        '''
        f = open(file,'r')
        if mode == 'list': 
            return f.readlines()
        if mode == 'string':
            return f.read()
    
    def generate_unittests(self): 
        file_paths = os.walk(self.dir)
        paths = []
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                if file[-3:] == '.py':
                    paths.append(file)
                    
        generated_files = 0
        errors = []
        for path in range(len(paths)):
            if not os.path.exists('./unittests'):
                os.makedirs('./unittests')
            out_name = './unittests/test_{}'.format(paths[path])
            try:
                self.generate_unittest(py_file=paths[path],
                                       outfile=out_name)
                generated_files += 1
            except: 
                errors.append(paths[path])
        print('{}/{} unit test files generated!'.format(generated_files,len(paths)))
        if len(errors) > 0:
            f = open('./unittests/error_files.txt','w')
            for i in range(len(errors)): 
                f.write('{}\n'.format(errors[i]))
            f.close()
            
    def generate_unittest(self,py_file,outfile): 
        header = 'import unittest\n\n'
        in_file = py_file.split('/')[-1].split('.py')[0]
        file_ast = self.python_parser.get_tree(py_file)
        classes = self.python_parser.get_classes()
        
        #file_ast = self.get_ast(py_file)
        #classes = self.get_classes()
        
        test_classes = []
        f = open('./unittests/{}_unittest.py'.format(in_file),'w')
        f.write(header)
        for i in range(len(classes)):
            methods = [j for j in classes[i].body if isinstance(j,ast.FunctionDef)]
            if len(methods) == 0:
                continue
            f.write('class Test{}(unittest.TestCase):\n\n'.format(classes[i].name))
            for k in range(len(methods)):
                if '__' in methods[k].name:
                    continue
                args_string = ','.join([methods[k].args.args[n].arg for n in range(len(methods[k].args.args))]).replace('self,','')
                if args_string == 'self':
                    name = 'test_{}()'.format(self.python_parser.camel_case(methods[k].name))
                else:
                    name = 'test_{}({}):\n'.format(self.python_parser.camel_case(methods[k].name),
                                               args_string)
               
                f.write('  def {}\n'.format(name))
                f.write('     #TODO\n')
                body = '      pass\n\n'
                f.write(body)
                
                
               
        f.write('if __name__ == "__main__":\n\tunittest.main()')
        f.close()
        
       
    
class ShellGenerator():
    def __init__(self,
                 shell_type='sh'):
        
        self.shell_type = shell_type
        
        
    def generate_header(self):
       
        return '#!/bin/{}'.format(self.shell_type)
        
  
    def generate_repeat_script(self,
                               script,
                               interval,
                               header_comments='default'):
        '''
        Generate a shell command to repeat a script at user-defined
        time intervals
        
        NOTE: check file extension on script
        '''
        if header_comments == 'default':
            header = self.generate_header()
        else:
            header = str(input('Enter in comments for the header: '))
        if self.shell_type in ['sh','bash','csh','ksh','zsh']: 
           
            name = parse_extension(script,self.shell_type)
            body = 'sudo chmod +x {}\nwhile ./{}; do sleep {}; done'.format(script,script,interval)
            f = open('{}_repeat.sh'.format(name),'w+')
            f.write('{}\n'.format(header))
            f.write(body)
            f.close()
            
        else:
            return 'only SH, BASH, CSH, KSH, and ZSH currently supported'
        

    