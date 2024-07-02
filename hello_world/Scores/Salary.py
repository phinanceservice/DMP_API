from . import descriptionUtilities as utils

import pandas as pd
import numpy as np
import itertools
import scipy
import re
import lists


#############################################################################



def initial_filters(inp_fuzzy_grp_df):
  out_fuzzy_grp_df = inp_fuzzy_grp_df.copy()
  out_fuzzy_grp_df['initial_filtered'] = 0
  def logic(inp_direction, inp_salary_exc_string, inp_group_size, inp_salary_inc_string, inp_person_name, inp_max_amt, inp_min_amt, inp_min_date_diff, inp_max_date_diff):
    if inp_direction != 'CREDIT':
      return 1
    elif inp_salary_inc_string == 1:
      return 0
    elif inp_group_size < 3:
      return 1
    elif inp_salary_exc_string == 1:
      return 1
    # elif inp_person_name == 1:
    #   return 1
    elif inp_max_amt < 50:
      return 1
    elif inp_min_amt > 10000:
      return 1
    elif inp_max_date_diff < 5:
      return 1
    elif inp_min_date_diff > 50:
      return 1
    else:
      return 0
  out_fuzzy_grp_df['Initial_filtered'] = out_fuzzy_grp_df.apply(lambda x: logic(x.direction, x.salary_exc_string, x.group_size, x.salary_inc_string, x.person_name, x.max_amt, x.min_amt, x.min_date_diff, x.max_date_diff), axis = 1)
  return out_fuzzy_grp_df


def regularity_filters(inp_fuzzy_grp_df):
  out_fuzzy_grp_df = inp_fuzzy_grp_df.copy()
  out_fuzzy_grp_df['regularity_filtered'] = 0
  def logic(inp_ratio_num_monthly_ints, inp_ratio_num_mult7_ints):
    if inp_ratio_num_monthly_ints >= 0.75 or inp_ratio_num_mult7_ints >= 0.75:
      return 0
    else:
      return 1
  out_fuzzy_grp_df['regularity_filtered'] = out_fuzzy_grp_df.apply(lambda x: logic(x.ratio_num_monthly_ints, x.ratio_num_mult7_ints), axis = 1)
  return out_fuzzy_grp_df


def amount_filters(inp_fuzzy_grp_df):
  out_fuzzy_grp_df = inp_fuzzy_grp_df.copy()
  out_fuzzy_grp_df['amount_filtered'] = 0
  def logic(inp_median_date_diff, inp_median_amt):
    if 0 <= inp_median_date_diff and inp_median_date_diff <= 20 and 20 <= inp_median_amt:
      return 0
    elif 20 < inp_median_date_diff and inp_median_date_diff <= 65 and 100 <= inp_median_amt:
      return 0
    else:
      return 1
  out_fuzzy_grp_df['amount_filtered'] = out_fuzzy_grp_df.apply(lambda x: logic(x.median_date_diff, x.median_amt), axis = 1)
  return out_fuzzy_grp_df


def roundness_filters(inp_fuzzy_grp_df):
  out_fuzzy_grp_df = inp_fuzzy_grp_df.copy()
  out_fuzzy_grp_df['roundness_filtered'] = 0
  def logic(inp_ratio_round_amt, inp_ratio_no_pence):
    if inp_ratio_round_amt > 0.5: # or inp_ratio_no_pence <= 0.5:
      return 1
    else:
      return 0
  out_fuzzy_grp_df['roundness_filtered'] = out_fuzzy_grp_df.apply(lambda x: logic(x.ratio_round_amt, x.ratio_no_pence), axis = 1)
  return out_fuzzy_grp_df



def salary_points_function(inp_df):
  out_df=inp_df.copy()
  out_df = initial_filters(out_df)
  out_df = regularity_filters(out_df)
  out_df = amount_filters(out_df)
  out_df = roundness_filters(out_df)

  def points(inp_Initial_filtered, inp_regularity_filtered, inp_amount_filtered, inp_roundness_filtered):
    if inp_Initial_filtered == 0 and inp_regularity_filtered == 0 and inp_amount_filtered == 0 and inp_roundness_filtered == 0:
        return 0.8
    else:
        return 0.1

  out_df['salary_points']=  out_df.apply(lambda x: points(x.Initial_filtered, x.regularity_filtered, x.amount_filtered, x.roundness_filtered), axis = 1)

  return out_df

