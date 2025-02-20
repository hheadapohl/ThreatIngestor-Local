import csv
import datetime
import logging
import requests

import io

from threatingestor.sources import Source

#logging
logger = logging.getLogger(__name__)

class Plugin(Source):

    def __init__(self):
        self.name = viriback
        self.url = "https://tracker.viriback.com/dump.php"


    def run():
        # Create saved state and define empty artifact list
        saved_state = str(datetime.date.today())
        artifact_list = []
        # request response from url using urlib
        url = "https://tracker.viriback.com/dump.php"

        #requests
        
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        #read csv file 'r.text' using io module, save to object 'csvstream'
        
        output = io.StringIO(r.text)
        csvstream = csv.DictReader(output)
        
        for row in csvstream:
            raw = row.split('#')[0].strip()
            if raw: yield row
        print(csvstream)
        
        #iterate over dictionary and process element
        for row in csvstream:
            print(row)
            artifact_list.append(row['IP'])
        logger.info("CSV succcessfully processed")

        #return list and saved state    
        print(artifact_list)
        return saved_state, artifact_list

#  def process_element(self, content, reference_link, include_nonobfuscated=False):
    

Plugin.run()
    
    