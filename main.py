import json
import time
import logging
import random
from colorama import Fore, Style
from wombat_dungeon_api import WombatDungeonAPI

# Cargar configuraciones desde el archivo config.json
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Cargar cookies desde el archivo cookie.json
def load_cookies_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Configuración del logging
def setup_logging(config):
    logging.basicConfig(level=config['logging']['level'],
                        format=config['logging']['format'])

def log(message):
    logging.info(Fore.GREEN + message + Style.RESET_ALL)

def main():
    config = load_config("config.json")  # Cargar configuraciones
    cookies = load_cookies_from_file(config['cookie_file'])  # Cargar cookies

    # Configurar logging
    setup_logging(config)

    # Inicializar la API con las configuraciones cargadas
    api = WombatDungeonAPI(
        config['account_name'], 
        config['private_key'], 
        cookies, 
        config['api_base_url'], 
        config['wax_rpc_url']
    )

    while True:
        log("Starting a trip in the dungeons...")
        trip_response = api.trip(duration_minutes=config['trip_duration_minutes'])
        log(f"Trip response: {trip_response}")
        log("Waiting 5 and a half minutes before the next cycle...")
        time.sleep(random.randint(config['sleep_duration_min'], config['sleep_duration_max']))

        log("Claiming trip result...")
        claim_trip_response = api.claim_trip()
        log(f"Claim trip response: {claim_trip_response}")
        time.sleep(random.randint(2, 7))

        log("Getting trip slots...")
        slots_response = api.get_trip_slots()
        log(f"Available slots: {slots_response}")
        time.sleep(random.randint(2, 7))

        log("Getting contributions...")
        contribution_response = api.get_contribution()
        log(f"Contributions: {contribution_response}")
        time.sleep(random.randint(2, 7))

        log("Getting currency balance...")
        balance_response = api.get_currency_balance()
        log(f"WOMBAT balance: {balance_response}")
        time.sleep(random.randint(2, 7))

if __name__ == "__main__":
    main()
