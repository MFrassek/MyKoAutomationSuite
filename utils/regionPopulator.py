from helper import get_relative_path_to_script
import csv
import collections
from region import Region


class RegionPopulator():
    def __init__(self):
        self._data_path = get_relative_path_to_script() + "/data"
        self._region_data = self.get_region_data_from_file()
        self._M_counter = self.get_region_counter_from_file("Ms_in_regions.csv")
        self._MY_counter = self.get_region_counter_from_file("MYs_in_regions.csv")

    def get_region_data_from_file(self):
        with open(f"{self._data_path}/LocSecRegions.txt", "r") \
                as all_region_file:
            result = [line[:-1].split("\t") for line
                      in all_region_file.readlines()]
        return result

    def get_region_counter_from_file(self, file_name):
        with open(
                f"{self._data_path}/{file_name}", "r",
                encoding='latin1', newline="") as M_region_file:
            home_regions = csv.reader(M_region_file)
            flattened_home_regions = [y for x in home_regions for y in x]
            patched_home_regions = \
                ["Ruhrgebiet" if x.startswith("Ruhrgebiet") else x
                 for x in flattened_home_regions]
        return collections.Counter(patched_home_regions)

    def populate_table(self):
        for region in self._region_data:
            region_name = region[1]
            reg = Region(
                *region, self._M_counter[region_name],
                self._MY_counter[region_name], True)
            reg.add_to_db()
