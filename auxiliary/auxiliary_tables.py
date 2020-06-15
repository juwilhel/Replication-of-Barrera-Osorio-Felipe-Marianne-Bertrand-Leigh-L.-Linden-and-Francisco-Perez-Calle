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

def create_table34(data1, data2, data3, variable):
    """
      Creates Table 3 and 4.
    """
    result_sancristobal = list()
    result_sancristobal1 = list()
    result_sancristobal2 = list()
    result_sancristobal3 = list()
    result_suba = list()
    result_suba1 = list()
    result_suba2 = list()
    result_suba3 = list()
    result_both = list()
    r2_sancristobal = list()
    r2_suba = list()
    y_sancristobal = data1[variable]
    y_suba = data2[variable]
    for i in [['T1_treat','T2_treat'],['T1_treat','T2_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age'],['T1_treat','T2_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']]:
        x_sancristobal = data1[i]
        x_sancristobal = sm_api.add_constant(x_sancristobal)
        reg_sancristobal = sm_api.OLS(y_sancristobal, x_sancristobal).fit(cov_type='cluster', cov_kwds={'groups': data1['school_code']})
        result_sancristobal.append(round(reg_sancristobal.params[1], 3))
        result_sancristobal.append(round(reg_sancristobal.bse[1], 3))
        result_sancristobal.append(round(reg_sancristobal.params[2], 3))
        result_sancristobal.append(round(reg_sancristobal.bse[2], 3))
        result_sancristobal.append(round(reg_sancristobal.f_test('T1_treat=T2_treat').fvalue[0][0], 3))
        result_sancristobal.append(round(float(reg_sancristobal.f_test('T1_treat=T2_treat').pvalue), 3))
        r2_sancristobal.append(round(reg_sancristobal.rsquared, 3))
    result_sancristobal1.append(result_sancristobal[0:6])
    result_sancristobal2.append(result_sancristobal[6:12])
    result_sancristobal3.append(result_sancristobal[12:])
    i = 4
    while i < 6:
        result_sancristobal1[0].insert(i, '')
        result_sancristobal2[0].insert(i, '')
        result_sancristobal3[0].insert(i, '')
        result_sancristobal1[0].append('')
        result_sancristobal2[0].append('')
        result_sancristobal3[0].append('')
        i += 1
    result_sancristobal1[0].append(len(y_sancristobal))
    result_sancristobal2[0].append(len(y_sancristobal))
    result_sancristobal3[0].append(len(y_sancristobal))
    result_sancristobal1[0].append(r2_sancristobal[0])
    result_sancristobal2[0].append(r2_sancristobal[1])
    result_sancristobal3[0].append(r2_sancristobal[2])
    for i in [['T3_treat'],['T3_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age'],['T3_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']]:
        x_suba = data2[i]
        x_suba = sm_api.add_constant(x_suba, has_constant='add')
        reg_suba = sm_api.OLS(y_suba, x_suba).fit(cov_type='cluster', cov_kwds={'groups': data2['school_code']})
        result_suba.append(round(reg_suba.params[1], 3))
        result_suba.append(round(reg_suba.bse[1], 3))
        r2_suba.append(round(reg_suba.rsquared, 3))
    result_suba1.append(result_suba[0:2])
    result_suba2.append(result_suba[2:4])
    result_suba3.append(result_suba[4:])
    i = 1
    while i < 5:
        result_suba1[0].insert(0, '')
        result_suba2[0].insert(0, '')
        result_suba3[0].insert(0, '')
        result_suba1[0].append('')
        result_suba2[0].append('')
        result_suba3[0].append('')
        i += 1
    result_suba1[0].append(len(y_suba))
    result_suba2[0].append(len(y_suba))
    result_suba3[0].append(len(y_suba))
    result_suba1[0].append(r2_suba[0])
    result_suba2[0].append(r2_suba[1])
    result_suba3[0].append(r2_suba[2])
    y_both = data3[variable]
    x_both = data3[['T1_treat','T2_treat','T3_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']]
    x_both = sm_api.add_constant(x_both, has_constant='add')
    reg_both = sm_api.OLS(y_both, x_both).fit(cov_type='cluster', cov_kwds={'groups': data3['school_code']})
    i = 1
    while i < 4:
        result_both.append(round(reg_both.params[i], 3))
        result_both.append(round(reg_both.bse[i], 3))
        i += 1
    result_both.append(round(reg_both.f_test('T1_treat=T2_treat').fvalue[0][0], 3))
    result_both.append(round(float(reg_both.f_test('T1_treat=T2_treat').pvalue), 3))
    result_both.append(round(reg_both.f_test('T1_treat=T3_treat').fvalue[0][0], 3))
    result_both.append(round(float(reg_both.f_test('T1_treat=T3_treat').pvalue), 3))
    result_both.append(len(y_both))
    result_both.append(round(reg_both.rsquared, 3))
    table3 = pd.DataFrame({'Basic-Savings': result_sancristobal1[0]}, index=['Basic treatment','Basic treatment SE','Savings treatment','Savings treatment SE','Tertiary treatment','Tertiary treatment SE','H0: Basic-Savings F-Stat','p-value','H0: Tertiary-Basic F-Stat','p-value','Observations','R squared'])
    table3['Basic-Savings with demographics'] = result_sancristobal2[0]
    table3['Basic-Savings with demographics and school fixed effects'] = result_sancristobal3[0]
    table3['Tertiary'] = result_suba1[0]
    table3['Tertiary with demographics'] = result_suba2[0]
    table3['Tertiary with demographics and school fixed effects'] = result_suba3[0]
    table3['Both'] = result_both
    
    return table3

def create_table5(data):
    sample_fu = data.drop(data[(data.fu_observed == 0) | (data.grade != 11)].index)
    sample_fu_sancristobal = sample_fu.drop(sample_fu[sample_fu.suba == 1].index)
    sample_fu_suba = sample_fu.drop(sample_fu[sample_fu.suba == 0].index)
    result_grad_sancristobal = list()
    result_grad_suba = list()
    result_grad_both = list()
    result_tert_sancristobal = list()
    result_tert_suba = list()
    result_tert_both = list()
    i = 1
    while i < 5:
        result_grad_suba.append('')
        result_tert_suba.append('')
        i += 1
    x = sm_api.add_constant(sample_fu_sancristobal[['T1_treat','T2_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']], has_constant='add')
    y = sample_fu_sancristobal['graduated']
    reg = sm_api.OLS(y, x).fit(cov_type='cluster', cov_kwds={'groups': sample_fu_sancristobal['school_code']})
    result_grad_sancristobal.append(round(reg.params[1], 3))
    result_grad_sancristobal.append(round(reg.bse[1], 3))
    result_grad_sancristobal.append(round(reg.params[2], 3))
    result_grad_sancristobal.append(round(reg.bse[2], 3))
    i = 1
    while i < 3:
        result_grad_sancristobal.append('')
        i += 1
    result_grad_sancristobal.append(round(reg.f_test('T1_treat=T2_treat').fvalue[0][0], 3))
    result_grad_sancristobal.append(round(float(reg.f_test('T1_treat=T2_treat').pvalue), 3))
    i = 1
    while i < 3:
        result_grad_sancristobal.append('')
        i += 1
    result_grad_sancristobal.append(len(y))
    result_grad_sancristobal.append(round(reg.rsquared, 3))
    sample_fu_sancristobal_tert = sample_fu_sancristobal.drop(sample_fu_sancristobal[sample_fu_sancristobal.tertiary.isnull()].index)
    x = sm_api.add_constant(sample_fu_sancristobal_tert[['T1_treat','T2_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']], has_constant='add')
    y = sample_fu_sancristobal_tert['tertiary']
    reg = sm_api.OLS(y, x).fit(cov_type='cluster', cov_kwds={'groups': sample_fu_sancristobal_tert['school_code']})
    result_tert_sancristobal.append(round(reg.params[1], 3))
    result_tert_sancristobal.append(round(reg.bse[1], 3))
    result_tert_sancristobal.append(round(reg.params[2], 3))
    result_tert_sancristobal.append(round(reg.bse[2], 3))
    i = 1
    while i < 3:
        result_tert_sancristobal.append('')
        i += 1
    result_tert_sancristobal.append(round(reg.f_test('T1_treat=T2_treat').fvalue[0][0], 3))
    result_tert_sancristobal.append(round(float(reg.f_test('T1_treat=T2_treat').pvalue), 3))
    i = 1
    while i < 3:
        result_tert_sancristobal.append('')
        i += 1
    result_tert_sancristobal.append(len(y))
    result_tert_sancristobal.append(round(reg.rsquared, 3))
    x = sm_api.add_constant(sample_fu_suba[['T3_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']], has_constant='add')
    y = sample_fu_suba['graduated']
    reg = sm_api.OLS(y, x).fit(cov_type='cluster', cov_kwds={'groups': sample_fu_suba['school_code']})
    result_grad_suba.append(round(reg.params[1], 3))
    result_grad_suba.append(round(reg.bse[1], 3))
    i = 1
    while i < 5:
        result_grad_suba.append('')
        i += 1
    result_grad_suba.append(len(y))
    result_grad_suba.append(round(reg.rsquared, 3))
    sample_fu_suba_tert = sample_fu_suba.drop(sample_fu_suba[sample_fu_suba.tertiary.isnull()].index)
    x = sm_api.add_constant(sample_fu_suba_tert[['T3_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']], has_constant='add')
    y = sample_fu_suba_tert['tertiary']
    reg = sm_api.OLS(y, x).fit(cov_type='cluster', cov_kwds={'groups': sample_fu_suba_tert['school_code']})
    result_tert_suba.append(round(reg.params[1], 3))
    result_tert_suba.append(round(reg.bse[1], 3))
    i = 1
    while i < 5:
        result_tert_suba.append('')
        i += 1
    result_tert_suba.append(len(y))
    result_tert_suba.append(round(reg.rsquared, 3))
    x = sm_api.add_constant(sample_fu[['T1_treat','T2_treat','T3_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']], has_constant='add')
    y = sample_fu['graduated']
    reg = sm_api.OLS(y, x).fit(cov_type='cluster', cov_kwds={'groups': sample_fu['school_code']})
    result_grad_both.append(round(reg.params[1], 3))
    result_grad_both.append(round(reg.bse[1], 3))
    result_grad_both.append(round(reg.params[2], 3))
    result_grad_both.append(round(reg.bse[2], 3))
    result_grad_both.append(round(reg.params[3], 3))
    result_grad_both.append(round(reg.bse[3], 3))
    result_grad_both.append(round(reg.f_test('T1_treat=T2_treat').fvalue[0][0], 3))
    result_grad_both.append(round(float(reg.f_test('T1_treat=T2_treat').pvalue), 3))
    result_grad_both.append(round(reg.f_test('T1_treat=T3_treat').fvalue[0][0], 3))
    result_grad_both.append(round(float(reg.f_test('T1_treat=T3_treat').pvalue), 3))
    result_grad_both.append(len(y))
    result_grad_both.append(round(reg.rsquared, 3))
    sample_fu_tert = sample_fu.drop(sample_fu[sample_fu.tertiary.isnull()].index)
    x = sm_api.add_constant(sample_fu_tert[['T1_treat','T2_treat','T3_treat','s_teneviv_int','s_utilities','s_durables','s_infraest_hh','s_age_sorteo','s_age_sorteo2','s_years_back','s_sexo_int','s_estcivil_int','s_single','s_edadhead','s_yrshead','s_tpersona','s_num18','s_estrato','s_puntaje','s_ingtotal','grade','suba','s_over_age','school_code']], has_constant='add')
    y = sample_fu_tert['tertiary']
    reg = sm_api.OLS(y, x).fit(cov_type='cluster', cov_kwds={'groups': sample_fu_tert['school_code']})
    result_tert_both.append(round(reg.params[1], 3))
    result_tert_both.append(round(reg.bse[1], 3))
    result_tert_both.append(round(reg.params[2], 3))
    result_tert_both.append(round(reg.bse[2], 3))
    result_tert_both.append(round(reg.params[3], 3))
    result_tert_both.append(round(reg.bse[3], 3))
    result_tert_both.append(round(reg.f_test('T1_treat=T2_treat').fvalue[0][0], 3))
    result_tert_both.append(round(float(reg.f_test('T1_treat=T2_treat').pvalue), 3))
    result_tert_both.append(round(reg.f_test('T1_treat=T3_treat').fvalue[0][0], 3))
    result_tert_both.append(round(float(reg.f_test('T1_treat=T3_treat').pvalue), 3))
    result_tert_both.append(len(y))
    result_tert_both.append(round(reg.rsquared, 3))
    table5 = pd.DataFrame({'Graduation Basic-Savings':result_grad_sancristobal}, index=['Basic treatment','Basic treatment SE','Savings treatment','Savings treatment SE','Tertiary treatment','Tertiary treatment SE','H0: Basic-Savings F-Stat','p-value','H0: Tertiary-Basic F-Stat','p-value','Observations','R squared'])
    table5['Graduation Tertiary'] = result_grad_suba
    table5['Graduation Both'] = result_grad_both
    table5['Tertiary enrollment Basic-Savings'] = result_tert_sancristobal
    table5['Tertiary enrollment Tertiary'] = result_tert_suba
    table5['Tertiary enrollment Both'] = result_tert_both
    
    return table5

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
