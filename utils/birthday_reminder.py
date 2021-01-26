from person import Volunteer
from datetime import datetime


def print_coming_birthdays():
    today = get_today_at_midnight()
    for volunteer in Volunteer.create_all():
        birthday_this_year = get_birthday_this_year(volunteer, today)
        days_until_birthday = get_days_until_birthday(birthday_this_year, today)
        if volunteer.is_active() and 0 <= days_until_birthday <= 21:
            print(f"{volunteer.name}'s birthday is in {days_until_birthday} days")


def get_today_at_midnight():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def get_birthday_this_year(volunteer, today):
    return datetime.strptime(volunteer.birth_date, "%Y-%m-%d")\
            .replace(year=today.year)


def get_days_until_birthday(birthday_this_year, today):
    return (birthday_this_year - today).days


if __name__ == "__main__":
    print_coming_birthdays()
