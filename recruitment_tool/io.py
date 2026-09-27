"""CSV 读写工具。"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# 报名表的标准字段（顺序固定）
EXPECTED_COLUMNS = ["姓名", "学号", "邮箱", "志愿1", "志愿2", "推荐人"]


def read_csv(path: str | Path) -> pd.DataFrame:
    """读入报名表 CSV。

    所有列按字符串读取，避免学号等被自动转成数字后丢失前导零或精度。
    空字符串统一视为缺失值（NaN）。
    """
    df = pd.read_csv(path, dtype=str, keep_default_na=True, na_values=[""])
    return df


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    """写出 CSV（UTF-8 with BOM，方便 Excel 直接打开中文不乱码）。"""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, encoding="utf-8-sig")
