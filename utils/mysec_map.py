from cairosvg import svg2png
from bs4 import BeautifulSoup
import os
import re
import sqlite3


def generate_mysec_map(data_path, output_path, db_name):
    soup = read_soup_from_svg_file(data_path)
    remove_malformed_attribute_from_soup(soup)
    conn, c = connect_to_db(db_name)
    for regionName, lookingBool in get_regionNames_and_lookingBools(c):
        change_fill_color_of_path(
            soup, regionName, get_region_looking_color(lookingBool))
    svg2png(bytestring=str(soup), write_to=output_path, dpi=300)


def read_soup_from_svg_file(data_path):
    with open("{}/LocSecRegions.svg".format(data_path), "r") as template:
        raw_code = "".join(template.readlines())
    return BeautifulSoup(raw_code, 'xml')


def remove_malformed_attribute_from_soup(soup):
    svg_tag = soup.svg
    del svg_tag["xmlns:"]


def get_regionNames_and_lookingBools(c):
    c.execute("""SELECT regionName, looking FROM regions""")
    return c.fetchall()


def change_fill_color_of_path(soup, id, fill_color):
    region_path_tag = soup("path", {"id": id})[0]
    region_style_attribute = region_path_tag["style"]
    region_style_attribute = re.sub(
        "(?<=fill:#).{6}", fill_color, region_style_attribute)
    region_path_tag["style"] = region_style_attribute


def get_region_looking_color(lookingBool):
    looking_colors = {0: "ff7d24", 1: "005497"}
    return looking_colors[lookingBool]


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    generate_mysec_map(data_path, "MYSec_map.png", "Weekend.db")
