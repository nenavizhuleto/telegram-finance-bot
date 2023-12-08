#!/bin/bash

echo "Initializing database"
python db.py

echo "Starting telegram bot"
python main.py
