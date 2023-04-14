import os
os.chdir('/Users/chrissymo/Documents/MSIS/research/with_Amanda/comments_tone')
from extract_section_from_pdf import pdf_from_url_to_txt,extract_text
import pandas as pd
import numpy as np
import pysentiment2 as ps

df_comment = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/2022new/Comment_Reg_20220203.xlsx'，sheet_name='regs-level')
df_reg_full = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/fetch_data_codes/Full-Sample_Reg_21-11-22.xlsx',sheet_name='sample')

reg_list = df_comment['documentNumber'].unique().tolist()
df_reg_sub = pd.DataFrame(reg_list, columns=['document_number'])
df_reg_merge = df_reg_sub.merge(df_reg_full,how='left',on='document_number')
df = df_reg_merge.dropna(subset=['pdf_url'])

def lm_main(text):
    lm = ps.LM()
    tokens = lm.tokenize(text)
    score = lm.get_score(tokens)
    pos = score['Positive']
    neg = score['Negative']
    tone = (pos - neg) /(pos + neg)
    return tone

tone_list = []
for i in range(len(df)):
    url = df.pdf_url.iloc[i]
    text = pdf_from_url_to_txt(url)
    #extarct section
    text_extraction = extract_text(text)
    #calculate tone
    tone = lm_main(text_extraction)
    print('finish record', str(i))
    tone_list.append(tone)

df['reg_tone'] = tone_list
df.to_excel('proposed_tone_0103.xlsx',index=False)

##extract proposed and final regulations based on regulation_id_numbers
reg_id = df['regulation_id_numbers'].tolist()
df_proposed_final = df_reg_full[df_reg_full['regulation_id_numbers'].isin(reg_id)]
df_final = df_proposed_final[df_proposed_final['type'] == 'Rule']
df_link = df.merge(df_final,how='left',on='regulation_id_numbers')