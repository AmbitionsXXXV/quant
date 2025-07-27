"""pandas Part-4 示例演示

该脚本演示了 Pandas 在数据索引、子集选择、布尔过滤、
时间序列计算等常用操作的用法，代码取材自
https://wqu.guru/blog/quantopia-quantitative-analysis-56-lectures/introduction-to-pandas-part-4
中的案例，并在关键步骤补充了底层公式解释。

运行方式：
    uv -m quant.pandas_demo.part4_demo

适合初学者：本文档从基础概念开始，逐步深入到高级应用
建议学习顺序：
1. 先理解 Series 和 DataFrame 的基本概念
2. 掌握索引和切片操作
3. 学习缺失值处理
4. 了解时间序列操作
5. 最后学习滚动窗口等高级功能
"""

import numpy as np
import pandas as pd

# --------------------------- 第一部分：基础概念和数据创建 ---------------------------

print("=" * 60)
print("第一部分：基础概念和数据创建")
print("=" * 60)

# 什么是 Series？
# Series 是 pandas 的一维数据结构，类似于 Excel 中的一列数据
# 它由两部分组成：数据值（values）和索引（index）
# 可以把它想象成一个带标签的数组

# 从列表创建 Series - 最简单的方式
print("\n1. 创建简单的 Series")
print("-" * 30)

# pandas.Series 底层使用 NumPy ndarray 存储数据，提供标签化的一维数组
s = pd.Series([1, 2, np.nan, 4, 5, 6, 7, 8, 9, 10], name="Toy Series")
print("原始 Series：")
print(s)
print(f"数据类型：{s.dtype}")  # 显示数据类型，通常是 float64
print(f"长度：{len(s)}")  # 显示数据长度
print(f"索引：{s.index}")  # 显示索引，默认是 0,1,2...

# 注意：np.nan 表示缺失值（Not a Number），在金融数据中很常见
# 比如某天股市休市，就没有价格数据

print("\n2. 设置时间索引")
print("-" * 30)

# 时间索引是金融数据分析的核心概念
# pd.date_range 生成连续的日期序列，就像日历一样
# freq="D" 表示每日频率（Daily），还可以用 "H"（小时）、"M"（分钟）等
# periods=10 生成 10 个连续日期
date_index = pd.date_range("2025-01-01", periods=10, freq="D")
print("生成的日期索引：")
print(date_index)

# 将日期索引赋给 Series
s.index = date_index
print("\n带时间索引的 Series：")
print(s)

# 现在每个数据点都有了对应的日期标签，就像股票的每日收盘价一样

# --------------------------- 第二部分：数据访问和切片 ---------------------------

print("\n" + "=" * 60)
print("第二部分：数据访问和切片")
print("=" * 60)

print("\n1. iloc - 基于位置的索引（类似数组下标）")
print("-" * 40)

# iloc 基于整数位置的索引，底层直接访问 ndarray 的指定位置
# 就像访问列表元素一样：list[0] 获取第一个元素
print("第一个元素（位置0）：", s.iloc[0])  # 结果：1.0
print("最后一个元素：", s.iloc[-1])  # 结果：10.0

# iloc 切片操作：s.iloc[1:4] 返回位置 1,2,3 的元素（不包括位置 4）
# 这和 Python 列表切片规则完全一样
print("位置1到3的元素：")
print(s.iloc[1:4])
# 输出：
# 2025-01-02    2.0
# 2025-01-03    NaN
# 2025-01-04    4.0

print("\n2. loc - 基于标签的索引（使用日期标签）")
print("-" * 40)

# loc 基于标签的索引，通过日期标签定位数据
# 在金融分析中更常用，因为我们通常关心"某个具体日期"的数据
print("2025年1月2日的值：", s.loc["2025-01-02"])  # 结果：2.0

# loc 切片：包含起始和结束标签的所有数据
# 注意：与 iloc 不同，loc 切片是包含结束标签的
print("2025-01-02 到 2025-01-04 的数据：")
print(s.loc["2025-01-02":"2025-01-04"])
# 输出：
# 2025-01-02    2.0
# 2025-01-03    NaN
# 2025-01-04    4.0

# 小技巧：记忆方法
# iloc：i = integer（整数），用数字位置
# loc：l = label（标签），用标签名称

# --------------------------- 第三部分：缺失值处理 ---------------------------

print("\n" + "=" * 60)
print("第三部分：缺失值处理")
print("=" * 60)

print("\n1. 检查缺失值")
print("-" * 20)

# 在真实数据中，缺失值很常见：停牌股票、节假日、数据错误等
print("是否有缺失值：", s.isnull().any())  # True 表示有缺失值
print("缺失值个数：", s.isnull().sum())  # 统计缺失值数量
print("缺失值位置：")
print(s.isnull())  # 显示每个位置是否为缺失值

print("\n2. 填充缺失值 - fillna() 方法")
print("-" * 30)

# fillna() 填充缺失值，有多种策略：
# 1. 用均值填充（适合数值数据）
print("原始数据的均值：", s.mean())  # 自动忽略 NaN 计算均值

# s.mean() 计算均值时自动忽略 NaN 值
# 底层逻辑：对于每个 NaN 位置，用计算得到的均值替换
s_filled = s.fillna(s.mean())
print("用均值填充后：")
print(s_filled)

# 其他填充方法示例：
print("\n其他常用填充方法：")
print("向前填充（用前一个有效值）：")
print(s.fillna(method="ffill"))  # forward fill

print("向后填充（用后一个有效值）：")
print(s.fillna(method="bfill"))  # backward fill

print("用固定值填充：")
print(s.fillna(0))  # 用 0 填充

print("\n3. 删除缺失值 - dropna() 方法")
print("-" * 30)

# dropna() 删除包含缺失值的行/列
# 底层逻辑：创建布尔掩码，标记非 NaN 位置，返回过滤后的数据
s_dropped = s.dropna()
print("删除缺失值后：")
print(s_dropped)
print(f"原始长度：{len(s)}，删除后长度：{len(s_dropped)}")

# 注意：删除数据会永久丢失信息，填充数据可能引入偏差
# 选择哪种方法取决于具体业务场景

# --------------------------- 第四部分：时间序列操作 ---------------------------

print("\n" + "=" * 60)
print("第四部分：时间序列操作")
print("=" * 60)

print("\n1. 重采样 - resample() 方法")
print("-" * 30)

# 时间序列重采样 - resample() 按指定频率重新组织数据
# 就像把日数据汇总成月数据，或者把分钟数据汇总成小时数据

# "ME" 表示按月末重采样（Month End，替代已弃用的"M"）
# mean() 对每月的数据计算平均值
# 底层逻辑：根据时间索引将数据分组，对每组应用聚合函数
monthly_data = s.resample("ME").mean()
print("按月重采样（月平均值）：")
print(monthly_data)

# 其他重采样频率示例：
print("按周重采样：")
print(s.resample("W").mean())

# 重采样的金融应用：
# - 日数据 → 周数据：计算周收益率
# - 分钟数据 → 日数据：计算日内波动
# - 小时数据 → 4小时数据：多时间框架分析

print("\n2. 时区处理")
print("-" * 20)

# 全球金融市场涉及多个时区，时区处理很重要
print("原始数据（无时区）：")
print(s.index)

# tz_localize() 为无时区数据添加时区信息
# 就像给数据贴上"这是UTC时间"的标签
s_utc = s.tz_localize("UTC")
print("本地化为UTC时区后：")
print(s_utc.index)

# tz_convert() 在已有时区数据间进行转换
# 就像把UTC时间转换成纽约时间
s_eastern = s_utc.tz_convert("US/Eastern")
print("转换为美东时区后：")
print(s_eastern.index)

# 实际应用：如果你在中国分析美股，需要处理时区差异

# --------------------------- 第五部分：DataFrame 操作 ---------------------------

print("\n" + "=" * 60)
print("第五部分：DataFrame 操作")
print("=" * 60)

print("\n1. 创建 DataFrame")
print("-" * 20)

# DataFrame 是什么？
# DataFrame 是二维数据结构，类似于 Excel 表格或数据库表
# 可以看作是多个 Series 的集合，每列是一个 Series，共享行索引

# DataFrame 创建 - 底层为多个 Series 的集合，共享行索引
data = {
    "A": np.random.randn(5),  # 标准正态分布随机数（模拟股票收益率）
    "B": ["X", "Y", "Z", "W", "V"],  # 字符串数据（模拟股票代码）
    "C": pd.date_range("2025-01-01", periods=5),  # 日期序列
}
df = pd.DataFrame(data)
print("创建的 DataFrame：")
print(df)
print(f"形状（行数，列数）：{df.shape}")
print(f"列名：{df.columns.tolist()}")
print(f"数据类型：\n{df.dtypes}")

print("\n2. 添加和删除列")
print("-" * 20)

# 新增计算列 - 向量化操作，底层使用 NumPy 的广播机制
# df["A"] * 2 对整列进行标量乘法，比 for 循环快数百倍
print("添加计算列 D = A * 2：")
df["D"] = df["A"] * 2
print(df[["A", "D"]])  # 只显示相关列

# 更多计算列示例：
df["A_squared"] = df["A"] ** 2  # 平方
df["A_abs"] = df["A"].abs()  # 绝对值
print("添加更多计算列后：")
print(df[["A", "A_squared", "A_abs"]])

# 删除列 - axis=1 表示按列删除（axis=0 为按行删除）
print("\n删除列 B 和多余的计算列：")
df = df.drop(["B", "A_squared", "A_abs"], axis=1)
print(df)

# 记忆技巧：axis=0 想象成垂直方向（行），axis=1 想象成水平方向（列）

print("\n3. 数据筛选和布尔索引")
print("-" * 25)

# 布尔索引 - 创建布尔掩码进行数据筛选
# 这是数据分析中最重要的技能之一

# 第一步：创建条件
condition = df["A"] > 0
print("条件 'A > 0' 的结果：")
print(condition)  # True/False 的 Series

# 第二步：应用条件筛选
# df["A"] > 0 生成布尔 Series，True 对应保留的行
filtered = df[condition]
print("筛选 A 列正值的行：")
print(filtered)

# 复杂条件示例：
print("\n复杂筛选条件示例：")
# 多条件组合（注意使用括号和 &、| 运算符）
complex_filter = df[(df["A"] > 0) & (df["D"] < 1)]
print("A > 0 且 D < 1 的行：")
print(complex_filter)

# 常用筛选模式：
print("其他常用筛选：")
print("A列最大值所在行：")
print(df[df["A"] == df["A"].max()])

print("A列前50%的行：")
print(df[df["A"] > df["A"].median()])

# --------------------------- 第六部分：数据合并和连接 ---------------------------

print("\n" + "=" * 60)
print("第六部分：数据合并和连接")
print("=" * 60)

print("\n1. 简单连接 - concat()")
print("-" * 25)

# DataFrame 合并 - concat() 沿指定轴连接多个对象
# 就像把两张表格拼接在一起
df1 = pd.DataFrame({"X": [1, 2], "Y": [3, 4]})
df2 = pd.DataFrame({"X": [5, 6], "Y": [7, 8]})

print("第一个 DataFrame：")
print(df1)
print("第二个 DataFrame：")
print(df2)

# 默认 axis=0（按行连接），ignore_index=False 保留原索引
combined = pd.concat([df1, df2])
print("垂直连接结果（axis=0）：")
print(combined)

# 水平连接
combined_horizontal = pd.concat([df1, df2], axis=1)
print("水平连接结果（axis=1）：")
print(combined_horizontal)

# 重置索引
combined_reset = pd.concat([df1, df2], ignore_index=True)
print("连接后重置索引：")
print(combined_reset)

# 实际应用：合并不同来源的股票数据、拼接历史数据等

# --------------------------- 第七部分：滚动窗口计算 ---------------------------

print("\n" + "=" * 60)
print("第七部分：滚动窗口计算（重要！）")
print("=" * 60)

print("\n1. 基础滚动窗口概念")
print("-" * 25)

# 什么是滚动窗口？
# 想象一个固定大小的"窗口"在数据上移动，每次计算窗口内的统计值
# 比如：30日移动平均线就是一个30天的滚动窗口

# 创建更长的时间序列用于演示
np.random.seed(42)  # 设置随机种子确保结果可重现
long_series = pd.Series(
    np.random.normal(0, 1, 50),  # 50个数据点
    index=pd.date_range("2025-01-01", periods=50, freq="D"),
)

print("原始数据（前10个）：")
print(long_series.head(10))

# 滚动窗口计算 - rolling() 创建滑动窗口对象
# window=5 表示 5 期窗口，每次计算使用最近 5 个数据点
print("\n5日滚动平均：")
rolling_5 = long_series.rolling(5).mean()
print(rolling_5.head(10))

# 注意：前4个值是NaN，因为不足5个数据点无法计算

# 滚动均值公式：MA_t = (X_t + X_{t-1} + ... + X_{t-4}) / 5
# 金融意义：平滑价格波动，识别趋势

print("\n2. 滚动统计指标")
print("-" * 20)

# 滚动标准差 - 衡量波动性
# 滚动标准差公式：σ_t = sqrt(Σ(X_i - MA_t)² / (n-1))，其中 i 从 t-4 到 t
rolling_std = long_series.rolling(5).std()
print("5日滚动标准差（前10个）：")
print(rolling_std.head(10))

# 其他有用的滚动统计：
print("5日滚动最大值：")
print(long_series.rolling(5).max().head(10))

print("5日滚动最小值：")
print(long_series.rolling(5).min().head(10))

# min_periods 参数 - 设置计算所需的最小观测数
print("\n使用 min_periods=1：")
# min_periods=1 表示即使数据不足窗口大小也进行计算
# 金融意义：在数据初期就能提供指标值，避免过多的缺失值
rolling_min_periods = long_series.rolling(5, min_periods=1).mean()
print(rolling_min_periods.head(10))
# 现在第一个值就不是NaN了

# --------------------------- 第八部分：收益率计算 ---------------------------

print("\n" + "=" * 60)
print("第八部分：收益率计算（金融核心）")
print("=" * 60)

print("\n1. 基础收益率概念")
print("-" * 20)

# 收益率是金融分析的核心概念
# 衡量投资的相对收益，消除了价格水平的影响

# 生成示例价格数据用于收益率演示
prices = pd.Series(
    [100, 105, 110, 108, 115], index=pd.date_range("2025-01-01", periods=5),
)
print("示例价格数据：")
print(prices)

print("\n2. 单期收益率计算")
print("-" * 20)

# 百分比变化率 - pct_change() 计算相邻期间的变化率
# 公式：return_t = (price_t - price_{t-1}) / price_{t-1}
# 这是金融中最基本的收益率计算方法

# 单期收益率计算 - 默认 periods=1，计算相邻期间收益率
# 公式：R_t = (P_t - P_{t-1}) / P_{t-1}
# 金融意义：衡量投资在单位时间内的相对收益
returns = prices.pct_change(fill_method=None)  # 默认计算单日收益率
print("单日收益率：")
print(returns)

# 解释结果：
# 第一天：NaN（没有前一天数据）
# 第二天：(105-100)/100 = 0.05 = 5%
# 第三天：(110-105)/105 = 0.047619 ≈ 4.76%
# 第四天：(108-110)/110 = -0.018182 ≈ -1.82%
# 第五天：(115-108)/108 = 0.064815 ≈ 6.48%

print("\n3. 多期收益率计算")
print("-" * 20)

# 多期收益率计算 - periods=3 表示计算 3 期间隔的收益率
# 公式：R_t = (P_t - P_{t-3}) / P_{t-3}
# 金融意义：衡量较长时间跨度的累积收益，常用于趋势分析
long_returns = prices.pct_change(periods=3, fill_method=None)
print("3日收益率：")
print(long_returns)

# 解释结果：
# 前3天：NaN（数据不足）
# 第4天：(108-100)/100 = 0.08 = 8%（3天累计涨8%）
# 第5天：(115-105)/105 = 0.095238 ≈ 9.52%（3天累计涨9.52%）

print("\n4. 处理收益率数据")
print("-" * 20)

# 清理缺失值 - pct_change() 第一个值为 NaN（无前期数据对比）
clean_returns = returns.dropna()
print("清理后的收益率：")
print(clean_returns)

# 收益率统计分析
print("\n收益率统计分析：")
print(f"平均收益率：{clean_returns.mean():.4f}")
print(f"收益率标准差（波动率）：{clean_returns.std():.4f}")
print(f"最大收益率：{clean_returns.max():.4f}")
print(f"最小收益率：{clean_returns.min():.4f}")

# --------------------------- 第九部分：技术指标计算 ---------------------------

print("\n" + "=" * 60)
print("第九部分：技术指标计算")
print("=" * 60)

print("\n1. 移动平均线")
print("-" * 15)

# 重新创建价格数据用于技术分析
np.random.seed(42)
# 模拟股价数据：起始价格100，随机波动
stock_price = 100 * np.cumprod(1 + np.random.normal(0.001, 0.02, 100))
stock_series = pd.Series(stock_price, index=pd.date_range("2025-01-01", periods=100))

print("股价数据（前10天）：")
print(stock_series.head(10))

# 移动平均线（MA）- 技术分析中的趋势指标
# 计算不同周期的移动平均线

# 短期移动平均（5日）
ma_5 = stock_series.rolling(5).mean()
print("\n5日移动平均（前10个）：")
print(ma_5.head(10))

# 中期移动平均（20日）
# 20日移动平均公式：MA20_t = (P_t + P_{t-1} + ... + P_{t-19}) / 20
# 金融意义：平滑价格波动，识别趋势方向，支撑/阻力位判断
ma_20 = stock_series.rolling(20).mean()

# 长期移动平均（50日）
ma_50 = stock_series.rolling(50).mean()

print("移动平均线对比（第50天）：")
print(f"股价：{stock_series.iloc[49]:.2f}")
print(f"5日均线：{ma_5.iloc[49]:.2f}")
print(f"20日均线：{ma_20.iloc[49]:.2f}")
print(f"50日均线：{ma_50.iloc[49]:.2f}")

print("\n2. 波动率指标")
print("-" * 15)

# 滚动标准差 - 衡量价格波动性的指标
# 公式：σ_20 = sqrt(Σ(P_i - MA20)² / 19)，i 从 t-19 到 t
# 金融意义：波动率指标，用于风险度量和布林带计算
volatility_20 = stock_series.rolling(20).std()
print("20日波动率（前25个，从第20个开始有效）：")
print(volatility_20.iloc[19:25])

# 年化波动率（假设一年252个交易日）
annualized_volatility = volatility_20 * np.sqrt(252)
print("年化波动率：")
print(annualized_volatility.iloc[19:25])

print("\n3. 自定义技术指标")
print("-" * 20)


# 自定义滚动函数 - apply() 允许应用自定义的聚合函数
def price_range(x):
    """自定义滚动函数：计算窗口内的价格波动幅度

    公式：(max - min) / 当前价格 * 100
    金融意义：衡量指定时间窗口内的价格波动范围，
    类似于技术分析中的真实波动幅度（ATR）的简化版本
    """
    if len(x) == 0:
        return np.nan
    return (x.max() - x.min()) / x.iloc[-1] * 100


# 应用自定义函数到 10 期滚动窗口
# 金融意义：每个时点都能得到过去 10 期的价格波动幅度
custom_indicator = stock_series.rolling(10).apply(price_range)
print("自定义波动幅度指标（%）：")
print(custom_indicator.dropna().head(10))

# --------------------------- 第十部分：实战案例 ---------------------------

print("\n" + "=" * 60)
print("第十部分：双均线交易系统实战案例")
print("=" * 60)

print("\n1. 数据准备")
print("-" * 15)

# 实战案例：构建双均线交易系统
# 获取数据（示例使用随机游走模拟股价）
dates = pd.date_range("2025-01-01", periods=100, freq="D")

# 使用几何布朗运动模拟股价走势
# 公式：S_t = S_{t-1} * (1 + μ*dt + σ*dW_t)
# 其中 μ 为漂移率，σ 为波动率，dW_t 为随机扰动
np.random.seed(42)
prices_df = pd.DataFrame(
    {
        # AAPL：日均收益 0.1%，年化波动率约 32%
        "AAPL": 150 * np.cumprod(1 + np.random.normal(0.001, 0.02, 100)),
        # GOOG：日均收益 0.08%，年化波动率约 24%
        "GOOG": 2800 * np.cumprod(1 + np.random.normal(0.0008, 0.015, 100)),
    },
    index=dates,
)

print("模拟股价数据（前5天）：")
print(prices_df.head())

print("\n2. 收益率分析")
print("-" * 15)

# 计算 5 日收益率 - 用于动量策略分析
# 公式：R_5d = (P_t - P_{t-5}) / P_{t-5}
# 金融意义：短期动量指标，正值表示上涨趋势，负值表示下跌趋势
returns_5d = prices_df.pct_change(5, fill_method=None).dropna()
print("5日收益率（前5个有效值）：")
print(returns_5d.head())

print("收益率统计摘要：")
print(returns_5d.describe())

print("\n3. 双均线系统构建")
print("-" * 20)

# 双均线系统构建 - 经典的趋势跟踪策略
# 短期均线（20日）：MA20 = Σ(P_i) / 20，i 从 t-19 到 t
# 长期均线（60日）：MA60 = Σ(P_i) / 60，i 从 t-59 到 t

print("计算AAPL的双均线系统...")
prices_df["AAPL_MA20"] = prices_df["AAPL"].rolling(20).mean()
prices_df["AAPL_MA60"] = prices_df["AAPL"].rolling(60).mean()

# 显示系统数据（去掉NaN）
system_data = prices_df[["AAPL", "AAPL_MA20", "AAPL_MA60"]].dropna()
print("双均线系统数据（前5个有效值）：")
print(system_data.head())

print("\n4. 交易信号生成")
print("-" * 20)

# 双均线交易信号逻辑：
# 金叉（Golden Cross）：短期均线上穿长期均线 → 买入信号
# 死叉（Death Cross）：短期均线下穿长期均线 → 卖出信号
# 理论基础：趋势跟踪，假设价格趋势具有持续性

# 创建交易信号
system_data["Signal"] = 0  # 初始化信号列
# 当短期均线高于长期均线时为1（看涨），否则为-1（看跌）
system_data.loc[system_data["AAPL_MA20"] > system_data["AAPL_MA60"], "Signal"] = 1
system_data.loc[system_data["AAPL_MA20"] <= system_data["AAPL_MA60"], "Signal"] = -1

# 检测信号变化（交叉点）
system_data["Position_Change"] = system_data["Signal"].diff()
# Position_Change = 2 表示从-1变为1（金叉，买入）
# Position_Change = -2 表示从1变为-1（死叉，卖出）

golden_crosses = system_data[system_data["Position_Change"] == 2]
death_crosses = system_data[system_data["Position_Change"] == -2]

print(f"金叉次数：{len(golden_crosses)}")
print(f"死叉次数：{len(death_crosses)}")

if len(golden_crosses) > 0:
    print("最近一次金叉：")
    print(golden_crosses.tail(1)[["AAPL", "AAPL_MA20", "AAPL_MA60"]])

if len(death_crosses) > 0:
    print("最近一次死叉：")
    print(death_crosses.tail(1)[["AAPL", "AAPL_MA20", "AAPL_MA60"]])

print("\n5. 策略回测")
print("-" * 15)

# 简单的策略回测
# 假设在金叉时买入，死叉时卖出
system_data["Returns"] = system_data["AAPL"].pct_change()
system_data["Strategy_Returns"] = (
    system_data["Signal"].shift(1) * system_data["Returns"]
)

# 累积收益计算
system_data["Cumulative_Returns"] = (1 + system_data["Returns"]).cumprod()
system_data["Strategy_Cumulative"] = (1 + system_data["Strategy_Returns"]).cumprod()

final_data = system_data.dropna()
if len(final_data) > 0:
    print("策略表现摘要：")
    print(
        f"买入持有策略累计收益：{(final_data['Cumulative_Returns'].iloc[-1] - 1) * 100:.2f}%",
    )
    print(
        f"双均线策略累计收益：{(final_data['Strategy_Cumulative'].iloc[-1] - 1) * 100:.2f}%",
    )
    print(
        f"策略年化波动率：{final_data['Strategy_Returns'].std() * np.sqrt(252) * 100:.2f}%",
    )

# 可视化双均线系统（如果需要显示图表，取消注释）
# plt.figure(figsize=(12, 8))
# system_data[["AAPL", "AAPL_MA20", "AAPL_MA60"]].plot(figsize=(12, 6))
# plt.title("苹果股价双均线系统")
# plt.ylabel("价格")
# plt.legend(["股价", "20日均线", "60日均线"])
# plt.grid(True)
# plt.show()

# --------------------------- 第十一部分：常见问题和最佳实践 ---------------------------

print("\n" + "=" * 60)
print("第十一部分：常见问题和最佳实践")
print("=" * 60)

print("\n1. 数据类型处理")
print("-" * 20)

# 常见问题1：数据类型不匹配
sample_df = pd.DataFrame(
    {
        "price": ["100.5", "101.2", "99.8"],  # 字符串类型
        "volume": [1000, 1500, 800],
    },
)

print("原始数据类型：")
print(sample_df.dtypes)

# 解决方案：转换数据类型
sample_df["price"] = pd.to_numeric(sample_df["price"])
print("转换后数据类型：")
print(sample_df.dtypes)

print("\n2. 内存优化")
print("-" * 15)

# 大数据集的内存优化
print("优化前内存使用：")
print(f"DataFrame内存使用：{sample_df.memory_usage(deep=True).sum()} bytes")

# 使用更小的数据类型
sample_df["volume"] = sample_df["volume"].astype("int32")  # 默认是int64
print("优化后内存使用：")
print(f"DataFrame内存使用：{sample_df.memory_usage(deep=True).sum()} bytes")

print("\n3. 链式操作最佳实践")
print("-" * 25)

# 推荐的链式操作写法
result = (
    sample_df.assign(price_change=lambda x: x["price"].pct_change())
    .dropna()
    .query("volume > 1000")
    .reset_index(drop=True)
)

print("链式操作结果：")
print(result)

print("\n4. 常见错误及解决方案")
print("-" * 25)

print("错误1：SettingWithCopyWarning")
print("原因：对DataFrame切片后直接赋值")
print("解决：使用.loc[]或.copy()")

print("\n错误2：日期索引时区问题")
print("原因：混合使用有时区和无时区的日期")
print("解决：统一时区处理")

print("\n错误3：滚动窗口计算结果全为NaN")
print("原因：窗口大小超过数据长度")
print("解决：使用min_periods参数或检查数据长度")

# --------------------------- 总结和学习建议 ---------------------------

print("\n" + "=" * 60)
print("总结和学习建议")
print("=" * 60)

print("\n本教程涵盖的核心概念：")
print("1. ✅ Series和DataFrame基础操作")
print("2. ✅ 索引和数据选择（iloc、loc）")
print("3. ✅ 缺失值处理（fillna、dropna）")
print("4. ✅ 时间序列操作（重采样、时区）")
print("5. ✅ 滚动窗口计算（移动平均、波动率）")
print("6. ✅ 收益率计算和金融指标")
print("7. ✅ 实战案例（双均线交易系统）")

print("\n下一步学习建议：")
print("1. 📚 深入学习pandas的groupby操作")
print("2. 📊 学习更多技术指标（RSI、MACD、布林带）")
print("3. 🔍 掌握数据清洗和异常值处理")
print("4. 📈 学习可视化库（matplotlib、seaborn、plotly）")
print("5. 🚀 学习更高级的金融分析（投资组合优化、风险模型）")

print("\n实用资源：")
print("- 官方文档：https://pandas.pydata.org/docs/")
print("- 金融数据源：yfinance, quandl, alpha_vantage")
print("- 回测框架：backtrader, zipline, vectorbt")

print("\n" + "=" * 60)
print("教程完成！希望这些详细注释能帮助你更好地理解pandas在金融分析中的应用。")
print("记住：实践是最好的老师，多动手尝试各种数据操作！")
print("=" * 60)
