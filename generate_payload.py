#!/usr/bin/env python3

import json
import random
import names
import string
from datetime import date, datetime,timedelta


JPN_EMOTICONS = ['(｡◕ ∀ ◕｡)','｀ｨ(´∀｀∩','__ﾛ(,_,*)','・(￣∀￣)・:*:','ﾟ･✿ヾ╲(｡◕‿◕｡)╱✿･ﾟ',',。・:*:・゜’( ☻ ω ☻ )。・:*:・゜’','(╯°□°）╯︵ ┻━┻)','(ﾉಥ益ಥ）ﾉ﻿ ┻━┻','┬─┬ノ( º _ ºノ)','¯\_(ツ)_/¯']
VALID_LOOKUP_IDS = ['0016300000fYeoMAAS', '0016300000fdvGjAAI', '0016300000fYgeIAAS', '0016300000fYgeBAAS', '0016300000fYgQsAAK', '0016300000fYgVmAAK', '0016300000fYgdUAAS']


def generate_payload(payload_primer):
    payload = {}
    payload['checkbox'] = generate_checkbox_values(payload_primer['checkbox'])
    payload['currency'] = generate_currency_values(payload_primer['currency'])
    payload['date'] = generate_date_values(payload_primer['date'])
    payload['datetime'] = generate_datetime_values(payload_primer['datetime'])
    payload['email'] = generate_email_values(payload_primer['email'])
    payload['geolocation'] = generate_geolocation_values(payload_primer['geolocation'])
    payload['lookup_relationship'] = generate_lookup_relationship_values(payload_primer['lookup_relationship'])
    payload['number'] = generate_number_values(payload_primer['number'])
    payload['percent'] = generate_percent_values(payload_primer['percent'])
    payload['phone'] = generate_phone_values(payload_primer['phone'])
    payload['picklist'] = generate_picklist_values(payload_primer['picklist'])
    payload['picklist_multiselect'] = generate_picklist_multiselect_values(payload_primer['picklist_multiselect'])
    payload['text'] = generate_text_values(payload_primer['text'])
    payload['text_area'] = generate_text_area_values(payload_primer['text_area'])
    payload['text_area_long'] = generate_text_area_long_values(payload_primer['text_area_long'])
    payload['text_area_rich'] = generate_text_area_rich_values(payload_primer['text_area_rich'])
    payload['text_encrypted'] = generate_text_encrypted_values(payload_primer['text_encrypted'])
    payload['time'] = generate_time_values(payload_primer['time'])
    payload['url'] = generate_url_values(payload_primer['url'])
    return payload


def generate_checkbox_values(num_checkbox_fields):
    checkbox_values = []
    for checkbox_fields in num_checkbox_fields:
        random_boolean = bool(random.getrandbits(1))
        checkbox_values.append(random_boolean)
    return checkbox_values

def generate_currency_values(num_currency_fields, len_left_deci = 8):
    currency_values = []
    for currency_fields in num_currency_fields:
        rand_dollar_value = randint_of_len(len_left_deci)
        rand_change_value = randint_of_len(2)/100.0
        rand_currency = rand_dollar_value + rand_change_value
        currency_values.append(rand_currency)
    return currency_values

def generate_date_values(num_date_fields):
    date_values = []
    for date_fields in num_date_fields:
        start_date = date(day = 25, month = 6, year = 1982).toordinal()
        end_date = date.today().toordinal()
        rand_date = date.fromordinal(random.randint(start_date, end_date))
        rand_date = rand_date.isoformat()
        date_values.append(rand_date)
    return date_values

def generate_datetime_values(num_datetime_fields):
    datetime_values = []
    for datetime_fields in num_datetime_fields:
        start_datetime = datetime.now().replace(day = 25, month = 6, year = 1982)
        years = datetime.now().year - start_datetime.year + 1
        end_datetime = start_datetime + timedelta(days=365 * years)
        rand_datetime = start_datetime + (end_datetime - start_datetime) * random.random()
        rand_datetime = rand_datetime.isoformat()
        datetime_values.append(rand_datetime)
    return datetime_values

def generate_email_values(num_email_fields):
    email_values = []
    domains = ['gmail.com','yahoo.com','hotmail.com','aol.com','outlook.com','salesforce.com']
    for email_fields in num_email_fields:
        rand_name = names.get_full_name().replace(' ', '.').lower()
        final_domain_index = len(domains) - 1
        rand_domain = domains[random.randint(0, final_domain_index)]
        rand_email = rand_name + '@' + rand_domain
        email_values.append(rand_email)
    return email_values

def generate_geolocation_values(num_geolocation_fields, len_deci = 8):
    geolocation_values = []
    rand_geolocation = {
                            'latitude':0,
                            'longitude':0
                        }
    for geolocation_fields in num_geolocation_fields:

        latitude_int = random.randint(-90,89)
        latitude_deci = randint_of_len(len_deci)/(10.0**len_deci)
        rand_latitude = latitude_int + latitude_deci
        rand_geolocation['latitude'] = rand_latitude

        longitude_int = random.randint(-180, 179)
        longitude_deci = randint_of_len(len_deci)/(10.0**len_deci)
        rand_longitude = longitude_int + longitude_deci
        rand_geolocation['longitude'] = rand_longitude

        geolocation_values.append(rand_geolocation)

    return  geolocation_values

def generate_lookup_relationship_values(num_lookup_relationship_fields):
    lookup_relationship_values = []
    # TODO - BASED AGAINST ACCOUNT
    valid_ids = VALID_LOOKUP_IDS
    for lookup_relationship_fields in num_lookup_relationship_fields:
        final_lookup_relationship_index = len(valid_ids) - 1
        rand_lookup_relationship = valid_ids[random.randint(0, final_lookup_relationship_index)]
        lookup_relationship_values.append(rand_lookup_relationship)
    return lookup_relationship_values

def generate_number_values(num_number_fields):
    number_values = []
    number_count = 0
    for number_fields in num_number_fields:
        #TODO come up with a better way to distinguish float and int on number columns
        if number_count % 2 is 0:
            rand_int_value = randint_of_len(5)
            rand_deci_value = randint_of_len(1)/10.0
            rand_number = rand_int_value + rand_deci_value
        if number_count % 2 is 1:
            rand_number = randint_of_len(4)
        number_values.append(rand_number)
        number_count += 1
    return number_values

def generate_percent_values(num_percent_fields, len_left_deci = 16):
    percent_values = []
    for percent_fields in num_percent_fields:
        rand_int_value = randint_of_len(len_left_deci)
        rand_deci_value = randint_of_len(2)/100.0
        rand_percent = rand_int_value + rand_deci_value
        percent_values.append(rand_percent)
    return percent_values

def generate_phone_values(num_phone_fields):
    phone_values = []
    for phone_fields in num_phone_fields:
        rand_area_code_value = str(randint_of_len(3))
        rand_exchange_value = str(randint_of_len(3))
        rand_line_number_value = str(randint_of_len(4))
        rand_phone = '+1 '+'('+rand_area_code_value+')' + ' ' + rand_exchange_value + '-' + rand_line_number_value
        phone_values.append(rand_phone)
    return phone_values

def generate_picklist_values(num_picklist_fields):
    picklist_values = []
    #TODO - define standard set
    valid_picklist_options = JPN_EMOTICONS
    for picklist_fields in num_picklist_fields:
        final_picklist_index = len(valid_picklist_options) - 1
        rand_picklist = valid_picklist_options[random.randint(0, final_picklist_index)]
        picklist_values.append(rand_picklist)
    return picklist_values

def generate_picklist_multiselect_values(num_picklist_multiselect_fields):
    picklist_multiselect_values = generate_picklist_values(num_picklist_multiselect_fields)
    return picklist_multiselect_values

def generate_text_values(num_text_fields, text_limit=255):
    text_values = []
    for text_fields in num_text_fields:
        #TODO Change back to being based on text limit, changing this for perf testing
        text_len = random.randint(10,100)
        rand_text = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(text_len)])
        text_values.append(rand_text)
    return text_values

def generate_text_area_values(num_text_area_fields):
    text_area_values = generate_text_values(num_text_area_fields)
    return text_area_values

def generate_text_area_long_values(num_text_area_long_fields):
    text_area_long_values = generate_text_values(num_text_area_long_fields, 500)
    return text_area_long_values

def generate_text_area_rich_values(num_text_area_rich_fields):
    text_area_rich_values = generate_text_values(num_text_area_rich_fields, 500)
    return text_area_rich_values

def generate_text_encrypted_values(num_text_encrypted_fields):
    text_encrypted_values = generate_text_values(num_text_encrypted_fields, 100)
    return text_encrypted_values

def generate_time_values(num_time_fields, text_limit = 255):
    time_values = []
    for time_fields in num_time_fields:
        rand_seconds = random.randint(0,86400)
        rand_time = str(timedelta(seconds=rand_seconds))
        time_values.append(rand_time)
    return time_values

def generate_url_values(num_url_fields, text_limit = 255):
    url_values = []
    for url_fields in num_url_fields:
        rand_url = 'https://www.httpbin.org/get'
        url_values.append(rand_url)
    return url_values

def randint_of_len(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)




# with open('./payload.json') as outfile:
#     json.dump(payload, outfile)
