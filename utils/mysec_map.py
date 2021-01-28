from cairosvg import svg2png
from bs4 import BeautifulSoup
import re
import functools
from helper import get_relative_path_to_script
from region import Region
from position import Position


def generate_looking_state_map(data_path, output_path):
    generate_map(
        data_path,
        change_fill_color_of_all_regions_based_on_looking_state,
        output_path)


def generate_mysec_presence_map(data_path, output_path):
    generate_map(
        data_path,
        change_fill_color_of_all_regions_based_on_presence_of_mysec,
        output_path)


def generate_m_count_map(data_path, output_path):
    generate_map(
        data_path,
        change_fill_color_all_regions_based_on_m_count,
        output_path)


def generate_my_count_map(data_path, output_path):
    generate_map(
        data_path,
        change_fill_color_all_regions_based_on_my_count,
        output_path)


def generate_m_frequency_map(data_path, output_path):
    generate_map(
        data_path,
        change_fill_color_all_regions_based_on_m_frequency,
        output_path)


def generate_map(data_path, coloring_function, output_path):
    soup = get_wellformed_soup_from_svg_file(data_path)
    coloring_function(soup)
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


def change_fill_color_of_all_regions_based_on_looking_state(soup):
    print_current_looking_state_of_regions()
    toggle_looking_states_in_db(prompt_region_ids_for_looking_state_change())
    for region in Region.create_all():
        change_fill_color_of_path(
            soup, region.name, get_region_looking_color(region.looking_state))


def change_fill_color_of_all_regions_based_on_presence_of_mysec(soup):
    all_regions_with_active_mysec = get_all_regions_with_active_mysec()
    for region in Region.create_all():
        change_fill_color_of_path(
            soup, region.name, get_region_mysec_presence_color(
                region in all_regions_with_active_mysec))


def change_fill_color_all_regions_based_on_m_count(soup):
    max_m_count = get_max_m_count_for_all_regions()
    for region in Region.create_all():
        change_fill_color_of_path(
            soup, region.name, get_region_count_fraction_color(
                region.m_count / max_m_count))


def change_fill_color_all_regions_based_on_my_count(soup):
    max_my_count = get_max_my_count_for_all_regions()
    for region in Region.create_all():
        change_fill_color_of_path(
            soup, region.name, get_region_count_fraction_color(
                region.my_count / max_my_count))


def change_fill_color_all_regions_based_on_m_frequency(soup):
    max_m_frequency = get_max_m_frequency_for_all_regions()
    for region in Region.create_all():
        change_fill_color_of_path(
            soup, region.name, get_region_count_fraction_color(
                region.m_frequency / max_m_frequency))


def print_current_looking_state_of_regions():
    for region in Region.create_all():
        print(f"{region.id}\t{region.looking_state}\t{region.name}")


def toggle_looking_states_in_db(region_ids):
    for region_id in region_ids:
        toggle_looking_state_in_db(region_id)


def toggle_looking_state_in_db(region_id):
    region = Region.create_by_id(region_id)
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


def get_all_regions_with_active_mysec():
    all_active_mysec_positions = Position.create_all_fitting_data(
        [["end_date", "=", ""]], title="MYSec")
    all_regions_with_active_mysec = set()
    for mysec in all_active_mysec_positions:
        all_regions_with_active_mysec.add(
            Region.create_by_name(mysec.region))
    return all_regions_with_active_mysec


def get_max_m_count_for_all_regions():
    all_regions = Region.create_all()
    region_with_max_m_count = functools.reduce(
        lambda a, b: a if a.m_count > b.m_count else b, all_regions)
    return region_with_max_m_count.m_count


def get_max_my_count_for_all_regions():
    all_regions = Region.create_all()
    region_with_max_my_count = functools.reduce(
        lambda a, b: a if a.my_count > b.my_count else b, all_regions)
    return region_with_max_my_count.my_count


def get_max_m_frequency_for_all_regions():
    all_regions = Region.create_all()
    region_with_max_m_frequency = functools.reduce(
        lambda a, b: a if a.m_frequency > b.m_frequency else b, all_regions)
    return region_with_max_m_frequency.m_frequency


def change_fill_color_of_path(soup, id, fill_color):
    region_path_tag = soup("path", {"id": id})[0]
    region_style_attribute = region_path_tag["style"]
    region_style_attribute = re.sub(
        "(?<=fill:#).{6}", fill_color, region_style_attribute)
    region_path_tag["style"] = region_style_attribute


def get_region_looking_color(lookingBool):
    looking_colors = {0: "ff7d24", 1: "005497"}
    return looking_colors[lookingBool]


def get_region_mysec_presence_color(presenceBool):
    presence_colors = {True: "ffaa11", False: "00bbbb"}
    return presence_colors[presenceBool]


def get_region_count_fraction_color(fraction: float):
    r = "26"
    g = f"{int((0.1 + 0.4 * (fraction)) * 255):02x}"
    b = f"{int((fraction) * 255):02x}"
    return r + g + b


def make_png_from_soup(soup, output_path):
    svg2png(bytestring=str(soup), write_to=output_path, dpi=300)


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    generate_mysec_presence_map(data_path, "MYSec_presence_map.png")
    generate_looking_state_map(data_path, "MYSec_map.png")
    generate_m_count_map(data_path, "M_density_map.png")
    generate_my_count_map(data_path, "MY_density_map.png")
    generate_m_frequency_map(data_path, "M_frequency_map.png")