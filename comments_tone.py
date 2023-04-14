import os
os.chdir('/Users/chrissymo/Documents/MSIS/research/with_Amanda/comments_tone')
from extract_section_from_pdf import pdf_from_url_to_txt
import pandas as pd
import numpy as np
import pysentiment2 as ps
import pdfminer

df = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/fetch_data_codes/2022/new/new_comments_all.xlsx')

# calculate filelinks num
df['num_url'] = ""

for i in range(len(df)):
    if df.iloc[i].fileLinks is np.nan:
        df['num_url'].iloc[i] = 0
    else:
        df['num_url'].iloc[i] = len(df.iloc[i].fileLinks.split())

df = pd.read_excel('new_comments_all_num_url.xlsx')


#mark the doc file, I can't parse the doc file using url

df['note_c'] = ""
for i in range(len(df)):
    if df.num_url.iloc[i] == 1 and df.fileLinks.iloc[i][-3:] =='doc':
        df['note_c'].iloc[i] = 1
    else:
        df['note_c'].iloc[i] = 0


#####start from here#########
#df = pd.read_excel('comment_all_4.xlsx')
#df = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/comments_tone/new/new_comments_all_clean2.xlsx')
df_p1 = pd.read_csv('/Users/chrissymo/Documents/MSIS/research/with_Amanda/fetch_data_codes/2022/new/treasy_regs_comments.csv')
def lm_main(text):
    lm = ps.LM()
    tokens = lm.tokenize(text)
    score = lm.get_score(tokens)
    pos = score['Positive']
    neg = score['Negative']
    tone = (pos - neg) / (pos + neg)
    return tone

import requests
import docx2txt
from io import BytesIO
def docx_from_url_txt(url):
    docx = BytesIO(requests.get(url).content)
    # extract text
    text = docx2txt.process(docx)
    return text

#note_c = 0, means we could parse the file using url directly, otherwise we need to download for parsing, which is processed in df_p2
df_p1 = df[df['note_c'] == 0]
##test a sample
#df_p1 = df_p1.sample(n=50)
df_p1['tone'] = ""

for i in range(len(df_p1)):
    #print ('Working on i ' + str(i) + '...')
    if df_p1.numIncluded.iloc[i] == 0:  ##process comment column
        if df_p1['comment'].iloc[i] is not np.nan:
            df_p1['tone'].iloc[i] = lm_main(df_p1['comment'].iloc[i])
        else:
            df_p1['tone'].iloc[i] = np.nan
    elif df_p1.numIncluded.iloc[i] == 1:
        url = df_p1.fileLinks.iloc[i]
        try:
             text = pdf_from_url_to_txt(url)
        except AttributeError:
            print('***AttributeError***', str(i), url)
            text = ''
        except pdfminer.pdfdocument.PDFSyntaxError:
            try:
                text = docx_from_url_txt(url)
            except:
                print('***PDFSyntaxError***', str(i), url)
                text = ''
        except pdfminer.pdfdocument.PDFEncryptionError:
            print('***PDFEncryptionError***', str(i), url)
            text = ''
        except pdfminer.psparser.PSSyntaxError:
            print('***PSSyntaxError***', str(i), url)
            text = ''
        #except:
        #   text = docx_from_url_txt(url)
        df_p1['tone'].iloc[i] = lm_main(text)
    elif df_p1.iloc[i].numIncluded == 2:
        url_list = df_p1.iloc[i].fileLinks.split()
        #if url_list[0][-3:] != 'pdf':##the content of docx and pdf is the same in this case
        if df_p1.iloc[i].numIncluded == 1:
            url = url_list[1]  ##process the second url(pdf file)
            try:
                text = pdf_from_url_to_txt(url)
            except AttributeError:
                print('***AttributeError***', str(i), url)
                text = ''
            except pdfminer.pdfdocument.PDFSyntaxError:
                print('***PDFSyntaxError***', str(i), url)
                text = ''
            except pdfminer.pdfdocument.PDFEncryptionError:
                print('***PDFEncryptionError***', str(i), url)
                text = ''
            except pdfminer.psparser.PSSyntaxError:
                print('***PSSyntaxError***', str(i), url)
                text = ''
            df_p1['tone'].iloc[i] = lm_main(text)
        else:
            try:
                text = pdf_from_url_to_txt(url_list[0]) + pdf_from_url_to_txt(url_list[1])
            except AttributeError:
                print('***AttributeError***', str(i), url)
                text = ''
            except pdfminer.pdfdocument.PDFSyntaxError:
                print('***PDFSyntaxError***', str(i), url)
                text = ''
            except pdfminer.pdfdocument.PDFEncryptionError:
                print('***PDFEncryptionError***', str(i), url)
                text = ''
            except pdfminer.psparser.PSSyntaxError:
                print('***PSSyntaxError***', str(i), url)
                text = ''
            df_p1['tone'].iloc[i] = lm_main(text)
    else: ##num_url >= 3
        url_list = df_p1.iloc[i].fileLinks.split()
        s = ""
        for ind in range(len(url_list)):
            url = url_list[ind]
            try:
                s += pdf_from_url_to_txt(url)
            except:
                print('***Error***', str(i), url)
        df_p1['tone'].iloc[i] = lm_main(s)


##process download files
import glob
import fitz
import textract

from urllib import request
df_p2 = df[df['note_c'] == 1]
#download files
for i in range(len(df_p2)):
    url = df_p2['fileLinks'].iloc[i]
    file_name = str(df_p2['id'].iloc[i])+'.' + str(url[-3:])
    request.urlretrieve(url, file_name)

# User defined directory for files to be parsed
TARGET_FILES = r'/Users/chrissymo/Documents/MSIS/research/with_Amanda/comments_tone/download_files/pdf_files/*.*'
file_list = glob.glob(TARGET_FILES)

def extractText(file):
    doc = fitz.open(file)
    text = []
    for page in doc:
        t = page.getText()
        text.append(t)
    if len(text) == 1:
        total = text[0]
    else:
        total = text[0]
        for i in range(1,len(text)):
            total = total + text[i]
    return total

rows = []
for i in range(len(file_list)):
    pdf_text = extractText(file_list[i])
    pdf_tone_score = lm_main(pdf_text)

    rows.append([file_list[i][-22:-4], pdf_tone_score])

df_downloadpdf = pd.DataFrame(rows, columns=["id", "tone"])
##merge results
df_p2_merge = df_p2.merge(df_downloadpdf,how='left',on = 'id')
df_all = pd.concat([df_p1,df_p2_merge])
##save to excel
df_all.to_excel('comment_tone_all_0103.xlsx', index = False)
df_p2_merge.to_excel('comment_tone_p2_0103.xlsx', index = False)



for item in i_list:
    df_p1.iloc[[item],-2] = 2