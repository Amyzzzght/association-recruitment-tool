# 协会招新数据处理小工具

处理协会每年招新从问卷导出的 CSV 报名表，一站式完成 **概览 → 校验清洗 → 统计导出** 三步处理。

## 功能

| 步骤 | 需求 | 说明 |
|------|------|------|
| 1. 读入与概览 | 打印总行数、每列空值数、完全重复行 | 不修改原文件 |
| 2. 校验与清洗 | 学号纯数字校验、邮箱匹配校验、重复报名检测 | 问题行单独导出「问题清单」并注明原因 |
| 3. 统计与导出 | 按第一志愿分组、双/单志愿人数统计、导出干净数据 | 输出汇总表 + 干净 CSV |

## 环境要求

- Python 3.8+
- pandas >= 2.0

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py <报名表.csv> [--output-dir ./output]
```

示例（使用项目自带的测试数据）：

```bash
python main.py sample_data/sample.csv
```

运行后终端会依次打印：数据概览、校验结果、统计结果。

## 输入 CSV 字段

报名表需包含以下列（列名需完全一致，顺序任意）：

| 字段 | 说明 |
|------|------|
| 姓名 | 报名人姓名 |
| 学号 | 纯数字 |
| 邮箱 | 应为 `学号@smbu.edu.cn` |
| 志愿1 | 第一志愿部门 |
| 志愿2 | 第二志愿部门（可空） |
| 推荐人 | 推荐人（可空） |

## 输出文件

运行后会在输出目录（默认 `./output`）生成以下文件：

| 文件 | 说明 |
|------|------|
| `问题清单.csv` | 校验未通过的行，附带「问题原因」列 |
| `第一志愿汇总.csv` | 按志愿1 分组的人数汇总表 |
| `干净数据.csv` | 通过全部校验的干净数据 |

## 校验规则与假设

> 拿不准的边界情况在此明确假设，如有出入可按实际修改 `recruitment_tool/validator.py`。

1. **学号**：必须是纯数字（正则 `^\d+$`）。**不限制位数**——不假设学号固定为 8 位或 10 位，只要求全部为数字，以兼容不同年级/学制。
2. **邮箱**：必须等于 `<学号>@smbu.edu.cn`。域名固定为 `smbu.edu.cn`，邮箱前缀必须与学号完全一致。
3. **重复报名**：同一学号出现多次视为重复。处理策略：**保留首次出现的行**，其余行标记为「学号重复」并进入问题清单。如果首次出现的行本身还有其他问题（如邮箱错误），则该行也会进入问题清单，该学号最终不会出现在干净数据中。
4. **完全重复行**：所有字段都相同的行。仅在概览中统计提示，不作为清洗依据（清洗依据是学号）。
5. **空值**：CSV 中的空单元格视为缺失值。学号为空 → 问题；邮箱为空 → 问题；志愿/推荐人为空是允许的。
6. **CSV 编码**：读入兼容 UTF-8；写出使用 UTF-8 with BOM（`utf-8-sig`），方便 Excel 直接打开中文不乱码。
7. **数据类型**：所有列按字符串读入，避免学号被自动转成数字后丢失前导零。

## 项目结构

```
.
├── main.py                      # CLI 入口，串联三步处理
├── requirements.txt             # 依赖
├── sample_data/
│   └── sample.csv               # 测试数据（含各种边界情况）
├── recruitment_tool/
│   ├── __init__.py
│   ├── io.py                    # CSV 读写
│   ├── overview.py              # 需求1：概览
│   ├── validator.py             # 需求2：校验与清洗
│   └── statistics.py            # 需求3：统计与导出
└── README.md
```

## 测试数据说明

`sample_data/sample.csv` 共 9 行，故意包含以下问题，可用于验证工具：

- `abc001004`：学号非纯数字
- `wrong@smbu.edu.cn`：邮箱与学号不匹配
- `2021001001` 出现 3 次：重复报名
- 最后一行与第一行完全相同：完全重复行
- 志愿1 / 志愿2 / 推荐人各有空值

## 开发：三次提交（PR）

本项目按需求拆分为三个独立分支，对应三次 PR：

| 分支 | 对应需求 | 说明 |
|------|----------|------|
| `feature/req1-overview` | 需求1 | 读入与概览 |
| `feature/req2-validation` | 需求2 | 校验与清洗 |
| `feature/req3-statistics` | 需求3 | 统计与导出 |

推送到 GitHub 后，可基于这三个分支分别向 `main` 发起 Pull Request。

### 推送到 GitHub 并创建 PR

```bash
# 1. 在 GitHub 上新建一个空仓库（不要勾选 README/LICENSE），假设地址为：
#    https://github.com/<你的用户名>/association-recruitment-tool.git

# 2. 添加远程仓库
git remote add origin https://github.com/<你的用户名>/association-recruitment-tool.git

# 3. 推送 main 分支及三个 feature 分支
git push -u origin main
git push origin feature/req1-overview
git push origin feature/req2-validation
git push origin feature/req3-statistics

# 4. 在 GitHub 网页上分别为三个 feature 分支创建 Pull Request（base: main）
```

三个 PR 对应：

1. `feature/req1-overview` → `main`：需求 1 读入与概览
2. `feature/req2-validation` → `main`：需求 2 校验与清洗
3. `feature/req3-statistics` → `main`：需求 3 统计与导出

