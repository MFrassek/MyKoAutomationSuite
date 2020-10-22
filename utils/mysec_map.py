from cairosvg import svg2png
from bs4 import BeautifulSoup
import os
import re
import sqlite3


def generate_mysec_map(data_path, output_path, db_name):
    soup = get_wellformed_soup_from_svg_file(data_path)
    change_fill_color_of_all_regions_based_on_db(db_name, soup)
    make_png_from_soup(soup, output_path)


def get_wellformed_soup_from_svg_file(data_path):
    soup = read_soup_from_svg_file(data_path)
    remove_malformed_attribute_from_soup(soup)
    return soup


def read_soup_from_svg_file(data_path):
    with open("{}/LocSecRegions.svg".format(data_path), "r") as template:
        raw_code = "".join(template.readlines())
    return BeautifulSoup(raw_code, 'xml')


def remove_malformed_attribute_from_soup(soup):
    svg_tag = soup.svg
    del svg_tag["xmlns:"]


def change_fill_color_of_all_regions_based_on_db(db_name, soup):
    conn, c = connect_to_db(db_name)
    print_current_looking_state_of_regions(c)
    for regionName, lookingBool in get_regionNames_and_lookingBools(c):
        change_fill_color_of_path(
            soup, regionName, get_region_looking_color(lookingBool))


def print_current_looking_state_of_regions(c):
    for i, (regionName, lookingBool)\
            in enumerate(get_regionNames_and_lookingBools(c)):
        print("{}\t{}\t{}".format(i, lookingBool, regionName))


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


def make_png_from_soup(soup, output_path):
    svg2png(bytestring=str(soup), write_to=output_path, dpi=300)


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    generate_mysec_map(data_path, "MYSec_map.png", "Weekend.db")
