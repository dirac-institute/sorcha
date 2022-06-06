#!/bin/bash

# 1. Ensure that objectsInField is installed, if not, then
# follow the instructions at https://github.com/AsteroidSurveySimulator/objectsInField
# to install objects in field

# Execute the following task

oif -f oif.test.input.config | awk 'NR>24' > oif_10MBAs_test.txt