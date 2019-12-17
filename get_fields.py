#!/usr/bin/env python3

import requests
import sys
import names
from generate_payload import generate_payload
import json
from datetime import date
from datetime import datetime
import csv


OBJECT_API_NAME =  'X100k_50_ROL__c'
API_VERSION = 'v47.0'
INSTANCE_URL = 'https://appian--rnisquad.my.salesforce.com'
DESCRIBE_URI = '/services/data/'+ API_VERSION + '/sobjects/' + OBJECT_API_NAME +'/describe/'
CREATE_LOAD_JOB_URI = '/services/data/'+ API_VERSION + '/jobs/ingest' +'/'
ACCESS_URI = '/services/oauth2/token'

num_checkbox_fields = []
num_currency_fields = []
num_date_fields = []
num_datetime_fields = []
num_email_fields = []
num_geolocation_fields = []
num_lookup_relationship_fields = []
num_number_fields = []
num_percent_fields = []
num_phone_fields = []
num_picklist_fields = []
num_picklist_multiselect_fields = []
num_text_fields = []
num_text_area_fields = []
num_text_area_long_fields = []
num_text_area_rich_fields = []
num_text_encrypted_fields = []
num_time_fields = []
num_url_fields = []


def get_access_token():

    access_token_request_body = {
    # your auth here
        'grant_type':'password',
        'client_id':'',
        'client_secret':'',
        'username':'',
        'password':'',
    }

    authentication_response = requests.post(url = INSTANCE_URL + ACCESS_URI, data = access_token_request_body)
    return authentication_response.json()['access_token']
# object_description = requests.get(INSTANCE_URL+DESCRIBE_URI, )

def get_fields():

    access_token = get_access_token()

    object = requests.get(url = INSTANCE_URL + DESCRIBE_URI, headers = {'Authorization':  'Bearer ' + access_token}).json()
    field_names = []
    for field in object['fields']:
        field_names.append(field['name'])
    return field_names

fields = get_fields()

def for_each_list_value_create_a_dictionary_keyed_value(dictionary, key, set_of_values):
    counter = 0
    for value in set_of_values:
        if key is 'GEOLOCATION':
            dictionary['GEOLOCATION_'+str(counter)+'__Longitude__s'] = value['longitude']
            dictionary['GEOLOCATION_'+str(counter)+'__Latitude__s'] = value['latitude']
        else:
            dictionary[key+'_'+str(counter)+'__c'] = value
        counter += 1

def format_payload(payload):
    formatted_payload = {}
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'CHECKBOX',payload['checkbox'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'CURRENCY',payload['currency'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'DATE',payload['date'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'DATETIME',payload['datetime'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'EMAIL',payload['email'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'GEOLOCATION',payload['geolocation'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'LOOKUP_RELATIONSHIP',payload['lookup_relationship'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'NUMBER',payload['number'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'PERCENT',payload['percent'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'PHONE',payload['phone'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'PICKLIST',payload['picklist'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'PICKLIST_MULTISELECT',payload['picklist_multiselect'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'TEXT',payload['text'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'TEXT_AREA',payload['text_area'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'TEXT_AREA_LONG',payload['text_area_long'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'TEXT_AREA_RICH',payload['text_area_rich'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'TEXT_ENCRYPTED',payload['text_encrypted'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'TIME',payload['time'])
    for_each_list_value_create_a_dictionary_keyed_value(formatted_payload, 'URL' ,payload['url'])
    formatted_payload['Name'] = names.get_full_name().replace(' ', '.').lower()
    return formatted_payload

def convert_json_to_csv_format(json):
    csv_payload = {
    'HEADERS': [],
    'VALUES': []
    }
    for key in json:
        csv_payload['HEADERS'].append(key)
        csv_payload['VALUES'].append(json[key])
    return csv_payload

def write_payload_to_csv(payload):
    with open('payload.csv', 'a') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_NONE)
        wr.writerow(payload)

def jsonconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

def create_records(access_token, filepath):
    with open(filepath) as csv_payload:
        csv_data = csv_payload.read()
        create_job_request_body = {
        'object': OBJECT_API_NAME,
        'contentType': 'CSV',
        'operation': 'insert',
        'lineEnding':'LF'
        }
        create_job_request_body = json.dumps(create_job_request_body)
        job_creation_response = requests.post(url = INSTANCE_URL + CREATE_LOAD_JOB_URI, headers = {'Authorization':  'Bearer ' + access_token, 'Content-Type': 'application/json; charset=UTF-8'}, data = create_job_request_body ).json()
        print(job_creation_response)
        job_id = job_creation_response['id']
        bulk_load_response = requests.put(url = INSTANCE_URL + CREATE_LOAD_JOB_URI + job_id + '/batches/', headers = {'Authorization':  'Bearer ' + access_token, 'Content-Type': 'text/csv', 'Accept': 'application/json'}, data = csv_data )
        print(bulk_load_response)
        bulk_load_close = requests.patch(url = INSTANCE_URL + CREATE_LOAD_JOB_URI + job_id + '/', headers = {'Authorization':  'Bearer ' + access_token, 'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json'}, data = json.dumps({'state':'UploadComplete'}) ).json()
        print(bulk_load_close)
        bulk_load_job_status = requests.get(url = INSTANCE_URL + CREATE_LOAD_JOB_URI + job_id + '/', headers = {'Authorization':  'Bearer ' + access_token, 'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json'}).json()
        print(bulk_load_job_status)

checkbox_count = 0
currency_count = 0
date_count = 0
datetime_count = 0
email_count = 0
geolocation_count = 0
lookup_relationship_count = 0
number_count = 0
percent_count = 0
phone_count = 0
picklist_count = 0
picklist_multiselect_count = 0
text_count = 0
text_area_count = 0
text_area_long_count = 0
text_area_rich_count = 0
text_encrypted_count = 0
time_count = 0
url_count = 0


for field in fields:
    if 'CHECKBOX' in field:
        num_checkbox_fields.append(checkbox_count)
        checkbox_count += 1
    elif 'CURRENCY' in field:
        num_currency_fields.append(currency_count)
        currency_count += 1
    elif 'DATETIME' in field:
        num_datetime_fields.append(datetime_count)
        datetime_count += 1
    elif 'DATE' in field:
        num_date_fields.append(date_count)
        date_count += 1
    elif 'EMAIL' in field:
        num_email_fields.append(email_count)
        email_count += 1
    elif '_Longitude_' in field:
        num_geolocation_fields.append(geolocation_count)
        geolocation_count += 1
    elif 'LOOKUP_RELATIONSHIP' in field:
        num_lookup_relationship_fields.append(lookup_relationship_count)
        lookup_relationship_count += 1
    elif 'NUMBER' in field:
        num_number_fields.append(number_count)
        number_count += 1
    elif 'PERCENT' in field:
        num_percent_fields.append(percent_count)
        percent_count += 1
    elif 'PHONE' in field:
        num_phone_fields.append(phone_count)
        phone_count += 1
    elif 'PICKLIST_MULTISELECT' in field:
        num_picklist_multiselect_fields.append(picklist_multiselect_count)
        picklist_multiselect_count += 1
    elif 'PICKLIST' in field:
        num_picklist_fields.append(picklist_count)
        picklist_count += 1
    elif 'TEXT_AREA_RICH' in field:
        num_text_area_rich_fields.append(text_area_rich_count)
        text_area_rich_count += 1
    elif 'TEXT_AREA_LONG' in field:
        num_text_area_long_fields.append(text_area_long_count)
        text_area_long_count += 1
    elif 'TEXT_AREA' in field:
        num_text_area_fields.append(text_area_count)
        text_area_count += 1
    elif 'TEXT_ENCRYPTED' in field:
        num_text_encrypted_fields.append(text_encrypted_count)
        text_encrypted_count += 1
    elif 'TEXT' in field:
        num_text_fields.append(text_count)
        text_count += 1
    elif 'TIME' in field:
        num_time_fields.append(time_count)
        time_count += 1
    elif 'URL' in field:
        num_url_fields.append(url_count)
        url_count += 1

# Payload primer provides the payload generator with a list for each data type
# These lists are just list of proper len and values equal to the position in the list ex: [0, 1, 2]
payload_primer = {
'checkbox': num_checkbox_fields,
'currency': num_currency_fields,
'date': num_date_fields,
'datetime': num_datetime_fields,
'email': num_email_fields,
'geolocation': num_geolocation_fields,
'lookup_relationship': num_lookup_relationship_fields,
'number': num_number_fields,
'percent': num_percent_fields,
'phone': num_phone_fields,
'picklist': num_picklist_fields,
'picklist_multiselect': num_picklist_multiselect_fields,
'text': num_text_fields,
'text_area': num_text_area_fields,
'text_area_long': num_text_area_long_fields,
'text_area_rich': num_text_area_rich_fields,
'text_encrypted': num_text_encrypted_fields,
'time': num_time_fields,
'url': num_url_fields
}
access_token = get_access_token()
# i = 0
# while i < 95783:
i = 0
csv_payload_2 = {
    'HEADERS': [],
    'VALUES': []
    }
while i < 95770:
    payload = generate_payload(payload_primer)
    formatted_payload = format_payload(payload)
    csv_payload = convert_json_to_csv_format(formatted_payload)
    csv_payload_2['HEADERS'] = csv_payload['HEADERS']
    csv_payload_2['VALUES'].append(csv_payload['VALUES'])
    i += 1
with open('payload.csv', 'w') as csv_file:
    wr = csv.writer(csv_file, quoting=csv.QUOTE_NONE)
    wr.writerow(csv_payload_2['HEADERS'])
    for value in csv_payload_2['VALUES']:
        wr.writerow(value)
create_records(access_token, 'payload.csv')
print("Done!")
