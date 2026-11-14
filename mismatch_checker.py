"""Catalog Mismatch Checker: compares 1P vs 3P item data and flags mismatches by type."""
import re
import pandas as pd

FIELDS = ["title", "brand", "color", "price"]
PRICE_TOLERANCE = 0.01  # differences smaller than this are ignored


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def run(p1_path="retailer_1p.csv", p3_path="seller_3p.csv"):
    p1, p3 = pd.read_csv(p1_path), pd.read_csv(p3_path)
    df = p1.merge(p3, on="item_id", how="outer", suffixes=("_1p", "_3p"), indicator=True)

    missing_in_3p = df[df["_merge"] == "left_only"]
    missing_in_1p = df[df["_merge"] == "right_only"]
    both = df[df["_merge"] == "both"].copy()

    for f in FIELDS:
        if f == "price":
            both[f"{f}_mismatch"] = (both["price_1p"] - both["price_3p"]).abs() > PRICE_TOLERANCE
        else:
            both[f"{f}_mismatch"] = both[f"{f}_1p"].map(norm) != both[f"{f}_3p"].map(norm)

    flags = [f"{f}_mismatch" for f in FIELDS]
    both["mismatch_count"] = both[flags].sum(axis=1)
    both["mismatch_types"] = both[flags].apply(
        lambda r: ", ".join(f.replace("_mismatch", "") for f in flags if r[f]), axis=1)
    bad = both[both["mismatch_count"] > 0]

    by_type = both[flags].sum().rename(lambda x: x.replace("_mismatch", "")).reset_index()
    by_type.columns = ["Mismatch Type", "Count"]
    by_type["% of matched items"] = (by_type["Count"] / len(both) * 100).round(1)

    by_cat = both.groupby("category_1p").agg(items=("item_id", "count"),
                                              mismatched=("mismatch_count", lambda s: (s > 0).sum())).reset_index()
    by_cat["mismatch_rate_%"] = (by_cat["mismatched"] / by_cat["items"] * 100).round(1)
    by_cat.columns = ["Category", "Items Checked", "Items With Mismatch", "Mismatch Rate %"]

    summary = {
        "Items in 1P catalog": len(p1),
        "Items in 3P catalog": len(p3),
        "Matched on item ID": len(both),
        "Items with 1+ mismatch": len(bad),
        "Catalog accuracy %": round((1 - len(bad) / len(both)) * 100, 1),
        "In 1P but missing in 3P": len(missing_in_3p),
        "In 3P but not in 1P": len(missing_in_1p),
    }
    detail_cols = ["item_id", "category_1p", "mismatch_types"] + \
        [c for f in FIELDS for c in (f"{f}_1p", f"{f}_3p")]
    return summary, by_type, by_cat, bad[detail_cols], missing_in_3p[["item_id", "title_1p"]], missing_in_1p[["item_id", "title_3p"]]


if __name__ == "__main__":
    summary, by_type, by_cat, bad, m3, m1 = run()
    print(pd.Series(summary).to_string())
    print("\n", by_type.to_string(index=False))
    print("\n", by_cat.to_string(index=False))
