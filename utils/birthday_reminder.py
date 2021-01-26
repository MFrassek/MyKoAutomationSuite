from person import Volunteer
from datetime import datetime


def print_coming_birthdays():
    today = datetime.now()\
        .replace(hour=0, minute=0, second=0, microsecond=0)
    for volunteer in Volunteer.create_all():
        birthday = datetime.strptime(volunteer.birth_date, "%Y-%m-%d")\
            .replace(year=today.year)
        days_until_birthday = (birthday - today).days
        if 0 <= days_until_birthday <= 21:
            print(f"{volunteer.name}'s birthday is in {days_until_birthday} days")


if __name__ == "__main__":
    print_coming_birthdays()
