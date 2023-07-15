##############################################################
# AB Testing: Comparison of Facebook Bidding Methods
# in terms of the Number of Products Sold after Clicks."
##############################################################

# Facebook bidding allows advertisers to set the amount they are willing to pay for their ads to reach their
# target audience through an auction-based system.

##############################################################
## 1. Business Problem
##############################################################

# Facebook introduced a new bidding type called "average bidding" as an alternative to the existing "maximum bidding"
# type. In this study, the statistical significance of any differences in the number of product purchases made by
# customers after clicking on ads will be examined, based on the utilization of these bidding methods.

# Variables:
# Impression: Number of ad impressions
# Click: Number of clicks on the ads
# Purchase: Number of product purchases after the clicks
# Earning: Revenue generated from the purchases

###############################################################
# 2. Data Preparation
###############################################################

## Importing libraries
##############################################

import pandas as pd
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.expand_frame_repr', False)

df_control = pd.read_excel('/Users/handeatasagun/Documents/Github/AB_Testing_Facebook_Biddings/ab_testing.xlsx',
                           sheet_name="Control Group")

df_test = pd.read_excel('/Users/handeatasagun/Documents/Github/AB_Testing_Facebook_Biddings/ab_testing.xlsx',
                        sheet_name="Test Group")

# Data understanding
##############################################
def check_df(dataframe, head=5):
    print('################# Shape ################# ')
    print(dataframe.columns)
    print('################# Types  ################# ')
    print(dataframe.dtypes)
    print('##################  Head ################# ')
    print(dataframe.head(head))
    print('#################  Shape ################# ')
    print(dataframe.shape)
    print('#################  NA ################# ')
    print(dataframe.isnull().sum())
    print('#################  Quantiles ################# ')
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99]).T)

check_df(df_control)

check_df(df_test)

# Merging the control and test group datasets
##############################################
df = pd.concat([df_control, df_test], ignore_index=True)


#####################################################
# AB Testing for 'Purchase' Variable
#####################################################

control_purchase = df['Purchase'].head(40)
control_purchase.mean()

test_purchase = df['Purchase'].tail(40)
test_purchase.mean()


# Assumption of normality
##############################################
def shapiro_test(x, y):
    test_stat_x, pvalue_x = shapiro(x)
    test_stat_y, pvalue_y = shapiro(y)
    if pvalue_x < 0.05:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat_x, pvalue_x),
              'HO is rejected, the assumption of normal distribution is not satisfied')
    else:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat_x, pvalue_x),
              'HO is not rejected, the assumption of normal distribution is satisfied')

    if pvalue_y < 0.05:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat_y, pvalue_y),
              'HO is rejected, the assumption of normal distribution is not satisfied')
    else:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat_y, pvalue_y),
              'HO is not rejected, the assumption of normal distribution is satisfied')

shapiro_test(control_purchase, test_purchase)
# Test Stat = 0.9773, p-value = 0.5891 HO is not rejected, the assumption of normal distribution is satisfied
# Test Stat = 0.9589, p-value = 0.1541 HO is not rejected, the assumption of normal distribution is satisfied


# Assumption of homogeneity of variance
##############################################
def levene_test(x,y):
    test_stat, pvalue = levene(x, y)
    if pvalue < 0.05:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              'HO is rejected, the homogeneity of variance is not satisfied')
    else:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              'HO is not rejected, the homogeneity of variance is satisfied')

levene_test(control_purchase, test_purchase)
# Test Stat = 2.6393, p-value = 0.1083 HO is not rejected, the homogeneity of variance is satisfied


# !! When both assumptions are met, an 'Two-Sample Independent t-Test' is conducted.


# Two-Sample Independent t-Test
##############################################
def b2t_test(x,y):
    test_stat, pvalue = ttest_ind(x,y)
    if pvalue < 0.05:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              'HO is rejected, there is a statistically significant difference between the groups')
    else:
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue),
              'HO is not rejected, there is not a statistically significant difference between the groups')

b2t_test(control_purchase, test_purchase)
# Test Stat = -0.9416, p-value = 0.3493 HO is not rejected, there is not a statistically significant difference
# between the groups.