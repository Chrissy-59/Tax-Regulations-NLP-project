from Porter_Stemming import stemSentence
from consine_similarity import cs_cv,cs_tv
from extract_section_from_pdf import pdf_from_url_to_txt,extract_text

import pandas as pd
import numpy as np

#df = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with Amanda/consine similarity/TCJA_Regs_test.xlsx')
#df = pd.read_excel('./consine similarity/TCJA_Regs_test.xlsx')
df = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/2022new/reg_level_new_22.3.7.xlsx',sheet_name='clean')
cv_score = []
tv_score = []
for i in range(len(df)):
    url1 = df['pdf_url_x'].iloc[i]
    url2 = df['pdf_url_y'].iloc[i]
    if url1 is not np.NAN and url2 is not np.NAN:
        #parse pdf url
        text1 = pdf_from_url_to_txt(url1)
        text2 = pdf_from_url_to_txt(url2)
        #extarct section
        text1 = extract_text(text1)
        text2 = extract_text(text2)
        if text1 != '' and text2 != '':
        #porter_stemming
            text1 = stemSentence(text1)
            text2 = stemSentence(text2)
            #consine similarity
            try:
                cv_score_test = cs_cv(text1,text2)
                tv_score_test = cs_tv(text1,text2)
            except:
                cv_score_test = np.NAN
                tv_score_test = np.NAN
                print('id:' + str(df['id'].iloc[i]), url1, url2)
        else:
            cv_score_test = np.NAN
            tv_score_test = np.NAN
            #append list
    else:
        cv_score_test = np.NAN
        tv_score_test = np.NAN
    cv_score.append(cv_score_test)
    tv_score.append(tv_score_test)

df['consine similarity(CV)'] = cv_score
df['consine similarity(TV)'] = tv_score

df.to_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/2022new/reg-level_3.25.xlsx',index=False)