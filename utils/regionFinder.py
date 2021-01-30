from rawDataAccessMixin import RawDataAccessMixin


class RegionFinder(RawDataAccessMixin):
    _region_to_zip_ranges = None

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
    def find_region_belonging_to_zip_code(cls, zip_code):
        if not cls._region_to_zip_ranges:
            cls._region_to_zip_ranges = cls.get_region_to_zip_ranges()
        for region_name in cls._region_to_zip_ranges.keys():
            if cls.zip_belongs_to_region(zip_code, region_name):
                return region_name
        return "None"

    @classmethod
    def zip_belongs_to_region(cls, zip_code, region_name):
        if not cls._region_to_zip_ranges:
            cls._region_to_zip_ranges = cls.get_region_to_zip_ranges()
        for zip_range in cls._region_to_zip_ranges[region_name]:
            zip_range = list(map(int, zip_range.split(",")))
            if zip_range[0] <= zip_code <= zip_range[-1]:
                return True
        return False
