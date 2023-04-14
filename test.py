import pandas as pd

df = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with Amanda/consine similarity/TCJA_Regs_test.xlsx')
for i in range(len(df)):
    try:
        url1 = df['pdf_url'].iloc[i]
        url2 = df['final_pdf_url'].iloc[i]
        #parse pdf url
        text1 = pdf_from_url_to_txt(url1)
        text2 = pdf_from_url_to_txt(url2)
    except:
        print('error index:'+ str(i))

