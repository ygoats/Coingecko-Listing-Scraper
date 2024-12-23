#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 19:29:56 2021

@ygoats
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import telegram_send
from time import sleep
from datetime import datetime

ticker_list = []
contract_list = []

googleList = []

def Main():
    try:
        googleList = []

        now = datetime.now()
        t = now.strftime("%m/%d/%Y, %H:%M:%S")

        url = 'https://www.coingecko.com/en/coins/recently_added'

        #print(url)

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        page_soup = soup(webpage, "html.parser")

        containers = page_soup.findAll("a", "d-lg-none font-bold")
        #print(containers)
        ticker = str(containers[0])

        tickerD = ticker.replace("""<a class="d-lg-none font-bold" href="/en/coins/""", "")
        tickerDD = tickerD.replace('"', '')
        tickerDDD = tickerDD.replace('>', '')
        tickerDDDD = tickerDDD.replace('</a', '')

        tickerR = tickerDDDD.partition('\n')[0]

        ticker_list.append(tickerR)

        #print(tickerR)

        url = str("https://www.coingecko.com/en/coins/"+str(ticker_list[0]))

        #print(url)

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        webpage = urlopen(req).read()

        page_soup = soup(webpage, "html.parser")

        containers1 = page_soup.findAll("i", "far tw-text-sm tw-ml-2 align-middle hover:tw-bg-gray-200 dark:hover:tw-bg-gray-500 fa-far fa-clone")
        #containers2 = page_soup.findAll("span", "text-muted mr-2")
        #print(containers2)
        contract = str(containers1[0]["data-address"])

        contract_list.append(contract)

        startProcess = True

    except Exception as e:
        print(e)
        startProcess = True

    while startProcess == True:
        sleep(3)
        try:
            url = 'https://www.coingecko.com/en/coins/recently_added'

            #print(url)

            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()

            page_soup = soup(webpage, "html.parser")

            containers = page_soup.findAll("a", "d-lg-none font-bold")

            ticker = str(containers[0])

            tickerD = ticker.replace("""<a class="d-lg-none font-bold" href="/en/coins/""", "")
            tickerDD = tickerD.replace('"', '')
            tickerDDD = tickerDD.replace('>', '')
            tickerDDDD = tickerDDD.replace('</a', '')

            tickerR = tickerDDDD.partition('\n')[0]
            #print(tickerR)

            sleep(3)

            url = str("https://www.coingecko.com/en/coins/"+str(tickerR))

            #print(url)

            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()

            page_soup = soup(webpage, "html.parser")

            containers1 = page_soup.findAll("i", "far tw-text-sm tw-ml-2 align-middle hover:tw-bg-gray-200 dark:hover:tw-bg-gray-500 fa-far fa-clone")
            containers2 = page_soup.findAll("span", "text-muted mr-2")

            contract = str(containers1[0]["data-address"])


            if tickerR not in ticker_list:
                ticker_list.append(tickerR)
                try:
                    contract_list.append(contract)
                except IndexError as e:
                    print(e)
                    contract_list.append('NULL')

                print('ticker ' + str(tickerR))
                print('contract ' + str(contract))
                print('containers2 ' + str(containers2))

                if "BSC" in str(containers2) or "binance" in str(containers2):
                    telegram_send.send(conf='channel3.conf',messages=["CoinGecko Listing Added" + "\n" + "\n" + \
                                                           str(tickerR) + "\n" + "\n" + \
                                                           "Contract Number" + "\n" + \
                                                           str(contract) + "\n" + "\n" + \
                                                           "https://www.dextools.io/app/pancakeswap/pair-explorer/" + str(contract)])

                elif "ETH" in str(containers2) or "ethereum" in str(containers2):
                    telegram_send.send(conf='channel3.conf',messages=["CoinGecko Listing Added" + "\n" + "\n" + \
                                                           str(tickerR) + "\n" + "\n" + \
                                                           "Contract Number" + "\n" + \
                                                           str(contract) + "\n" + "\n" + \
                                                           "https://www.dextools.io/app/uniswap/pair-explorer/" + str(contract)])

                elif "MATIC" in str(containers2) or "polygon" in str(containers2):
                    telegram_send.send(conf='channel3.conf',messages=["CoinGecko Listing Added" + "\n" + "\n" + \
                                                           str(tickerR) + "\n" + "\n" + \
                                                           "Contract Number" + "\n" + \
                                                           str(contract) + "\n" + "\n" + \
                                                           "https://www.dextools.io/app/quickswap/pair-explorer/" + str(contract)])

                elif "SOL" in str(containers2) or "solana" in str(containers2):
                    telegram_send.send(conf='channel3.conf',messages=["CoinGecko Listing Added" + "\n" + "\n" + \
                                                           str(tickerR) + "\n" + "\n" + \
                                                           "Contract Number" + "\n" + \
                                                           str(contract)])

                googleList.append(tickerR)

            lengthGoogle = len(googleList)
            if lengthGoogle > 0:
                f = open('geckoCoins.txt', 'a')
                f.write(str(tickerR) + ", ")
                f.close()
                googleList = []
        except Exception as e:
            print(e)
            #print(contract_list)
            continue

if __name__ == '__main__':
    Main()
