# Student Project: Replication of Barrera-Osorio, Felipe, Marianne Bertrand, Leigh L. Linden, and Francisco Perez-Calle (2011)

This repository contains my replication of 

> Barrera-Osorio, Felipe, Marianne Bertrand, Leigh L. Linden, and Francisco Perez-Calle (2011) "Improving the Design of Conditional Transfer Programs: Evidence from a Randomized Education Experiment in Colombia." American Economic Journal: Applied Economics, 3 (2): 167-95. 

The following badges allow to easily access the project notebook.

<a href="https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/microeconometrics-course-project-juwilhel/blob/master/replication-notebook.ipynb"
   target="_parent">
   <img align="center"
  src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.png"
      width="109" height="20">
</a>
<a href="https://mybinder.org/v2/gh/HumanCapitalAnalysis/microeconometrics-course-project-juwilhel/master?filepath=replication-notebook.ipynb"
    target="_parent">
    <img align="center"
       src="https://mybinder.org/badge_logo.svg"
       width="109" height="20">
</a>

## Replication of Barrera-Osorio, Felipe, Marianne Bertrand, Leigh L. Linden, and Francisco Perez-Calle (2011)

Barrera-Osorio et al.(2011) examine the effects of three different education-based conditional cash transfer programs on academic participation. They use data from a pilot study in Bogota, Colombia and analyse whether the different designs of the programs have different effects. The authors find that all designs significantly increase school attendance and that treatments with a lump-sum payment at the time where students have to re-enroll to school or when they graduate, increase enrollment rates more strongly than treatment consisting only of a bi-monthly transfer. They conclude that the structure of the intervention can help targeting resources. 

The main part of this project is my replication of the results from Barrera_osorio et al. (2011). I illustrate their identification strategy using causal graphs, briefly discuss the empirical strategy the authors use for estimation and a critical discuss their results. In addition to the replication, I provide extensions implementing robustness checks for nthe findings presented in the paper. 

## This Repository

My replication, which is conducted using Python, is presented in the Jupyter notebook [_replication-notebook.ipynb_](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-juwilhel/blob/master/replication-notebook.ipynb). The best way to view the notebook is by downloading this [_repository_](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-juwilhel) from GitHub. Alternatively, the notebook can be viewed via mybinder or nbviewer by clicking the badges above. However, these viewing options may have issues with displaying images or coloring of certain parts (missing images can be viewed in the folder [_files_](https://github.com/HumanCapitalAnalysis/microeconometrics-course-project-juwilhel/tree/master/files)). The original paper as well as the data and code provided by the authors can be accessed [here](https://www.aeaweb.org/articles?id=10.1257/app.3.2.167). 

## Reproducibility

To ensure full reproducibility of my project, I set up a [Travis CI](https://travis-ci.org) as my continuous integration service. 

[![Build Status](https://travis-ci.org/HumanCapitalAnalysis/microeconometrics-course-project-juwilhel.svg?branch=master)](https://travis-ci.org/HumanCapitalAnalysis/microeconometrics-course-project-juwilhel)

## References

* __Barrera-Osorio, Felipe, Marianne Bertrand, Leigh L. Linden, and Francisco Perez-Calle (2011)__. "Improving the Design of Conditional Transfer Programs: Evidence from a Randomized Education Experiment in Colombia." _American Economic Journal: Applied Economics_, 3 (2): 167-95.

* __Eisenhauer, P. (2020)__. Course project template, _HumanCapitalAnalysis_, [https://github.com/HumanCapitalAnalysis/template-course-project](https://github.com/HumanCapitalAnalysis/template-course-project).
