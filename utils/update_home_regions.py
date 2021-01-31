import json
import requests
from bs4 import BeautifulSoup


def update_volunteer_home_regions():
    url = "https://db.mensa.de/psuche?mpn=MemberSeek&vs=049/"
    with open("./config_db_mensa.json", 'r') as config_file:
        params = json.load(config_file)
    data = {
        "mpn": "MemberSeek",
        "vs": "049?spgrp1=1",
        "suchstr1": "Funktion",
        "operator1": "6",
        "text1": "MY",
        "choice8": "Suchen",
        "lastchoice": "8"}
    req = requests.get(url, params=params, data=data)
    soup = BeautifulSoup(req.text, "html5lib")


if __name__ == "__main__":
    update_volunteer_home_regions()
