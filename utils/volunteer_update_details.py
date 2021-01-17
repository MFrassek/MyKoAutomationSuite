from userPrompt import UserPrompt
from position import Position


def update_position():
    position = UserPrompt.select_from_options(
        Position.create_all_held_positions(UserPrompt.get_volunteer_name()))
    UserPrompt.inform_about_update_start()
    position.end_date = UserPrompt.get_end_date()
    position.update_in_db()


if __name__ == '__main__':
    update_position()
