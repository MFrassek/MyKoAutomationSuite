import os
import subprocess
import re
from helper import get_relative_path_to_script, connect_to_db,\
    get_general_volunteer_details, get_position_details


def make_mysec_intro(db_name):
    volunteerName = input("MYSec name: ")
    firstName = volunteerName.split(" ")[0]
    formerMYSec = input("Name of former MYSec: ")
    allOrganizers = input("All organizers: ")
    conn, c = connect_to_db(db_name)
    _, gender, _ = get_general_volunteer_details(c, volunteerName)
    _, regionName, startDate, _ =\
        get_position_details(c, volunteerName, "mysecs")
    startDate = convert_YYYYMMDD_to_DDMMYYYY_date(startDate)
    regionMailName = c.execute(
        f"""SELECT regionMailName FROM regions
            WHERE regionName = '{regionName}'""").fetchall()[0][0]
    mailAddress = f"mysec-{regionMailName}@mensa.de"
    basename = volunteerName.replace(" ", "_")
    data_path = f"{get_relative_path_to_script()}/data"
    with open(f"{data_path}/intros/texts/{basename}.txt", "r")\
            as intro_text:
        intro_first_line = intro_text.readline()
        intro_remaining_text = re.sub(
            r"(?<!\n)\n", r"\\\\\n", "".join(intro_text.readlines()[1:]))
    picture_path = f"""{data_path}/intros/pictures/{list(filter(
        lambda x: x.startswith(basename),
        (os.listdir(f'{data_path}/intros/pictures'))))[0]}"""
    intro_formatting_variables = {
        "Geschlecht": gender,
        "Gebiet": regionName,
        "Name": volunteerName,
        "Vorname": firstName,
        "Amtsantritt": startDate,
        "Mailadresse": mailAddress,
        "MYSecAbgelöst": formerMYSec,
        "AlleVeranstalter": allOrganizers,
        "VorstellungStart": intro_first_line,
        "VorstellungText": intro_remaining_text,
        "BildPfad": picture_path}

    generate_tex_file_from_template(basename, intro_formatting_variables)
    generate_pdf_from_tex_file(basename)
    generate_pdf_from_tex_file(basename)
    remove_byproduct_files(basename)

    with open(f"{data_path}/IntroMailTemplate.txt", "r") as template:
        raw_mail = "".join(template.readlines())
    pronouns = {
        "m": "er",
        "f": "sie",
        "d": "em",
        "n": "em"
    }
    mail_vars = {
        "Gebiet": regionName,
        "Name": volunteerName,
        "Vorname": firstName,
        "Pronomen": pronouns[gender],
        "Mailadresse": mailAddress
        }

    print(raw_mail % mail_vars)


def convert_YYYYMMDD_to_DDMMYYYY_date(date):
    return ".".join(date.split("-")[::-1])


def generate_tex_file_from_template(basename, intro_formatting_variables):
    data_path = f"{get_relative_path_to_script()}/data"
    with open(f"{data_path}/IntroTemplate.txt", "r") as template:
        raw_intro = "".join(template.readlines())
    with open(f"{basename}.tex", "w") as tex_file:
        tex_file.write(raw_intro % intro_formatting_variables)


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


if __name__ == "__main__":
    make_mysec_intro("MY-Ko.db")
