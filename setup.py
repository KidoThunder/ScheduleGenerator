#!/usr/bin/env python3
"""
Setup script for ScheduleGenerator
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="schedule-generator",
    version="0.1.4",
    author="Kido Zhao",
    author_email="zgdisgod@gmail.com",
    description="一个用于计算周期事件时间分布的Python库，支持日、周、月三种重复模式",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ScheduleGenerator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords="schedule appointment calendar time distribution recurring",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ScheduleGenerator/issues",
        "Source": "https://github.com/yourusername/ScheduleGenerator",
        "Documentation": "https://github.com/yourusername/ScheduleGenerator#readme",
    },
) 