cd ("/Users/chrissymo/Documents/MSIS/research/with_Amanda/2022new")
import pandas as pd
import numpy as np

df_reg = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/2022new/Comments_Regs_22.04.12.xlsx',sheet_name='Regs-level')
df_comment = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/2022new/Comments_Regs_22.04.12.xlsx',sheet_name='Comments-level')

'''
Reg_ID = []
for i in range(len(df_reg)):
    if df_reg.comment_count[i] != 0:
        regid = df_reg.Reg_ID[i]
        Reg_ID.append(regid)
    else:
        Reg_ID
'''
Reg_ID = df_reg.document_number_x.tolist()
mean_tone = []
comment_counts = []
for item in Reg_ID:
    df_subset = df_comment[df_comment.documentNumber == item]
    subset_mean = np.mean(df_subset.tone)
    counts = len(df_subset)
    #mean_tone.append(subset_mean)
    comment_counts.append(counts)

df_reg['average_tone'] = mean_tone
df_reg['comment_counts'] = comment_counts



comment = pd.DataFrame()
for item in Reg_ID:
    comment_sub = df_comment[df_comment.documentNumber == item]
    comment = comment.append(comment_sub,ignore_index=True)


#company indicators count and avg tone
big4_count = []
corporate_count = []
firm_mid_count = []
Firm_Small_count = []
Broader_Orgs_Indicator_count = []
Standards_count = []
Advocates_count = []
for item in Reg_ID:
    df_subset = df_comment[df_comment.documentNumber == item]
    big4_count.append(df_subset['big4'].sum())
    corporate_count.append(df_subset['corporate'].sum())
    firm_mid_count.append(df_subset['firm_mid'].sum())
    Firm_Small_count.append(df_subset['Firm_Small'].sum())
    Broader_Orgs_Indicator_count.append(df_subset['Broader_Orgs_Indicator'].sum())
    Standards_count.append(df_subset['Standards'].sum())
    Advocates_count.append(df_subset['Advocates'].sum())

df_reg['big4_count'] = big4_count
df_reg['corporate_count'] = corporate_count
df_reg['firm_mid_count'] = firm_mid_count
df_reg['Firm_Small_count'] = Firm_Small_count
df_reg['Broader_Orgs_Indicator_count'] = Broader_Orgs_Indicator_count
df_reg['Standards_count'] = Standards_count
df_reg['Advocates_count'] = Advocates_count



big4_tone = []
corporate_tone = []
firm_mid_tone = []
Firm_Small_tone = []
Broader_Orgs_Indicator_tone = []
Standards_tone = []
Advocates_tone = []

for item in Reg_ID:
    df_subset = df_comment[df_comment.documentNumber == item]
    big4_tone.append(np.mean(df_subset[df_subset['big4'] == 1].tone))
    corporate_tone.append(np.mean(df_subset[df_subset['corporate'] == 1].tone))
    firm_mid_tone.append(np.mean(df_subset[df_subset['firm_mid'] == 1].tone))
    Firm_Small_tone.append(np.mean(df_subset[df_subset['Firm_Small'] == 1].tone))
    Broader_Orgs_Indicator_tone.append(np.mean(df_subset[df_subset['Broader_Orgs_Indicator'] == 1].tone))
    Standards_tone.append(np.mean(df_subset[df_subset['Standards'] == 1].tone))
    Advocates_tone.append(np.mean(df_subset[df_subset['Advocates'] == 1].tone))


df_reg['big4_tone'] = big4_tone
df_reg['corporate_tone'] = corporate_tone
df_reg['firm_mid_tone'] = firm_mid_tone
df_reg['Firm_Small_tone'] = Firm_Small_tone
df_reg['Broader_Orgs_Indicator_tone'] = Broader_Orgs_Indicator_tone
df_reg['Standards_tone'] = Standards_tone
df_reg['Advocates_tone'] = Advocates_tone