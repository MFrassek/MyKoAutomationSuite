from cairosvg import svg2png


def generate_mysec_map():
    with open("LocSecRegions.svg", "r") as template_svg:
        svg_code = "".join(template_svg.readlines())
        print(svg_code)
        svg2png(bytestring=svg_code, write_to='MYSec_map.png', dpi=300)


generate_mysec_map()
