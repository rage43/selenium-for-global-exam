
from selenium import webdriver
from browsermobproxy import Server
import colorama
from termcolor import colored
import json
from browsermobproxy.server import Client

def quit(server:Server,driver:webdriver):
    driver.quit()
    server.stop()
    exit(1)


def get_page_data(page_name:str,proxy:Client):
    entries = proxy.har['log']["entries"]

    for entry in entries:
        url:str = str(entry['request']['url'])
        if url.endswith(page_name) :
            response_content = entry['response']['content'].get('text', None)
            if response_content:
                return response_content
            else:
                return None
                
 


def msg_green(msg:str):
    print(colored(msg,'green'))

def msg_red(msg:str):
    print(colored(msg,'red'))




if __name__=='__main__':
    a={'n':1}
    print(type(a))
    exit(1)
