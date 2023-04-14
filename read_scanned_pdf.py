# Import libraries
from PIL import Image
import pytesseract
import pandas as pd
from pdf2image import convert_from_bytes
import requests
import pysentiment2 as ps
import os
os.chdir('/Users/chrissymo/Documents/MSIS/research/with_Amanda/comments_tone/pages')
# url of the pdf
#url = "https://downloads.regulations.gov/IRS-2012-0006-0036/attachment_1.pdf"

def scanned_pdf_from_url_to_txt(url):
    '''
    Part #1 : Converting PDF to images
    '''
    # Store all the pages of the PDF in a variable
    pdf = requests.get(url)
    pages = convert_from_bytes(pdf.content,500)
    # Counter to store images of each page of PDF to image
    image_counter = 1
    # Iterate through all the pages stored above
    for page in pages:
        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        # ....
        # PDF page n -> page_n.jpg
        filename = "page_" + str(image_counter) + ".jpg"
        # Save the image of the page in system
        page.save(filename, 'JPEG')
        # Increment the counter to update filename
        image_counter = image_counter + 1
    # Variable to get count of total number of pages
    filelimit = image_counter - 1

    text_all = ""
    for i in range(1, filelimit + 1):
        # Set filename to recognize text from
        # Again, these files will be:
        # page_1.jpg
        # page_2.jpg
        # ....
        # page_n.jpg
        filename = "page_" + str(i) + ".jpg"
        # Recognize the text as string in image using pytesserct
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        text = text.replace('-\n', '')
        text_all += text
    #remove image file
    for i in range(1, filelimit + 1):
        filename = "page_" + str(i) + ".jpg"
        os.remove(filename)
        #print("Deleting", str(filename))

    return text_all

def lm_main(text):
    lm = ps.LM()
    tokens = lm.tokenize(text)
    score = lm.get_score(tokens)
    pos = score['Positive']
    neg = score['Negative']
    tone = (pos - neg) / (pos + neg)
    return tone


df = pd.read_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/comments_tone/new/temp_files/pdf_fix_bugs.xlsx')
df.tone = ""
'''
#for i in range(len(df)):
for i in range(3): # for test
    if df.num_url.iloc[i] == 1:
        url = df.fileLinks.iloc[i]
        text = scanned_pdf_from_url_to_txt(url)
        df.tone.iloc[i] = lm_main(text)
    else:
        url_list = df.iloc[i].fileLinks.split()
        text = scanned_pdf_from_url_to_txt(url_list[0]) + scanned_pdf_from_url_to_txt(url_list[1])
        df['tone'].iloc[i] = lm_main(text)
        
'''
df.tone = ""
for i in range(2800,len(df)):
#for i in range(450,500):  # for test
    try:
        if df.num_url.iloc[i] == 1:
            url = df.fileLinks.iloc[i]
            text = scanned_pdf_from_url_to_txt(url)
            df.iloc[[i],-1] = lm_main(text)
        else:
            url_list = df.iloc[i].fileLinks.split()
            text = ''
            for item in url_list:
                text += scanned_pdf_from_url_to_txt(item)
            df.iloc[[i],-1] = lm_main(text)
    except:
        print('***Error*** ind ' + str(df.ind.iloc[i]) + ' ' + df.fileLinks.iloc[i])
    df.to_excel('/Users/chrissymo/Documents/MSIS/research/with_Amanda/comments_tone/new/temp_files/pdf_fix_bugs.xlsx',index=False)