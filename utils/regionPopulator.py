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
                non_m_count=non_m_counter[region_name], looking_state=True
                ).add_to_db()

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
        for region_name, zip_ranges in region_to_zip_ranges.items():
            region_non_m_count = 0
            for zip_range in zip_ranges:
                zip_range = list(map(int, zip_range.split(",")))
                for zip_, inhabitants in zip_to_inhabitants.items():
                    if zip_range[0] <= zip_ <= zip_range[-1]:
                        region_non_m_count += inhabitants
            region_to_inhabitants[region_name] = region_non_m_count
        return region_to_inhabitants
