#!/bin/bash
set -e  # Exit on first error
set -o pipefail

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}


FORCE_UPDATE=""
for arg in "$@"; do
  if [[ "$arg" == "--force-update" ]]; then
    FORCE_UPDATE="--force-update"
  fi
done


log "🚀 Starting COVID-19 Data Pipeline..."

log "📤 Uploading raw COVID-19 data to Snowflake..."
python scripts/upload_raw.py $FORCE_UPDATE

log "🏗  Running all dbt models..."
dbt run

log "✅ Running dbt tests..."
dbt test

log "📚 Generating documentation..."
dbt docs generate

log "✅ Done!"
echo ""
log "To view the docs, run: dbt docs serve"
