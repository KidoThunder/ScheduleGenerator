import calendar
from typing import Optional, List, Dict, Tuple

import arrow

calendar.setfirstweekday(calendar.SUNDAY)
AM = "AM"
PM = "PM"

HOUR = "hour"
MINUTE = "minute"

TIME_FORMAT_WITHOUT_SECOND = "YYYY-MM-DD HH:mm"

START_TIME = "start_time"
END_TIME = "end_time"

WEEKDAYS = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6
}

WEEK_DAYS_KEYWORDS = {
    "First": 0,
    "Second": 1,
    "Third": 2,
    "Fourth": 3,
    "Last": -1
}


def get_weekly_day_offset_from_first_day(weekdays: List[str], start_date: arrow.Arrow) -> tuple[List[int], int, int]:
    month_weeks = calendar.monthcalendar(start_date.year, start_date.month)
    cur_month_day = int(start_date.format("D"))  # current day of month
    cur_week = 0

    day_offset = []
    skip_days = 0
    for i, month_week in enumerate(month_weeks):
        if cur_month_day in month_week:
            day_index = month_week.index(cur_month_day)
            for weekday in weekdays:
                weekday_index = WEEKDAYS[weekday]
                day_offset.append(weekday_index - day_index)
            if not day_offset:
                skip_days = len([d for d in month_week if d == 0])
            cur_week = i
            break
    return day_offset, skip_days, cur_week


def get_schedule_ranges(start_time: str, end_time: Optional[str] = None) -> Tuple[Dict[str, int], Dict[str, int]]:
    def split_time(original_time) -> Tuple[int, int, str]:
        _time, _day_part = original_time.split(" ")
        _hour, _minutes = _time.split(":")
        return int(_hour), int(_minutes), _day_part

    def construct_time(original_time) -> Dict[str, int]:
        _hour, _minutes, _day_part = split_time(original_time)
        _result = {HOUR: _hour, MINUTE: _minutes}
        if _day_part == AM and _hour == 12:
            _result[HOUR] = 0
        if _day_part == PM and _hour != 12:
            _result[HOUR] += 12
        return _result

    _start = construct_time(start_time)
    _end = construct_time(end_time) if end_time is not None else {}
    return _start, _end


def get_arrow_time_from_string_with_timezone(
        date_string: str,
        timezone: str,
        date_format: Optional[str] = "YYYY-MM-DD"
) -> arrow.Arrow:
    return arrow.get(date_string, date_format, tzinfo=timezone)


def get_schedule_range_time(range_start: str, range_end: str, timezone: str) -> Tuple[arrow.Arrow, arrow.Arrow]:
    _start = get_arrow_time_from_string_with_timezone(range_start, timezone)
    _end = get_arrow_time_from_string_with_timezone(range_end, timezone)
    if _start > _end:
        raise ValueError("Range start date is bigger than range end date")
    return _start, _end


def calc_daily_distributions(
        range_start_date: str,
        range_end_date: str,
        daily_steps: int,
        timezone: str,
        schedule_start: str,
        schedule_end: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Calculate schedule distributions by daily pattern
    :param range_start_date:
        This distributions range start date. e.g. 2022-05-18
    :param range_end_date:
        This distributions range end date. e.g. 2022-06-18
    :param daily_steps:
        Daily schedule pattern. e.g. If daily steps is 3, which means there will have a schedule every 3 days
    :param timezone:
        Should calculate by which timezone. e.g. Asia/Shanghai
    :param schedule_start:
        Schedule start time. e.g. 08:30 PM
    :param schedule_end:
        Schedule end time, which is optional. e.g. 11:00 PM
    :return:
        A list with all schedule distribution start&end time string.
    :raise:
        ValueError
    """
    ranges: Tuple[arrow.Arrow, arrow.Arrow] = get_schedule_range_time(range_start_date, range_end_date, timezone)
    range_start, range_end = ranges
    range_distance = range_end - range_start
    schedule_ranges: Tuple[Dict[str, int], Dict[str, int]] = get_schedule_ranges(
        schedule_start, schedule_end
    )
    _schedule_start, _schedule_end = schedule_ranges

    instance_times = []
    for day in range(0, range_distance.days + 1, daily_steps):
        _start = range_start.shift(days=day, hours=_schedule_start[HOUR], minutes=_schedule_start[MINUTE])
        if _start > range_end.shift(days=1) or _start < range_start:
            continue

        _distribution = {START_TIME: _start.format(TIME_FORMAT_WITHOUT_SECOND)}
        if _schedule_end:
            _end = range_start.shift(days=day, hours=_schedule_end[HOUR], minutes=_schedule_end[MINUTE])
            if _schedule_end[HOUR] < _schedule_start[HOUR]:
                _end = _end.shift(days=1)
            _distribution[END_TIME] = _end.format(TIME_FORMAT_WITHOUT_SECOND)

        instance_times.append(_distribution)
    return instance_times


def calc_weekly_distributions(
        range_start_date: str,
        range_end_date: str,
        weekly_steps: int,
        weekdays: List[str],
        timezone: str,
        schedule_start: str,
        schedule_end: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Calculate schedule distributions by weekly pattern
    :param range_start_date:
        This distributions range start date. e.g. 2022-05-18
    :param range_end_date:
        This distributions range end date. e.g. 2022-06-18
    :param weekly_steps:
        Weekly schedule pattern. e.g. If weekly steps is 3, which means the schedules will repeat every 3 week
    :param weekdays:
        Weekly days list. e.g. ['Monday', 'Friday']
    :param timezone:
        Should calculate by which timezone. e.g. Asia/Shanghai
    :param schedule_start:
        Schedule start time. e.g. 08:30 PM
    :param schedule_end:
        Schedule end time, which is optional. e.g. 11:00 PM
    :return:
        A list with all schedule distribution start&end time string.
    :raise:
        ValueError
    """
    ranges: Tuple[arrow.Arrow, arrow.Arrow] = get_schedule_range_time(range_start_date, range_end_date, timezone)
    range_start, range_end = ranges
    range_distance = range_end - range_start
    schedule_ranges: Tuple[Dict[str, int], Dict[str, int]] = get_schedule_ranges(
        schedule_start, schedule_end
    )
    _schedule_start, _schedule_end = schedule_ranges

    instance_times = []
    start_day_offsets, start_range, _ = get_weekly_day_offset_from_first_day(weekdays, range_start)
    _range_start = start_range + 7 if not start_day_offsets else 0

    calculated_weeks = set()
    for day in range(_range_start, range_distance.days + 7, weekly_steps * 7):
        _each_start = range_start.shift(days=day)
        week_day_offsets, _, cur_week = get_weekly_day_offset_from_first_day(weekdays, _each_start)
        cur_month = int(_each_start.format("M"))  # current day month
        cur_year = int(_each_start.format("YYYY"))  # current day month
        _week_index = f"{cur_year}-{cur_month}-{cur_week}"
        if _week_index in calculated_weeks:  # already calculated
            continue
        calculated_weeks.add(_week_index)

        for week_day_offset in week_day_offsets:
            _start = range_start.shift(
                days=day + week_day_offset, hours=_schedule_start[HOUR], minutes=_schedule_start[MINUTE]
            )
            if _start > range_end.shift(days=1) or _start < range_start:
                continue

            _distribution = {START_TIME: _start.format(TIME_FORMAT_WITHOUT_SECOND)}
            if _schedule_end:
                _end = range_start.shift(
                    days=day + week_day_offset, hours=_schedule_end[HOUR], minutes=_schedule_end[MINUTE]
                )
                if _schedule_end[HOUR] < _schedule_start[HOUR]:
                    _end = _end.shift(days=1)
                _distribution[END_TIME] = _end.format(TIME_FORMAT_WITHOUT_SECOND)
            instance_times.append(_distribution)
    return instance_times


def get_monthly_day_offset_from_first_day_by_days(days: int, start: arrow.Arrow) -> int:
    # get the most days in a month according to the days in the month
    _, month_max_days = calendar.monthrange(start.year, start.month)  # get months' days in a year
    max_days = days if days < month_max_days else month_max_days
    return max_days - start.day  # get the offset from the first day of the month


def get_monthly_day_offset_from_first_day_by_weeks(week_ordinal: str, weekday: str, range_start: arrow.Arrow) -> int:
    # get offset ByWeekDays
    monthly_weeks: List[List[int]] = calendar.monthcalendar(range_start.year, range_start.month)
    week_position_index: int = WEEK_DAYS_KEYWORDS[week_ordinal]
    weekdays: List[int] = monthly_weeks[week_position_index]
    weekday_index: int = WEEKDAYS[weekday]
    day_of_month: int = weekdays[weekday_index]

    if week_position_index == -1:
        day_of_month = weekdays[weekday_index]
        if day_of_month == 0:
            day_of_month = monthly_weeks[week_position_index - 1][weekday_index]
    else:
        day_of_month_seen_count = 0
        for monthly_week in monthly_weeks:
            _week_day = monthly_week[weekday_index]
            if _week_day == 0:
                continue
            elif day_of_month_seen_count == week_position_index:
                day_of_month = _week_day
                break
            day_of_month_seen_count += 1
    return day_of_month - range_start.day


def get_monthly_steps_by_every_months(monthly_steps: int, range_start: arrow.Arrow) -> int:
    _monthly_steps = 0
    for _step in range(monthly_steps):
        _next_month_start = range_start.shift(months=_step)
        _, next_month_max_days = calendar.monthrange(_next_month_start.year, _next_month_start.month)
        _monthly_steps += next_month_max_days
    return _monthly_steps


def calc_monthly_distributions_by_days(
        range_start_date: str,
        range_end_date: str,
        timezone: str,
        day_of_month: int,
        monthly_steps: int,
        schedule_start: str,
        schedule_end: Optional[str] = None
) -> List[Dict[str, str]]:
    """
        Calculate schedule distributions by monthly day pattern
        :param range_start_date:
            This distributions range start date. e.g. 2022-05-18
        :param range_end_date:
            This distributions range end date. e.g. 2022-06-18
        :param timezone:
            Should calculate by which timezone. e.g. Asia/Shanghai
        :param day_of_month:
            Day of the month. e.g. 1 means the first day of the month
        :param monthly_steps:
            Monthly schedule pattern.
            e.g. If monthly steps is 3, which means the schedules will repeat every 3 month
        :param schedule_start:
            Schedule start time. e.g. 08:30 PM
        :param schedule_end:
            Schedule end time, which is optional. e.g. 11:00 PM
        :return:
            A list with all schedule distribution start&end time string.
        :raise:
            ValueError
        """
    ranges: Tuple[arrow.Arrow, arrow.Arrow] = get_schedule_range_time(range_start_date, range_end_date, timezone)
    range_start, range_end = ranges
    range_distance = range_end - range_start
    schedule_ranges: Tuple[Dict[str, int], Dict[str, int]] = get_schedule_ranges(
        schedule_start, schedule_end
    )
    _schedule_start, _schedule_end = schedule_ranges

    instances = []
    cur_step = -1
    for day in range(0, range_distance.days + 31):
        _each_start = range_start.shift(days=day)
        _cur_month_day = int(_each_start.format("D"))  # current day of month
        _month_day_offset = get_monthly_day_offset_from_first_day_by_days(day_of_month, _each_start)
        # get the total steps need to skip according to the schedule's monthly options
        _monthly_steps = get_monthly_steps_by_every_months(monthly_steps, _each_start)

        is_terminated, cur_step = _calc_monthly_distributions_step_process(cur_step, _monthly_steps, _cur_month_day)
        if is_terminated:
            continue
        _distribution = _generate_schedule_distribution_instance(
            day, range_start, range_end, _month_day_offset, _schedule_start, _schedule_end
        )
        if _distribution:
            instances.append(_distribution)
    return instances


def _generate_schedule_distribution_instance(
        day: int,
        range_start: arrow.Arrow,
        range_end: arrow.Arrow,
        month_day_offset: int,
        schedule_start: dict,
        schedule_end: dict
) -> dict:
    _start = range_start.shift(
        days=day + month_day_offset, hours=schedule_start[HOUR], minutes=schedule_start[MINUTE]
    )  # shift the range start to each instance start time
    if _start > range_end.shift(days=1) or _start < range_start:  # skip instance if out of range
        return {}

    _distribution = {START_TIME: _start.format(TIME_FORMAT_WITHOUT_SECOND)}
    if schedule_end:
        _end = range_start.shift(
            days=day + month_day_offset, hours=schedule_end[HOUR], minutes=schedule_end[MINUTE]
        )  # shift the range end to each instance end time

        if schedule_end[HOUR] < schedule_start[HOUR]:  # cross a day, then end time need to shift 1 day
            _end = _end.shift(days=1)
        _distribution[END_TIME] = _end.format(TIME_FORMAT_WITHOUT_SECOND)
    return _distribution


def _calc_monthly_distributions_step_process(cur_step: int, monthly_steps, cur_month_day) -> tuple[bool, int]:
    skip_steps = monthly_steps - cur_month_day + 1  # skip steps calculated by every month days length
    if cur_step == 0:
        cur_step = -1  # reset
        return True, cur_step
    elif cur_step == -1:
        cur_step = skip_steps
    # skip same month
    elif cur_step < skip_steps or not (cur_step == skip_steps and cur_month_day == 1):
        cur_step -= 1  # reduce step to zero for reset step and start add next instance
        return True, cur_step
    return False, cur_step


def calc_monthly_distributions_by_weeks(
        range_start_date: str,
        range_end_date: str,
        timezone: str,
        week_ordinal: str,
        weekday: str,
        monthly_steps: int,
        schedule_start: str,
        schedule_end: Optional[str] = None
) -> List[Dict[str, str]]:
    """
        Calculate schedule distributions by monthly day pattern
        :param range_start_date:
            This distributions range start date. e.g. 2022-05-18
        :param range_end_date:
            This distributions range end date. e.g. 2022-06-18
        :param timezone:
            Should calculate by which timezone. e.g. Asia/Shanghai
        :param week_ordinal:
            The week ordinal of week.
            e.g. First/Second/Third/Fourth/Last means the 1st/2nd/3rd/4th/last `weekday` of the week
        :param weekday:
            The weekday of week. e.g. Monday
        :param monthly_steps:
            Monthly schedule pattern.
            e.g. If monthly steps is 3, which means the schedules will repeat every 3 month
        :param schedule_start:
            Schedule start time. e.g. 08:30 PM
        :param schedule_end:
            Schedule end time, which is optional. e.g. 11:00 PM
        :return:
            A list with all schedule distribution start&end time string.
        :raise:
            ValueError
        """

    ranges: Tuple[arrow.Arrow, arrow.Arrow] = get_schedule_range_time(range_start_date, range_end_date, timezone)
    range_start, range_end = ranges
    range_distance = range_end - range_start
    schedule_ranges: Tuple[Dict[str, int], Dict[str, int]] = get_schedule_ranges(
        schedule_start, schedule_end
    )
    _schedule_start, _schedule_end = schedule_ranges

    instances = []
    cur_step = -1
    for day in range(0, range_distance.days + 31):
        _each_start = range_start.shift(days=day)
        _cur_month_day = int(_each_start.format("D"))  # current day of month
        _month_day_offset = get_monthly_day_offset_from_first_day_by_weeks(week_ordinal, weekday, _each_start)
        # get the total steps need to skip according to the schedule's monthly options
        _monthly_steps = get_monthly_steps_by_every_months(monthly_steps, _each_start)

        is_terminated, cur_step = _calc_monthly_distributions_step_process(cur_step, _monthly_steps, _cur_month_day)
        if is_terminated:
            continue
        _distribution = _generate_schedule_distribution_instance(
            day, range_start, range_end, _month_day_offset, _schedule_start, _schedule_end
        )
        if _distribution:
            instances.append(_distribution)
    return instances


def get_daily_schedule_distributions(schedule: dict) -> List[dict]:
    return calc_daily_distributions(
        range_start_date=schedule["Range"]["StartDateAt"],
        range_end_date=schedule["Range"]["EndDateAt"],
        daily_steps=schedule["DailyOptions"]["EveryDays"],
        timezone=schedule["TimeZone"]["Name"],
        schedule_start=schedule["StartTime"],
        schedule_end=schedule.get("EndTime")
    )


def get_weekly_schedule_distributions(schedule: dict) -> List[dict]:
    return calc_weekly_distributions(
        range_start_date=schedule["Range"]["StartDateAt"],
        range_end_date=schedule["Range"]["EndDateAt"],
        weekly_steps=schedule["WeeklyOptions"]["RecursiveEveryWeeks"],
        weekdays=schedule["WeeklyOptions"]["WeekDays"],
        timezone=schedule["TimeZone"]["Name"],
        schedule_start=schedule["StartTime"],
        schedule_end=schedule.get("EndTime")
    )


def get_monthly_schedule_distributions(schedule: dict) -> List[dict]:
    range_start = schedule["Range"]["StartDateAt"]
    range_end = schedule["Range"]["EndDateAt"]
    timezone = schedule["TimeZone"]["Name"]
    schedule_start = schedule["StartTime"]
    schedule_end = schedule.get("EndTime")

    if schedule["MonthlyOptions"]["Type"] == "ByDays":
        by_days_options = schedule["MonthlyOptions"]["ByDays"]
        return calc_monthly_distributions_by_days(
            range_start_date=range_start,
            range_end_date=range_end,
            timezone=timezone,
            day_of_month=by_days_options["Days"],
            monthly_steps=by_days_options["EveryMonths"],
            schedule_start=schedule_start,
            schedule_end=schedule_end
        )
    by_weeks_options = schedule["MonthlyOptions"]["ByWeekDays"]
    return calc_monthly_distributions_by_weeks(
        range_start_date=range_start,
        range_end_date=range_end,
        timezone=timezone,
        week_ordinal=by_weeks_options["Ordinal"],
        weekday=by_weeks_options["WeekDay"],
        monthly_steps=by_weeks_options["EveryMonths"],
        schedule_start=schedule_start,
        schedule_end=schedule_end
    )


def calc_distributions_by_pattern(schedule: dict) -> List[dict]:
    """
    :param schedule: schedule dict object
    :return:
    """
    schedule_pattern_ctrls = {
        "Daily": get_daily_schedule_distributions,
        "Weekly": get_weekly_schedule_distributions,
        "Monthly": get_monthly_schedule_distributions
    }
    return schedule_pattern_ctrls[schedule["Pattern"]](schedule) 