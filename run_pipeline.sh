#!/bin/bash
set -e  # exit on first error

echo "Fetching latest COVID-19 data from OWID..."
python fetch_data.py

echo "Seeding data into your warehouse..."
dbt seed

echo "Running dbt models..."
dbt run

echo "Running dbt tests..."
dbt test

echo "Generating documentation..."
dbt docs generate

echo "Done!"
echo "To view the docs, run: dbt docs serve"
