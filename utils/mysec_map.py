from cairosvg import svg2png
import os


def generate_mysec_map(data_path):
    with open("{}/LocSecRegions.svg".format(data_path), "r") as template_svg:
        svg_code = "".join(template_svg.readlines())
    svg2png(bytestring=svg_code, write_to='MYSec_map.png', dpi=300)


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    generate_mysec_map(data_path)
