from cairosvg import svg2png
from bs4 import BeautifulSoup
import os
import re


def generate_mysec_map(data_path, output_path):
    with open("{}/LocSecRegions.svg".format(data_path), "r") as template:
        raw_code = "".join(template.readlines())
    soup = BeautifulSoup(raw_code, 'xml')
    remove_malformed_attribute_from_soup(soup)
    change_fill_color_of_path(soup, "Düsseldorf")
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


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    generate_mysec_map(data_path, "MYSec_map.png")
