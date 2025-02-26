
'''
Hunter's note: this module works correctly with Viriback's CSV files, but only Viriback files due to the position of the columns. More work, as with the others, is needed on the saved_state functionality.

The proper invocation of this module in config.yml is the following:

sources:  
  - name: viriback
    module: viriback
    url: 'https://threatfox.abuse.ch/export/csv/ip-port/recent/'
 
'''

import csv
import datetime
import requests

import io

from threatingestor.sources import Source

class Plugin(Source):

    def __init__(self, name, url):
        self.name = name
        self.url = url


    def run(self, saved_state):
        # Create saved state and define empty artifact list
        saved_state = str(datetime.date.today())
        artifact_list = []
        # request response from url using urlib
        url = self.url

        #if getting a 403 error, change the user agent
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        }
        #request data from viriback site
        r = requests.get(url, headers=headers)
        r.raise_for_status()

        #read csv file 'r.text' using io module, save to object 'csvstream'
        
        output = io.StringIO(r.text)
        csvstream = csv.DictReader(output)
    
        
        #iterate over csvstream and process each element
        for row in csvstream:
            for value in row.values():
                artifact_list += self.process_element(value, url)

        #return list and saved state    
        print(artifact_list)
        return saved_state, artifact_list