import pandas as pd
import numpy as np
import scipy
from Levenshtein import ratio
import itertools
from scipy.sparse.csgraph import connected_components
from scipy.stats import median_abs_deviation
from statistics import mean
import lists
import re
from collections import defaultdict

################################################
#description groups

def find_desc_groups_and_features(inp_df):
    # input: a dataframe of transactions withh descriptions, dates and amounts
    # return: a dataframe with one row per group and columns containing group properties (size, average amount, average transaction interval)

    grouped_df = inp_df.groupby(['description', 'direction']).agg({'day_diff': ['size','mean', 'median', lambda x: scipy.stats.mode(x).mode, 'nunique']
                                                               , 'amount': ['mean', 'median', lambda x: scipy.stats.mode(x).mode, 'nunique']}).reset_index()
    
    grouped_df.columns = ['_'.join(col).strip() for col in grouped_df.columns.values]

    grouped_df.columns = [c.replace('<lambda_0>', 'mode') for c in grouped_df.columns]
    grouped_df.columns = [c.replace('accountid_', 'accountid') for c in grouped_df.columns]
    grouped_df.columns = [c.replace('description_', 'description') for c in grouped_df.columns]
    grouped_df.columns = [c.replace('direction_', 'direction') for c in grouped_df.columns]
    grouped_df.columns = [c.replace('size_day_diff', 'group_size') for c in grouped_df.columns]

    # grouped_df.set_index('description')

    grouped_df['desc_grp'] = range(len(grouped_df))

    # out_dict = grouped_df.to_dict('index')

    return grouped_df

################################################
#fuzzy groups

def find_unique_descs(inp_desc_lst):
    return sorted(np.unique(inp_desc_lst))

def find_num_unique_desc(inp_desc_arr):
    return len(np.unique(inp_desc_arr))

def find_lev_adj_mat(inp_desc_arr, threshold):
    lev_dists = [ratio(x[0], x[1]) for x in itertools.combinations(np.unique(inp_desc_arr), 2)]
    num_unique_desc = len(np.unique(inp_desc_arr))
    tri = np.zeros((num_unique_desc, num_unique_desc))
    tri[np.triu_indices(num_unique_desc, 1)] = lev_dists
    return (tri>=threshold).astype(int)

def find_group_labels(inp_adj_mat):
    group_size, group_labels = connected_components(inp_adj_mat, directed = False)
    return group_size, group_labels

def find_fuzzy_groups(inp_df):
    # print('inp_df',inp_df)
    desc_grouped_df = inp_df.groupby(['description', 'direction']).size().to_frame(name='count').reset_index()
    #debits
    debit_unique_desc_arr = desc_grouped_df[desc_grouped_df['direction'] == 'DEBIT'].description.values
    if len(debit_unique_desc_arr) == 0:
    #    print('no_debit_trans')
       max_debit_group = 0
       debit_grouped_df = pd.DataFrame([], columns = ['description', 'direction', 'fuzzy_grp', 'group_size'])
    else:
        # print('some_debit_trans')
        debit_lev_adj_mat = find_lev_adj_mat(debit_unique_desc_arr, 0.65)
        group_size, debit_group_labels = find_group_labels(debit_lev_adj_mat)
        # print('desc_grouped_df',desc_grouped_df)
        # print('debit_unique_desc_arr',debit_unique_desc_arr)
        # print('debit_lev_adj_mat',debit_lev_adj_mat)
        # print('debit_group_labels', debit_group_labels)
        # print('debit_unique_desc_arr', debit_unique_desc_arr)
        # print('debit_group_labels', debit_group_labels)
        # print('group_size', group_size)
        debit_grouped_df = pd.DataFrame({'description': debit_unique_desc_arr, 'direction':['DEBIT']*len(debit_unique_desc_arr), 'fuzzy_grp': debit_group_labels, 'group_size': group_size})
        max_debit_group = np.max(debit_group_labels)
    #credits
    credit_unique_desc_arr = desc_grouped_df[desc_grouped_df['direction'] == 'CREDIT'].description.values
    if len(credit_unique_desc_arr) == 0:
    #    print('no_credit_trans')
       max_debit_group = 0
       credit_grouped_df = pd.DataFrame([], columns = ['description', 'direction', 'fuzzy_grp', 'group_size'])
    else:
        # print('some_credit_trans')
        credit_lev_adj_mat = find_lev_adj_mat(credit_unique_desc_arr, 0.65)
        # print('credit_lev_adj_mat', credit_lev_adj_mat)
        group_size, credit_group_labels = find_group_labels(credit_lev_adj_mat)
        credit_group_labels = credit_group_labels + max_debit_group + 1
        # print('credit_group_labels', credit_group_labels)
        credit_grouped_df = pd.DataFrame({'description': credit_unique_desc_arr, 'direction':['CREDIT']*len(credit_unique_desc_arr), 'fuzzy_grp': credit_group_labels, 'group_size': group_size})
        # print('credit_grouped_df', credit_grouped_df)
    grouped_df = pd.concat([debit_grouped_df, credit_grouped_df])
    return grouped_df


#features functions


def find_group_size(inp_grouping):
   (_, grp_df) = inp_grouping
   return [[len(grp_df)], ['group_size']]


combined_salary_inc_lst = "(" + ")|(".join(lists.salary_inc_lst) + ")"
combined_salary_exc_lst = "(" + ")|(".join(lists.salary_exc_lst) + ")"

# def contains_salary_exclusion(inp_desc_arr):
#   salary_exc_lst = ['BARCLAYS PINGIT', 'XFER', 'FUNDS TRANSFER', 'TRANSFER FROM', 'TRANSFER TO', 'SENT FROM MONZO', 'MOBILE-CHANNEL',  'LOAN', 'CASHBACK', 'INTEREST', 'PENSION', 'REFUND', 'RFD', 'RETURNED', 'DIRECT DEBIT', 'ME', 'MUM', 'DAD', 'MY ACCOUNT', 'LOVE FROM' ]
#   return int(any(any(exc_str in inp_desc for exc_str in salary_exc_lst) for inp_desc in inp_desc_arr))

def contains_salary_exclusion(inp_grouping, inp_combined_exc_lst = combined_salary_exc_lst):
  (_, grp_df) = inp_grouping
  inp_desc_arr = grp_df.description.values
  salary_exclusion_flag = int(any(bool(re.search(inp_combined_exc_lst, desc_str)) for desc_str in inp_desc_arr))
  return [[salary_exclusion_flag], ['salary_exc_string']]

# def contains_salary_inclusion(inp_desc_arr):
#   salary_inc_lst = ['SALARY', 'SALARIES', 'WAGES', 'PAYROLL']
#   return int(any(any(inc_str in inp_desc for inc_str in salary_inc_lst) for inp_desc in inp_desc_arr))

def contains_salary_inclusion(inp_grouping, inp_combined_inc_lst = combined_salary_inc_lst):
  (_, grp_df) = inp_grouping
  inp_desc_arr = grp_df.description.values
  salary_inclusion_flag = int(any(bool(re.search(inp_combined_inc_lst, desc_str)) for desc_str in inp_desc_arr))
  return  [[salary_inclusion_flag],  ['salary_inc_string']]


combined_hb_inc_lst = "(" + ")|(".join(lists.hb_inc_lst) + ")"
combined_hb_exc_lst = "(" + ")|(".join(lists.hb_exc_lst) + ")"
combined_hb_id_lst = "(" + ")|(".join(lists.hb_identifiers_lst) + ")"

# def contains_HB_inclusion(inp_desc_arr, inp_combined_inc_lst = combined_inc_lst):
#   return int(any(bool(re.search(inp_combined_inc_lst, desc_str)) for desc_str in inp_desc_arr))

def contains_HB_inclusion(inp_grouping, inp_combined_inc_lst = combined_hb_inc_lst):
  (group_label, grp_df) = inp_grouping
  inp_desc_arr = grp_df.description.values
  hb_inclusion_flag = int(any(bool(re.search(inp_combined_inc_lst, desc_str)) for desc_str in inp_desc_arr))
  return [[hb_inclusion_flag], ['hb_inc_string']]

# def contains_HB_exclusion(inp_desc_arr, inp_combined_exc_lst = combined_exc_lst):
#   return int(any(bool(re.search(inp_combined_exc_lst, desc_str)) for desc_str in inp_desc_arr))

def contains_HB_exclusion(inp_grouping, inp_combined_exc_lst = combined_hb_exc_lst):
  (group_label, grp_df) = inp_grouping
  inp_desc_arr = grp_df.description.values
  hb_exclusion_flag = int(any(bool(re.search(inp_combined_exc_lst, desc_str)) for desc_str in inp_desc_arr))
  return [[hb_exclusion_flag], ['hb_exc_string']]

# def contains_HB_identifier(inp_desc_arr, inp_combined_id_lst = combined_id_lst):
#   return int(any(bool(re.search(inp_combined_id_lst, desc_str)) for desc_str in inp_desc_arr))

def contains_HB_identifier(inp_grouping, inp_combined_id_lst = combined_hb_id_lst):
  (group_label, grp_df) = inp_grouping
  inp_desc_arr = grp_df.description.values
  hb_id_flag = int(any(bool(re.search(inp_combined_id_lst, desc_str)) for desc_str in inp_desc_arr))
  return [[hb_id_flag], ['hb_id_string']]

# def contains_person_name(inp_desc_arr):
#    #check if any name string in desc array
#    if any(any(fname in inp_desc for fname in lists.first_names_list) for inp_desc in inp_desc_arr) and any(any(sname in inp_desc for sname in lists.surnames_list) for inp_desc in inp_desc_arr):
#       return 1
#    else:
#       return 0
   
def contains_person_name(inp_grouping):
   #check if any name string in desc array
  (group_label, grp_df) = inp_grouping
  inp_desc_arr = grp_df.description.values
  if any(any(fname in inp_desc for fname in lists.first_names_list) for inp_desc in inp_desc_arr) and any(any(sname in inp_desc for sname in lists.surnames_list) for inp_desc in inp_desc_arr):
    person_name_flag =  1
  else:
    person_name_flag =  0
  return [[person_name_flag], ['person_name']]


# def find_date_features(inp_date_arr):
#   sorted_date_arr = np.sort(inp_date_arr)
#   day_diffs_arr = np.diff(sorted_date_arr, n=1)/np.timedelta64(1, 'D')
#   mean_date_diff = np.mean(day_diffs_arr)
#   median_date_diff = np.median(day_diffs_arr)
#   mode_date_diff = scipy.stats.mode(day_diffs_arr, keepdims = True)[0][0]
#   min_date_diff = np.min(day_diffs_arr)
#   max_date_diff = np.max(day_diffs_arr)
#   return mean_date_diff, median_date_diff, mode_date_diff, min_date_diff, max_date_diff


def spread1(inp_lst):
    if len(inp_lst) == 0:
       return np.nan
    else:
      spread1 = (max(inp_lst) - min(inp_lst)) / mean(inp_lst)
      return spread1

def spread2(inp_lst):
    if len(inp_lst) == 0:
      return np.nan
    else:
      median = np.percentile(np.array(inp_lst), 50)
      perc_10 = np.percentile(np.array(inp_lst), 10)
      perc_90 = np.percentile(np.array(inp_lst), 90)
      spread2 = (perc_90 - perc_10) / median
      return spread2

def spread3(inp_lst):
    if len(inp_lst) == 0:
      return np.nan
    else:
      return median_abs_deviation(inp_lst)


def find_date_features(inp_grouping):
  (group_label, grp_df) = inp_grouping
  inp_date_arr = grp_df.Date.values
  sorted_date_arr = np.sort(inp_date_arr)
  day_diffs_arr = np.diff(sorted_date_arr, n=1)/np.timedelta64(1, 'D')
  if len(day_diffs_arr) == 0:
    mean_date_diff = np.nan
    median_date_diff = np.nan
    mode_date_diff = np.nan
    min_date_diff = np.nan
    max_date_diff = np.nan
    spread1_date_diff = np.nan
    spread2_date_diff = np.nan
    spread3_date_diff = np.nan
    num_distinct_date_diffs = np.nan
    ratio_num_distinct_date_diffs = np.nan
    num_monthly_ints = np.nan
    num_mult7_ints = np.nan
    ratio_num_monthly_ints = np.nan
    ratio_num_mult7_ints = np.nan
  else:
    mean_date_diff = np.mean(day_diffs_arr)
    median_date_diff = np.median(day_diffs_arr)
    mode_date_diff = scipy.stats.mode(day_diffs_arr).mode
    min_date_diff = np.min(day_diffs_arr)
    max_date_diff = np.max(day_diffs_arr)
    spread1_date_diff = spread1(day_diffs_arr)
    spread2_date_diff = spread2(day_diffs_arr)
    spread3_date_diff = spread3(day_diffs_arr)
    num_distinct_date_diffs = len(set(day_diffs_arr))
    ratio_num_distinct_date_diffs = num_distinct_date_diffs / len(day_diffs_arr)
    num_monthly_ints = np.sum(np.array([int(x in [28, 29, 30, 31, 32, 33]) for x in day_diffs_arr]))
    num_mult7_ints = np.sum(np.array([int(x%7 == 0) and x <= 56 and x > 0 for x in day_diffs_arr]))
    ratio_num_monthly_ints = num_monthly_ints / len(day_diffs_arr)
    ratio_num_mult7_ints = num_mult7_ints / len(day_diffs_arr)

  return [[mean_date_diff, median_date_diff, mode_date_diff, min_date_diff, max_date_diff, spread1_date_diff, spread2_date_diff, spread3_date_diff, num_distinct_date_diffs, ratio_num_distinct_date_diffs, num_monthly_ints,num_mult7_ints,ratio_num_monthly_ints, ratio_num_mult7_ints]
          , ['mean_date_diff','median_date_diff','mode_date_diff','min_date_diff','max_date_diff', 'spread1_date_diff', 'spread2_date_diff', 'spread3_date_diff', 'num_distinct_date_diffs', 'ratio_num_distinct_date_diffs','num_monthly_ints','num_mult7_ints', 'ratio_num_monthly_ints', 'ratio_num_mult7_ints']]


# def find_amt_features(inp_amt_arr):
#   mean_amt = np.mean(inp_amt_arr)
#   median_amt = np.median(inp_amt_arr)
#   mode_amt = scipy.stats.mode(inp_amt_arr, keepdims = True)[0][0]
#   min_amt = np.min(inp_amt_arr)
#   max_amt = np.max(inp_amt_arr)
#   round_amt = any(x%10 == 0 for x in inp_amt_arr)
#   num_distinct = len(set(inp_amt_arr))
#   spread1_amt = spread1(inp_amt_arr)
#   spread2_amt = spread2(inp_amt_arr)
#   spread3_amt = spread3(inp_amt_arr)
#   return mean_amt, median_amt, mode_amt, min_amt, max_amt, round_amt, num_distinct, spread1_amt, spread2_amt, spread3_amt


def find_amt_features(inp_grouping):
  (group_label, grp_df) = inp_grouping
  inp_amt_arr = grp_df.amount.values
  mean_amt = np.mean(inp_amt_arr)
  median_amt = np.median(inp_amt_arr)
  mode_amt = scipy.stats.mode(inp_amt_arr).mode
  min_amt = np.min(inp_amt_arr)
  max_amt = np.max(inp_amt_arr)
  num_round_amt = np.sum(np.array([int(x%10 == 0) for x in inp_amt_arr]))
  ratio_round_amt = np.sum(np.array([int(x%10 == 0) for x in inp_amt_arr])) / len(inp_amt_arr)
  num_no_pence = np.sum(np.array([int(x%11 == 0) for x in inp_amt_arr]))
  ratio_no_pence = np.sum(np.array([int(x%1 == 0) for x in inp_amt_arr])) / len(inp_amt_arr)
  num_distinct = len(set(inp_amt_arr))
  spread1_amt = spread1(inp_amt_arr)
  spread2_amt = spread2(inp_amt_arr)
  spread3_amt = spread3(inp_amt_arr)
  return [[mean_amt, median_amt, mode_amt, min_amt, max_amt, num_round_amt, ratio_round_amt, num_no_pence, ratio_no_pence, num_distinct, spread1_amt, spread2_amt, spread3_amt]
          , ['mean_amt','median_amt','mode_amt','min_amt','max_amt','num_round_amt', 'ratio_round_amt', 'num_no_pence', 'ratio_no_pence', 'num_distinct','spread1_amt','spread2_amt', 'spread3_amt']]


# def group_duration(inp_date_arr):
#   return (np.max(inp_date_arr) - np.min(inp_date_arr)) / np.timedelta64(1, 'D')


def group_duration(inp_grouping):
  (group_label, grp_df) = inp_grouping
  inp_date_arr = grp_df.Date.values
  return [[(np.max(inp_date_arr) - np.min(inp_date_arr)) / np.timedelta64(1, 'D')], ['group_duration_val']]


# def density(inp_date_arr):
#   if group_duration(inp_date_arr) == 0:
#      return np.nan
#   else:
#      return len(inp_date_arr) / group_duration(inp_date_arr)
  

def density(inp_grouping):
  (group_label, grp_df) = inp_grouping
  inp_date_arr = grp_df.Date.values
  group_duration = (np.max(inp_date_arr) - np.min(inp_date_arr)) / np.timedelta64(1, 'D')
  if group_duration == 0:
     out_den = np.nan
  else:
     out_den =  len(inp_date_arr) / group_duration
  return [[out_den], ['density_val']]


# def penetration(inp_date_arr, statement_start_date, statement_end_date):
#   statement_duration = (statement_end_date - statement_start_date) / np.timedelta64(1, 'D')
#   if statement_duration == 0:
#      return np.nan
#   else:
#     return group_duration(inp_date_arr) / statement_duration
  

def penetration(inp_grouping):
  (group_label, grp_df) = inp_grouping
  inp_date_arr = grp_df.Date.values
  statement_start_date = np.min(inp_date_arr)
  statement_end_date = np.max(inp_date_arr)
  statement_duration = (statement_end_date - statement_start_date) / np.timedelta64(1, 'D')
  group_duration = (np.max(inp_date_arr) - np.min(inp_date_arr)) / np.timedelta64(1, 'D')
  if statement_duration == 0:
     out_pen =  np.nan
  else:
    out_pen = group_duration / statement_duration
  return [[out_pen], ['penetration_val']]


def grp_direction(inp_grouping):
  (group_label, grp_df) = inp_grouping
  direction_arr = grp_df.direction.values
  return [[np.max(direction_arr)], ['direction']]




# def find_fuzzy_features(inp_df):
#     inp_grouped_df = inp_df.groupby('fuzzy_grp')
#     out_df = inp_grouped_df.size().to_frame(name = 'group_size').reset_index()
#     # print('out_df.columns', out_df.columns)
#     # out_df['group_size'] = inp_grouped_df['description'].transform(lambda x: len(x))
#     out_df['direction'] = inp_grouped_df['direction'].transform(lambda x: max(x)) #should all be the same so this acts to distill the series to it's unique value
#     out_df['salary_exc_string'] = inp_grouped_df['description'].transform(lambda x: contains_salary_exclusion(x))
#     out_df['salary_inc_string'] = inp_grouped_df['description'].transform(lambda x: contains_salary_inclusion(x))
#     out_df['hb_inc_string'] = inp_grouped_df['description'].transform(lambda x: contains_HB_inclusion(x))
#     out_df['hb_excstring'] = inp_grouped_df['description'].transform(lambda x: contains_HB_exclusion(x))
#     out_df['hb_id_string'] = inp_grouped_df['description'].transform(lambda x: contains_HB_identifier(x))
#     out_df['person_name'] = inp_grouped_df['description'].transform(lambda x: contains_person_name(x))
#     out_df['mean_date_diff'] = inp_grouped_df['day_diff'].transform(lambda x: np.mean(x))
#     out_df['median_date_diff'] = inp_grouped_df['day_diff'].transform(lambda x: np.median(x))
#     out_df['mode_date_diff'] = inp_grouped_df['day_diff'].transform(lambda x: scipy.stats.mode(x, keepdims = True)[0][0])
#     out_df['min_date_diff'] = inp_grouped_df['day_diff'].transform(lambda x: np.min(x))
#     out_df['max_date_diff'] = inp_grouped_df['day_diff'].transform(lambda x: np.max(x))

#     out_df['mean_amt'] = inp_grouped_df['amount'].transform(lambda x: np.mean(x))
#     out_df['median_amt'] = inp_grouped_df['amount'].transform(lambda x: np.median(x))
#     out_df['mode_amt'] = inp_grouped_df['amount'].transform(lambda x:scipy.stats.mode(x, keepdims = True)[0][0])
#     out_df['min_amt'] = inp_grouped_df['amount'].transform(lambda x: np.min(x))
#     out_df['max_amt'] = inp_grouped_df['amount'].transform(lambda x: np.max(x))
#     out_df['round_amt'] = inp_grouped_df['amount'].transform(lambda x: any(y%10 == 0 for y in x))
#     out_df['num_distinct'] = inp_grouped_df['amount'].transform(lambda x: len(set(x)))
#     out_df['spread1'] = inp_grouped_df['amount'].transform(lambda x: spread1(x))
#     out_df['spread2'] = inp_grouped_df['amount'].transform(lambda x: spread2(x))

#     out_df['group_duration_val'] = inp_grouped_df['Date'].transform(lambda x: group_duration(x))
#     out_df['density_val'] = inp_grouped_df['Date'].transform(lambda x: density(x))

#     return out_df



def find_fuzzy_features(inp_df):
    inp_grouped_df = inp_df.groupby('fuzzy_grp')
    # out_df = inp_grouped_df.size().to_frame(name = 'group_size').reset_index()

    features_functions_lst = [find_group_size
                              , grp_direction
                              , contains_salary_exclusion
                              , contains_salary_inclusion
                              , contains_HB_inclusion
                              , contains_HB_exclusion
                              , contains_HB_identifier
                              , contains_person_name
                              , find_date_features
                              , find_amt_features
                              , group_duration
                              , density
                              , penetration]

    group_features_df_lst = []

    for grp in inp_grouped_df:
      this_fuzzy_grp = grp[0]
      features_output_lst = [f(grp) for f in features_functions_lst]
      grp_feature_vals_lst = [i for s in [f[0] for f in features_output_lst] for i in s]
      grp_features_names_lst = [i for s in [f[1] for f in features_output_lst] for i in s]
      group_features_df = pd.DataFrame([[this_fuzzy_grp] + grp_feature_vals_lst], columns = ['fuzzy_grp'] + grp_features_names_lst)
      group_features_df_lst = group_features_df_lst + [group_features_df]

    out_df = pd.concat(group_features_df_lst)
    return out_df





# def find_fuzzy_features(inp_df):
#     return inp_df.groupby('fuzzy_grp').apply(get_fuzzy_features)
