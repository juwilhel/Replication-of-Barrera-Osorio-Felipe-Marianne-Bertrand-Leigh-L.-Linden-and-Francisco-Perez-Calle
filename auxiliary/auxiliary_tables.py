"""This module contains auxiliary functions for the creation of tables in the main notebook."""

import json

import matplotlib as plt
import pandas as pd
import numpy as np
import statsmodels as sm

from auxiliary.example_project_auxiliary_predictions import *
from auxiliary.example_project_auxiliary_plots import *
from auxiliary.example_project_auxiliary_tables import *


def color_pvalues(value):
    """
    Color pvalues in output tables.
    """

    if value < 0.01:
        color = "darkorange"
    elif value < 0.05:
        color = "red"
    elif value < 0.1:
        color = "magenta"
    else:
        color = "black"

    return "color: %s" % color


def create_table1(data):
    """
      Creates Table 1.
    """
    table1 = pd.crosstab(data.grade_group, [data.suba, data.group], colnames=['Experiment', 'Group'], margins=True, margins_name="Total")
    table11 = table1.drop(index = "Total")
    table12 = pd.crosstab(data.r_be_gene, [data.suba, data.group], margins=True, margins_name="Total")
    table1 = table11.append(table12).rename(index={"F": "Female", "M": "Male"}, columns={0.0: "Basic-Savings", 1.0: "Tertiary"})
    
    return table1


def create_table6(dictionary, keys, regressors):
    """
      Creates Table 6.
    """
    table6 = pd.concat([estimate_RDD_multiple_datasets(dictionary=dictionary,
                                                       keys=keys,
                                                       outcome='gradin4',
                                                       regressors=regressors),
                        estimate_RDD_multiple_datasets(dictionary=dictionary,
                                                       keys=keys,
                                                       outcome='gradin5',
                                                       regressors=regressors),
                        estimate_RDD_multiple_datasets(dictionary=dictionary,
                                                       keys=keys,
                                                       outcome='gradin6',
                                                       regressors=regressors),
                        ], axis=1
                       )
    table6.columns = pd.MultiIndex.from_product([['Graduated after 4 years',
                                                  'Graduated after 5 years',
                                                  'Graduated after 6 years'],
                                                 ['GPA below cutoff (1)', 'P-Value (1)', 'Std.err (1)',
                                                  'Intercept (0)', 'P-Value (0)', 'Std.err (0)',
                                                  'Observations']
                                                 ])
    return table6


def describe_covariates_at_cutoff(data, bandwidth):
    """
      Summary table used for validity checks. 
    """
    variables = ['hsgrade_pct', 'totcredits_year1', 'age_at_entry', 'male', 'english', 
                 'bpl_north_america','loc_campus1', 'loc_campus2', 'loc_campus3']

    treat = pd.DataFrame()
    untreat = pd.DataFrame()

    sample = data[abs(data['dist_from_cut']) < bandwidth]
    sample_treat = sample[sample['dist_from_cut'] < 0]
    sample_untreat = sample[sample['dist_from_cut'] >= 0]

    # treated sample.
    treat['Mean'] = sample_treat[variables].mean()
    treat['Std.'] = sample_treat[variables].std()
    # untreated sample.
    untreat['Mean'] = sample_untreat[variables].mean()
    untreat['Std.'] = sample_untreat[variables].std()

    table = pd.concat([treat, untreat], axis=1)
    table.columns = pd.MultiIndex.from_product([['Below cutoff', 'Above cutoff'],
                                                ['Mean', 'Std.']])
    table = table.astype(float).round(2)

    table['Description'] = ["High School Grade Percentile", "Credits attempted first year", 
                            "Age at entry", "Male", "English is first language", 
                            "Born in North America", "At Campus 1", "At Campus 2", "At Campus 3"]

    return table
