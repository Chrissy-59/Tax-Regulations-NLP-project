#!/usr/bin/env python3

import requests
import json
import csv
import sys
import html
import collections
from pathlib import Path

api_key = '6ZMV3bxTtoj5jMMSW85N4wwDhkAjtlwonDLmWVVq'
# extra 
#api_key = 'EBO9en2lTQicpTfmASGa2p5EvsN10dvSWPDmBnjJ'
regs_api_url = lambda request: ('https://api.regulations.gov/v4/%s&api_key=%s' % (request, api_key))
fedregs_api_url = lambda doc_num: ('https://www.federalregister.gov/api/v1/documents/%s.json?fields%%5B%%5D=regulations_dot_gov_info' % (doc_num))
fedregs_search_api_url = lambda reg_num: ('https://www.federalregister.gov/api/v1/documents.json?fields%%5B%%5D=regulations_dot_gov_info&per_page=20&conditions%%5Bdocket_id%%5D=%s' % reg_num)
filename = sys.argv[1] if (len(sys.argv) > 1) else 'iloveyouuuu.csv'

fieldnames = [
'docket_id',
'document_id',
'total_comments'
]


docket_ids = {
# 'IRS-2019-0041': '2019-20035',
# 'IRS-2018-0018': '2018-23636',
# 'IRS-2019-0054': '2019-25745',
# 'IRS-2019-0037': '2019-19197',
# 'IRS-2018-0030': '2018-24140',
# 'IRS_FRDOC_0001': '2018-22022',
# 'IRS-2019-0002': '2018-27391',
# 'IRS-2019-0057': '2019-26116',
# 'IRS-2020-0003': '2020-05701',
# 'IRS-2019-0046': '2019-21477',
# 'IRS-2018-0025': '2018-18377',
# 'IRS-2019-0012': '2019-03848',
# 'IRS-2020-0008': '2020-08649',
# 'IRS-2020-0014': '2020-10224',
# 'IRS-2019-0036': '2019-18044',
# 'IRS-2020-0007': '2020-09801',
# 'IRS-2019-0049': '2019-24098',
# 'IRS-2020-0026': '2020-15504',
# 'IRS-2019-0003': '2018-28167',
# 'IRS-2020-0011': '2020-10069',
# 'IRS-2020-0004': '2020-05923',
# 'IRS-2019-0034': '2019-12030',
# 'IRS-2021-0003': '2020-27003',
# 'IRS-2019-0033': '2019-13935',
# 'IRS-2018-0013': '2018-20304',
# 'IRS-2019-0055': '2019-24847',
# 'IRS-2018-0040': '2018-26322',
# 'IRS-2020-0040': '2020-21818',
# 'IRS-2020-0030': '2020-17108',
# 'IRS-2020-0024': '2020-15349',
# 'IRS-2019-0029': '2019-12436',
# 'IRS-2020-0001': '2020-02849',
# 'IRS-2020-0012': '2020-10679',
# 'IRS-2019-0014': '2019-05400',
# 'IRS-2018-0029': '2018-23382',
'IRS-2019-0022': '2019-08075',
'IRS-2019-0004': '2018-26257',
'IRS-2020-0035': '2020-16532',
'IRS-2019-0027': '2019-12441',
'IRS-2020-0002': '2020-03723',
'IRS-2019-0024': '2019-10464',
'IRS-2020-0036': '2020-17550',
'IRS-2019-0043': '2019-20567',
'IRS-2018-0021': '2018-17276',
'IRS-2019-0009': '2019-01023',
'IRS-2020-0019': '2020-13506',
'IRS-2018-0033': '2018-24285',
'IRS-2020-0010': '2020-09879',
'IRS-2020-0031': '2020-16564',
'IRS-2019-0028': '2019-11501',
'IRS-2020-0028': '2020-16364',
'IRS-2019-0059': '2019-27813',
'IRS-2020-0018': '2020-11530',
'IRS-2020-0017': '2020-11859',
'IRS-2018-0017': '2018-15351',
'IRS-2019-0038': '2019-19325',
'IRS-2019-0056': '2019-26969',
'IRS-2020-0006': '2020-06604',
'IRS-2019-0023': '2019-09515',
'IRS-2019-0025': '2019-11292'
}

# open csv writer to write for each docketId
with open(filename, 'w', newline='') as csvfile:
  print('Getting comment data for docket_ids...')
  writer = csv.DictWriter(csvfile, fieldnames = fieldnames, lineterminator='\n')
  writer.writeheader()

  formatted_docket = {}
  # first need to get all documents for the given docket_id
  for docket_id in docket_ids:
    print('   On docket %s...' % docket_id)
    documents_url = regs_api_url("documents?filter[docketId]=%s" % docket_id)
    documents = requests.get(documents_url).json()
    # go through each and get comments for each object_id
    total_comments = 0
    if 'data' in documents: 
      for response_object in documents['data']:
        all_comments = []
        object_id = response_object['attributes']['objectId']
        comments_url = regs_api_url('comments?filter[commentOnId]=%s' % object_id)
        comments = requests.get(comments_url).json()
        print('   Looking at comments for document %s...' % object_id)
        total_comments += comments['meta']['totalElements']

      formatted_docket['total_comments'] = total_comments
      formatted_docket['docket_id'] = docket_id
      formatted_docket['document_id'] = docket_ids[docket_id]
      writer.writerow(formatted_docket)
    else:
      print('Skipped docket -- No data %s' % docket_id)       

print('CSV written at %s/%s' % (Path.cwd(), filename))
