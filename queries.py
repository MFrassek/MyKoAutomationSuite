import sqlite3


def make_query(query):
    conn = sqlite3.connect('Weekend.db')
    c = conn.cursor()
    c.execute(query)
    for entry in c.fetchall():
        print(entry)


def query_participants_sorted_by_attendance():
    make_query(
        """SELECT participantName, count(participantName) AS participationCount
            FROM weekend_participant
            GROUP BY participantName
            ORDER BY participationCount DESC""")


def total_length_of_all_weekends():
    make_query(
        """SELECT SUM(JulianDay(endDate) - JulianDay(startDate))
        FROM weekends""")


def get_average_age_at_event(weekendId):
    make_query(
        """SELECT AVG(
            strftime("%Y.%m%d", w.startDate)
            - strftime("%Y.%m%d", p.birthDate))
        FROM weekends w
        INNER JOIN weekend_participant wp
        ON (w.weekendId == wp.weekendId)
        INNER JOIN participants p
        ON (wp.participantName == p.participantName)
        WHERE w.weekendId = {}
        """.format(weekendId))


def get_average_participant_age_by_year_and_gender(year, gender):
    make_query(
        """SELECT AVG(
            strftime("%Y.%m%d", w.startDate)
            - strftime("%Y.%m%d", p.birthDate))
        FROM weekends w
        INNER JOIN weekend_participant wp
        ON (w.weekendId == wp.weekendId)
        INNER JOIN participants p
        ON (wp.participantName == p.participantName)
        WHERE strftime("%Y", w.startDate) = "{}"
        AND p.gender = "{}"
        """.format(year, gender))


def get_oldest_participant_per_year_per_gender(year, gender):
    make_query(
        """SELECT p.participantName, p.birthDate
        FROM weekends w
        INNER JOIN weekend_participant wp
        ON (w.weekendId == wp.weekendId)
        INNER JOIN participants p
        ON (wp.participantName == p.participantName)
        WHERE strftime("%Y", w.startDate) = "{}"
        AND gender = "{}"
        ORDER BY p.birthDate DESC
        LIMIT 1
        """.format(year, gender))


def get_participants_at_event_on_birthday():
    make_query(
        """SELECT p.participantName, w.name, w.startDate
        FROM weekends w
        INNER JOIN weekend_participant wp
        ON (w.weekendId == wp.weekendId)
        INNER JOIN participants p
        ON (wp.participantName == p.participantName)
        WHERE strftime("%m%d", p.birthDate)
        BETWEEN strftime("%m%d", w.startDate)
        AND strftime("%m%d", w.endDate)
        """)


def get_number_of_participant_days():
    make_query(
        """SELECT SUM(x.participantDay)
        FROM (
            SELECT (JulianDay(w.endDate) - JulianDay(w.startDate)) *  COUNT(*)
            AS participantDay
            FROM weekends w
            INNER JOIN weekend_participant wp
            ON (w.weekendId = wp.weekendId)
            GROUP BY w.weekendId) x
        """)


def get_average_age_now():
    make_query(
        """SELECT AVG(
            strftime("%Y.%m%d", datetime("now"))
            - strftime("%Y.%m%d", p.birthDate))
        FROM participants p
        """)


def get_fraction_of_gender_per_weekend(gender, weekendId):
    make_query(
        """SELECT SUM(case when p.gender = "{}" then 1.0 end) / SUM(1) * 100
        FROM participants p
        INNER JOIN weekend_participant wp
        ON (p.participantName = wp.participantName)
        WHERE wp.weekendId = {}
        """.format(gender, weekendId))


def get_weekend_with_highest_female_ratio():
    make_query(
        """SELECT SUM(case when p.gender = "f" then 1.0 end)
                / SUM(1) * 100 malePercentage, wp.weekendId, w.name
        FROM participants p
        INNER JOIN weekend_participant wp
        ON (p.participantName = wp.participantName)
        INNER JOIN weekends w
        ON (wp.weekendId = w.weekendId)
        GROUP BY wp.weekendId
        ORDER BY malePercentage DESC
        LIMIT 1
        """)


def get_average_age_multiple_cnt_by_gender(gender):
    make_query(
        """SELECT AVG(
            strftime("%Y.%m%d", DATETIME("now"))
            - strftime("%Y.%m%d", p.birthDate))
        FROM participants p
        INNER JOIN weekend_participant wp
        ON (p.participantName = wp.participantName)
        WHERE p.gender = "{}"
        """.format(gender))


def get_unique_participants_per_birthMonth():
    make_query(
        """SELECT count(*), STRFTIME("%m", birthDate) birthMonth
        FROM participants
        GROUP BY birthMonth
        """)


def get_average_age_at_weekends_over_time():
    make_query(
        """SELECT w.startDate || "_" || w.name, AVG(
            STRFTIME("%Y.%m%d", w.startDate)
            - STRFTIME("%Y.%m%d", p.birthDate))
        FROM weekends w
        INNER JOIN weekend_participant wp
        ON (w.weekendId = wp.weekendId)
        INNER JOIN participants p
        ON (wp.participantName = p.participantName)
        GROUP BY w.weekendId
        """)


def get_lowest_m_nr():
    make_query(
        """SELECT wp.weekendId, MIN(p.membershipNr), p.participantName
        FROM participants p
        INNER JOIN weekend_participant wp
        ON (p.participantName = wp.participantName)
        WHERE p.membershipNr <> ""
        GROUP BY wp.weekendId
        """)


def get_yearly_counts_of_non_members():
    make_query(
        """SELECT STRFTIME("%Y", w.startDate) year, COUNT(*)
        FROM participants p
        INNER JOIN weekend_participant wp
        ON (p.participantName = wp.participantName)
        INNER JOIN weekends w
        ON (wp.weekendId = w.weekendId)
        WHERE p.status = "Interessent"
        GROUP BY year
        """)

# query_participants_sorted_by_attendance()
# total_length_of_all_weekends()
# get_average_age_at_event(1)
# get_average_participant_age_by_year_and_gender(2019, "m")
# get_oldest_participant_per_year_per_gender(2019, "f")
# get_participants_at_event_on_birthday()
# get_number_of_participant_days()
# get_average_age_now()
# get_fraction_of_gender_per_weekend("f", 1)
# get_weekend_with_highest_female_ratio()
# get_average_age_multiple_cnt_by_gender("m")
# get_unique_participants_per_birthMonth()
# get_average_age_at_weekends_over_time()
# get_lowest_m_nr()
# get_yearly_counts_of_non_members()
