import requests
from requests.sessions import Session
from wombat_dungeon_auth import WombatDungeonAuth

class WombatDungeonAPI:
    def __init__(self, account_name, private_key, cookie, base_url, wax_rpc_url):
        self.auth = WombatDungeonAuth(account_name, private_key)
        self.base_url = base_url
        self.wax_rpc_url = wax_rpc_url
        self.session = self._setup_session(cookie)

    def _setup_session(self, cookie):
        session = Session()
        session.headers.update({
            "accept": "*/*",
            "accept-language": "es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-api-variant": "JVM",
            "x-sec-ua": "2:32f756f9981d90a60f8dce6510b4b5aa9fc48112e76309a92f7bed5131056bd9"
        })
        session.cookies.update(cookie)
        return session

    def _make_request(self, method, url, data=None):
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {e}")

    def trip(self, duration_minutes=5):
        url = f"{self.base_url}/user/dungeon/trip"
        data = {"durationMinutes": duration_minutes}
        return self._make_request("POST", url, data)

    def claim_trip(self):
        url = f"{self.base_url}/user/dungeon/trip/claim"
        return self._make_request("POST", url)

    def get_trip_slots(self):
        url = f"{self.base_url}/user/dungeon/trip/slots"
        return self._make_request("GET", url)

    def get_contribution(self):
        url = f"{self.base_url}/user/contribution"
        return self._make_request("GET", url)

    def get_currency_balance(self, code="wombattokens", symbol="WOMBAT"):
        url = f"{self.wax_rpc_url}/get_currency_balance"
        data = {
            "code": code,
            "account": self.auth.account_name,
            "symbol": symbol
        }
        return self._make_request("POST", url, data)
