#!/bin/bash

# create folders if missing
mkdir -p ~/Library/Script\ Libraries
mkdir -p ~/Library/LaunchAgents

sudo osacompile -o Discipline.scpt Discipline.applescript
cp Discipline.scpt ~/Library/Script\ Libraries
