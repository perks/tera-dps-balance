"""Refresh the DPS class balance page end to end.

    python refresh_dps.py

Steps: pull the solo DPS rankings for the five endgame dungeons, fetch gear
for any encounter not already cached in enc/, recompute final.json, then
regenerate tera-dps-balance/index.html and the landing page. Encounters
already in enc/ are never refetched, so repeat runs only cost the new ones.
"""
import json, subprocess, sys, os

def run(script):
    print(f"\n=== {script} ===", flush=True)
    r = subprocess.run([sys.executable, script], env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode:
        raise SystemExit(f"{script} failed ({r.returncode})")

run("fetch.py")

rows = json.load(open("rows.json"))
uids = sorted({r["encounterUid"] for r in rows if r.get("encounterUid")})
json.dump(uids, open("pick.json", "w"))
cached = len(os.listdir("enc")) if os.path.isdir("enc") else 0
print(f"\n{len(uids)} encounters referenced, {cached} already cached, "
      f"~{max(0, len(uids) - cached)} to fetch")

run("fetchgear.py")
run("final.py")
run("report.py")
run("hub.py")
print("\nDone. Regenerated tera-dps-balance/index.html and index.html")
