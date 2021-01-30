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
    def get_former_mysec_name():
        while True:
            mysec_name = input("Name of former MYSec [a-üA-Ü ,-]:\n")
            if string_follows_input_pattern(mysec_name, "name"):
                return mysec_name

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
    def post_about_update_start():
        print("\nPrompting for new values of all mutable attributes:")

    @staticmethod
    def post_volunteer_details(volunteer):
        print(f"Name: {volunteer.name}")
        print(f"Gender: {volunteer.gender}")
        print(f"Birth date: {volunteer.birth_date}")
        print("Positions:")
        for position in volunteer.positions:
            if position:
                print(f"\t{position}")

    @staticmethod
    def post_position_details(position):
        print(f"Title: {position.title}")
        print(f"Held by: {position.held_by}")
        print(f"Region: {position.region}")
        print(f"Start date: {position.start_date}")
        print(f"End date: {position.end_date}")

    @staticmethod
    def post_region_details(region):
        print(f"Id: {region.id}")
        print(f"Region name: {region.name}")
        print(f"Mail name: {region.mail_name}")
        print(f"Magazine name: {region.magazine_name}")
        print(f"M Count: {region.m_count}")
        print(f"MY Count: {region.my_count}")
        print(f"Non-M Count: {region.non_m_count}")
        print(f"Looking state: {region.looking_state}")


def string_follows_input_pattern(string, data_type):
    data_type_patterns = {
        "name": r"^[a-üA-Ü, -]+$",
        "date": r"^\d\d\d\d-\d\d-\d\d$",
        "gender": r"^[mfdu]$",
        "id": r"\d+"}
    return string == "" or re.match(data_type_patterns[data_type], string)
