"""Services for balance app."""
import json

import requests

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
            balance = self.get_balance()
            cache.set(self.balance_cache_key, balance)

            return balance

        return cached_balance
    
    def update_balance(self):
        """
        Update the cached balance by fetching the latest balance from the API.

        :return: The updated balance in UAH.
        """
        balance = self.get_balance()

        cache.set(self.balance_cache_key, balance)

        return balance

    def get_balance(self) -> int or None:
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
