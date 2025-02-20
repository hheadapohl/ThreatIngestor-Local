'''
Hunter's Note: this module functions correctly when fed a threatfox link in JSON format (e.g. https://threatfox.abuse.ch/export/json/recent/). However, the saved_state system is note well definied and just
uses today's date.

The proper invocation of this module in config.yml is the following:
sources:  
  - name: threatfox
    module: threatfox
    url: 'https://threatfox.abuse.ch/export/csv/ip-port/recent/'

Good Luck!!
'''

import datetime
import requests

from threatingestor.sources import Source

class Plugin(Source):

    def __init__(self, name, url):
        self.name = name
        self.url = url


    def run(self, saved_state):
        # Create saved state (today's date) and define empty artifact list
        saved_state = str(datetime.date.today())
        artifact_list = []
        # request response from url using urlib
        url = self.url

        #request data from threatfox site using custom headers to avoid 403 error
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        }

        response = requests.get(url, headers=headers)
        #if getting a 403 error, raise for status
        response.raise_for_status()

        #read json output using requests module, save to json object 'output_json'
        output_json = response.json()

        #iterate through each item in output_json 
        for items in output_json.values():
            #iterate through nested list in each item
            for ioc in items:
                #iterate through nested dictionary in each list, returning the values for processing
                for value in ioc.values():
                    #check that the value is not "none"
                    if value is not None:
                        #process the value using threatingestor, adding it to artifact_list
                        artifact_list += self.process_element(str(value), url)

        #return list and saved state    
        print(artifact_list)
        return saved_state, artifact_list