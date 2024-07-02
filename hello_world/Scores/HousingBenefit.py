from . import descriptionUtilities as utils

import pandas as pd
import numpy as np
import itertools
import scipy
import re
import lists


#############################################################################
#Description Points



# combined_inc_lst = "(" + ")|(".join(lists.hb_inc_lst) + ")"
# combined_exc_lst = "(" + ")|(".join(lists.hb_exc_lst) + ")"
# combined_id_lst = "(" + ")|(".join(lists.hb_identifiers_lst) + ")"

# def contains_HB_inc_str(inp_desc, inp_combined_inc_lst = combined_inc_lst):
#   return bool(re.search(inp_combined_inc_lst, inp_desc))

# def contains_HB_exc_str(inp_desc, inp_combined_exc_lst = combined_exc_lst):
#   return bool(re.search(inp_combined_exc_lst, inp_desc))

# def contains_HB_id_str(inp_desc, inp_combined_id_lst = combined_id_lst):
#   return bool(re.search(inp_combined_id_lst, inp_desc))



def housingBenefit_desc_points_function(inp_df):
  out_df=inp_df.copy()

  def points(inp_group_size, inp_hb_inc_string, inp_hb_excstring, inp_hb_id_string):
    if not(inp_hb_inc_string):
      return 0.1
    elif inp_hb_excstring:
      return 0.1
    elif inp_group_size < 3:
      if inp_hb_id_string:
        return 0.9
      else:
        return 0.1
    elif inp_group_size >= 3:
      if inp_hb_id_string:
        return 0.9
      else:
        return 0.7
    else:
      return 0.1
       
  out_df['housing_benefit_desc_points'] = out_df.apply(lambda x: points(x.group_size, x.hb_inc_string, x.hb_exc_string, x.hb_id_string), axis = 1)

  return out_df


  
#############################################################################
#Frequency Points

def housingBenefit_freq_points_function(inp_df):
    out_df=inp_df.copy()

    def points(inp_date_diff_mode, inp_date_diff_median, inp_group_size):
        if inp_group_size < 3:
           return 1
        elif inp_date_diff_mode in [7, 14, 28] or inp_date_diff_median in [7, 14, 28] :
            return 1
        else:
            return 0.1    
          
    out_df['housing_benefit_freq_points'] = out_df.apply(lambda x: points(x.mode_date_diff, x.median_date_diff, x.group_size), axis = 1)

    return out_df


#############################################################################
#Amount Points


def housingBenefit_amt_points_function(inp_df):

    out_df=inp_df.copy()

    def points(inp_direction, inp_amt_median, inp_date_diff_mode, inp_date_diff_median, inp_group_size):
        if inp_direction == 'DEBIT':
           return 0.1
        elif inp_group_size < 3:
           if inp_amt_median > 500:
              return 0.1
           else:
              return 1
        elif (inp_date_diff_mode  == 7 or inp_date_diff_median == 7):
            if inp_amt_median > 350:
                return 0.1
            else:
                return 1
        elif (inp_date_diff_mode  == 14 or inp_date_diff_median == 14):
            if inp_amt_median > 500:
                return 0.1
            else:
                return 1
        elif (inp_date_diff_mode  == 28 or inp_date_diff_median == 28):
            if inp_amt_median > 1400:
                return 0.1
            else:
                return 1
        else:
            return 0.1
        
    out_df['housing_benefit_amt_points'] = out_df.apply(lambda x: points(x.direction, x.median_amt, x.mode_date_diff, x.median_date_diff, x.group_size), axis = 1)
        
    return out_df

