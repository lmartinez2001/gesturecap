#!/bin/bash


# python main.py --scenario scenarios/main_scenario.yml
# python main.py --scenario scenarios/barycenter_scenario.yml
source .venv/bin/activate
python main.py --scenario scenarios/pose_scenario_flircam.yml
