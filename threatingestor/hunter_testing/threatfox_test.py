import csv
import requests
import pandas
import io
import json
import pprint

def run():
    # Create saved state and define empty artifact list
    artifact_list = []
    # request response from url using urlib
    url = "https://threatfox.abuse.ch/export/json/ip-port/recent/"
    #requests
    
    headers = {
        "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
    }

    response = requests.get(url, headers=headers)

    #read csv file 'r.text' using io module, save to object 'csvstream'

    #output = io.StringIO(r.text)

    output_json = response.json()

    for items in output_json.values():
        for ioc in items:
            for key, value in ioc.items():
                if key == 'ioc_value':
                    print(value)


   
    #iterate over dictionary and process element
    #for row in csvstream:
    #    print(row)
    #    artifact_list.append(row['IP'])

    #return list and saved state    
    #print(artifact_list)
    #return artifact_list
    




run()
    
    