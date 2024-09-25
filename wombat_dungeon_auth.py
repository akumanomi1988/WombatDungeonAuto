from eospy.cleos import Cleos
from eospy.keys import EOSKey

class WombatDungeonAuth:
    
    def __init__(self, account_name, private_key):
        """Initialize with account name and private key"""
        self.account_name = account_name
        self.private_key = EOSKey(private_key)
        self.cleos = Cleos(url='https://wax.greymass.com')

    def sign_transaction(self, transaction):
        """Sign the transaction using the private key"""
        try:
            signed_transaction = self.cleos.sign_transaction(transaction, self.private_key)
            return signed_transaction
        except Exception as e:
            print(f"Error signing transaction: {e}")
            return None

    def push_transaction(self, signed_transaction):
        """Send the signed transaction to the blockchain"""
        try:
            response = self.cleos.push_transaction(signed_transaction)
            return response
        except Exception as e:
            print(f"Error pushing transaction: {e}")
            return None

    def get_account_info(self):
        """Retrieve account information"""
        return self.cleos.get_account(self.account_name)

    def get_currency_balance(self, code="wombattokens", symbol="WOMBAT"):
        """Check the balance of a specific currency"""
        balance = self.cleos.get_currency_balance(code, self.account_name, symbol)
        return balance
