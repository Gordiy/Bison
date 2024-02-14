"""Services for balance app."""
import json

import requests
from bs4 import BeautifulSoup
from lxml import etree

from balance.constants import (MERCHANT_ACCOUNT, MERCHANT_SIGNATURE,
                               WAYFORPAY_BASE_URL)
from django.core.cache import cache


class WayForPayService:
    """Service to use WayForPay API."""
    balance_cache_key = 'balance'

    @property
    def balance(self):
        """
        Get the current balance from the cache, or fetch it from the API if not cached.

        :return: The current balance in UAH.
        """
        cached_balance = cache.get(self.balance_cache_key)

        if cached_balance is None:
            balance = self.get_balance_bs4()
            cache.set(self.balance_cache_key, balance)

            return balance

        return cached_balance
    
    def update_balance(self):
        """
        Update the cached balance by fetching the latest balance from the API.

        :return: The updated balance in UAH.
        """
        balance = self.get_balance_bs4()

        cache.set(self.balance_cache_key, balance)

        return balance

    def get_balance_api(self) -> int:
        """
        Get the current balance from the WayForPay API.

        :return: The current balance in UAH, or None if unable to fetch.
        """
        payload = json.dumps({
            "merchantAccount": MERCHANT_ACCOUNT,
            "merchantSignature": MERCHANT_SIGNATURE
        })

        url = f'{WAYFORPAY_BASE_URL}/mms/merchantBalance.php'

        response = requests.post(url, data=payload)

        if not response.status_code == 200:
            print(response.json())
            return None

        return response.json().get('balance_UAH')

    def get_balance_bs4(self) -> int:
        donate_page_url = 'https://secure.wayforpay.com/donate/db5c92813866e'
        HEADERS = ({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
            'Accept-Language': 'en-US, en;q=0.5'}) 

        response = requests.get(donate_page_url, headers=HEADERS)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")

            amount_xpath = '/html/body/div/div[1]/div[2]/div/div[1]/div[2]'

            tree = etree.HTML(str(soup))

            # Use XPath to get elements
            elements = tree.xpath(amount_xpath)
            for element in elements:
                return element.text
        else:
            print(f"Can't get balance value. Response: {response.status_code} -{response.json()}")
            return None
