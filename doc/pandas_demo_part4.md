# Pandas Part-4 示例脚本说明

本示例脚本位于 `quant/pandas_demo/part4_demo.py`，展示了博客
《[Introduction to Pandas Part 4](https://wqu.guru/blog/quantopia-quantitative-analysis-56-lectures/introduction-to-pandas-part-4)》
中的核心操作，并辅以中文注释解析底层公式与 API 行为。

## 运行方法

# 方式一：在项目根目录执行

uv run -m quant.pandas_demo.part4_demo

# 方式二：直接运行脚本

uv run quant/pandas_demo/part4_demo.py

## 主要演示内容

1. **时间序列构造**：`pd.date_range` 生成日期索引。
2. **收益率计算**：`pct_change()` 对应公式 \( r*t = (P_t/P*{t-1}) - 1 \)。
3. **移动平均**：`rolling(window).mean()`，公式 \( MA*t^{(n)} = \frac{1}{n}\sum*{i=0}^{n-1}P\_{t-i}\)。
4. **布尔过滤**：利用布尔掩码提取满足条件的行。
5. **`loc` / `iloc`**：标签与位置索引取值对比。
6. **`shift`**：序列平移实现前后期比较。

## 输出示例

运行后将打印：

- 带有 `return`、`ma_3`、`prev_close`、`close_change` 等计算列的完整 DataFrame。
- 收盘价大于 100 的筛选结果。
- `loc` 与 `iloc` 取值示范。

通过这些示例可快速理解 Part-4 中关于索引与子集选择、滚动窗口以及
时间序列移位等高频用法。
