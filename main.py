import json
import time
import requests
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from hashlib import sha256

def generate_signature(params, private_key_hex):
    sorted_params = sorted(params.items())
    signature_base_str = "&".join(f"{k}={v}" for k, v in sorted_params)
    hashed_message = sha256(signature_base_str.encode()).digest()
    private_key = ec.derive_private_key(
        int(private_key_hex, 16),
        ec.SECP256K1(),
        default_backend())
    signature = private_key.sign(hashed_message, ec.ECDSA(hashes.SHA256()))
    return signature.hex()

class ArbelosRFQApiClient:
    def __init__(self, public_key, private_key, base_url):
        self.public_key = public_key
        self.private_key = private_key
        self.base_url = base_url

    def _get_current_time_ms(self):
        return time.time_ns() // 1_000_000

    def _make_request(self, endpoint, params):
        headers = {
            "x-api-key": self.public_key,
            "x-signature": generate_signature(params, self.private_key),
        }
        try:
            response = requests.post(self.base_url + endpoint, json=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_status(self):
        params = {"time": self._get_current_time_ms()}
        return self._make_request("/status", params)

    def get_volumes(self):
        params = {"time": self._get_current_time_ms()}
        return self._make_request("/volumes", params)

    def get_instruments(self):
        params = {"time": self._get_current_time_ms()}
        return self._make_request("/instruments", params)

    def get_quotes(self, instruments):
        params = {"time": self._get_current_time_ms(), "instruments": instruments}
        return self._make_request("/quotes", params)

    def execute_trade(self, quote_id, quantity):
        params = {
            "time": self._get_current_time_ms(),
            "quote_id": quote_id,
            "quantity": quantity,
        }
        return self._make_request("/trade", params)

    def get_trades(self):
        params = {"time": self._get_current_time_ms()}
        return self._make_request("/trades", params)

    def get_balances(self):
        params = {"time": self._get_current_time_ms()}
        return self._make_request("/balances", params)

# Example usage:
public_key_hex = 'your_public_key'
private_key_hex = 'your_private_key'
base_url = "https://dev-api.arbeloslabs.xyz/rfq/v1"
client = ArbelosRFQApiClient(public_key_hex, private_key_hex, base_url)

# Demonstrating each api endpoint:
status = client.get_status()
print('STATUS:', json.dumps(status, indent=2))

instruments = client.get_instruments()
print('INSTRUMENTS:', json.dumps(instruments, indent=2))

quotes = client.get_quotes("s sol,s btc,s eth")
print('QUOTES:', json.dumps(quotes, indent=2))

# Execute a quote from the quotes response:
if quotes and 'quotes' in quotes:
    example_quote = quotes['quotes'][0]
    quote_id = example_quote['quote_id_ask']
    quantity = example_quote['max_quantity_ask'] / 2
    trade = client.execute_trade(quote_id, quantity)
    print('TRADE:', json.dumps(trade, indent=2))

trades = client.get_trades()
print('TRADES:', json.dumps(trades, indent=2))

balances = client.get_balances()
print('BALANCES:', json.dumps(balances, indent=2))

volumes = client.get_volumes()
print('VOLUMES:', json.dumps(volumes, indent=2))
