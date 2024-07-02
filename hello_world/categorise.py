# control the flow of functions used to categorise transactions


import numpy as np
import pandas as pd
from collections import defaultdict
from functools import reduce


# from hello_world.Scores import CentralBenefits
# from hello_world.Scores import HousingBenefit
# from hello_world.Scores import Salary
# from hello_world.Grouping import descriptionGroupingFunctions as descriptionGroupingFunctions

from Scores import CentralBenefits
from Scores import HousingBenefit
from Scores import Salary
from Grouping import descriptionGroupingFunctions as descriptionGroupingFunctions


categories_list = ['attendance_allowance',
'bereavement_benefit',
'carers_allowance',
'child_benefit',
'child_maintenance_scheme',
'child_support_agency',
'child_tax_credit',
'christmas_bonus',
'cold_weather_payment',
'cash_refund',
'cost_of_living_payment',
'disability_living_allowance',
'education_maintenance_allowance',
'employment_support_allowance',
'hmrc_covid19_support',
'income_support',
'industrial_injuries_disablement_benefit',
'job_seekers_allowance',
'maternity_allowance',
'hmrc_overpayments',
'pension_credit',
'personal_independance_payment',
'saas_payment',
'self_employed_income_support_scheme',
'state_pension',
'social_fund',
'universal_credit',
'winter_fuel_payment',
'widows_benefit',
'widowed_parents_allowance',
'work_and_child_tax_credit',
'working_tax_credit',
'housing_benefit',
'salary']



point_functions_dist = defaultdict(dict)


def categorise(inp_df):
    
    out_df = inp_df.copy()

    num_trans = len(out_df)
    num_cats = len(categories_list)



    #############################################
    #Data cleaning

    #uppercase the description
    out_df.description = out_df.description.str.upper()
    out_df.direction = out_df.direction.str.upper()


    #############################################
    #transaction-level features

    #calculate the day_diff field that will be passed to the grouping and features functions
    out_df.sort_values(by = ['accountid', 'direction',  'description', 'Date'], inplace = True)
    out_df['day_diff'] = out_df['Date'].diff() / np.timedelta64(1, 'D')
    mask = np.logical_or(np.logical_or((out_df.accountid != out_df.accountid.shift(1)), (out_df.direction != out_df.direction.shift(1))), (out_df.description != out_df.description.shift(1)))
    out_df.loc[mask, 'day_diff']  = np.nan


    #############################################
    #grouping and group features

    #desc_grp

    #group by description and return group features in a group-level df
    desc_groups_df = descriptionGroupingFunctions.find_desc_groups_and_features(out_df)
    # put the groupids back into the df
    out_df = out_df.merge(desc_groups_df[['description', 'direction', 'desc_grp']],  how='left', on = ['description', 'direction'])
    # print('1. out_df.shape', out_df.shape)
    # print('')

    #fuzzy_grp

    #group by fuzzy groups
    fuzzy_groups_df = descriptionGroupingFunctions.find_fuzzy_groups(out_df)
    # print('2. fuzzy_groups_df.shape', fuzzy_groups_df.shape)
    # print('')
    # put the groupids back into the df
    out_df = out_df.merge(fuzzy_groups_df[['description', 'direction', 'fuzzy_grp']], how='left', on = ['description', 'direction'])
    # print('3. out_df.shape', out_df.shape)
    # print('')
    #supply fuzzy groups transaction to features function and return features (remove the desc_grp or it get returned as part of the fuzzy group df)
    fuzzy_groups_df = descriptionGroupingFunctions.find_fuzzy_features(out_df[['accountid', 'description', 'direction', 'amount', 'Date', 'day_diff', 'fuzzy_grp']])
    # print('4. fuzzy_groups_df.columns', fuzzy_groups_df.columns)
    # print('')

    # put the groupids back into the df
    # out_df = out_df.merge(fuzzy_groups_df[['description', 'direction', 'fuzzy_grp']], how='left', on = ['description', 'direction'])
    # print('out_df.columns after initial merge with fuzzy groups', out_df.columns)
    # print('')

    #############################################
    #Score appropriate features for each category

    cat_scoring_dict = {'attendance_allowance':{'group_level': 'description', 'score_function_lst': [CentralBenefits.attendance_allowance_desc_points_function]},
                        'bereavement_benefit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.bereavement_benefit_desc_points_function]},
                        'carers_allowance':{'group_level': 'description', 'score_function_lst': [CentralBenefits.carers_allowance_desc_points_function]},
                        'child_benefit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.child_benefit_desc_points_function]},
                        'child_maintenance_scheme':{'group_level': 'description', 'score_function_lst': [CentralBenefits.child_maintenance_scheme_desc_points_function]},
                        'child_support_agency':{'group_level': 'description', 'score_function_lst': [CentralBenefits.child_support_agency_desc_points_function]},
                        'child_tax_credit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.child_tax_credit_desc_points_function]},
                        'christmas_bonus':{'group_level': 'description', 'score_function_lst': [CentralBenefits.christmas_bonus_desc_points_function]},
                        'cold_weather_payment':{'group_level': 'description', 'score_function_lst': [CentralBenefits.cold_weather_payment_desc_points_function]},
                        'cash_refund':{'group_level': 'description', 'score_function_lst': [CentralBenefits.cash_refund_desc_points_function]},
                        'cost_of_living_payment':{'group_level': 'description', 'score_function_lst': [CentralBenefits.cost_of_living_payment_desc_points_function]},
                        'disability_living_allowance':{'group_level': 'description', 'score_function_lst': [CentralBenefits.disability_living_allowance_desc_points_function]},
                        'education_maintenance_allowance':{'group_level': 'description', 'score_function_lst': [CentralBenefits.education_maintenance_allowance_desc_points_function]},
                        'employment_support_allowance':{'group_level': 'description', 'score_function_lst': [CentralBenefits.employment_support_allowance_desc_points_function]},
                        'hmrc_covid19_support':{'group_level': 'description', 'score_function_lst': [CentralBenefits.hmrc_covid19_support_desc_points_function]},
                        'income_support':{'group_level': 'description', 'score_function_lst': [CentralBenefits.income_support_desc_points_function]},
                        'industrial_injuries_disablement_benefit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.industrial_injuries_disablement_benefit_desc_points_function]},
                        'job_seekers_allowance':{'group_level': 'description', 'score_function_lst': [CentralBenefits.job_seekers_allowance_desc_points_function]},
                        'maternity_allowance':{'group_level': 'description', 'score_function_lst': [CentralBenefits.maternity_allowance_desc_points_function]},
                        'hmrc_overpayments':{'group_level': 'description', 'score_function_lst': [CentralBenefits.hmrc_overpayments_desc_points_function]},
                        'pension_credit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.pension_credit_desc_points_function]},
                        'personal_independance_payment':{'group_level': 'description', 'score_function_lst': [CentralBenefits.personal_independance_payment_desc_points_function]},
                        'saas_payment':{'group_level': 'description', 'score_function_lst': [CentralBenefits.saas_payment_desc_points_function]},
                        'self_employed_income_support_scheme':{'group_level': 'description', 'score_function_lst': [CentralBenefits.self_employed_income_support_scheme_desc_points_function]},
                        'state_pension':{'group_level': 'description', 'score_function_lst': [CentralBenefits.state_pension_desc_points_function]},
                        'social_fund':{'group_level': 'description', 'score_function_lst': [CentralBenefits.social_fund_desc_points_function]},
                        'universal_credit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.universal_credit_desc_points_function]},
                        'winter_fuel_payment':{'group_level': 'description', 'score_function_lst': [CentralBenefits.winter_fuel_payment_desc_points_function]},
                        'widows_benefit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.widows_benefit_desc_points_function]},
                        'widowed_parents_allowance':{'group_level': 'description', 'score_function_lst': [CentralBenefits.widowed_parents_allowance_desc_points_function]},
                        'work_and_child_tax_credit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.work_and_child_tax_credit_desc_points_function]},
                        'working_tax_credit':{'group_level': 'description', 'score_function_lst': [CentralBenefits.working_tax_credit_desc_points_function]},
                        'housing_benefit':{'group_level': 'fuzzy', 'score_function_lst': [HousingBenefit.housingBenefit_desc_points_function, HousingBenefit.housingBenefit_freq_points_function, HousingBenefit.housingBenefit_amt_points_function]},
                        'salary':{'group_level': 'fuzzy', 'score_function_lst': [Salary.salary_points_function]}
                        }

    points_dfs_dict = {}

    #cycle throught the categories
    for cat in categories_list:
        # print(cat)
        score_function_lst = cat_scoring_dict[cat]['score_function_lst']
        #select from the dictionary the grouping and functions

        # print('desc_groups_df.columns', desc_groups_df.columns)
        # print('')

        if cat_scoring_dict[cat]['group_level'] == 'description':
            #supply each function the group_df using reduce and write these to a copy of the group_df
            score_for_this_cat_df = reduce(lambda res, f: f(res), score_function_lst, desc_groups_df)
            # print('desc_groups_df.columns', desc_groups_df.columns)
            # print('')


            #take the product of the points in the new points groupdf and join back the group original df
            points_cols = [col for col in score_for_this_cat_df.columns if 'points' in col]
            score_for_this_cat_df.loc[:, points_cols].fillna(value = 0.1, inplace = True)
            # print('score_for_this_cat_df.columns', score_for_this_cat_df.columns)          
            # print('')
            score_for_this_cat_df[cat+'_points'] = score_for_this_cat_df.loc[:, points_cols].prod(axis=1)
            # print('score_for_this_cat_df', score_for_this_cat_df)          
            # print('')
            # print('desc_groups_df.columns', desc_groups_df.columns)
            # print('')
            desc_groups_df = pd.merge(desc_groups_df, score_for_this_cat_df[['desc_grp', cat+'_points']], on= 'desc_grp', how = 'left')
            #join this group df back to the trans-level df and attach points
            # print('desc_groups_df.columns', desc_groups_df.columns)
            # print('')
            # print('out_df.columns', out_df.columns)
            # print('')
            out_df = pd.merge(out_df, desc_groups_df[['desc_grp', cat+'_points']], on= 'desc_grp', how = 'left')
            #put the points group df in a list to be output at the end of categorisaion for review
            points_dfs_dict[cat] = score_for_this_cat_df

        elif cat_scoring_dict[cat]['group_level'] == 'fuzzy':
            #supply each function the group_df using reduce and write these to a copy of the group_df
            score_for_this_cat_df = reduce(lambda res, f: f(res), score_function_lst, fuzzy_groups_df)
            print('cat = ', cat)
            print('5. score_for_this_cat_df.columns', score_for_this_cat_df.columns)
            # print('score_for_this_cat_df', score_for_this_cat_df[['fuzzy_grp', 'group_size', cat+'_points']])

            

            #take the product of the points in the new points groupdf and join back the group original df
            points_cols = [col for col in score_for_this_cat_df.columns if 'points' in col and cat in col]
            print('points_cols', points_cols)
            print('score_for_this_cat_df.loc[:, points_cols]', score_for_this_cat_df.loc[:, points_cols])

            score_for_this_cat_df.loc[:, points_cols].fillna(value = 0.1, inplace = True)
            score_for_this_cat_df[cat+'_points'] = score_for_this_cat_df.loc[:, points_cols].prod(axis=1)
            print('score_for_this_cat_df[cat+_points]', score_for_this_cat_df[cat+'_points'])

            # print('6. score_for_this_cat_df.columns', score_for_this_cat_df.columns)          
            # print('')
            fuzzy_groups_df = pd.merge(fuzzy_groups_df, score_for_this_cat_df[['fuzzy_grp', cat+'_points']], on= 'fuzzy_grp', how = 'left')
            # print('7. fuzzy_groups_df.shape', fuzzy_groups_df.shape)
            # print('')
            
            #join this group df back to the trans-level df and attach points
            out_df = pd.merge(out_df, fuzzy_groups_df[['fuzzy_grp', cat+'_points']], on= 'fuzzy_grp', how = 'left')
            #put the points group df in a list to be output at the end of categorisaion for review
            points_dfs_dict[cat] = score_for_this_cat_df

        else:
            pass

        # print('out_df.shape', out_df.shape)
        # print('')


    point_cols = [cat+'_points' for cat in categories_list]
    out_df['cat'] = out_df[point_cols].idxmax(axis=1)

    out_df['max_points'] = out_df[point_cols].max(axis=1)
    out_df.loc[out_df['max_points']  < 0.2, 'cat'] = 'UNKNOWN'

    return out_df, desc_groups_df, fuzzy_groups_df



 
