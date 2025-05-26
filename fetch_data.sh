#!/bin/bash
set -e  # exit on first error

echo "Fetching latest COVID-19 data from OWID..."
python scripts/fetch_data.py
echo "Done!"

