#!/usr/bin/env bash
# run_daily.sh — one edition, start to finish. Called by launchd (Mac) or CI.
#
#   ./run_daily.sh              today
#   ./run_daily.sh 2026-09-07   a specific date
#
# Exit codes:  0 ok · 2 G13 FAIL (a row was never attempted) · 3 draft unavailable
#              — on 3 it has ALREADY produced a degraded, facts-only edition.
set -uo pipefail
cd "$(dirname "$0")"

DATE="${1:-$(date +%F)}"
LOG="logs/${DATE}.log"
mkdir -p logs out raw state
exec > >(tee -a "$LOG") 2>&1

echo "=================================================================="
echo " DAYBREAK  $DATE   started $(date '+%F %T %Z')   host $(hostname -s)"
echo "=================================================================="

python3 daybreak.py fetch --date "$DATE"
FETCH=$?
if [ $FETCH -eq 2 ]; then
  echo "!! G13 FAIL — a manifest row was never attempted. Not drafting."
  exit 2
fi

python3 daybreak.py draft --date "$DATE"
DRAFT=$?

if [ $DRAFT -ne 0 ]; then
  echo "!! draft stage unavailable (exit $DRAFT) — falling back to a degraded edition."
  python3 daybreak.py build --date "$DATE" --degraded
  echo "!! A facts-only brief is at out/brief_${DATE}.md."
  echo "!! It is on time and it is true. A human should add the judgement layer."
  exit 3
fi

python3 daybreak.py build   --date "$DATE"
python3 daybreak.py publish --date "$DATE"

echo "-- done $(date '+%F %T %Z') --"
