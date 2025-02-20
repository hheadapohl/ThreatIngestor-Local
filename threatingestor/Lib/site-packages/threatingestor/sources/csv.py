
'''
Hunter's Note: This module is incomplete. The idea here is to ingest all types of structured CSV files (for example, threatfox) but there are two snags:
 - First, the saved state functionality necessary for each source module is not documented. Other sources have used the RSS last published date as the basis for the old state, but since CSV files are
   not dated this was not possible. The attempted approach below was to use 48 hours as the last published time for comparison.

- Second, some CSV files, notably threatfox, contain nonstandard comments at the start of each file. The standard CSV modules in Python do not have functionality to skip those and get the correct column headers.

- Hopefully another Python wizard can finish the quest that I started. Good luck!
'''
import csv
import datetime
import requests

import io

from threatingestor.sources import Source

class Plugin(Source):

    def __init__(self, name, url, ioc_field):
        self.name = name
        self.url = url
        self.ioc_field = ioc_field
    '''
    def compare_states(self, self.saved_state, self.update_frequency):
        compared = self.saved_state - datetime.timedelta(hours = 48)
    '''
    
    def decomment(self, source_data):
        #remove nested list items containing "#" in the first or second position, indicating a comment
        cleaned_list = [[entry for entry in sublist if not (len(entry) > 0 and entry[0] == '#') and not (len(entry) > 1 and entry[1] == '#')] for sublist in source_data]
        #remove empty sublists created by decommenting
        return [sublist for sublist in cleaned_list if sublist]
    
    def get_csv_data(self, url):
        # request response from url using urlib
        #if getting a 403 error, change the user agent
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        }
        #request data from source URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        #read csv file 'response.text' using io module, save to object 'csvstream'
        stream_output = io.StringIO(response.text)
        #read stream output using csv reader
        source_data = csv.reader(stream_output)
        #remove comments
        clean_data = self.decomment(source_data)
        return clean_data
    
    def process_csv_field(self, clean_data, ioc_field, artifact_list, url):
        #process
        #iterate over cleaned data and process each pitem in predefined column
        for row in clean_data:
            artifact_list += self.process_element(row[ioc_field], url)
        #print(artifact_list)
        return artifact_list
    
    def run(self, saved_state):
        #check if saved state exists. if exists, do not run. if None, continue
        artifact_list = []
        if saved_state == None:
            saved_state = str(datetime.date.today())
            clean_data = self.get_csv_data(self.url)
            artifact_list = self.process_csv_field(clean_data, self.ioc_field, artifact_list, self.url)
        elif saved_state != None:
            print("saved state exists") 
        '''
        elif:
            compare_states == True:
            saved_state = str(datetime.date.today())
            clean_data = self.get_csv_data(self.url)
            artifact_list = self.process_csv_field(clean_data, self.ioc_field, self.url)
        '''
        #return list and saved state    
        return saved_state, artifact_list

            