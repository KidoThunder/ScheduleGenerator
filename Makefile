.PHONY: help install install-dev test lint format clean build publish

help: ## 显示帮助信息
	@echo "ScheduleGenerator 开发命令"
	@echo "========================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装项目依赖
	pip install -r requirements.txt

install-dev: ## 安装开发依赖
	pip install -r requirements-dev.txt

test: ## 运行测试
	python -m pytest tests/ -v

test-cov: ## 运行测试并生成覆盖率报告
	python -m pytest tests/ --cov=schedule_generator --cov-report=html --cov-report=term

lint: ## 运行代码检查
	flake8 schedule_generator/ tests/
	mypy schedule_generator/

format: ## 格式化代码
	black schedule_generator/ tests/
	isort schedule_generator/ tests/

clean: ## 清理构建文件
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean ## 构建包
	python setup.py sdist bdist_wheel

publish: build ## 发布到PyPI (需要配置)
	twine upload dist/*

check-build: build ## 检查构建的包
	twine check dist/*

example: ## 运行示例
	python cli.py daily 2022-05-01 2022-05-31 3 "Asia/Shanghai" "08:30 PM" "11:00 PM"

example-config: ## 运行配置文件示例
	python cli.py pattern examples/config.json 