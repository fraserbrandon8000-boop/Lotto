"""Step 1: audit the original workbook (read-only) and build a normalized analysis dataset."""
import json, hashlib, pandas as pd, numpy as np
ORIG = "data/original/Lotto-Draw-Dataset.xlsx"
OUT = "results/claude_lotto_2340"
sha = hashlib.sha256(open(ORIG, "rb").read()).hexdigest()
raw = pd.read_excel(ORIG, header=4)
raw.columns = ["draw", "date", "n1", "n2", "n3", "n4", "n5", "n6", "bonus", "source"]
issues = []
n_rows = len(raw)
if raw.isna().any().any():
    issues.append(f"rows with missing cells: {raw[raw.isna().any(axis=1)].index.tolist()}")
raw = raw.dropna(subset=["draw"]).copy()
raw["draw"] = raw["draw"].astype(int)
raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
if raw["date"].isna().any(): issues.append("malformed dates present")
M = ["n1", "n2", "n3", "n4", "n5", "n6"]
dup_ids = raw["draw"][raw["draw"].duplicated()].tolist()
dup_rec = int(raw.duplicated(subset=M + ["bonus"]).sum())
for _, r in raw.iterrows():
    nums = [int(r[c]) for c in M]
    if len(set(nums)) != 6: issues.append(f"#{r.draw}: duplicate main numbers")
    if not all(1 <= v <= 38 for v in nums): issues.append(f"#{r.draw}: main out of range")
    if nums != sorted(nums): issues.append(f"#{r.draw}: mains not sorted (info)")
    b = int(r.bonus)
    if not 1 <= b <= 38: issues.append(f"#{r.draw}: bonus out of range")
    if b in nums: issues.append(f"#{r.draw}: bonus overlaps main")
    if r.date.day_name() not in ("Wednesday", "Saturday"):
        issues.append(f"#{r.draw}: unexpected weekday {r.date.day_name()} {r.date.date()}")
s = raw.sort_values("draw")
chrono_ok = bool(s["date"].is_monotonic_increasing and s["date"].is_unique)
ids = set(s["draw"]); missing = [i for i in range(min(ids), max(ids) + 1) if i not in ids]
# date spacing around the gap
gap_ctx = s[(s.draw >= 2248) & (s.draw <= 2265)][["draw", "date"]].astype(str).values.tolist()

recent = pd.DataFrame([
    dict(draw=2338, date=pd.Timestamp("2026-09-16"), n1=1, n2=3, n3=10, n4=13, n5=18, n6=29, bonus=17,
         source="RECENT ADDITION (user-supplied; Supreme Ventures validation blocked by network policy)"),
    dict(draw=2339, date=pd.Timestamp("2026-09-19"), n1=1, n2=4, n3=6, n4=13, n5=23, n6=28, bonus=20,
         source="RECENT ADDITION (user-supplied; Supreme Ventures validation blocked by network policy)"),
])
for _, r in recent.iterrows():
    nums = [r[c] for c in M]; assert len(set(nums)) == 6 and r.bonus not in nums and r.date.day_name() in ("Wednesday", "Saturday")
s = s.assign(provenance="ORIGINAL WORKBOOK")
recent = recent.assign(provenance="RECENT OFFICIAL ADDITION (unverified externally)")
norm = pd.concat([s, recent]).sort_values("draw").reset_index(drop=True)
norm["segment"] = np.where(norm.draw < 2252, 0, 1)   # break at unrecovered gap 2252-2261
norm[M] = np.sort(norm[M].values, axis=1)
norm.to_csv(f"{OUT}/normalized_draws.csv", index=False, date_format="%Y-%m-%d")
audit = dict(original_workbook=ORIG, original_sha256=sha, header_rows_skipped=4, data_rows=n_rows,
             draw_range=[int(s.draw.min()), int(s.draw.max())], date_range=[str(s.date.min().date()), str(s.date.max().date())],
             duplicate_draw_ids=dup_ids, duplicate_records=dup_rec, chronological_consistent=chrono_ok,
             missing_draw_ids=missing, gap_context=gap_ctx, issues=issues,
             external_recoveries="NONE: supremeventures.com denied by environment network policy (HTTP 403 on CONNECT); 2252-2261 left missing, not fabricated",
             recent_additions=[2338, 2339], normalized_rows=len(norm),
             series_consecutive_through_2339=False, source_counts=s["source"].value_counts().to_dict())
json.dump(audit, open(f"{OUT}/data_audit.json", "w"), indent=2, default=str)
print(json.dumps(audit, indent=2, default=str))
