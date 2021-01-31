import json
import requests
from bs4 import BeautifulSoup
from regionFinder import RegionFinder
from person import Volunteer


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

    person_table = soup("table")[15]("tr")[1:-1]
    for row in person_table:
        row_details = row("td")[3:]
        if row_details and row_details_are_valid(row_details):
            last_name = row_details[0].text.strip()
            first_name = row_details[1].text.strip()
            zip_code = int(row_details[3].text.strip() or -1)
            region = RegionFinder.find_region_belonging_to_zip_code(zip_code)
            name = first_name + " " + last_name
            vol = Volunteer.create_by_name(name)
            if vol and vol.is_active() and vol.home_region != region:
                print(name + " " + region)


def row_details_are_valid(row_details: str):
    if row_details[0].text \
            and not row_details[0].text.strip().startswith("Vertreter"):
        return True
    return False


if __name__ == "__main__":
    update_volunteer_home_regions()
