from ping3 import ping

from utils.get_url import get_json_from_url


def get_game_pings():
    cs2 = get_cs2()
    valo = get_valorant()
    return {
        "cs2_sgp": cs2["sgp"],
        "cs2_bom": cs2["bom"],
        "valo_sea": valo["sea"]
    }


def get_cs2():
    req = get_json_from_url("https://api.steampowered.com/ISteamApps/GetSDRConfig/v1/?appid=730")
    sgp_relays = req.get("pops").get("sgp").get("relays")
    first_relay_ipv4 = sgp_relays[0].get("ipv4")
    sgp_round_trip_time = ping_ipv4(first_relay_ipv4)

    bom_relays = req.get("pops").get("bom2").get("relays")
    first_relay_ipv4 = bom_relays[0].get("ipv4")
    bom_round_trip_time = ping_ipv4(first_relay_ipv4)

    return {
        "sgp": sgp_round_trip_time,
        "bom": bom_round_trip_time
    }


def get_valorant():
    sea_valo = "dynamodb.ap-southeast-1.amazonaws.com"
    sea_round_trip_time = ping_ipv4(sea_valo)
    return {
        "sea": sea_round_trip_time
    }


def ping_ipv4(ipv4_address):
    response = ping(ipv4_address, unit='ms', timeout=1)
    return int(response)
