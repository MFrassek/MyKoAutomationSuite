import re


class UserInteraction():
    @staticmethod
    def get_volunteer_name():
        while True:
            volunteer_name = input("Name [a-üA-Ü ,-]:\n")
            if string_follows_input_pattern(volunteer_name, "name"):
                return volunteer_name

    @staticmethod
    def get_gender():
        while True:
            gender = input("Gender [f, m, d, u]:\n")
            if string_follows_input_pattern(gender, "gender"):
                return gender

    @staticmethod
    def get_birth_date():
        while True:
            birth_date = input("Birthdate [YYYY-MM-DD]:\n")
            if string_follows_input_pattern(birth_date, "date"):
                return birth_date

    @staticmethod
    def get_position_names():
        return [position.strip() for position in
                input("Comma separated positions [MYSec, MY-VeranstalterIn]:\n")
                .split(",")]

    @staticmethod
    def get_region_name():
        while True:
            region_name = input("Region name:\n")
            if string_follows_input_pattern(region_name, "name"):
                return region_name

    @staticmethod
    def get_start_date():
        while True:
            start_date = input("Start date [YYYY-MM-DD]:\n")
            if string_follows_input_pattern(start_date, "date"):
                return start_date

    @staticmethod
    def get_end_date():
        while True:
            end_date = input("End date [YYYY-MM-DD]:\n")
            if string_follows_input_pattern(end_date, "date"):
                return end_date

    @staticmethod
    def get_position_id():
        while True:
            position_id = input("Position id:\n")
            if string_follows_input_pattern(position_id, "id"):
                return position_id

    @staticmethod
    def specify_command():
        return [input(
            "Specify 'keyword name' 'comparator' 'argument'\n").split(" ")]

    @staticmethod
    def select_from_options(options: super(list)):
        if len(options) == 1:
            return options[0]
        elif len(options) == 0:
            raise LookupError("Found no options to select from")
        else:
            for i, option in enumerate(options):
                print(str(i) + ": " + str(option))
            selected_index = int(input("Select number:\n"))
        return options[selected_index]

    @staticmethod
    def inform_about_update_start():
        print("\nPrompting for new values of all mutable attributes:")


def string_follows_input_pattern(string, data_type):
    data_type_patterns = {
        "name": r"^[a-üA-Ü, -]+$",
        "date": r"^\d\d\d\d-\d\d-\d\d$",
        "gender": r"^[mfdu]$",
        "id": r"\d+"}
    return string == "" or re.match(data_type_patterns[data_type], string)
