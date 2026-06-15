#!/bin/bash

cd /home/tiago/football-analytics-platform
source /home/tiago/football-analytics-platform/venv/bin/activate
python3 -m pipeline.runner >> /home/tiago/football-analytics-platform/logs/pipeline_$(date +%Y%m%d_%H%M%S).log 2>&1
