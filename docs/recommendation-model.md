# Smartphone scoring

The illustrative ranking uses PHP price as a cost and battery capacity in mAh as a benefit. A hard filter is inclusive. Unknown specifications fail a requirement on that field. Each excluded phone carries the first unmet requirement or the missing-data reason.

Only records with complete scored fields enter the ranges. For eligible minimum L, maximum H, and raw value x, price uses (H − x) / (H − L) and capacity uses (x − L) / (H − L). A constant field contributes nothing and is omitted before the remaining weights are rescaled. If the remaining weights sum to zero, another input is required.

Each contribution is the normalized value multiplied by the effective weight. The sum is ranked in descending order at full precision. Scores within 0.000001 of the leader of a tie group share the same competition rank, with alphabetical display inside the group. Two-decimal display can hide small differences between distinct ranks.

The three scenarios reuse the same normalized values. The equal-weight baseline assigns 1/m to each of m active criteria. In each focused scenario, price or performance receives 0.60 and the others divide 0.40 equally. A focus needs at least two active criteria including its focus measure. The current example catalog lacks comparable benchmark records, so the performance scenario is not assessable.

See [thesis alignment](THESIS_ALIGNMENT.md) for data limits and verification.
