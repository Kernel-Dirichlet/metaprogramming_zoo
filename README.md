# METAPROGRAMMING ZOO 

Metaprogramming is a broad software branch in which programs are themselves inputs & outputs from/to other programs. While most metaprogramming techniques
are more concerned with low-level optimization (ex. C++ template metaprogramming), this repository will be more focused on metaprogramming at a higher level
of software abstraction. Often times, the performance boosts of low-level metaprogramming optimizations fail to justify the technical sophistication needed to write the code to achieve the boosts. For this repository in particular, there will be an emphasis on two key metaprogramming subdomains: 

1) **Generative programming** - using programs to generate other programs

2) **Reflexive programming** - programs which modify themselves, often at run-time. 

As of 2/26/2023, this repository uses Python exclusively, but the bulk of future code will be written in Julia which has a similar syntax to Python but more features for both high and low level metaprogramming support. Bindings to other languages will be provided if sufficient interest in the project crosses a threshold. 


### Object Dependency Inversion 
   - Performs dependency inversion between two classes A and B where B inherits from A. Here, an interface class C is created
     where class B inherits interface C and class A references it. 
   - Usage: Simply import the DependencyInverter object and call the "map_files" method to walk a directory. The "map_files" method will 
     determine dependency relationships among classes and invert dependencies. 
   - **NOTE: Preserving docstrings from class A and B is an upcoming feature!**
 
     
```python
from dependency_inverter import DependencyInverter
inverter_obj = DependencyInverter()
inverter_obj.map_files('/path_do_dir') #walks a directory and inverts class dependencies
```

### Unit Test Template Generation 
   - automatically generates unit test templates for each function and method for .py files in a given directory. 
   - Simply import the UnitTestGenerator object, pass in a directory, and call the "generate_unittests" method. 
   - **NOTE**: Since Python is dynamically typed, applying robust type inference is an upcoming feature. With type inference,
     it will be possible (in some cases) to generate the unit tests *themselves* rather than templates only. 
   
     
```python
from ast_utils import UnitTestGenerator
test_obj = UnitTestGenerator('/path_to_dir')
test_obj.generate_unittests() #walks a directory and generates unit test templates for each .py file
```
