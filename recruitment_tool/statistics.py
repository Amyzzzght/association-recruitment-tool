"""需求 3：统计与导出。

- 按第一志愿（志愿1）分组统计人数
- 统计两个志愿都填了 / 只填一个的人数
- 导出清洗后的干净数据为新 CSV
"""

from __future__ import annotations

import pandas as pd


def group_by_first_choice(clean_df: pd.DataFrame) -> pd.DataFrame:
    """按志愿1分组统计人数。

    空的志愿1 归入「未填写」。
    """
    df = clean_df.copy()
    df["志愿1"] = df["志愿1"].fillna("未填写")
    summary = (
        df.groupby("志愿1", dropna=False)
        .size()
        .reset_index(name="人数")
        .sort_values("人数", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def count_volunteer_filled(clean_df: pd.DataFrame) -> dict[str, int]:
    """统计志愿填写情况。

    返回：
        both: 志愿1 和 志愿2 都填了的人数
        only_one: 只填了其中一个的人数
        none: 两个都没填的人数
    """
    v1_filled = clean_df["志愿1"].notna()
    v2_filled = clean_df["志愿2"].notna()

    both = int((v1_filled & v2_filled).sum())
    only_one = int((v1_filled ^ v2_filled).sum())
    none = int((~v1_filled & ~v2_filled).sum())

    return {"both": both, "only_one": only_one, "none": none}


def print_statistics(
    first_choice_summary: pd.DataFrame, volunteer_stats: dict[str, int]
) -> None:
    """打印统计结果。"""
    print()
    print("=" * 50)
    print("【统计结果】")
    print("=" * 50)

    print("按第一志愿分组人数：")
    print(first_choice_summary.to_string(index=False))
    print()

    total = sum(volunteer_stats.values())
    print("志愿填写情况（基于干净数据）：")
    print(f"  - 两个志愿都填了：{volunteer_stats['both']} 人")
    print(f"  - 只填了一个志愿：{volunteer_stats['only_one']} 人")
    print(f"  - 两个都没填：{volunteer_stats['none']} 人")
    print(f"  - 合计：{total} 人")
    print("=" * 50)
