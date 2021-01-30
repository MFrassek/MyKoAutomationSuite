import csv
import collections
from tablePopulator import TablePopulator
from region import Region


class RegionPopulator(TablePopulator):
    @classmethod
    def populate_table(cls):
        region_data = cls.get_data_from_file()
        m_counter = cls.get_region_counter_from_file("Ms_in_regions.csv")
        my_counter = cls.get_region_counter_from_file("MYs_in_regions.csv")
        non_m_counter = cls.get_region_non_m_count()
        for region in region_data:
            region_name = region[1]
            Region(
                id_=region[0], name=region[1], mail_name=region[2],
                magazine_name=region[3], m_count=m_counter[region_name],
                my_count=my_counter[region_name],
                non_m_count=non_m_counter.get(region_name, 0),
                looking_state=True).add_to_db()

    @classmethod
    def get_data_from_file(cls):
        with open(f"{cls.data_path}/LocSecRegions.txt", "r") \
                as all_region_file:
            result = [line[:-1].split("\t") for line
                      in all_region_file.readlines()]
        return result

    @classmethod
    def get_region_counter_from_file(cls, file_name):
        with open(
                f"{cls.data_path}/{file_name}", "r",
                encoding='latin1', newline="") as M_region_file:
            home_regions = csv.reader(M_region_file)
            flattened_home_regions = [y for x in home_regions for y in x]
            patched_home_regions = \
                ["Ruhrgebiet" if x.startswith("Ruhrgebiet") else x
                 for x in flattened_home_regions]
        return collections.Counter(patched_home_regions)

    @classmethod
    def get_region_to_zip_ranges(cls):
        with open(
                f"{cls.data_path}/RegionZipCodes.txt", "r") \
                as region_zip_code_file:
            region_zip_specs = [line[:-1].split("\t") for line
                                in region_zip_code_file.readlines()]
            region_to_zip_ranges = {zip_spec[0]: zip_spec[1:]
                                    for zip_spec in region_zip_specs}
        return region_to_zip_ranges

    @classmethod
    def get_zip_to_non_m_inhabitants(cls):
        with open(
                f"{cls.data_path}/ZipToInhabitants.csv", "r",
                encoding='latin1', newline="") as inhabitants_region_file:
            zip_to_inhabitants = {
                int(zip_): int(inhabitants)
                for (zip_, inhabitants) in csv.reader(inhabitants_region_file)}
        return zip_to_inhabitants

    @classmethod
    def get_region_non_m_count(cls):
        region_to_zip_ranges = cls.get_region_to_zip_ranges()
        zip_to_inhabitants = cls.get_zip_to_non_m_inhabitants()
        region_to_inhabitants = {}
        for zip_code, inhabitants in zip_to_inhabitants.items():
            region_name = cls.find_region_belonging_to_zip_code(
                zip_code, region_to_zip_ranges)
            region_to_inhabitants[region_name] = \
                region_to_inhabitants.setdefault(region_name, 0) + inhabitants
        return region_to_inhabitants

    @classmethod
    def find_region_belonging_to_zip_code(cls, zip_code, region_to_zip_ranges):
        for region_name in region_to_zip_ranges.keys():
            if cls.zip_belongs_to_region(
                    zip_code, region_name, region_to_zip_ranges):
                return region_name
        return "None"

    @classmethod
    def zip_belongs_to_region(cls, zip_code, region_name, region_to_zip_ranges):
        for zip_range in region_to_zip_ranges[region_name]:
            zip_range = list(map(int, zip_range.split(",")))
            if zip_range[0] <= zip_code <= zip_range[-1]:
                return True
        return False
