"""Step 2: exact random baseline for one 6-number ticket and for top-k pools (hypergeometric)."""
import math
import os
from fractions import Fraction

from common import K_DRAW, N_BALLS, OUT, pool_pmf, write_json


def main():
    total = math.comb(N_BALLS, K_DRAW)
    ticket = {}
    for k in range(7):
        ways = math.comb(K_DRAW, k) * math.comb(N_BALLS - K_DRAW, K_DRAW - k)
        fr = Fraction(ways, total)
        ticket[str(k)] = {"ways": ways, "fraction": f"{fr.numerator}/{fr.denominator}", "probability": ways / total,
                          "one_in": total / ways}
    pmf = pool_pmf(6)
    expected = sum(k * p for k, p in enumerate(pmf))
    var = sum((k - expected) ** 2 * p for k, p in enumerate(pmf))
    tails = {f"P({m}+)": float(pmf[m:].sum()) for m in range(1, 7)}
    pools = {}
    for m in (6, 8, 10, 12, 15, 20):
        p = pool_pmf(m)
        e = sum(k * q for k, q in enumerate(p))
        pools[str(m)] = {"expected_winners_captured": e, "pmf": {str(k): float(q) for k, q in enumerate(p)},
                         **{f"P({j}+)": float(p[j:].sum()) for j in (3, 4, 5, 6)}}
    out = {
        "total_combinations": total,
        "single_ticket": ticket,
        "expected_matches_per_ticket": expected,
        "expected_matches_exact": "36/38 = 18/19",
        "variance_matches": var,
        "sd_matches": math.sqrt(var),
        "tails": tails,
        "jackpot_probability": 1 / total,
        "top_k_pool_baselines": pools,
    }
    write_json(os.path.join(OUT, "02_exact_baseline.json"), out)
    for k, v in ticket.items():
        print(f"P({k}) = {v['fraction']:>22} = {v['probability']:.8f}  (1 in {v['one_in']:.2f})")
    print("E[matches] =", expected, " sd =", math.sqrt(var))
    print(tails)
    for m, v in pools.items():
        print(m, round(v["expected_winners_captured"], 4), {k: round(v[k], 5) for k in ("P(3+)", "P(4+)", "P(5+)", "P(6+)")})


if __name__ == "__main__":
    main()
