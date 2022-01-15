#!/usr/bin/python

import requests
import textwrap
import os
import argparse
import time
import json
from tabulate import tabulate
import sys
import datetime
from subprocess import (PIPE, Popen)
from dotenv import dotenv_values
global environment 
global printed_orders
global line_len
global API_DS
line_len = 22
API_DS = "http://api.tabme.io/api/v1/ds/print/"
printed_orders = []

def center(t):
    return " "*(int(line_len/2-len(t)/2))+str(t)

def order_type(cart, id):
    print(cart)
    tnum = int(cart['tablenum'])
    label = "Table #"
    if tnum < 0:
        if tnum == -1:
            label = "Pickup "
        elif tnum == -2:
            label = "Delivery "
        elif tnum == -3:
            label = cart['order_label'] + " "
        label += str(int(id[18:], base=16))[-3:]
    else:
        label += str(tnum)

    return center(label)

def format_customisation(cust):
    return cust.split("_")[0]

def max_len(s,q=1, l=line_len-6, title=False):
    
    # s = s[:l] + "\n"
    
    # print(pieces)
    if not q<=0:
        q = "x"+str(q)
    else:
        q = ""
    pieces = textwrap.wrap(s, l-len(q))
    name = ""
    # if title:
    #     name = pieces[0][:l-3]+(" "`*(l - len(pieces[0]) - len(q))) + q
    name = pieces[0]+(" " * (l - len(pieces[0]) - len(q))) + q + "\n"
    for i in range(1, len(pieces)):
        name += pieces[i] + "\n"
    
    return name


def get_print_text2(data):
    print_text = ""
    update_url = API_DS + "cloud/rpi/job/dequeue"
    for jobs in data['queue']:
        order = jobs['job']
        # if order['_id'] not in printed_orders:
        #     printed_orders.append(order['_id'])
        # else:
        #     continue

        item_data = []
        order_str = center("tabme.") + "\n"

        # Restuarant Name
        order_str += textwrap.fill(order['rname'], line_len) + "\n"

        # Type and Number
        order_str += order_type(order['cart'], order['_id']) + "\n"

        # Dishes - iterate optionsets
        for item in order['cart']['dishes']:
            for optns in item['optionSets']:
                # print('option', optns)
                item_data.append([max_len(item['name'], optns['option_dish_count'], line_len)])
                for optn in optns['optionset']:
                    item_data.append([max_len("." + optn['title'], 0, line_len - 3)])
                    for optn_val in optn['values']:
                        item_data.append([max_len(". " + optn_val['value'], 0, line_len - 4)])

        # if order['cart']['tip'] > 0:
        #     item_data.append(["Tip", float(order['cart']['tip'])])
        # if order['cart']['delivery_fee'] > 0:
        #     item_data.append(["Delivery fee", float(order['cart']['delivery_fee'])])
        # if order['cart']['promo'] > 0:
        #     item_data.append(["(Promo)", float(order['cart']['promo'])])
        # # Add Total
        # item_data.append(["Total", float(order['cart']['totalCost'])])

        order_str += "\n" + tabulate(item_data, headers=['Item'])
        order_str += '\n' + textwrap.fill(order['cart']['pmethod'], line_len)
        # user name
        order_str += "\n\n" + textwrap.fill(order['user']['fname'] + " " + order['user']['lname'], 28)
        # Payment and Order ID
        order_str += '\nPID-' + order['paymentInfo'][18:].upper() + " | OID-" + order['_id'][18:].upper()
        # Time Placed
        order_str += '\n' + textwrap.fill("Placed: "+str(datetime.datetime.strptime(order['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ"))[:-7], line_len)

        # main text
        print_text += order_str + "\n"
        # Dequeue Job
        # jobs
        print(jobs)
        requests.post(update_url, data={'job_id': jobs['_id']})

    return print_text



# change fro queue
def get_print_text(data):
    print_text = ""
    update_url = API_DS + "cloud/rpi/job/dequeue"
    for jobs in data['queue']:
        order = jobs['job']
        # if order['_id'] not in printed_orders:
        #     printed_orders.append(order['_id'])
        # else:
        #     continue

        item_data = []
        order_str = center("tabme.") + "\n"

        # Restuarant Name
        order_str += textwrap.fill(center(order['rname']), line_len) + "\n"

        # Type and Number
        order_str += order_type(order['cart'], order['_id']) + "\n"

        # Dishes - iterate optionsets
        for item in order['cart']['dishes']:
            for optns in item['optionSets']:
                # print('option', optns)
                item_data.append([max_len(item['name'], optns['option_dish_count']), round(float(optns['option_price'] + item['basePrice']), 2)])
                for optn in optns['optionset']:
                    item_data.append([max_len("." + format_customisation(optn['title']), 0, line_len - 6), ''])
                    for optn_val in optn['values']:
                        item_data.append([max_len(". " + optn_val['value'], 0, line_len - 7), ''])

        if order['cart']['tip'] > 0:
            item_data.append(["Tip", float(order['cart']['tip'])])
        if order['cart']['delivery_fee'] > 0:
            item_data.append(["Delivery fee", float(order['cart']['delivery_fee'])])
        if order['cart']['promo'] > 0:
            item_data.append(["(Promo)", float(order['cart']['promo'])])
        # Add Total
        item_data.append(["Total", float(order['cart']['totalCost'])])

        order_str += "\n" + tabulate(item_data, headers=['Item', order['cart']['currency']], floatfmt=".2f")
        order_str += '\n' + textwrap.fill(order['cart']['pmethod'], line_len)
        # user name
        order_str += "\n\n" + textwrap.fill(order['user']['fname'] + " " + order['user']['lname'], 28) + "\n"
        # additional order  details 
        # Delivery address (and time)
        if 'Delivery' in order_type(order['cart'], order['_id']):
            order_str += textwrap.fill(order['user']['address'], line_len) + "\n"
        # Pickup / Delivery  Time.
        if order['cart']['pickup_date']:
            order_str += '\n' + textwrap.fill("Pickup-Time", line_len) +"\n"
            order_str += textwrap.fill(order['cart']['pickup_date'], line_len) + "\n"

        # Payment and Order ID
        order_str += '\nPID-' + order['paymentInfo'][18:].upper() + " | OID-" + order['_id'][18:].upper()
        # Time
        order_str += '\n' + textwrap.fill(str(datetime.datetime.strptime(order['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ"))[:-7], line_len)
        # main text

        print_text += order_str + "\n\n\n"
        # Dequeue Job
        # jobs
        print(jobs)
        requests.post(update_url, data={'job_id': jobs['_id']})

    return print_text


def check_orders():
    print('cycle')
    url = (API_DS + 'cloud/rpi/job/get')
    response = requests.post(url, data={'m_id':environment['rid']})
    data = json.loads(response.text)
    print(data)
    # if data['success'] == True:
    #     # print(list(data['queue']))

    printer = open("print2.txt", "w")
    if '-l' in sys.argv:
        print_text = get_print_text2(data)
    else:
        print_text = get_print_text(data)
    
    if len(print_text) > 10:
        printer.write(str(print_text) + "\n\n")
        printer.close()
        print(print_text)
        Popen('paps --left-margin=14 --font=\"Monospace\" --cpi 17 print2.txt | lp', stdout=PIPE, shell=True).stdout.read()

        # os.system('paps --left-margin=14 --font=\"Monospace\" --cpi 17 print2.txt | lp')
#     else:
#         printer.write(str(""))
    

if __name__ == '__main__':
    environment = dotenv_values(".env")
    line_len = int(environment['line_len'])
    while True:
        try:
            check_orders()
        except Exception as e:
            print("ERROR in printing", e)
        time.sleep(10)
