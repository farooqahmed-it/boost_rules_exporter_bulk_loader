# The utility scrip takes csv export of keywords array, skus array as input
# builds json payload to be posted to LW fusion5 to bulk upload boost rules.

import csv
import json
import requests
import ast

basePath = 'content\Test Rules'                                                   # input directory of the csv export
filename = 'boost_rules_export.csv'                                               # csv export filename
lw_f5_url = "https://fusion5host/api/apps/test/query-rewrite/instances"           # sample URL
user = "xxxxxxx"
password = "xxxxxxxx"

# function for the cURL requests
def lw_f5_post(uri, json_body, user, passw, verb):
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        # make HTTP verb parameter case-insensitive by converting to lower()
        if verb.lower() == "get":
            resp = requests.get(uri, headers=headers, data=json_body)
        elif verb.lower() == "post":
            resp = requests.post(uri, headers=headers, data=json_body, auth=(user, passw))
        elif verb.lower() == "put":
            resp = requests.put(uri, headers=headers, data=json_body)

        # read the text object string
        try:
            resp_text = json.loads(resp.text)
        except:
            resp_text = resp.text

        # catch exceptions and print errors to terminal
    except Exception as error:
        print ('\nlw_f5_curl() error:', error)
        resp_text = error

    # return the Python dict of the request
    print ("resp_text:", resp_text)
    return resp_text

# ___main___

rows = []

# Reading csv file
with open(basePath+'\\'+filename, 'r') as csvfile:
    data = csv.DictReader(csvfile)

    for row in data:
        json_str = {
            "enabled": True,
            "name": row['name'],
            "matching": "keywords",
            "search_terms": ast.literal_eval(row['keywords']),
            "field_name": "product_id_s",
            "field_values": ast.literal_eval(row['skus']),
            "type":"boost_list",
            "review":"approved",
            "use_qec": False
        }

        boost_rule_json = json.dumps(json_str)
        #print(jsonStr)

        resp_text = lw_f5_post(lw_f5_url, boost_rule_json, user, password, "post")