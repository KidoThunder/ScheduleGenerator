"""
Tests for the calculator module
"""

import pytest
from schedule_generator.calculator import (
    calc_daily_distributions,
    calc_weekly_distributions,
    calc_monthly_distributions_by_days,
    calc_monthly_distributions_by_weeks,
    calc_distributions_by_pattern,
)


class TestDailyDistributions:
    def test_daily_distributions_basic(self):
        """测试基本的每日重复功能"""
        result = calc_daily_distributions(
            range_start_date="2022-05-01",
            range_end_date="2022-05-10",
            daily_steps=3,
            timezone="Asia/Shanghai",
            schedule_start="08:30 PM",
            schedule_end="11:00 PM"
        )
        
        assert len(result) == 4  # 应该有4个周期事件
        assert result[0]["start_time"] == "2022-05-01 20:30"
        assert result[0]["end_time"] == "2022-05-01 23:00"
        assert result[1]["start_time"] == "2022-05-04 20:30"
        assert result[2]["start_time"] == "2022-05-07 20:30"
        assert result[3]["start_time"] == "2022-05-10 20:30"

    def test_daily_distributions_no_end_time(self):
        """测试没有结束时间的每日重复"""
        result = calc_daily_distributions(
            range_start_date="2022-05-01",
            range_end_date="2022-05-05",
            daily_steps=2,
            timezone="Asia/Shanghai",
            schedule_start="09:00 AM"
        )
        
        assert len(result) == 3
        assert "end_time" not in result[0]
        assert result[0]["start_time"] == "2022-05-01 09:00"


class TestWeeklyDistributions:
    def test_weekly_distributions_basic(self):
        """测试基本的每周重复功能"""
        result = calc_weekly_distributions(
            range_start_date="2022-05-01",
            range_end_date="2022-05-31",
            weekly_steps=1,
            weekdays=["Monday"],
            timezone="Asia/Shanghai",
            schedule_start="10:00 AM",
            schedule_end="11:00 AM"
        )
        
        # 验证所有周期事件都在周一
        for schedule in result:
            from datetime import datetime
            dt = datetime.strptime(schedule["start_time"], "%Y-%m-%d %H:%M")
            assert dt.weekday() == 0  # 0 = Monday


class TestMonthlyDistributions:
    def test_monthly_by_days_basic(self):
        """测试按月份天数的重复功能"""
        result = calc_monthly_distributions_by_days(
            range_start_date="2022-05-01",
            range_end_date="2022-08-31",
            timezone="Asia/Shanghai",
            day_of_month=15,
            monthly_steps=1,
            schedule_start="02:00 PM"
        )
        
        assert len(result) == 4  # 5月、6月、7月、8月的15号
        assert result[0]["start_time"] == "2022-05-15 14:00"
        assert result[1]["start_time"] == "2022-06-15 14:00"
        assert result[2]["start_time"] == "2022-07-15 14:00"
        assert result[3]["start_time"] == "2022-08-15 14:00"

    def test_monthly_by_weeks_basic(self):
        """测试按月份周几的重复功能"""
        result = calc_monthly_distributions_by_weeks(
            range_start_date="2022-05-01",
            range_end_date="2022-07-31",
            timezone="Asia/Shanghai",
            week_ordinal="First",
            weekday="Monday",
            monthly_steps=1,
            schedule_start="03:00 PM"
        )
        
        assert len(result) == 3  # 5月、6月、7月的第一个周一


class TestPatternDistributions:
    def test_daily_pattern(self):
        """测试每日模式的统一接口"""
        schedule_config = {
            "Pattern": "Daily",
            "DailyOptions": {
                "EveryDays": 2
            },
            "WeeklyOptions": {
                "RecursiveEveryWeeks": 1,
                "WeekDays": ["Monday"]
            },
            "MonthlyOptions": {
                "Type": "ByDays",
                "ByDays": {
                    "Days": 1,
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
                "StartDateAt": "2022-05-01",
                "EndDateAt": "2022-05-10"
            }
        }
        
        result = calc_distributions_by_pattern(schedule_config)
        assert len(result) == 5  # 每2天一次，从5月1日到5月10日


class TestErrorCases:
    def test_invalid_date_range(self):
        """测试无效的日期范围"""
        with pytest.raises(ValueError, match="Range start date is bigger than range end date"):
            calc_daily_distributions(
                range_start_date="2022-05-10",
                range_end_date="2022-05-01",
                daily_steps=1,
                timezone="Asia/Shanghai",
                schedule_start="08:00 AM"
            ) 