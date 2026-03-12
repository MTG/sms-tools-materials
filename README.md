sms-tools-materials
===================

Materials accompanying the [sms-tools](https://github.com/MTG/sms-tools) package, including:

- lecture material
- exercises
- example notebooks
- sound files
- graphical interfaces for analysis, synthesis, and transformation models

This repository is intended as a companion to the `sms-tools` library and is organized for teaching, experimentation, and interactive exploration of sound and music analysis techniques.

Overview
--------

The repository combines several kinds of learning material:

- **Examples**: Jupyter notebooks demonstrating analysis and transformation workflows
- **Exercises**: notebooks intended for hands-on practice
- **Graphical interfaces**: Tk-based applications for running common models without writing code
- **Lecture and lab material**: supporting course content
- **Audio assets**: example sounds used by notebooks and GUIs

The two main desktop interfaces are:

- [interface-models/models_GUI.py](interface-models/models_GUI.py): analysis and synthesis models
- [interface-transformations/transformations_GUI.py](interface-transformations/transformations_GUI.py): sound transformation models

Requirements
------------

You need a working Python 3 environment with the dependencies listed in [requirements.txt](requirements.txt):

- `sms-tools`
- `notebook`
- `matplotlib`
- `numpy`
- `scipy`
- `ipython`
- `essentia`
- `freesound-python`

On macOS and Linux, a typical setup is:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

On Windows, activate the environment with:

    .venv\Scripts\activate

Installation Notes
------------------

- Install dependencies from the repository root.
- Some notebooks and examples rely on audio analysis libraries that may take longer to install than standard Python packages.
- The GUIs are designed around mono WAV files, typically at **44.1 kHz**.

Repository Structure
--------------------

Main top-level directories:

- [examples](examples): example notebooks covering most models and transformations
- [exercises](exercises): exercise notebooks for practice
- [interface-models](interface-models): GUI and helper functions for analysis/synthesis models
- [interface-transformations](interface-transformations): GUI and helper functions for transformations
- [lectures](lectures): lecture resources
- [sounds](sounds): audio files used by the notebooks and interfaces

Important interface entry points:

- [interface-models/models_GUI.py](interface-models/models_GUI.py)
- [interface-transformations/transformations_GUI.py](interface-transformations/transformations_GUI.py)

Generated audio files are written to:

- [interface-models/output_sounds](interface-models/output_sounds)
- [interface-transformations/output_sounds](interface-transformations/output_sounds)

Running the Graphical Interfaces
--------------------------------

### Recommended launcher

From the repository root, run:

    python launch_gui.py

This opens a small launcher window where you can choose:

- **Models GUI**
- **Transformations GUI**

On macOS, you can also double-click [launch_gui.command](launch_gui.command).

### Models GUI

You can still launch the models interface directly:

    cd interface-models
    python models_GUI.py

This launcher gives access to several model interfaces, including DFT, STFT, sinusoidal, harmonic, stochastic, and combined models.

### Transformations GUI

You can also launch the transformations interface directly:

    cd interface-transformations
    python transformations_GUI.py

This launcher provides access to transformation workflows such as sine, harmonic, stochastic, HPS, and morphing-based transformations.

GUI Features
------------

The interface applications include:

- default example sound files resolved from the repository `sounds` folder
- scrollable windows for smaller displays
- resizable layouts
- lazy tab loading for faster startup
- clearer audio playback buttons for input and output sounds
- interactive plot windows with Matplotlib toolbar support for pan, zoom, and navigation

If a computation generates audio output, playback buttons in the interface can be used to audition the resulting WAV files.

Examples and Exercises
----------------------

The [examples](examples) and [exercises](exercises) directories contain Jupyter notebooks.

To work with them, install the dependencies and launch Jupyter from the repository root:

    jupyter notebook

or:

    python -m notebook

Example topics include:

- DFT and Fourier analysis
- STFT analysis and morphing
- sinusoidal and harmonic models
- sinusoidal plus residual / stochastic models
- sound and music description
- classification and clustering workflows

Typical Workflow
----------------

1. Create and activate a virtual environment.
2. Install the dependencies from [requirements.txt](requirements.txt).
3. Launch either GUI application or Jupyter notebooks.
4. Use audio files from [sounds](sounds) or your own mono WAV files.
5. Inspect plots, listen to outputs, and compare analysis/transformation results.

Additional Notes
----------------

- The GUI code in [interface-models](interface-models) and [interface-transformations](interface-transformations) calls corresponding `*_function.py` modules.
- Those modules are useful both as GUI backends and as compact examples of how to call `sms-tools` programmatically.
- The notebooks in [examples](examples) are the best starting point for learning the underlying concepts step by step.

License
-------

All software is distributed under the **GNU Affero GPL v3**:

- http://www.gnu.org/licenses/agpl-3.0.en.html

Lecture slides are distributed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0**:

- http://creativecommons.org/licenses/by-nc-sa/4.0/

Sounds in this repository are released under **Creative Commons Attribution 4.0**:

- http://creativecommons.org/licenses/by/4.0/
