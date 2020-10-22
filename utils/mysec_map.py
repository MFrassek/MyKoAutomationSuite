from cairosvg import svg2png
from bs4 import BeautifulSoup
import os


def generate_mysec_map(data_path, output_path):
    with open("{}/LocSecRegions.svg".format(data_path), "r") as template_svg:
        svg_code = "".join(template_svg.readlines())
    soup = BeautifulSoup(svg_code, 'xml')
    svg_tag = soup.svg
    del svg_tag["xmlns:"]
    svg2png(bytestring=str(soup), write_to=output_path, dpi=300)


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    generate_mysec_map(data_path, "MYSec_map.png")
