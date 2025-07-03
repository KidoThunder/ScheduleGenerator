#!/usr/bin/env python3
"""
Command line interface for ScheduleGenerator
"""

import json
import sys
from typing import Dict, Any

from schedule_generator import (
    calc_daily,
    calc_weekly,
    calc_monthly_by_days,
    calc_monthly_by_weeks,
    calc_dist_by_pattern,
)


def print_usage():
    """打印使用说明"""
    print("""
ScheduleGenerator - 周期事件时间分布计算器

用法:
    python cli.py daily <start_date> <end_date> <daily_steps> <timezone> <start_time> [end_time]
    python cli.py weekly <start_date> <end_date> <weekly_steps> <weekdays> <timezone> <start_time> [end_time]
    python cli.py monthly-days <start_date> <end_date> <timezone> <day_of_month> <monthly_steps> <start_time> [end_time]
    python cli.py monthly-weeks <start_date> <end_date> <timezone> <week_ordinal> <weekday> <monthly_steps> <start_time> [end_time]
    python cli.py pattern <config_file>

示例:
    python cli.py daily 2022-05-01 2022-05-31 3 "Asia/Shanghai" "08:30 PM" "11:00 PM"
    python cli.py weekly 2022-05-01 2022-05-31 1 "Monday,Friday" "Asia/Shanghai" "10:00 AM"
    python cli.py monthly-days 2022-05-01 2022-08-31 "Asia/Shanghai" 15 1 "02:00 PM"
    python cli.py monthly-weeks 2022-05-01 2022-07-31 "Asia/Shanghai" "First" "Monday" 1 "03:00 PM"
    python cli.py pattern config.json
""")


def parse_weekdays(weekdays_str: str) -> list[str]:
    """解析星期几字符串"""
    return [day.strip() for day in weekdays_str.split(",")]


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "daily":
            if len(sys.argv) < 7:
                print("错误: 每日模式需要至少6个参数")
                print_usage()
                sys.exit(1)
            
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            daily_steps = int(sys.argv[4])
            timezone = sys.argv[5]
            start_time = sys.argv[6]
            end_time = sys.argv[7] if len(sys.argv) > 7 else None
            
            result = calc_daily(
                range_start_date=start_date,
                range_end_date=end_date,
                daily_steps=daily_steps,
                timezone=timezone,
                appointment_start=start_time,
                appointment_end=end_time
            )
            
        elif command == "weekly":
            if len(sys.argv) < 7:
                print("错误: 每周模式需要至少7个参数")
                print_usage()
                sys.exit(1)
            
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            weekly_steps = int(sys.argv[4])
            weekdays = parse_weekdays(sys.argv[5])
            timezone = sys.argv[6]
            start_time = sys.argv[7]
            end_time = sys.argv[8] if len(sys.argv) > 8 else None
            
            result = calc_weekly(
                range_start_date=start_date,
                range_end_date=end_date,
                weekly_steps=weekly_steps,
                weekdays=weekdays,
                timezone=timezone,
                appointment_start=start_time,
                appointment_end=end_time
            )
            
        elif command == "monthly-days":
            if len(sys.argv) < 7:
                print("错误: 每月按天数模式需要至少7个参数")
                print_usage()
                sys.exit(1)
            
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            timezone = sys.argv[4]
            day_of_month = int(sys.argv[5])
            monthly_steps = int(sys.argv[6])
            start_time = sys.argv[7]
            end_time = sys.argv[8] if len(sys.argv) > 8 else None
            
            result = calc_monthly_by_days(
                range_start_date=start_date,
                range_end_date=end_date,
                timezone=timezone,
                day_of_month=day_of_month,
                monthly_steps=monthly_steps,
                appointment_start=start_time,
                appointment_end=end_time
            )
            
        elif command == "monthly-weeks":
            if len(sys.argv) < 8:
                print("错误: 每月按周几模式需要至少8个参数")
                print_usage()
                sys.exit(1)
            
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            timezone = sys.argv[4]
            week_ordinal = sys.argv[5]
            weekday = sys.argv[6]
            monthly_steps = int(sys.argv[7])
            start_time = sys.argv[8]
            end_time = sys.argv[9] if len(sys.argv) > 9 else None
            
            result = calc_monthly_by_weeks(
                range_start_date=start_date,
                range_end_date=end_date,
                timezone=timezone,
                week_ordinal=week_ordinal,
                weekday=weekday,
                monthly_steps=monthly_steps,
                appointment_start=start_time,
                appointment_end=end_time
            )
            
        elif command == "pattern":
            if len(sys.argv) < 3:
                print("错误: 模式配置需要配置文件路径")
                print_usage()
                sys.exit(1)
            
            config_file = sys.argv[2]
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            result = calc_dist_by_pattern(config)
            
        else:
            print(f"错误: 未知命令 '{command}'")
            print_usage()
            sys.exit(1)
        
        # 输出结果
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 