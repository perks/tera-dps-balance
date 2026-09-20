"""Verify every glyph's skill link independently of the field we group by.

The leaderboard API gives each glyph a `skillName`. Glyph *display names* are
legacy and often name a different skill than the one they modify, so grouping
by name is wrong. This checks the API's skillName against the game's own
skillNameToIcon map: a glyph's skillIcon must be the icon of the skill it
claims. Run after refreshing glyph_catalogue.json.

Usage: python verify_glyphs.py [path-to-skills-data.json]
  skills data: GET /api/leaderboard/skills-data?locale=en
"""
import json,re,collections,os,sys,urllib.request

SKILLS = sys.argv[1] if len(sys.argv) > 1 else "skills-data.json"
if not os.path.exists(SKILLS):
    print("fetching skills-data (~21MB) ...")
    req = urllib.request.Request(
        "https://tera-europe-classic.com/api/leaderboard/skills-data?locale=en",
        headers={"User-Agent": "curl/8.0"})
    open(SKILLS, "wb").write(urllib.request.urlopen(req, timeout=300).read())

d = json.load(open(SKILLS, encoding="utf-8"))
ROM = re.compile(r"\s+(?:[IVXL]+)$")
icon2skill = collections.defaultdict(set)
for name, m in d["skillNameToIcon"].items():
    ic = m.get("Slayer")
    if ic:
        icon2skill[ic.split("/")[-1].lower()].add(ROM.sub("", name).strip())

cat = json.load(open("glyph_catalogue.json", encoding="utf-8"))
used = collections.Counter()
for f in os.listdir("slayer"):
    for s in json.load(open("slayer/" + f))["slayers"]:
        for g in s["glyphs"]:
            if g["enabled"]:
                used[g["name"]] += 1

seen, bad, unknown, ok = set(), [], [], 0
for v in cat.values():
    n, api = v.get("name"), v.get("skill")
    if not n or n not in used or n in seen:
        continue
    seen.add(n)
    truth = icon2skill.get((v.get("skillIcon") or "").split("/")[-1].lower(), set())
    if not truth:
        unknown.append((n, api))
    elif api in truth:
        ok += 1
    else:
        bad.append((n, api, sorted(truth)))

print(f"{ok} verified, {len(bad)} mismatched, {len(unknown)} unresolved "
      f"(of {len(seen)} glyphs in use)")
for n, api, truth in bad:
    print(f"  MISMATCH {n}: API says {api}, icon says {', '.join(truth)}")
for n, api in unknown:
    print(f"  UNRESOLVED {n}: API says {api}, no icon match")

mismatched_names = [n for n in seen
                    if (lambda g: g and not n.endswith(" " + (g or "")))(
                        next((v.get("skill") for v in cat.values()
                              if v.get("name") == n), None))]
if mismatched_names:
    print("\nGlyphs whose display name does not match the skill they modify:")
    for n in sorted(mismatched_names):
        sk = next(v.get("skill") for v in cat.values() if v.get("name") == n)
        print(f"  {n:34} -> {sk}")
raise SystemExit(1 if bad else 0)
