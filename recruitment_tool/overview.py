"""需求 1：读入与概览。"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Overview:
    """数据概览结果。"""

    total_rows: int
    null_counts: dict[str, int]
    duplicate_row_count: int  # 完全重复的行数（即出现次数 > 1 的行所多出来的条数）
    duplicate_row_groups: int = 0  # 有多少组不同的完全重复行


def generate_overview(df: pd.DataFrame) -> Overview:
    """计算概览信息。"""
    total_rows = len(df)

    # 每列空值数量
    null_counts = {col: int(df[col].isna().sum()) for col in df.columns}

    # 完全重复行：所有字段都相同的行
    # keep=False 把所有重复行都标记为 True
    dup_mask = df.duplicated(keep=False)
    duplicate_row_groups = int(df[dup_mask].drop_duplicates().shape[0])
    # 重复行数 = 总行数中属于重复组的行数 - 去重后的组数
    duplicate_row_count = int(dup_mask.sum()) - duplicate_row_groups if duplicate_row_groups else 0

    return Overview(
        total_rows=total_rows,
        null_counts=null_counts,
        duplicate_row_count=duplicate_row_count,
        duplicate_row_groups=duplicate_row_groups,
    )


def print_overview(overview: Overview) -> None:
    """打印概览信息。"""
    print("=" * 50)
    print("【数据概览】")
    print("=" * 50)
    print(f"总行数：{overview.total_rows}")
    print()
    print("各列空值数量：")
    for col, cnt in overview.null_counts.items():
        print(f"  - {col}: {cnt}")
    print()
    if overview.duplicate_row_count > 0:
        print(
            f"存在完全重复的行：共 {overview.duplicate_row_count} 行 "
            f"（涉及 {overview.duplicate_row_groups} 组重复）"
        )
    else:
        print("不存在完全重复的行。")
    print("=" * 50)
