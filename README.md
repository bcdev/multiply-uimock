# multiply-uimock

A GUI mock for the [Multiply](https://github.com/multiply-org) project based on
[Jupyter Widgets](https://ipywidgets.readthedocs.io) and [Bokeh](https://bokeh.pydata.org).

# Installation

Create environment:

    $ cd multiply-uimock
    $ conda env create

Activate environment and install sources:

    $ source activate muimock

Install jupyter-widgets extension for Jupyter-Lab

    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager

Install muimock from source code:

    $ python setup.py develop

Run Jupyter Lab

    $ jupyter-lab notebooks/muimock.ipynb

# Options

* Define custom widgets that are implemented using JavaScript 
  (e.g. Leaflet Map, Cesium Globe)
* Using Bokeh for plotting and as visualisation server



# Related Reads

* Jupyter Lab: https://jupyterlab.readthedocs.io
* Jupyter Widgets: https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html
* Bokeh docs: https://bokeh.pydata.org/en/latest/docs/user_guide/notebook.html
* Bokeh examples: https://github.com/bokeh/bokeh/tree/1.0.4/examples/howto/notebook_comms

* Integrating your objects with IPython: https://ipython.readthedocs.io/en/stable/config/integrating.html