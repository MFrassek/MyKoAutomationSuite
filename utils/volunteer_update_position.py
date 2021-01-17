from userInteraction import UserInteraction
from position import Position


def update_position():
    position = UserInteraction.select_from_options(
        Position.create_all_held_positions(
            UserInteraction.get_volunteer_name()))
    UserInteraction.post_about_update_start()
    position.end_date = UserInteraction.get_end_date()
    position.update_in_db()


if __name__ == '__main__':
    update_position()
