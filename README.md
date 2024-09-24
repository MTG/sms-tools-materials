sms-tools-materials
==================


Material accompanying the sms-tools package (https://github.com/MTG/sms-tools), including lecture material, exercises, sounds, examples, and graphical interfaces to the sms-tools models.

Installation
------------

To install sms-tools and jupyter notebook, create a virtual environment and install the dependencies.
On Mac/Linux this will be:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Graphical Interfaces
--------------------

The graphical interface and individual example functions to the models in `interface-models`.
To execute the models GUI, change to the directory and run:

     python models_GUI.py

To execute the transformations GUI that calls various sound transformation functions, change to
the directory `interface-transformations` and run:

    python transformations_GUI.py

Exercises
---------

The exercises, in the `exercises` directory, are jupyter notebooks. To read them and do them you should install Jupyter Notebook.

Examples
---------

The examples, in the `examples` directory, are jupyter notebooks covering most of the models and transformation functions.

License
-------
All the software is distributed with the Affero GPL license (http://www.gnu.org/licenses/agpl-3.0.en.html), the lecture slides are distributed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0) license (http://creativecommons.org/licenses/by-nc-sa/4.0/) and the sounds in this repository are released under Creative Commons Attribution 4.0 (CC BY 4.0) license (http://creativecommons.org/licenses/by/4.0/)
