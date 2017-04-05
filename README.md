# RDFG - RDF Generator

Description
-----
RDFG is a module for generating a RDF-formatted file (Turtle file) from a list of triples expressed in JSON. It is a part of the information extraction framework for the EUROSTAR - QAMEL project.

Prerequisite
-----
The module is working on Python 2.7. It must be prepared to install Python 2.7 and PIP (Python Package Index) before the installation of the module.

How to install
-----
Before executing the module, we need to install all of the dependencies.
To install dependencies, execute the following command.

```
sh dependency.sh
```

To execute the module, run the service by the following command.

```
python service.py
```

The address of REST API is as follows.

```
http://(server-address):7402/service
```

The module accepts only a POST request which of content type must be "application/json".

AUTHOR(S)
---------
* Jiseong Kim, MachineReadingLab@KAIST

License
-------
Released under the MIT license (http://opensource.org/licenses/MIT).