from . import descriptionUtilities as utils
import numpy as np
import pandas as pd


#############################################################################
#Description Points

def attendance_allowance_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['attendance_allowance_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP AA') for desc in out_df.description.values])
    out_df.loc[mask, 'attendance_allowance_description_points'] = 0.9
    return out_df

def bereavement_benefit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['bereavement_benefit_description_points'] = 0.1
    mask1 = np.array([utils.word_in_string(desc, 'DWP BSP') for desc in out_df.description.values])
    mask2 = np.array([utils.word_in_string(desc, 'DWP BB') for desc in out_df.description.values])
    mask = np.logical_or(mask1, mask2)
    out_df.loc[mask, 'bereavement_benefit_description_points'] = 0.9
    return out_df

def carers_allowance_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['carers_allowance_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP CA') for desc in out_df.description.values])
    out_df.loc[mask, 'carers_allowance_description_points'] = 0.9
    return out_df

def child_benefit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['child_benefit_description_points'] = 0.1
    mask1 = np.array([utils.word_in_string(desc, 'HMRC CHILD BENEFIT') for desc in out_df.description.values])
    mask2 = np.array([utils.word_in_string(desc, '-CHB') for desc in out_df.description.values])
    mask3 = np.array([utils.word_in_string(desc, 'DWPCMS') for desc in out_df.description.values])
    mask = np.logical_or(np.logical_or(mask1, mask2), mask3)
    out_df.loc[mask, 'child_benefit_description_points'] = 0.9
    return out_df

def child_maintenance_scheme_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['child_maintenance_scheme_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWPCMSGB2012SCHEME') for desc in out_df.description.values])
    out_df.loc[mask, 'child_maintenance_scheme_description_points'] = 0.9
    return out_df

def child_support_agency_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['child_support_agency_description_points'] = 0.1
    mask1 = np.array([utils.word_in_string(desc, ' CSA') for desc in out_df.description.values])
    mask2 = np.array([utils.word_in_string(desc, 'CSA ') for desc in out_df.description.values])
    mask = np.logical_or(mask1, mask2)
    out_df.loc[mask, 'child_support_agency_description_points'] = 0.9
    return out_df

def child_tax_credit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['child_tax_credit_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'CHILD TAX CREDIT') for desc in out_df.description.values])
    out_df.loc[mask, 'child_tax_credit_description_points'] = 0.9
    return out_df

def christmas_bonus_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['christmas_bonus_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP XB') for desc in out_df.description.values])
    out_df.loc[mask, 'christmas_bonus_description_points'] = 0.9
    return out_df

def cold_weather_payment_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['cold_weather_payment_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP CWP') for desc in out_df.description.values])
    out_df.loc[mask, 'cold_weather_payment_description_points'] = 0.9
    return out_df

def cash_refund_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['cash_refund_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP CSHR') for desc in out_df.description.values])
    out_df.loc[mask, 'cash_refund_description_points'] = 0.9
    return out_df

def cost_of_living_payment_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['cost_of_living_payment_description_points'] = 0.1
    mask1 = np.array([utils.word_in_string(desc, 'DWP COL') for desc in out_df.description.values])
    mask2 = np.array([utils.word_in_string(desc, 'DWP C O L') for desc in out_df.description.values])
    mask3 = np.array([utils.word_in_string(desc, 'DWP C    O  L') for desc in out_df.description.values])
    mask = np.logical_or(np.logical_or(mask1, mask2), mask3)
    out_df.loc[mask, 'cost_of_living_payment_description_points'] = 0.9
    return out_df

def disability_living_allowance_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['disability_living_allowance_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP DLA') for desc in out_df.description.values])
    out_df.loc[mask, 'disability_living_allowance_description_points'] = 0.9
    return out_df

def education_maintenance_allowance_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['education_maintenance_allowance_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'EMA PAYMENT SCHEME') for desc in out_df.description.values])
    out_df.loc[mask, 'education_maintenance_allowance_description_points'] = 0.9
    return out_df

def employment_support_allowance_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['employment_support_allowance_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP EESA') for desc in out_df.description.values])
    out_df.loc[mask, 'employment_support_allowance_description_points'] = 0.9
    return out_df

def hmrc_covid19_support_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['hmrc_covid19_support_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'HMRC C19 SUPPORT') for desc in out_df.description.values])
    out_df.loc[mask, 'hmrc_covid19_support_description_points'] = 0.9
    return out_df

def income_support_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['income_support_description_points'] = 0.1
    mask1 = np.array([utils.word_in_string(desc, 'DWP IS') for desc in out_df.description.values])
    mask2 = np.array([utils.word_in_string(desc, 'DWP ISCS') for desc in out_df.description.values])
    mask = np.logical_or(mask1, mask2)
    out_df.loc[mask, 'income_support_description_points'] = 0.9
    return out_df

def industrial_injuries_disablement_benefit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['industrial_injuries_disablement_benefit_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP IIB') for desc in out_df.description.values])
    out_df.loc[mask, 'industrial_injuries_disablement_benefit_description_points'] = 0.9
    return out_df

def job_seekers_allowance_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['job_seekers_allowance_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP JSA') for desc in out_df.description.values])
    out_df.loc[mask, 'job_seekers_allowance_description_points'] = 0.9
    return out_df

def maternity_allowance_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['maternity_allowance_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP MA') for desc in out_df.description.values])
    out_df.loc[mask, 'maternity_allowance_description_points'] = 0.9
    return out_df

def hmrc_overpayments_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['hmrc_overpayments_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'HMRC NDDS') for desc in out_df.description.values])
    out_df.loc[mask, 'hmrc_overpayments_description_points'] = 0.9

    return out_df

def pension_credit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['pension_credit_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP PC') for desc in out_df.description.values])
    out_df.loc[mask, 'pension_credit_description_points'] = 0.9
    return out_df

def personal_independance_payment_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['personal_independance_payment_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP PIP') for desc in out_df.description.values])
    out_df.loc[mask, 'personal_independance_payment_description_points'] = 0.9
    return out_df

def saas_payment_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['saas_payment_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'SAAS PAYMENTS') for desc in out_df.description.values])
    out_df.loc[mask, 'saas_payment_description_points'] = 0.9
    return out_df

def self_employed_income_support_scheme_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['self_employed_income_support_scheme_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'SEISS GRANT') for desc in out_df.description.values])
    out_df.loc[mask, 'self_employed_income_support_scheme_description_points'] = 0.9
    return out_df

def state_pension_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['state_pension_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP SP') for desc in out_df.description.values])
    out_df.loc[mask, 'state_pension_description_points'] = 0.9
    return out_df

def social_fund_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['social_fund_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP SF') for desc in out_df.description.values])
    out_df.loc[mask, 'social_fund_description_points'] = 0.9
    return out_df

def universal_credit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['universal_credit_description_points'] = 0.1
    mask1 = np.array([utils.word_in_string(desc, 'DWP UC') for desc in out_df.description.values])
    mask2 = np.array([utils.word_in_string(desc, 'DWPGB UC') for desc in out_df.description.values])
    mask = np.logical_or(mask1, mask2)
    out_df.loc[mask, 'universal_credit_description_points'] = 0.9
    return out_df

def winter_fuel_payment_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['winter_fuel_payment_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP WFP') for desc in out_df.description.values])
    out_df.loc[mask, 'winter_fuel_payment_description_points'] = 0.9
    return out_df

def widows_benefit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['widows_benefit_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP WB') for desc in out_df.description.values])
    out_df.loc[mask, 'widows_benefit_description_points'] = 0.9
    return out_df

def widowed_parents_allowance_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['widowed_parents_allowance_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'DWP WPA') for desc in out_df.description.values])
    out_df.loc[mask, 'widowed_parents_allowance_description_points'] = 0.9
    return out_df

def work_and_child_tax_credit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['work_and_child_tax_credit_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'WORK AND CHILD TC') for desc in out_df.description.values])
    out_df.loc[mask, 'work_and_child_tax_credit_description_points'] = 0.9
    return out_df

def working_tax_credit_desc_points_function(inp_df):
    out_df = inp_df.copy()
    out_df['working_tax_credit_description_points'] = 0.1
    mask = np.array([utils.word_in_string(desc, 'WORKING TAX CREDIT') for desc in out_df.description.values])
    out_df.loc[mask, 'working_tax_credit_description_points'] = 0.9
    return out_df


#############################################################################
#Amount Points


# def attendance_allowance_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def bereavement_benefit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def carers_allowance_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def child_benefit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def child_maintenance_scheme_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def child_support_agency_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def child_tax_credit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def christmas_bonus_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def cold_weather_payment_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def cash_refund_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def cost_of_living_payment_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def disability_living_allowance_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def education_maintenance_allowance_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def employment_support_allowance_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def hmrc_covid19_support_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def income_support_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def industrial_injuries_disablement_benefit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def job_seekers_allowance_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def maternity_allowance_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def hmrc_overpayments_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def pension_credit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def personal_independance_payment_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def saas_payment_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def self_employed_income_support_scheme_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def state_pension_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def social_fund_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def universal_credit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def winter_fuel_payment_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def widows_benefit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def widowed_parents_allowance_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def work_and_child_tax_credit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1

# def working_tax_credit_amt_points_function(inp_amt_median, inp_direction, inp_date_diff_mode, inp_date_diff_median):
#     return 1


#############################################################################
#Freq Points



# def attendance_allowance_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def bereavement_benefit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def carers_allowance_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def child_benefit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def child_maintenance_scheme_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def child_support_agency_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def child_tax_credit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def christmas_bonus_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def cold_weather_payment_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def cash_refund_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def cost_of_living_payment_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def disability_living_allowance_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def education_maintenance_allowance_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def employment_support_allowance_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def hmrc_covid19_support_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def income_support_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def industrial_injuries_disablement_benefit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def job_seekers_allowance_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def maternity_allowance_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def hmrc_overpayments_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def pension_credit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def personal_independance_payment_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def saas_payment_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def self_employed_income_support_scheme_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def state_pension_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def social_fund_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def universal_credit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def winter_fuel_payment_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def widows_benefit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def widowed_parents_allowance_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def work_and_child_tax_credit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points

# def working_tax_credit_freq_points_function(inp_date_diff_mode, inp_date_diff_median):
#     return_points = 0.9
#     return return_points



