#!/usr/bin/env python3

import requests
import json
import csv

filename = 'all_irs_revised.csv'
api_url = lambda year, page: ('''https://www.federalregister.gov/api/v1/documents.json\
?per_page=1000\
&page=%s\
&conditions%%5Bpublication_date%%5D%%5Byear%%5D=%s\
&conditions%%5Bagencies%%5D%%5B%%5D=internal-revenue-service\
&conditions%%5Btype%%5D%%5B%%5D=RULE\
&conditions%%5Btype%%5D%%5B%%5D=PRORULE\
&conditions%%5Btype%%5D%%5B%%5D=NOTICE\
&fields%%5B%%5D=abstract\
&fields%%5B%%5D=action\
&fields%%5B%%5D=agency_names\
&fields%%5B%%5D=body_html_url\
&fields%%5B%%5D=citation\
&fields%%5B%%5D=comment_url\
&fields%%5B%%5D=dates\
&fields%%5B%%5D=docket_id\
&fields%%5B%%5D=docket_ids\
&fields%%5B%%5D=document_number\
&fields%%5B%%5D=effective_on\
&fields%%5B%%5D=full_text_xml_url\
&fields%%5B%%5D=html_url\
&fields%%5B%%5D=page_length\
&fields%%5B%%5D=page_views\
&fields%%5B%%5D=pdf_url\
&fields%%5B%%5D=publication_date\
&fields%%5B%%5D=regulation_id_number_info\
&fields%%5B%%5D=regulation_id_numbers\
&fields%%5B%%5D=regulations_dot_gov_info\
&fields%%5B%%5D=title\
&fields%%5B%%5D=topics\
&fields%%5B%%5D=type''' % (page, year))

headers = [
    'abstract',
    'action',
    'agency_names',
    'body_html_url',
    'citation',
    'comment_url',
    'dates',
    'docket_id',
    'docket_ids',
    'document_number',
    'effective_on',
    'full_text_xml_url',
    'html_url',
    'page_length',
    'page_views',
    'pdf_url',
    'publication_date',
    'regulation_id_number_info',
    'regulation_id_numbers',
    'regulations_dot_gov_info',
    'title',
    'topics',
    'type']
# for big one need to filter for year and agency
# for IRS one need to have linking b/t notice/proposed/rule

# IRS
#Do you think it’s possible/reasonable to create a new variable (new var = “final_effective”) for all regs where 
#type=Proposed Rule where proposed rule’s “final_effective”= effective_on date of the type=rule with the same regulation_id_numbers?
with open(filename, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = headers, lineterminator='\n')
    writer.writeheader()
    for year in range(2000,2022):
        first_page_url = api_url(year, 1)
        print('Looking at year %s - %s' % (year,first_page_url))
        # get the data for the year and then loop through pages
        year_data = requests.get(first_page_url).json()
        num_pages = 1
        if ('total_pages' in year_data and year_data['total_pages']):
            num_pages = year_data['total_pages']
        for page in range(1, num_pages+1):
            print('   Looking at page %s' % page)
            data = requests.get(api_url(year, page)).json()
            counter = 0
            for result in data['results']:
                formatted_row = result
                agencies = ';'.join(result['agency_names'])
                formatted_row['agency_names'] = agencies
                docket_ids = ';'.join(result['docket_ids'])
                formatted_row['docket_ids'] = docket_ids
                page_views = 'count: %s; last_updated: %s' % (result['page_views']['count'], result['page_views']['last_updated'])
                formatted_row['page_views'] = page_views
                #reg_id_number_info = str(result['regulation_id_number_info'])
                reg_id_numbers = ';'.join(result['regulation_id_numbers'])
                formatted_row['regulation_id_numbers'] = reg_id_numbers
                #topics
                writer.writerow(formatted_row)
                counter += 1
            print('    Printed %s rows.' % counter)









