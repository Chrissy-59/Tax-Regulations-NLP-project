import os
os.chdir('/Users/chrissymo/Documents/MSIS/research/with_Amanda/proposed_reg_tone')
from extract_section_from_pdf import pdf_from_url_to_txt,extract_text
import pandas as pd
import numpy as np
import pysentiment2 as ps

df = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/2022new/Comment_Reg_20220203.xlsx',sheet_name='regs-level')

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
    url = df.pdf_url_x.iloc[i]
    text = pdf_from_url_to_txt(url)
    #extarct section
    text_extraction = extract_text(text)
    #calculate tone
    tone = lm_main(text_extraction)
    print('finish record', str(i))
    tone_list.append(tone)

df['proposed_tone'] = tone_list
df.to_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/2022new/proposed_tone.xlsx',index=False)