#!/usr/bin/env python3
"""协会招新数据处理小工具 - CLI 入口。

用法：
    python main.py <报名表.csv> [--output-dir ./output]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from recruitment_tool.io import read_csv, write_csv
from recruitment_tool.overview import generate_overview, print_overview
from recruitment_tool.validator import validate_and_clean, print_validation_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="协会招新数据处理小工具")
    parser.add_argument("input", type=str, help="报名表 CSV 文件路径")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="输出目录（默认 ./output）",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 读入数据
    df = read_csv(input_path)
    print(f"已读入文件：{input_path}")

    # 需求 1：概览
    overview = generate_overview(df)
    print_overview(overview)

    # 需求 2：校验与清洗
    clean_df, problems_df = validate_and_clean(df)
    print_validation_summary(problems_df, len(df))

    # 导出问题清单（不修改原文件）
    problems_path = output_dir / "问题清单.csv"
    write_csv(problems_df, problems_path)
    print(f"\n问题清单已导出：{problems_path}")


if __name__ == "__main__":
    main()
