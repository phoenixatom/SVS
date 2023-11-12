import requests
from ping3 import ping


def get_game_pings():
    csgo_sgp = get_csgo_sgp()
    return {
        "csgo_sgp": csgo_sgp
    }


def get_csgo_sgp():
    req = requests.get("https://api.steampowered.com/ISteamApps/GetSDRConfig/v1/?appid=730").json()
    sgp_relays = req.get("pops").get("sgp").get("relays")
    first_relay_ipv4 = sgp_relays[0].get("ipv4")
    sgp_round_trip_time = ping_ipv4(first_relay_ipv4)
    return sgp_round_trip_time


def ping_ipv4(ipv4_address):
    response = ping(ipv4_address, unit='ms', timeout=1)
    return int(response)
