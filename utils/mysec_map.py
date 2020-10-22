from cairosvg import svg2png
from bs4 import BeautifulSoup
import os
import re
import sqlite3


def generate_mysec_map(data_path, output_path, db_name):
    with open("{}/LocSecRegions.svg".format(data_path), "r") as template:
        raw_code = "".join(template.readlines())
    soup = BeautifulSoup(raw_code, 'xml')
    remove_malformed_attribute_from_soup(soup)
    conn, c = connect_to_db(db_name)
    c.execute("""SELECT regionName, looking FROM regions""")
    for regionName, lookingBool in c.fetchall():
        change_fill_color_of_path(soup, regionName)
    svg2png(bytestring=str(soup), write_to=output_path, dpi=300)


def remove_malformed_attribute_from_soup(soup):
    svg_tag = soup.svg
    del svg_tag["xmlns:"]


def change_fill_color_of_path(soup, id):
    region_path_tag = soup("path", {"id": id})[0]
    region_style_attribute = region_path_tag["style"]
    region_style_attribute = re.sub(
        "(?<=fill:#).{6}", "111111", region_style_attribute)
    region_path_tag["style"] = region_style_attribute


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    generate_mysec_map(data_path, "MYSec_map.png", "Weekend.db")
