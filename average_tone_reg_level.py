cd "/Users/chrissymo/Documents/MSIS/research/with_Amanda"
import pandas as pd

df_reg = pd.read_excel('TCJA_Regs_21.09.08_v2.xlsx',sheet_name='sample_reg-level')
df_comment = pd.read_excel('TCJA_Regs_21.09.08_v2.xlsx',sheet_name='sample_comment-level')
'''
Reg_ID = []
for i in range(len(df_reg)):
    if df_reg.comment_count[i] != 0:
        regid = df_reg.Reg_ID[i]
        Reg_ID.append(regid)
    else:
        Reg_ID
'''
Reg_ID = df_reg.Reg_ID.tolist()
mean_tone = []
for item in Reg_ID:
    df_subset = df_comment[df_comment.Reg_ID == item]
    subset_mean = np.mean(df_subset.tone)
    mean_tone.append(subset_mean)

df_reg['average_tone'] = mean_tone