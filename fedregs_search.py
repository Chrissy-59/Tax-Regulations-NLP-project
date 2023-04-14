#!/usr/bin/env python3

import requests
#import json
import csv

filename = 'all_regs_by_year.csv'
api_url = lambda year, page: ('https://www.federalregister.gov/api/v1/documents.json?per_page=1000&conditions%%5Bpublication_date%%5D%%5Byear%%5D=%s&conditions%%5Btype%%5D%%5B%%5D=RULE&page=%s' % (year, page))
headers = ['title',    
           'type',    
           'agency_names',
           'abstract',
           'document_number', 
           'html_url',    
           'pdf_url', 
           'publication_date']
# for big one need to filter for year and agency
# for IRS one need to have linking b/t notice/proposed/rule

# BIG
# loop through year
# get all rules for each year
with open(filename, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = headers, lineterminator='\n')
    writer.writeheader()
    for year in range(2000,2022):
        print('Looking at year %s' % year)
        # get the data for the year and then loop through pages
        first_page_url = api_url(year, 1)
        year_data = requests.get(first_page_url).json()
        num_pages = 1
        if ('total_pages' in year_data and year_data['total_pages']):
            num_pages = year_data['total_pages']
        for page in range(1, num_pages+1):
            print('   Looking at page %s' % page)
            data = requests.get(api_url(year, page)).json()
            for result in data['results']:
                formatted_row = result
                agencies = []
                for agency in result['agencies']:
                    if 'name' in agency:
                        agencies.append(agency['name'])
                    elif 'raw_name' in agency:
                        agencies.append(agency['raw_name'])
                formatted_row['agency_names'] = ';'.join(agencies)
                formatted_row.pop('agencies')
                formatted_row.pop('public_inspection_pdf_url')
                formatted_row.pop('excerpts')
                writer.writerow(formatted_row)

# IRS
#Do you think it’s possible/reasonable to create a new variable (new var = “final_effective”) for all regs where 
#type=Proposed Rule where proposed rule’s “final_effective”= effective_on date of the type=rule with the same regulation_id_numbers?






















