#!/bin/bash
set -e
set -x

# generate flake8 reports
# Things to fix
flake8 service > flake8_report/report.txt
# Stats
flake8 --statistics service > flake8_report/stats.txt
