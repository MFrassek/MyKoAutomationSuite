import os
import subprocess
import re
from helper import get_relative_path_to_script, connect_to_db,\
    get_general_volunteer_details, get_position_details


def make_mysec_intro(db_name):
    data_path = "{}/data".format(get_relative_path_to_script())
    with open(f"{data_path}/IntroTemplate.txt", "r") as template:
        raw_content = "".join(template.readlines())

    volunteerName = input("MYSec name: ")
    firstName = volunteerName.split(" ")[0]
    lastName = volunteerName.split(" ")[-1]
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
    underscored_volunteerName = volunteerName.replace(" ", "_")
    with open(f"{data_path}/intros/texts/{underscored_volunteerName}.txt", "r")\
            as intro_text:
        intro_first_line = intro_text.readline()
        intro_remaining_text = re.sub(
            r"(?<!\n)\n", r"\\\\\n", "".join(intro_text.readlines()[1:]))
    picture_path = f"""{data_path}/intros/pictures/{list(filter(
        lambda x: x.startswith(underscored_volunteerName),
        (os.listdir(f'{data_path}/intros/pictures'))))[0]}"""
    formatting_vars = {
        "Geschlecht": gender,
        "Gebiet": regionName,
        "Vorname": firstName,
        "Nachname": lastName,
        "Amtsantritt": startDate,
        "Mailadresse": mailAddress,
        "MYSecAbgelöst": formerMYSec,
        "AlleVeranstalter": allOrganizers,
        "VorstellungStart": intro_first_line,
        "VorstellungText": intro_remaining_text,
        "BildPfad": picture_path}

    with open(f"{underscored_volunteerName}.tex", "w") as tex_file:
        tex_file.write(raw_content % formatting_vars)

    for i in range(2):
        cmd = [
            "xelatex",
            "-interaction",
            "nonstopmode",
            f"{underscored_volunteerName}.tex"]
        proc = subprocess.Popen(cmd)
        proc.communicate()

        retcode = proc.returncode
        if not retcode == 0:
            os.unlink(f"{underscored_volunteerName}.pdf")
            raise ValueError(
                "Error {} executing command: {}".format(retcode, " ".join(cmd)))

    os.unlink(f"{underscored_volunteerName}.tex")
    os.unlink(f"{underscored_volunteerName}.log")
    os.unlink(f"{underscored_volunteerName}.aux")

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
        "Vorname": firstName,
        "Nachname": lastName,
        "Pronomen": pronouns[gender],
        "Mailadresse": mailAddress
        }

    print(raw_mail % mail_vars)


def convert_YYYYMMDD_to_DDMMYYYY_date(date):
    return ".".join(date.split("-")[::-1])


if __name__ == "__main__":
    make_mysec_intro("MY-Ko.db")
