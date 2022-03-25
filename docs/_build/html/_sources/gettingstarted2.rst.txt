Getting Started
===============

The survey simulator post processing code can be used with any orbital calculator code. We recommend using `Objects in Field <https://github.com/eggls6/objectsInField>`_, 
but you can use any, as long as the orbital parameters are in a compatible format.

The first step is running Objects in Field which will produce a set of ephemerides to be used throughout the simulation. 




Running Objects in Field
----------------------------------
After successfully installing Objects in Field, the code should be run in the main directory. In order to use OIF run::

   $python main.py configfile > output
   
Here, configfile is the name of the configuration file which contains the input parameters for the simulation.

By default, OIF will not allow you to overwrite files. In order to do so, run::

   $python main.py -f configfile > output


**Configuration File**

The configuration file contains a list of input parameters for each simulation. Each config file is composed of 
four sections, which are titled [ASTEROID], [SURVEY], [OUTPUT] and [CAMERA]. Within each section is a list of 
keywords which each have an associated value. The keywords are described below. An ***** indicates that the 
keyword is mandatory.


+----------+-------------------------+--------------------+-------------------------+
| Section  | Keyword                 | Default Value      | Description             |
+==========+=========================+====================+=========================+
| ASTEROID | *Population Model       | NA                 |                         |
+----------+-------------------------+--------------------+-------------------------+
| ASTEROID | *Asteroid SPK path      | NA                 |                         |
+----------+-------------------------+--------------------+-------------------------+
| ASTEROID | *Asteroid SPKs          | NA                 |                         |
+----------+-------------------------+--------------------+-------------------------+
| ASTEROID | Object1                 | 1                  |                         |
+----------+-------------------------+--------------------+-------------------------+