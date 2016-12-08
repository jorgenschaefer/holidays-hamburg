#!/usr/bin/env python
# coding: utf-8

import sys
from datetime import date, timedelta

FREE_DAYS = [#0,  # Monday
             #4,  # Friday
             5,  # Saturday
             6,  # Sunday
             ]

VACATION_DAYS = 27


def main():
    if len(sys.argv) > 1:
        year = int(sys.argv[1])
    else:
        year = date.today().year
    cal = get_calendar(year)
    print "{} Arbeitstage in {}".format(
        sum(1 for day, free in cal if not free),
        year)
    print "{} Urlaubstage (ohne Übertrag)".format(VACATION_DAYS)
    print
    print "Brückentage:"
    for i in range(len(cal) - 1):
        if cal[i][1] and not cal[i + 1][1] and cal[i + 2][1]:
            print "- {}".format(cal[i + 1][0].strftime("%Y-%m-%d %a"))
    print
    print "Feiertage:"
    free = {}
    free.update(holidays(year))
    free.update(other_free(year))
    for day, reason in sorted(free.items()):
        print "- {}: {}".format(day.strftime("%Y-%m-%d %a"),
                                reason)


def get_calendar(year):
    free = {}
    free.update(holidays(year))
    free.update(other_free(year))
    start = date(year, 1, 1)
    now = start
    days = []
    while now.year == year:
        if now in free:
            days.append((now, free[now]))
        elif now.weekday() in FREE_DAYS:
            days.append((now, "Freier Tag"))
        else:
            days.append((now, False))
        now += timedelta(days=1)
    return days


def holidays(year):
    # FeiertG
    easter = easter_sunday(year)
    return {
        date(year, 1, 1): "Neujahrstag",
        easter - timedelta(days=2): "Karfreitag",
        easter + timedelta(days=1): "Ostermontag",
        date(year, 5, 1): "1. Mai",
        easter + timedelta(days=39): "Himmelfahrtstag",
        easter + timedelta(days=50): "Pfingstmontag",
        date(year, 10, 3): "Tag der Deutschen Einheit",
        date(year, 12, 25): "1. Weihnachtstag",
        date(year, 12, 26): "2. Weihnachtstag",
    }


def other_free(year):
    return {date(year, 12, 24): "Heiligabend (Halbtag)",
            date(year, 12, 31): "Neujahr (Halbtag)",
            }

# From Wikipedia
EASTER = {2000: (23, 4),
          2001: (15, 4),
          2002: (31, 3),
          2003: (20, 4),
          2004: (11, 4),
          2005: (27, 3),
          2006: (16, 4),
          2007: (8, 4),
          2008: (23, 3),
          2009: (12, 4),
          2010: (4, 4),
          2011: (24, 4),
          2012: (8, 4),
          2013: (31, 3),
          2014: (20, 4),
          2015: (5, 4),
          2016: (27, 3),
          2017: (16, 4),
          2018: (1, 4),
          2019: (21, 4),
          2020: (12, 4),
          2021: (4, 4),
          2022: (17, 4),
          2023: (9, 4),
          2024: (31, 3),
          2025: (20, 4),
          2026: (5, 4),
          2027: (28, 3),
          2028: (16, 4),
          2029: (1, 4),
          2030: (21, 4),
          }


def easter_sunday(year):
    day, month = EASTER[year]
    return date(year, month, day)

if __name__ == '__main__':
    main()
