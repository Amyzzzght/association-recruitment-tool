"""需求 2：校验与清洗。

校验规则：
1. 学号必须是纯数字
2. 邮箱必须是 学号@smbu.edu.cn
3. 同一学号出现多次视为重复报名（保留首次出现，其余标记为重复）

不修改原文件；问题行单独导出为「问题清单」，并注明原因。
"""

from __future__ import annotations

import re

import pandas as pd

# 学号：纯数字（不限制位数，位数假设见 README）
STUDENT_ID_PATTERN = re.compile(r"^\d+$")

# 邮箱域名
EMAIL_DOMAIN = "smbu.edu.cn"

# 问题清单中新增的原因列名
REASON_COLUMN = "问题原因"


def _validate_row(row: pd.Series) -> list[str]:
    """对单行进行独立校验，返回问题原因列表（空列表表示该行无独立校验问题）。"""
    reasons: list[str] = []
    student_id = row.get("学号")
    email = row.get("邮箱")

    # 学号为空
    if pd.isna(student_id) or str(student_id).strip() == "":
        reasons.append("学号为空")
    elif not STUDENT_ID_PATTERN.match(str(student_id).strip()):
        reasons.append("学号不是纯数字")

    # 邮箱校验
    if pd.isna(email) or str(email).strip() == "":
        reasons.append("邮箱为空")
    elif not pd.isna(student_id) and str(student_id).strip() != "":
        expected_email = f"{str(student_id).strip()}@{EMAIL_DOMAIN}"
        if str(email).strip() != expected_email:
            reasons.append(f"邮箱与学号不匹配（应为 {expected_email}）")

    return reasons


def validate_and_clean(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """校验并清洗数据。

    返回：
        clean_df: 通过所有校验的干净数据
        problems_df: 有问题的行，附带「问题原因」列
    """
    df = df.copy()

    # 1. 逐行独立校验
    reasons_per_row: list[list[str]] = []
    for _, row in df.iterrows():
        reasons_per_row.append(_validate_row(row))

    # 2. 学号重复检测：同一学号出现多次，除首次外均标记为「学号重复」
    seen_ids: dict[str, int] = {}
    for idx, row in df.iterrows():
        sid = row.get("学号")
        if pd.isna(sid) or str(sid).strip() == "":
            continue
        sid_str = str(sid).strip()
        if sid_str in seen_ids:
            reasons_per_row[idx].append("学号重复")
        else:
            seen_ids[sid_str] = idx

    # 组装原因字符串
    reason_strings = ["；".join(r) if r else "" for r in reasons_per_row]

    # 3. 拆分干净数据与问题数据
    problem_mask = [bool(r) for r in reason_strings]
    clean_df = df.loc[[not p for p in problem_mask]].copy()

    problems_df = df.loc[problem_mask].copy()
    problems_df[REASON_COLUMN] = [r for r, p in zip(reason_strings, problem_mask) if p]

    return clean_df, problems_df


def print_validation_summary(problems_df: pd.DataFrame, total_rows: int) -> None:
    """打印校验摘要。"""
    problem_count = len(problems_df)
    print()
    print("=" * 50)
    print("【校验结果】")
    print("=" * 50)
    print(f"总行数：{total_rows}")
    print(f"问题行数：{problem_count}")
    print(f"干净行数：{total_rows - problem_count}")
    if problem_count > 0:
        print()
        print("问题原因分布：")
        # 拆分多行原因统计
        all_reasons: list[str] = []
        for reasons in problems_df[REASON_COLUMN]:
            all_reasons.extend(reasons.split("；"))
        reason_counts: dict[str, int] = {}
        for r in all_reasons:
            reason_counts[r] = reason_counts.get(r, 0) + 1
        for reason, cnt in sorted(reason_counts.items(), key=lambda x: -x[1]):
            print(f"  - {reason}: {cnt}")
    print("=" * 50)
