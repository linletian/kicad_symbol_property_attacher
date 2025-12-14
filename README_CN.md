# KiCAD 符号属性批量附加工具

一个用于在 KiCAD v9.x `.kicad_sym` 库中，为所有 Symbol 批量添加指定 Property 的命令行工具；保持 S 表达式有效性与格式；跨平台，支持生成 Markdown 报告以及安全更新工作流。

## 功能特性
- 为缺少该属性的 Symbol 添加属性；不覆盖同名已存在属性
- 若已有同名但不同值，跳过且不重复添加
- 输出到新文件，或省略 `--output` 时默认写回输入（保存前创建原始备份，使用递增命名）
- 支持 dry-run 预览统计与报告，不写文件
- Markdown 报告含错误/警告高亮与跳过的 Symbol 列表
- 支持一次添加多个属性（重复传入 `--property-name`），`--property-value` 可省略，默认空字符串并应用到所有属性名

## 安装（开发环境示例）
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install click==8.1.* sexpdata==0.0.3 pytest==8.* pytest-cov==5.* ruff==0.6.* black==24.* mypy==1.11.*
```

## 用法
```bash
# 显式输出到新文件
kicad-sym-prop attach \
  --input path/to/lib.kicad_sym \
  --property-name SzlcscCode \
  # --property-value 可省略，默认空字符串
  --output path/to/lib.out.kicad_sym \
  --report path/to/lib.out.report.md

# 省略 --output：默认写回输入（保存前在同目录创建原始备份，命名为 .orig, .orig.1, ...）
kicad-sym-prop attach \
  --input path/to/lib.kicad_sym \
  --property-name SzlcscCode \
  --report path/to/lib.kicad_sym.report.md

# dry-run：不写文件，仍生成报告
kicad-sym-prop attach \
  --input path/to/lib.kicad_sym \
  --property-name SzlcscCode \
  --dry-run \
  --report path/to/lib.kicad_sym.report.md

# 多属性一次添加（--property-name 可重复；--property-value 作用于全部属性，默认空）
kicad-sym-prop attach \
  --input path/to/lib.kicad_sym \
  --property-name SzlcscCode \
  --property-name SzlcscPriceRef \
  --property-name SzlcscLink \
  --report path/to/lib.kicad_sym.report.md
```

### 属性块格式（KiCAD 校验通过）
工具插入完整的多行属性块，保持缩进与换行风格：

```text
(property "SzlcscCode" ""
  (at 0 0 0)
  (effects
    (font
      (size 1.27 1.27)
    )
    (hide yes)
  )
)
```

## 报告示例
```markdown
# Attachment Report
**Input**: `tests/fixtures/kicad_v9/official-basic-no-prop-SzlcscCode.kicad_sym`  
**Output**: `out/basic-added.kicad_sym`
**Timestamp**: `2025-12-13 10:08:42`

## Summary
- Processed: **117**
- Added: **116**
- Skipped: **1**

## Errors
- None

## Warnings
- None

## Skipped Symbols (already had property)
- `X1224WRS-02-LPV01`
```

## 失败路径示例
当输入为非法 S 表达式或无写权限时，CLI 会返回非零并仍然写出报告：
```text
Error: Failed to parse S-expression: unexpected token near line 42
```
报告中包含错误列表与零统计。

## 说明
- KiCAD v9.x 可正常加载输出文件，无警告/错误。
- 编码：UTF-8；行尾风格保持一致。
- 省略 `--output` 时，默认写回输入路径；在同目录创建不覆盖的递增原始备份（`.orig`, `.orig.1`, ...）。
- 省略 `--report` 时，会在目标文件同目录生成带时间戳的报告。
- 详见 `specs/001-kicad-symbol-property/` 获取完整规范与任务。

## 版本发布
- 当前：`v0.1.2` — 支持多属性一次添加；省略 `--report` 默认生成报告；文档与规范已更新；测试通过。
- 历史：`v0.1.0` — US1/US2/US3 完成；质量门（ruff、black、mypy、pytest）在 macOS 通过。
- 变更记录：见 `CHANGELOG.md`。

## 依赖
参见 `docs/dependencies.md` 获取版本钉住与 LTS 说明。

## 硬件相关
N/A（纯软件）；参见 `docs/hardware-adjustment.md`。
