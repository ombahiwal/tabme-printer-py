#!/usr/bin/python

import requests
import textwrap
import os
import argparse
import time
import json
from tabulate import tabulate


global printed_orders
printed_orders = []

def center(t):
    return " "*(14 - int(len(t)/2))+str(t)

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

def max_len(s, l=23, q=1):
    s = s[:l]
    q = "x"+str(q)
    return s + (" "*(l - len(s) - len(q))) + q

def check_orders():

    url = ('http://api.tabme.io/api/v1/ds/' + 'order/fetch/open')
    response = requests.post(url, data={'restaurant_id':"5f4298d1a1f2d03aedeb6cb3", 'open':'true'})
    data = json.loads(response.text)

    # print(data)

    if data['success'] == True:

        print(list(data['orders']))

    printer = open("print.txt", "w")

    print_text =""
    for order in data['orders']:
        item_data = []
        order_str = center("tabme.") + "\n"

        # Restuarant Name
        order_str += textwrap.fill(order['rname'], 28)+"\n"

        # Type and Number
        order_str += order_type(order['cart'], order['_id'])+"\n"
        # print()

        # Dishes
        for item in order['cart']['dishes']:
            # amount = str('%.2f' % float(item['totalPrice']))
            item_data.append([max_len(item['name']), float(item['totalPrice'])])
            # Dish Customisation


        # Add Total
        item_data.append(["Total", float(order['cart']['totalCost'])])

        order_str += "\n"+tabulate(item_data, headers=['Item',  "  "+order['cart']['currency']], floatfmt=".2f")

        # user name
        order_str += "\n\n"+textwrap.fill(order['user']['fname']+" "+order['user']['lname'],28)

        # Payment and Order ID
        order_str += '\nPID-'+order['paymentInfo'][18:].upper()+ " "*12 + "OID-" +order['_id'][18:].upper()

        # main text
        print_text += order_str + "\n"




    printer.write(str(print_text) + "\n\n")
    # print(print_text)
    # data = [['Liquid', 220.00],['Liquid', 220.00], ['-Liquid', ""], ['Liquid', 220.00]]
    # x = tabulate(data, headers=["Item", "EUR"])
    # printer.write(x + "\n\n")

    # for article in response.json()['articles'][:headlines]:
    #     news = str(article['title'])
    #     news = textwrap.fill(news,20)
    #     printer.write(str(news) + "\n\n")
    printer.close()

    os.system('paps --left-margin=0 --font=\"Courier, Monospace Bold Italic 9\" print.txt | lp')



if __name__ == '__main__':
    # while True:
    check_orders()

    # check_orders()
        # time.sleep(10)