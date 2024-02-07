"""Services for balance app."""
import json

import requests

from balance.constants import (MERCHANT_ACCOUNT, MERCHANT_SIGNATURE,
                               WAYFORPAY_BASE_URL)


class WayForPayService:
    """Service to use WayForPay API."""
    def get_balace(self) -> int or None:
        payload = json.dumps({
            "merchantAccount": MERCHANT_ACCOUNT,
            "merchantSignature": MERCHANT_SIGNATURE
        })

        url = f'{WAYFORPAY_BASE_URL}/mms/merchantBalance.php'

        response = requests.post(url, data=payload)

        if not response.status_code == 200:
            return 

        return response.json().get('balance_UAH')

