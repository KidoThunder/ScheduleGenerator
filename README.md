# ScheduleGenerator

一个用于计算周期事件时间分布的Python库，支持日、周、月三种重复模式，遵循Microsoft标准的时间模式表示。

## 功能特性

- 🗓️ **多种重复模式**: 支持每日、每周、每月三种重复模式
- 🌍 **时区支持**: 完全支持时区计算
- 📅 **灵活的时间设置**: 支持按天数、按周几、按月份第几周等多种设置
- ⚡ **高性能**: 基于Arrow库的高效时间计算
- 🎯 **Microsoft标准**: 遵循Microsoft的时间模式标准

## 安装

```bash
pip install schedule-generator
```

或者从源码安装：

```bash
git clone https://github.com/yourusername/ScheduleGenerator.git
cd ScheduleGenerator
pip install -e .
```

## 快速开始

### 每日重复模式

```python
from schedule_generator import calc_daily

# 每3天重复一次，从2022-05-01到2022-05-31
schedules = calc_daily(
    range_start_date="2022-05-01",
    range_end_date="2022-05-31",
    daily_steps=3,
    timezone="Asia/Shanghai",
    schedule_start="08:30 PM",
    schedule_end="11:00 PM"
)

print(schedules)
# 输出:
# [{'start_time': '2022-05-01 20:30', 'end_time': '2022-05-01 23:00'},
#  {'start_time': '2022-05-04 20:30', 'end_time': '2022-05-04 23:00'},
#  {'start_time': '2022-05-07 20:30', 'end_time': '2022-05-07 23:00'},
#  ...]
```

### 每周重复模式

```python
from schedule_generator import calc_weekly

# 每2周重复一次，在周一和周六
schedules = calc_weekly(
    range_start_date="2022-05-01",
    range_end_date="2022-05-31",
    weekly_steps=2,
    weekdays=["Monday", "Saturday"],
    timezone="Asia/Shanghai",
    schedule_start="08:30 PM",
    schedule_end="11:00 PM"
)
```

### 每月重复模式

#### 按天数重复

```python
from schedule_generator import calc_monthly_by_days

# 每月15号重复，每2个月一次
schedules = calc_monthly_by_days(
    range_start_date="2022-05-01",
    range_end_date="2023-09-30",
    timezone="Asia/Shanghai",
    day_of_month=15,
    monthly_steps=2,
    schedule_start="08:30 PM"
)
```

#### 按周几重复

```python
from schedule_generator import calc_monthly_by_weeks

# 每月第三个周一重复，每2个月一次
schedules = calc_monthly_by_weeks(
    range_start_date="2022-05-01",
    range_end_date="2022-09-30",
    timezone="Asia/Shanghai",
    week_ordinal="Third",
    weekday="Monday",
    monthly_steps=2,
    schedule_start="08:30 PM",
    schedule_end="11:00 PM"
)
```

### 使用统一接口

```python
from schedule_generator import calc_dist_by_pattern

schedule_config = {
    "Pattern": "Daily",
    "DailyOptions": {
        "EveryDays": 1
    },
    "WeeklyOptions": {
        "RecursiveEveryWeeks": 1,
        "WeekDays": ["Monday"]
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

schedules = calc_dist_by_pattern(schedule_config)
```

## 命令行使用

ScheduleGenerator 还提供了命令行接口：

```bash
# 每日模式
python cli.py daily 2022-05-01 2022-05-31 3 "Asia/Shanghai" "08:30 PM" "11:00 PM"

# 每周模式
python cli.py weekly 2022-05-01 2022-05-31 1 "Monday,Friday" "Asia/Shanghai" "10:00 AM"

# 每月按天数模式
python cli.py monthly-days 2022-05-01 2022-08-31 "Asia/Shanghai" 15 1 "02:00 PM"

# 每月按周几模式
python cli.py monthly-weeks 2022-05-01 2022-07-31 "Asia/Shanghai" "First" "Monday" 1 "03:00 PM"

# 使用配置文件
python cli.py pattern examples/config.json
```

## API 文档

### 核心函数

#### `calc_daily(range_start_date, range_end_date, daily_steps, timezone, schedule_start, schedule_end=None)`

计算每日重复的周期事件时间分布。

**参数:**
- `range_start_date` (str): 开始日期，格式: "YYYY-MM-DD"
- `range_end_date` (str): 结束日期，格式: "YYYY-MM-DD"
- `daily_steps` (int): 每隔多少天重复一次
- `timezone` (str): 时区名称，如 "Asia/Shanghai"
- `schedule_start` (str): 开始时间，格式: "HH:MM AM/PM"
- `schedule_end` (str, optional): 结束时间，格式: "HH:MM AM/PM"

**返回:**
- `List[Dict[str, str]]`: 周期事件时间列表，每个元素包含 `start_time` 和可选的 `end_time`

#### `calc_weekly(range_start_date, range_end_date, weekly_steps, weekdays, timezone, schedule_start, schedule_end=None)`

计算每周重复的周期事件时间分布。

**参数:**
- `range_start_date` (str): 开始日期
- `range_end_date` (str): 结束日期
- `weekly_steps` (int): 每隔多少周重复一次
- `weekdays` (List[str]): 星期几列表，如 ["Monday", "Friday"]
- `timezone` (str): 时区名称
- `schedule_start` (str): 开始时间
- `schedule_end` (str, optional): 结束时间

#### `calc_monthly_by_days(range_start_date, range_end_date, timezone, day_of_month, monthly_steps, schedule_start, schedule_end=None)`

按月份天数计算重复周期事件。

**参数:**
- `day_of_month` (int): 月份中的第几天 (1-31)
- `monthly_steps` (int): 每隔多少个月重复一次

#### `calc_monthly_by_weeks(range_start_date, range_end_date, timezone, week_ordinal, weekday, monthly_steps, schedule_start, schedule_end=None)`

按月份周几计算重复周期事件。

**参数:**
- `week_ordinal` (str): 周序数，可选值: "First", "Second", "Third", "Fourth", "Last"
- `weekday` (str): 星期几，如 "Monday"

### 配置对象格式

使用 `calc_dist_by_pattern` 函数时，需要提供配置对象：

```python
{
    "Pattern": "Daily|Weekly|Monthly",
    "DailyOptions": {
        "EveryDays": int
    },
    "WeeklyOptions": {
        "RecursiveEveryWeeks": int,
        "WeekDays": List[str]
    },
    "MonthlyOptions": {
        "Type": "ByDays|ByWeekDays",
        "ByDays": {
            "Days": int,
            "EveryMonths": int
        },
        "ByWeekDays": {
            "Ordinal": str,
            "WeekDay": str,
            "EveryMonths": int
        }
    },
    "StartTime": str,
    "EndTime": str,
    "TimeZone": {
        "Name": str
    },
    "Range": {
        "StartDateAt": str,
        "EndDateAt": str
    }
}
```

## 支持的时区

支持所有标准时区名称，例如：
- `Asia/Shanghai`
- `America/New_York`
- `Europe/London`
- `UTC`

## 支持的星期几

- `Sunday`
- `Monday`
- `Tuesday`
- `Wednesday`
- `Thursday`
- `Friday`
- `Saturday`

## 支持的周序数

- `First` - 第一周
- `Second` - 第二周
- `Third` - 第三周
- `Fourth` - 第四周
- `Last` - 最后一周

## 开发

### 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

### 运行测试

```bash
python -m pytest tests/
```

### 代码格式化

```bash
black .
isort .
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.1.4
- 修复时区计算问题
- 优化性能
- 添加更多测试用例

### v0.1.0
- 初始版本发布
- 支持日、周、月三种重复模式

一个用于计算周期事件时间分布的Python库，支持日、周、月三种重复模式，遵循Microsoft标准的时间模式表示。

## 功能特性

- 🗓️ **多种重复模式**: 支持每日、每周、每月三种重复模式
- 🌍 **时区支持**: 完全支持时区计算
- 📅 **灵活的时间设置**: 支持按天数、按周几、按月份第几周等多种设置
- ⚡ **高性能**: 基于Arrow库的高效时间计算
- 🎯 **Microsoft标准**: 遵循Microsoft的时间模式标准

## 安装

```bash
pip install schedule-generator
```

或者从源码安装：

```bash
git clone https://github.com/yourusername/ScheduleGenerator.git
cd ScheduleGenerator
pip install -e .
```

## 快速开始

### 每日重复模式

```python
from schedule_generator import calc_daily

# 每3天重复一次，从2022-05-01到2022-05-31
schedules = calc_daily(
    range_start_date="2022-05-01",
    range_end_date="2022-05-31",
    daily_steps=3,
    timezone="Asia/Shanghai",
    schedule_start="08:30 PM",
    schedule_end="11:00 PM"
)

print(schedules)
# 输出:
# [{'start_time': '2022-05-01 20:30', 'end_time': '2022-05-01 23:00'},
#  {'start_time': '2022-05-04 20:30', 'end_time': '2022-05-04 23:00'},
#  {'start_time': '2022-05-07 20:30', 'end_time': '2022-05-07 23:00'},
#  ...]
```

### 每周重复模式

```python
from schedule_generator import calc_weekly

# 每2周重复一次，在周一和周六
schedules = calc_weekly(
    range_start_date="2022-05-01",
    range_end_date="2022-05-31",
    weekly_steps=2,
    weekdays=["Monday", "Saturday"],
    timezone="Asia/Shanghai",
    schedule_start="08:30 PM",
    schedule_end="11:00 PM"
)
```

### 每月重复模式

#### 按天数重复

```python
from schedule_generator import calc_monthly_by_days

# 每月15号重复，每2个月一次
schedules = calc_monthly_by_days(
    range_start_date="2022-05-01",
    range_end_date="2023-09-30",
    timezone="Asia/Shanghai",
    day_of_month=15,
    monthly_steps=2,
    schedule_start="08:30 PM"
)
```

#### 按周几重复

```python
from schedule_generator import calc_monthly_by_weeks

# 每月第三个周一重复，每2个月一次
schedules = calc_monthly_by_weeks(
    range_start_date="2022-05-01",
    range_end_date="2022-09-30",
    timezone="Asia/Shanghai",
    week_ordinal="Third",
    weekday="Monday",
    monthly_steps=2,
    schedule_start="08:30 PM",
    schedule_end="11:00 PM"
)
```

### 使用统一接口

```python
from schedule_generator import calc_dist_by_pattern

schedule_config = {
    "Pattern": "Daily",
    "DailyOptions": {
        "EveryDays": 1
    },
    "WeeklyOptions": {
        "RecursiveEveryWeeks": 1,
        "WeekDays": ["Monday"]
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

schedules = calc_dist_by_pattern(schedule_config)
```

## API 文档

### 核心函数

#### `calc_daily(range_start_date, range_end_date, daily_steps, timezone, schedule_start, schedule_end=None)`

计算每日重复的周期事件时间分布。

**参数:**
- `range_start_date` (str): 开始日期，格式: "YYYY-MM-DD"
- `range_end_date` (str): 结束日期，格式: "YYYY-MM-DD"
- `daily_steps` (int): 每隔多少天重复一次
- `timezone` (str): 时区名称，如 "Asia/Shanghai"
- `schedule_start` (str): 开始时间，格式: "HH:MM AM/PM"
- `schedule_end` (str, optional): 结束时间，格式: "HH:MM AM/PM"

**返回:**
- `List[Dict[str, str]]`: 周期事件时间列表，每个元素包含 `start_time` 和可选的 `end_time`

#### `calc_weekly(range_start_date, range_end_date, weekly_steps, weekdays, timezone, schedule_start, schedule_end=None)`

计算每周重复的周期事件时间分布。

**参数:**
- `range_start_date` (str): 开始日期
- `range_end_date` (str): 结束日期
- `weekly_steps` (int): 每隔多少周重复一次
- `weekdays` (List[str]): 星期几列表，如 ["Monday", "Friday"]
- `timezone` (str): 时区名称
- `schedule_start` (str): 开始时间
- `schedule_end` (str, optional): 结束时间

#### `calc_monthly_by_days(range_start_date, range_end_date, timezone, day_of_month, monthly_steps, schedule_start, schedule_end=None)`

按月份天数计算重复周期事件。

**参数:**
- `day_of_month` (int): 月份中的第几天 (1-31)
- `monthly_steps` (int): 每隔多少个月重复一次

#### `calc_monthly_by_weeks(range_start_date, range_end_date, timezone, week_ordinal, weekday, monthly_steps, schedule_start, schedule_end=None)`

按月份周几计算重复周期事件。

**参数:**
- `week_ordinal` (str): 周序数，可选值: "First", "Second", "Third", "Fourth", "Last"
- `weekday` (str): 星期几，如 "Monday"

### 配置对象格式

使用 `calc_dist_by_pattern` 函数时，需要提供配置对象：

```python
{
    "Pattern": "Daily|Weekly|Monthly",
    "DailyOptions": {
        "EveryDays": int
    },
    "WeeklyOptions": {
        "RecursiveEveryWeeks": int,
        "WeekDays": List[str]
    },
    "MonthlyOptions": {
        "Type": "ByDays|ByWeekDays",
        "ByDays": {
            "Days": int,
            "EveryMonths": int
        },
        "ByWeekDays": {
            "Ordinal": str,
            "WeekDay": str,
            "EveryMonths": int
        }
    },
    "StartTime": str,
    "EndTime": str,
    "TimeZone": {
        "Name": str
    },
    "Range": {
        "StartDateAt": str,
        "EndDateAt": str
    }
}
```

## 支持的时区

支持所有标准时区名称，例如：
- `Asia/Shanghai`
- `America/New_York`
- `Europe/London`
- `UTC`

## 支持的星期几

- `Sunday`
- `Monday`
- `Tuesday`
- `Wednesday`
- `Thursday`
- `Friday`
- `Saturday`

## 支持的周序数

- `First` - 第一周
- `Second` - 第二周
- `Third` - 第三周
- `Fourth` - 第四周
- `Last` - 最后一周

## 开发

### 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

### 运行测试

```bash
python -m pytest tests/
```

### 代码格式化

```bash
black .
isort .
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.1.4
- 修复时区计算问题
- 优化性能
- 添加更多测试用例

### v0.1.0
- 初始版本发布
- 支持日、周、月三种重复模式