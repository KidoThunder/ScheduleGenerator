"""schedule_distribution_calc is a calculator of schedule distribution, use the microsoft standard patten to
represent the params need to be calculated.

Calculate a series schedule distributions by daily::

    >>> from schedule_distribution_calc import calc_daily
    >>> print(calc_daily(
            range_start_date="2022-05-01",
            range_end_date="2022-05-31",
            daily_steps=9,
            timezone="Asia/Shanghai",
            schedule_start="08:30 PM",
            schedule_end="11:00 PM"
        ))
    [{'start_time': '2022-05-01 20:30', 'end_time': '2022-05-01 23:00'},
    {'start_time': '2022-05-10 20:30', 'end_time': '2022-05-10 23:00'},
    {'start_time': '2022-05-19 20:30', 'end_time': '2022-05-19 23:00'},
    {'start_time': '2022-05-28 20:30', 'end_time': '2022-05-28 23:00'}]


    >>> from schedule_distribution_calc import calc_weekly
    >>> print(calc_weekly(
             range_start_date="2022-05-01",
             range_end_date="2022-05-31",
             weekly_steps=2,
             weekdays=["Monday", "Saturday"],
             timezone="Asia/Shanghai",
             schedule_start="08:30 PM",
             schedule_end="11:00 PM"
        ))
     [{'start_time': '2022-05-09 20:30', 'end_time': '2022-05-09 23:00'},
     {'start_time': '2022-05-14 20:30', 'end_time': '2022-05-14 23:00'},
     {'start_time': '2022-05-23 20:30', 'end_time': '2022-05-23 23:00'}]


    >>> from schedule_distribution_calc import calc_monthly_by_days
    >>> print(calc_monthly_by_days(
            range_start_date="2022-05-01",
            range_end_date="2023-09-30",
            timezone="Asia/Shanghai",
            day_of_month=15,
            monthly_steps=2,
            schedule_start="08:30 PM"
        ))
    [{'start_time': '2022-05-15 20:30'}, {'start_time': '2022-07-15 20:30'},
    {'start_time': '2022-09-15 20:30'}, {'start_time': '2022-11-15 20:30'},
    {'start_time': '2023-01-15 20:30'}, {'start_time': '2023-03-15 20:30'},
    {'start_time': '2023-05-15 20:30'}, {'start_time': '2023-07-15 20:30'},
    {'start_time': '2023-09-15 20:30'}]


    >>> from schedule_distribution_calc import calc_monthly_by_weeks
    >>> print(calc_monthly_by_weeks(
            range_start_date="2022-05-01",
            range_end_date="2022-09-30",
            timezone="Asia/Shanghai",
            week_ordinal="Third",
            weekday="Monday",
            monthly_steps=2,
            schedule_start="08:30 PM",
            schedule_end="11:00 PM"
        ))
    [{'start_time': '2022-05-16 20:30', 'end_time': '2022-05-16 23:00'},
    {'start_time': '2022-07-18 20:30', 'end_time': '2022-07-18 23:00'},
    {'start_time': '2022-09-19 20:30', 'end_time': '2022-09-19 23:00'}]


    >>> from schedule_distribution_calc import calc_dist_by_pattern
    >>> print(calc_dist_by_pattern(
            {
                "Pattern": "Daily",
                "DailyOptions": {
                    "EveryDays": 1
                },
                "WeeklyOptions": {
                    "RecursiveEveryWeeks": 1,
                    "WeekDays": [
                        "Monday"
                    ]
                },
                "MonthlyOptions": {
                    "Type": "ByDays",
                    "ByDays": {
                        "Days": 7,
                        "EveryMonths": 1
                    },
                    "ByWeekDays": {
                        "Ordinal": "First",
                        "WeekDay": "Monday",
                        "EveryMonths": 1
                    }
                },
                "StartTime": "04:00 PM",
                "EndTime": "05:00 PM",
                "TimeZone": {
                    "Name": "Asia/Shanghai",
                },
                "Range": {
                    "StartDateAt": "2022-05-18",
                    "EndDateAt": "2022-05-21"
                }
            }
        ))
        [{'start_time': '2022-05-18 16:00', 'end_time': '2022-05-18 17:00'},
        {'start_time': '2022-05-19 16:00', 'end_time': '2022-05-19 17:00'},
        {'start_time': '2022-05-20 16:00', 'end_time': '2022-05-20 17:00'},
        {'start_time': '2022-05-21 16:00', 'end_time': '2022-05-21 17:00'}]

"""
from .calculator import (
    calc_distributions_by_pattern as calc_dist_by_pattern,
    calc_daily_distributions as calc_daily,
    calc_weekly_distributions as calc_weekly,
    calc_monthly_distributions_by_days as calc_monthly_by_days,
    calc_monthly_distributions_by_weeks as calc_monthly_by_weeks,
)

__all__ = [
    "calc_dist_by_pattern",
    "calc_daily",
    "calc_weekly",
    "calc_monthly_by_days",
    "calc_monthly_by_weeks"
]
__version__ = "0.1.4"
