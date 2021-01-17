import os
import subprocess
import re
from helper import get_relative_path_to_script
from person import Volunteer
from position import Position
from region import Region
from userInteraction import UserInteraction


def get_target_volunteer():
    volunteers = Volunteer.create_all_fitting_data(
        UserInteraction.specify_command())
    return UserInteraction.select_from_options(volunteers)


def get_target_region(position: Position):
    return Region.create_by_name(position.region)


def make_mysec_intro():
    volunteer = get_target_volunteer()
    position = UserInteraction.select_from_options(volunteer.positions)
    region = get_target_region(position)
    intro_format_variables, mail_format_variables = \
        make_format_variable_dicts(volunteer, position, region)
    basename = volunteer.name.replace(" ", "_")
    generate_tex_file_from_template(basename, intro_format_variables)
    generate_pdf_from_tex_file(basename)
    generate_pdf_from_tex_file(basename)
    remove_byproduct_files(basename)
    print(generate_mail_text_from_template(basename, mail_format_variables))


def make_format_variable_dicts(
        volunteer: Volunteer, position: Position, region: Region):
    firstName = volunteer.name.split(" ")[0]
    mysecAddress = f"mysec-{region.mail_name}@mensa.de"
    basename = volunteer.name.replace(" ", "_")
    intro_first_line, intro_remaining_text = \
        get_intro_first_line_and_remaining_text(basename)
    intro_format_variables = {
        "Geschlecht": volunteer.gender,
        "Gebiet": position.region,
        "Name": volunteer.name,
        "Vorname": firstName,
        "Amtsantritt": convert_YYYYMMDD_to_DDMMYYYY_date(position.start_date),
        "Mailadresse": mysecAddress,
        "MYSecAbgelöst": input("Name of former MYSec: "),
        "AlleVeranstalter": input("All organizers: "),
        "VorstellungStart": intro_first_line,
        "VorstellungText": intro_remaining_text,
        "BildPfad": get_path_to_picture(basename)}
    mail_format_variables = {
        "Gebiet": position.region,
        "Name": volunteer.name,
        "Vorname": firstName,
        "Pronomen": get_pronoun_from_gender(volunteer.gender),
        "Mailadresse": mysecAddress}
    return intro_format_variables, mail_format_variables


def convert_YYYYMMDD_to_DDMMYYYY_date(date):
    return ".".join(date.split("-")[::-1])


def get_intro_first_line_and_remaining_text(basename):
    data_path = f"{get_relative_path_to_script()}/data"
    with open(f"{data_path}/intros/texts/{basename}.txt", "r")\
            as intro_text:
        intro_first_line = intro_text.readline()
        intro_remaining_text = re.sub(
            r"(?<!\n)\n", r"\\\\\n", "".join(intro_text.readlines()[1:]))
    return intro_first_line, intro_remaining_text


def get_path_to_picture(basename):
    data_path = f"{get_relative_path_to_script()}/data"
    return f"""{data_path}/intros/pictures/{list(filter(
        lambda x: x.startswith(basename),
        (os.listdir(f'{data_path}/intros/pictures'))))[0]}"""


def generate_tex_file_from_template(basename, intro_format_variables):
    data_path = f"{get_relative_path_to_script()}/data"
    with open(f"{data_path}/IntroTemplate.txt", "r") as template:
        raw_intro = "".join(template.readlines())
    with open(f"{basename}.tex", "w") as tex_file:
        tex_file.write(raw_intro % intro_format_variables)


def generate_pdf_from_tex_file(basename):
    proc = subprocess.Popen(
        ["xelatex", "-interaction", "nonstopmode", f"{basename}.tex"])
    proc.communicate()
    raise_error_if_returncode_is_not_zero(proc, basename)


def raise_error_if_returncode_is_not_zero(proc, basename):
    if proc.returncode:
        os.unlink(f"{basename}.pdf")
        raise ValueError(f"Error {proc.returncode}")


def remove_byproduct_files(basename):
    os.unlink(f"{basename}.tex")
    os.unlink(f"{basename}.log")
    os.unlink(f"{basename}.aux")


def get_pronoun_from_gender(gender):
    pronouns = {"m": "er", "f": "sie", "d": "em", "n": "em"}
    return pronouns[gender]


def generate_mail_text_from_template(basename, mail_format_variables):
    data_path = f"{get_relative_path_to_script()}/data"
    with open(f"{data_path}/IntroMailTemplate.txt", "r") as template:
        raw_mail = "".join(template.readlines())
    return raw_mail % mail_format_variables


if __name__ == "__main__":
    make_mysec_intro()
