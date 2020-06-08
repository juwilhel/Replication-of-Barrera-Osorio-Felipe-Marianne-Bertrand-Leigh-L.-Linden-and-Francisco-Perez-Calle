"""This module contains auxiliary functions for the creation of tables in the main notebook."""

import json

import matplotlib as plt
import pandas as pd
import numpy as np
import statsmodels as sm
import statsmodels.api as sm_api

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

def create_table2(data1, data2):
    """
      Creates Table 2.
    """
    x_sancristobal = data1[['T1_treat','T2_treat']]
    x_sancristobal = sm_api.add_constant(x_sancristobal)
    x_suba = data2['T3_treat']
    x_suba = sm_api.add_constant(x_suba)
    result_sancristobal = list()
    result_suba = list()
    T_Test = list()
    Control_avg_bs = list()
    Control_avg_t = list()
    for i in ['s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_sexo_int','s_yrs','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal']:
        y_sancristobal = data1[i]
        y_suba = data2[i]
        reg_sancristobal = sm_api.OLS(y_sancristobal, x_sancristobal).fit(cov_type='cluster', cov_kwds={'groups': data1['school_code']})
        result_sancristobal.append(round(reg_sancristobal.params, 2))
        result_sancristobal.append(round(reg_sancristobal.bse, 2))
        T_Test.append(round(reg_sancristobal.t_test('T1_treat=T2_treat').effect[0], 2))
        T_Test.append(round(reg_sancristobal.t_test('T1_treat=T2_treat').sd[0][0], 2))
        reg_suba = sm_api.OLS(y_suba, x_suba).fit(cov_type='cluster', cov_kwds={'groups': data2['school_code']})
        result_suba.append(round(reg_suba.params, 2))
        result_suba.append(round(reg_suba.bse, 2))
        Control_avg_bs.append("%.2f" % round(data1.groupby(data1['control']).mean()[i][1], 2))
        Control_avg_bs.append(round(data1.groupby(data1['control']).std()[i][1], 2))
        Control_avg_t.append("%.2f" % round(data2.groupby(data2['control']).mean()[i][1], 2))
        Control_avg_t.append(round(data2.groupby(data2['control']).std()[i][1], 2))
    table21 = pd.DataFrame(result_sancristobal, index=['Possessions','Possessions SE','Utilities','Utilities SE','Durable Goods','Durable Goods SE','Physical Infrastructure','Physical Infrastructure SE','Age','Age SE','Gender','Gender SE','Years of Education','Years of Education SE','Single Head','Single Head SE','Age of Head','Age of Head SE','Years of ed., head','Years of ed., head SE','People in Household','People in Household SE','Member under 18','Member under 18 SE','Estrato','Estrato SE','SISBEN score','SISBEN score SE','Household income (1,000 pesos)','Household income (1,000 pesos) SE'])
    table21.columns = ['Control average B-S', 'Basic-Control', 'Savings-Control']
    table21['Control average B-S'] = Control_avg_bs
    table21['Basic-Savings'] = T_Test
    table22 = pd.DataFrame(result_suba, index=['Possessions','Possessions SE','Utilities','Utilities SE','Durable Goods','Durable Goods SE','Physical Infrastructure','Physical Infrastructure SE','Age','Age SE','Gender','Gender SE','Years of Education','Years of Education SE','Single Head','Single Head SE','Age of Head','Age of Head SE','Years of ed., head','Years of ed., head SE','People in Household','People in Household SE','Member under 18','Member under 18 SE','Estrato','Estrato SE','SISBEN score','SISBEN score SE','Household income (1,000 pesos)','Household income (1,000 pesos) SE'])
    table22.columns = ['Control average T', 'Tertiary-Control']
    table22['Control average T'] = Control_avg_t
    table2 = table21.join(table22)
    
    return table2


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
