import requests  
from botHandler import BotHandler 
from blinkTradeApi import BlinkTradeApi
from boto.s3.connection import S3Connection
import os

token = os.environ.get('token', None)

bot = BotHandler(token)  
api = BlinkTradeApi("BRL", "BTC")

def format_status(status):
    high = 'R${:,.2f}'.format(float(status["high"]))
    low = 'R${:,.2f}'.format(float(status["low"]))
    buy = 'R${:,.2f}'.format(float(status["buy"]))
    sell = 'R${:,.2f}'.format(float(status["sell"]))
    message = "Fox bit status:\nHigh: %s\nLow: %s\nBuy: %s\nSell: %s\n" % (high, low, buy, sell)
    return message

def get_ids():
    file = open("ids.txt","r")
    ids = []
    for line in file.readlines():
        ids.append(int(line.strip()))
    file.close()
    return ids

def save_id(id):
    file = open("ids.txt","w+") 
    if str(id) not in get_ids():
        file.write(str(id))
        file.close()
        return "Subscribed successfully!"
    else:
        file.close()
        return "User is already subscribed"

def remove_id(id):
    file = open("ids.txt","r") 
    ids = file.readlines()
    file.close()
    if str(id) not in ids:
        return "You were never subscribed to the alert channel! Type /subscribe to receive our alerts!"
    else:
        file = open("ids.txt", "w+")
        for line in ids:
            if line != str(id) + "\n":
                file.write(line)
        file.close()
        return "Unsubscription successfull!"
        

def main():  
    new_offset = None
    while True:
        bot.get_updates(new_offset)
        last_update = bot.get_last_update()
        if last_update != "":
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['from']['first_name']

            if last_chat_text.lower() == '/status':            
                bot.send_message(last_chat_id, format_status(api.get_last_status()))
            elif last_chat_text.lower() == '/variance':
                bot.send_message(last_chat_id, "Variance between Buy and Low is: " + str('{:,.2f}'.format(api.get_buylow_variance())))
            elif last_chat_text.lower() == '/subscribe':
                bot.send_message(last_chat_id, save_id(last_chat_id))
            elif last_chat_text.lower() == '/unsubscribe':
                bot.send_message(last_chat_id, remove_id(last_chat_id))
            
        variance = api.get_buylow_variance()
        spected_var = 10
        if variance < spected_var:
            variance_value = str('{:,.2f}'.format(api.get_buylow_variance()))
            message = "Variance is lower than %s (%s)!!!\n Type /status to see the values" % (spected_var, variance_value)
            bot.notify_all(get_ids(), message)

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()