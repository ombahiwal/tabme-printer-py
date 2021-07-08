#!/usr/bin/python

import requests
import textwrap
import os
import argparse
import time
import json
from tabulate import tabulate


global printed_orders
global line_len
printed_orders = []
line_len = 22

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
    print(cust)

def max_len(s, l=line_len-6, q=1):
    s = s[:l]
    q = "x"+str(q)
    return s + (" "*(l - len(s) - len(q))) + q

def get_print_text(data):
    print_text = ""
    for order in data['orders']:

        if order['_id'] not in printed_orders:
            printed_orders.append(order['_id'])
        else:
            continue

        item_data = []
        order_str = center("tabme.") + "\n"

        # Restuarant Name
        order_str += textwrap.fill(order['rname'], line_len) + "\n"

        # Type and Number
        order_str += order_type(order['cart'], order['_id']) + "\n"
        # print()

        # Dishes
        for item in order['cart']['dishes']:
            # amount = str('%.2f' % float(item['totalPrice']))
            item_data.append([max_len(item['name']), float(item['totalPrice'])])
            # Dish Customisation

        # Add Total
        item_data.append(["Total", float(order['cart']['totalCost'])])

        order_str += "\n" + tabulate(item_data, headers=['Item', "  " + order['cart']['currency']], floatfmt=".2f")

        # user name
        order_str += "\n\n" + textwrap.fill(order['user']['fname'] + " " + order['user']['lname'], 28)

        # Payment and Order ID
        order_str += '\nPID-' + order['paymentInfo'][18:].upper() + " | OID-" + order['_id'][18:].upper()

        # main text
        print_text += order_str + "\n"
    return print_text


def check_orders():
    print('cycle')
    url = ('http://api.tabme.io/api/v1/ds/' + 'order/fetch/open')
    response = requests.post(url, data={'restaurant_id':"5f4298d1a1f2d03aedeb6cb3", 'open':'true'})
    data = json.loads(response.text)

    # print(data)

    if data['success'] == True:

        print(list(data['orders']))

    printer = open("print.txt", "w")
    print_text = get_print_text(data)
    printer.write(str(print_text) + "\n\n")
    printer.close()
    os.system('paps --left-margin=15 --font=\"Monospace\" --cpi 15 print.txt | lp')

if __name__ == '__main__':
    while True:
        check_orders()
        time.sleep(10)
        print(printed_orders)
    # check_orders()
        # time.sleep(10)