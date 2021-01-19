from helper import get_relative_path_to_script
from region import Region


class RegionPopulator():
    def __init__(self):
        self._data_path = get_relative_path_to_script() + "/data"
        self._region_data = self.get_region_data_from_file()

    def get_region_data_from_file(self):
        with open(f"{self._data_path}/LocSecRegions.txt", "r") \
                as all_region_file:
            result = [line[:-1].split("\t") for line
                      in all_region_file.readlines()]
        return result

    def populate_table(self):
        for region in self._region_data:
            reg = Region(*region, True)
            reg.add_to_db()
