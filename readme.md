# Recycling

This project is about modeling and linear optimization of a municipal solid waste recycling system. We allow 

* distinguished types of waste 
* arbitrary processing facilities that admit a linear description
* unsorted waste and sorting facilities
* graphical output through SVG files

and optimize over the material flow as well as capacities if needed.

# What we answer?

* Is recycling worth it? 
* Is sorting worth it?
* What is a sustainable recycling policy?
* What capacities are best allocated for facilities?

# How does it work?
We use [Python 3](https://www.python.org/downloads/) and the LP solver [PuLP](https://pythonhosted.org/PuLP/). Separate installation of PuLP is necessary and works best with the Python script `EasyInstall`. [**Installation guide**](https://pythonhosted.org/PuLP/main/installing_pulp_at_home.html#installation)

Then just run `python recycling.py`.