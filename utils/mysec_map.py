from cairosvg import svg2png
from bs4 import BeautifulSoup
import re
from helper import connect_to_db, get_relative_path_to_script
from region import Region


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
    print_current_looking_state_of_regions()
    toggle_looking_states_in_db(prompt_region_ids_for_looking_state_change())
    for _, regionName, _, lookingBool \
            in get_regionIds_regionNames_and_lookingBools(c):
        change_fill_color_of_path(
            soup, regionName, get_region_looking_color(lookingBool))
    conn.commit()


def print_current_looking_state_of_regions():
    for region in Region.create_all_regions():
        print(f"{region.id}\t{region.looking_state}\t{region.name}")


def toggle_looking_states_in_db(region_ids):
    for region_id in region_ids:
        toggle_looking_state_in_db(region_id)


def toggle_looking_state_in_db(region_id):
    region = Region.create_region_by_id(region_id)
    region.looking_state = int(not region.looking_state)
    region.update_in_db()


def prompt_region_ids_for_looking_state_change():
    region_ids = input("\nType comma separated identifiers of regions "
                       + "to change their looking state"
                       + "\nPress enter to proceed without changes\n")
    if region_ids:
        return list(map(int, region_ids.split(",")))
    else:
        return []


def get_regionIds_regionNames_and_lookingBools(c):
    c.execute("""SELECT * FROM regions""")
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


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    generate_mysec_map(data_path, "MYSec_map.png", "MY-Ko.db")
