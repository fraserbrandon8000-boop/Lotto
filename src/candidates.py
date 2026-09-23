"""Step 11: rankings and complete-ticket candidates for #2340 using only draws through #2339."""
import sys, json, hashlib, numpy as np, pandas as pd
sys.path.insert(0, "src"); from models import *
OUT = "results/claude_lotto_2340"; SEED = 23402026
d = pd.read_csv(f"{OUT}/normalized_draws.csv"); assert d.draw.max() == 2339 and 2340 not in d.draw.values
D = d[["n1","n2","n3","n4","n5","n6"]].values.astype(int); T = len(D)
X = np.zeros((T, N), bool)
for t in range(T): X[t, D[t]-1] = True
A = json.load(open(f"{OUT}/analysis_results.json"))
pools = pd.read_csv(f"{OUT}/model_performance_pools.csv"); tks = pd.read_csv(f"{OUT}/model_performance_tickets.csv").set_index("method")
rng = np.random.default_rng([SEED, T])
sc = {m: model_scores(X, m, rng) for m in MODELS}
rk = {m: rank_numbers(sc[m], rng) for m in MODELS}
rank_pos = {m: {int(n)+1: int(np.where(rk[m] == n)[0][0])+1 for n in range(N)} for m in MODELS}
rk_tab = pd.DataFrame({m: [rank_pos[m][n] for n in range(1, N+1)] for m in MODELS}, index=pd.Index(range(1, N+1), name="number"))
rk_tab.to_csv(f"{OUT}/rankings_2340.csv")
# EWMA decay sensitivity (walk-forward pool-8 mean) — sensitivity only, not used for tuning
sens = {}
for lam in (0.8, 0.85, 0.9, 0.95):
    h = []
    for t in range(40, T):
        H = X[:t]; w = lam**np.arange(t)[::-1]; s = (H*w[:, None]).sum(0)
        r = rank_numbers(s, np.random.default_rng([SEED, t])); h.append(int(X[t, r[:8]].sum()))
    sens[lam] = float(np.mean(h))
tickets = build_tickets(X, rk, rng)
H = X; g = gap_now(H); L = pairlift(H)
idxh = np.where(H)[1].reshape(-1, K)+1; smean, ssd = idxh.sum(1).mean(), idxh.sum(1).std()
seen, cands = {}, []
for meth, tk in tickets.items():
    if meth == "top6:random_control": continue
    key = tuple(int(x)+1 for x in tk)
    if key in seen: seen[key].append(meth); continue
    seen[key] = [meth]
for key, meths in seen.items():
    c0 = [n-1 for n in key]
    bt = {m: dict(mean=round(float(tks.loc[m, "mean"]), 3), p_one_sided=round(float(tks.loc[m, "p_full"]), 3),
                  p_holm=round(float(tks.loc[m, "p_full_holm"]), 3), dev_mean=round(float(tks.loc[m, "dev_mean"]), 3),
                  conf_mean=round(float(tks.loc[m, "conf_mean"]), 3)) for m in meths}
    ag = {m: int(sum(rank_pos[m][n] <= 10 for n in key)) for m in MODELS if m != "random_control"}
    cands.append(dict(numbers=list(key), generating_methods=meths, walkforward_backtest_vs_random_0947=bt,
        models_count_of_ticket_numbers_in_their_top10=ag,
        mean_rank={m: round(float(np.mean([rank_pos[m][n] for n in key])), 1) for m in ["freq_all", "ewma_0.9", "freq_w10", "trend_20v20", "overdue_gap", "pair_last"]},
        recent_last10_appearances=[int(H[-10:, n].sum()) for n in c0], long_term_appearances_169=[int(H[:, n].sum()) for n in c0],
        current_gaps=[int(g[n]) for n in c0], repeats_from_2339=int(sum(n in D[-1] for n in key)),
        internal_pair_log_lift=round(float(sum(np.log(L[a, b]) for a in c0 for b in c0 if a < b)), 3),
        structure=dict(sum=int(sum(key)), sum_z=round((sum(key)-smean)/ssd, 2), odd=int(sum(n % 2 for n in key)),
                       low_1_19=int(sum(n <= 19 for n in key)), range=int(key[-1]-key[0]), consecutive_pairs=int(sum(b-a == 1 for a, b in zip(key, key[1:])))),
        expected_matches_under_uniform=round(36/38, 4)))
order = np.random.default_rng(SEED+99).permutation(len(cands))   # seeded presentation order (limits order artifacts)
cands = [cands[i] for i in order]
for i, c in enumerate(cands): c["id"] = f"C{i+1:02d}"
common = dict(validated_edge=A["gate"]["validated_edge"], gate_rule=A["gate"]["rule"],
    randomness_tests_min_holm_p=min(v["p_holm"] for v in A["randomness_tests"]["tests"].values()),
    best_single_ticket_method_mean=float(tks["mean"].max()), best_of_22_random_strategies_median=A["random_control_sim"]["best_of_M_mean_q50"],
    random_ticket_expected_matches=36/38, P_3plus_random=A["baseline"]["P3plus"], walkforward_targets=A["walkforward"]["n_targets"],
    ewma_decay_sensitivity_pool8_mean=sens, pool8_random_expectation=48/38,
    note_2339="Prior ticket 01-04-13-14-24-38 hit 3/6; P(>=3 | random ticket)=0.0387; one observation, not evidence of skill.")
json.dump(dict(common_context=common, candidates=cands), open(f"{OUT}/candidate_evidence.json", "w"), indent=1)
print(json.dumps(common, indent=1)); print(len(cands))
for c in cands: print(c["id"], c["numbers"], c["generating_methods"], c["structure"])
print(rk_tab.sort_values("ensemble_eq").head(12).T.to_string())
