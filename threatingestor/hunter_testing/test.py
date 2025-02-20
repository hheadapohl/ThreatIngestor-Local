#!/usr/bin/env python3

import csv
from datetime import datetime
import requests

import io

def main():
    #static variables
    #url = "https://threatfox.abuse.ch/export/csv/ip-port/recent/"
    url = "https://tracker.viriback.com/dump.php"
    ioc_field = 2
    saved_state = None
    artifact_list = []
    compared_state = compare_state(saved_state)
    if saved_state is None:
        print("save state none")
        create_save_state(saved_state)
        clean_data = get_csv_data(url)
        process_csv_field_all(artifact_list, clean_data, ioc_field)
    if compared_state == True:
        print("save state exists and is in the past")
        #artifact_list = process_csv_field_new(clean_data, ioc_field)
    #artifact_list = process_csv_field(ioc_field, url)
    print(artifact_list)
        
def decomment(source_data):
    #remove nested list items containing "#" in the first or second position, indicating a comment
    cleaned_list = [[entry for entry in sublist if not (len(entry) > 0 and entry[0] == '#') and not (len(entry) > 1 and entry[1] == '#')] for sublist in source_data]
    #remove empty sublists created by decommenting
    return [sublist for sublist in cleaned_list if sublist]

def create_save_state(saved_state):
    if saved_state is None:
        saved_state = datetime.now()
    return saved_state

def compare_state(saved_state):
    current_time = datetime.now()
    if saved_state.time() < current_time.time():
        return True
    else:
        return False


def get_csv_data(url):
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
    source_data = csv.reader(stream_output)
    clean_data = decomment(source_data)
    print(clean_data)
    return clean_data

def process_csv_field_new(clean_data, ioc_field, url):
    #process
    artifact_list = []
    #iterate over csvstream and process each predefined field
    for row in clean_data:
        artifact_list.append(row[ioc_field])
    #print(artifact_list)
    return artifact_list

def process_csv_field_all(artifact_list, clean_data, ioc_field):
    #process
    #iterate over csvstream and process each predefined field
    for row in clean_data:
        artifact_list.append(row[ioc_field])
    #print(artifact_list)
    return artifact_list

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
