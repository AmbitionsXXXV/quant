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

import warnings

import numpy as np
import pandas as pd

# 抑制不必要的警告信息
warnings.filterwarnings("ignore", category=FutureWarning)

# 检查 yfinance 是否可用
try:
    import yfinance as yf

    YFINANCE_AVAILABLE = True
    print("✅ yfinance 已安装，可以获取真实股票数据")
    print(f"📦 yfinance 版本: {yf.__version__}")
except ImportError:
    YFINANCE_AVAILABLE = False
    print("❌ yfinance 未安装，将使用模拟数据")
    print("如需获取真实数据，请运行：pip install yfinance")

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
s = pd.Series([1, 2, np.nan, 4, 5, 6, 7, np.nan, 9, 10], name="Toy Series")
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

print("向前填充（用前一个有效值，pad 是 ffill 的别名）：")
print(s.fillna(method="pad"))  # pad = forward fill

print("向后填充（用后一个有效值，backfill 是 bfill 的别名）：")
print(s.fillna(method="backfill"))  # backfill = backward fill

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
    [100, 105, 110, 108, 115],
    index=pd.date_range("2025-01-01", periods=5),
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

# --------------------------- 第十部分：真实市场数据分析（yfinance）---------------------------

print("\n" + "=" * 60)
print("第十部分：真实市场数据分析（yfinance）")
print("=" * 60)
5
if YFINANCE_AVAILABLE:
    print("\n1. yfinance 库介绍和参数说明")
    print("-" * 30)

    # yfinance 是什么？
    # yfinance 是一个Python库，可以免费获取Yahoo Finance的股票数据
    # 包括：股价、成交量、财务数据等
    # 优点：免费、简单、数据质量好
    # 缺点：依赖Yahoo Finance，可能有访问限制

    print("📚 yfinance.download() 重要参数说明：")
    print("""
    🎯 基本参数：
    ├── tickers: 股票代码，如 'AAPL' 或 ['AAPL', 'GOOGL']
    ├── start/end: 日期范围，如 '2025-06-01', '2025-08-01'
    ├── period: 时间段，如 '1y', '6mo', '1d'（与start/end二选一）
    └── interval: 数据频率，如 '1d'(日), '1h'(小时), '1m'(分钟)

    ⚙️  重要配置（最新版默认值）：
    ├── auto_adjust: 自动调整价格（默认True，处理分红拆股）
    ├── progress: 显示下载进度条（默认True）
    ├── threads: 多线程下载（批量获取时有用）
    └── group_by: 数据分组方式，'ticker'或'column'

    💡 最佳实践：
    - 批量下载时设置 progress=False 减少输出
    - 使用 try-except 处理网络错误
    - 缓存数据避免重复下载
    - 利用多线程加速批量下载
    """)

    print("\n2. 获取真实股票数据")
    print("-" * 20)

    try:
        # 获取苹果公司（AAPL）的历史数据
        # period 和 start/end 二选一
        # period选项：1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        print("正在获取AAPL数据...")
        # 最新版 yfinance 默认 auto_adjust=True，只需设置 progress=False
        aapl = yf.download("AAPL", start="2022-01-01", end="2024-01-01", progress=False)

        print("数据获取成功！数据形状：", aapl.shape)
        print("列名：", aapl.columns.tolist())
        print("\n前5行数据：")
        print(aapl.head())

        # yfinance 返回的数据结构解释（最新版默认已复权）：
        # Open: 复权开盘价
        # High: 复权最高价
        # Low: 复权最低价
        # Close: 复权收盘价
        # Adj Close: 复权收盘价（与Close相同）
        # Volume: 成交量

        print("\n数据统计摘要：")
        print(aapl.describe())

        print("\n2. 数据质量检查")
        print("-" * 15)

        # 检查缺失值
        print("缺失值检查：")
        print(aapl.isnull().sum())

        # 检查数据完整性
        print(f"数据日期范围：{aapl.index.min()} 到 {aapl.index.max()}")
        print(f"总交易日数：{len(aapl)}")

        # 检查异常值（收盘价为0或成交量异常大）
        print("异常值检查：")
        print(f"收盘价为0的天数：{(aapl['Close'] == 0).sum()}")
        print(
            f"成交量超过平均值10倍的天数：{(aapl['Volume'] > aapl['Volume'].mean() * 10).sum()}",
        )

        print("\n3. 基础技术分析")
        print("-" * 15)

        # 使用真实数据计算技术指标
        # 移动平均线
        aapl["MA20"] = aapl["Close"].rolling(20).mean()
        aapl["MA50"] = aapl["Close"].rolling(50).mean()
        aapl["MA200"] = aapl["Close"].rolling(200).mean()

        # 布林带（Bollinger Bands）
        aapl["BB_middle"] = aapl["Close"].rolling(20).mean()
        aapl["BB_std"] = aapl["Close"].rolling(20).std()
        aapl["BB_upper"] = aapl["BB_middle"] + (aapl["BB_std"] * 2)
        aapl["BB_lower"] = aapl["BB_middle"] - (aapl["BB_std"] * 2)

        # 相对强弱指数（RSI）
        def calculate_rsi(prices, window=14):
            """计算RSI指标

            RSI = 100 - (100 / (1 + RS))
            RS = 平均上涨幅度 / 平均下跌幅度
            """
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi

        aapl["RSI"] = calculate_rsi(aapl["Close"])

        # 成交量加权平均价格（VWAP）
        def calculate_vwap(high, low, close, volume):
            """计算VWAP

            VWAP = Σ(价格 × 成交量) / Σ(成交量)
            价格通常用 (高+低+收) / 3
            """
            typical_price = (high + low + close) / 3
            return (typical_price * volume).cumsum() / volume.cumsum()

        # 计算每日VWAP（这里简化为累计VWAP）
        aapl["VWAP"] = calculate_vwap(
            aapl["High"],
            aapl["Low"],
            aapl["Close"],
            aapl["Volume"],
        )

        print("技术指标计算完成！")
        print("最新的技术指标值：")
        latest_data = aapl[
            ["Close", "MA20", "MA50", "RSI", "BB_upper", "BB_lower"]
        ].tail(1)
        print(latest_data)

        print("\n4. 收益率和波动率分析")
        print("-" * 25)

        # 日收益率
        aapl["Daily_Return"] = aapl["Close"].pct_change()

        # 对数收益率（连续复利）
        aapl["Log_Return"] = np.log(aapl["Close"] / aapl["Close"].shift(1))

        # 收益率统计
        print("收益率统计分析：")
        returns_stats = aapl["Daily_Return"].describe()
        print(returns_stats)

        # 年化指标
        trading_days = 252
        annual_return = aapl["Daily_Return"].mean() * trading_days
        annual_volatility = aapl["Daily_Return"].std() * np.sqrt(trading_days)
        sharpe_ratio = (
            annual_return / annual_volatility
        )  # 简化的夏普比率（假设无风险利率为0）

        print("\n年化指标：")
        print(f"年化收益率: {annual_return:.2%}")
        print(f"年化波动率: {annual_volatility:.2%}")
        print(f"夏普比率: {sharpe_ratio:.2f}")

        # 最大回撤分析
        aapl["Cumulative"] = (1 + aapl["Daily_Return"]).cumprod()
        aapl["Running_Max"] = aapl["Cumulative"].expanding().max()
        aapl["Drawdown"] = (aapl["Cumulative"] - aapl["Running_Max"]) / aapl[
            "Running_Max"
        ]
        max_drawdown = aapl["Drawdown"].min()

        print(f"最大回撤: {max_drawdown:.2%}")

        print("\n5. 多股票对比分析")
        print("-" * 20)

        # 获取多只股票数据进行对比
        print("获取科技股对比数据...")
        tickers = ["AAPL", "GOOGL", "MSFT", "TSLA"]

        # 使用字典存储多只股票数据
        stocks_data = {}
        for ticker in tickers:
            try:
                stock = yf.download(
                    ticker,
                    start="2022-01-01",
                    end="2024-01-01",
                    progress=False,
                )
                stocks_data[ticker] = stock["Close"]
                print(f"✅ {ticker} 数据获取成功")
            except Exception as e:
                print(f"❌ {ticker} 数据获取失败: {e}")

        if stocks_data:
            # 合并股票价格数据
            prices_df = pd.DataFrame(stocks_data)

            # 计算相关性
            returns_df = prices_df.pct_change().dropna()
            correlation_matrix = returns_df.corr()

            print("\n股票收益率相关性矩阵：")
            print(correlation_matrix)

            # 计算各股票的表现指标
            print("\n各股票表现对比：")
            performance_summary = pd.DataFrame(
                {
                    "Total_Return": (prices_df.iloc[-1] / prices_df.iloc[0] - 1) * 100,
                    "Volatility": returns_df.std() * np.sqrt(252) * 100,
                    "Sharpe_Ratio": returns_df.mean() / returns_df.std() * np.sqrt(252),
                },
            )
            print(performance_summary)

        print("\n6. 真实数据的双均线策略回测")
        print("-" * 30)

        # 使用真实AAPL数据进行双均线策略回测
        strategy_data = aapl[["Close", "MA20", "MA50"]].copy()
        strategy_data = strategy_data.dropna()

        # 生成交易信号
        strategy_data["Signal"] = 0
        strategy_data.loc[strategy_data["MA20"] > strategy_data["MA50"], "Signal"] = 1
        strategy_data.loc[strategy_data["MA20"] <= strategy_data["MA50"], "Signal"] = -1

        # 计算信号变化
        strategy_data["Position_Change"] = strategy_data["Signal"].diff()

        # 计算策略收益
        strategy_data["Returns"] = strategy_data["Close"].pct_change()
        strategy_data["Strategy_Returns"] = (
            strategy_data["Signal"].shift(1) * strategy_data["Returns"]
        )

        # 计算累积收益
        strategy_data["Buy_Hold_Cumulative"] = (1 + strategy_data["Returns"]).cumprod()
        strategy_data["Strategy_Cumulative"] = (
            1 + strategy_data["Strategy_Returns"]
        ).cumprod()

        # 回测结果
        final_buy_hold = strategy_data["Buy_Hold_Cumulative"].iloc[-1] - 1
        final_strategy = strategy_data["Strategy_Cumulative"].iloc[-1] - 1

        print("真实数据回测结果：")
        print(f"买入持有策略收益: {final_buy_hold:.2%}")
        print(f"双均线策略收益: {final_strategy:.2%}")
        print(f"策略相对表现: {final_strategy - final_buy_hold:.2%}")

        # 交易次数统计
        trades = len(strategy_data[strategy_data["Position_Change"] != 0])
        print(f"总交易次数: {trades}")

        # 可视化（可选，如果需要显示图表）
        # import matplotlib.pyplot as plt
        #
        # fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        #
        # # 价格和移动平均线
        # axes[0,0].plot(aapl.index, aapl['Close'], label='Close Price')
        # axes[0,0].plot(aapl.index, aapl['MA20'], label='MA20')
        # axes[0,0].plot(aapl.index, aapl['MA50'], label='MA50')
        # axes[0,0].set_title('AAPL Price and Moving Averages')
        # axes[0,0].legend()
        #
        # # RSI
        # axes[0,1].plot(aapl.index, aapl['RSI'])
        # axes[0,1].axhline(y=70, color='r', linestyle='--', label='Overbought')
        # axes[0,1].axhline(y=30, color='g', linestyle='--', label='Oversold')
        # axes[0,1].set_title('RSI Indicator')
        # axes[0,1].legend()
        #
        # # 成交量
        # axes[1,0].bar(aapl.index, aapl['Volume'])
        # axes[1,0].set_title('Trading Volume')
        #
        # # 策略累积收益对比
        # axes[1,1].plot(strategy_data.index, strategy_data['Buy_Hold_Cumulative'], label='Buy & Hold')
        # axes[1,1].plot(strategy_data.index, strategy_data['Strategy_Cumulative'], label='MA Strategy')
        # axes[1,1].set_title('Strategy Performance Comparison')
        # axes[1,1].legend()
        #
        # plt.tight_layout()
        # plt.show()

    except Exception as e:
        print(f"❌ 数据获取失败: {e}")
        print("可能的原因：")
        print("1. 网络连接问题")
        print("2. Yahoo Finance 服务暂时不可用")
        print("3. 股票代码不正确")
        print("4. 日期范围有问题")
        print("\n解决建议：")
        print("- 检查网络连接")
        print("- 确认股票代码正确")
        print("- 确保使用最新版 yfinance")

    print("\n3. 数据缓存和最佳实践")
    print("-" * 25)

    # 数据缓存示例
    print("💾 数据缓存最佳实践：")
    print("""
    为什么需要缓存？
    - 避免重复下载相同数据
    - 提高程序运行速度
    - 减少网络请求，避免被限制
    - 离线分析数据

    常用缓存方法：
    1. CSV文件缓存（简单易用）
    2. Pickle文件缓存（保持数据类型）
    3. HDF5文件缓存（大数据集）
    4. 数据库缓存（PostgreSQL, SQLite）
    """)

    # CSV缓存示例
    def get_stock_data_with_cache(ticker, start_date, end_date, cache_dir="./cache"):
        """
        带缓存的股票数据获取函数

        Args:
            ticker: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            cache_dir: 缓存目录

        Returns:
            pandas.DataFrame: 股票数据
        """
        import os
        from datetime import datetime

        # 创建缓存目录
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # 缓存文件名
        cache_file = f"{cache_dir}/{ticker}_{start_date}_{end_date}.csv"

        # 检查缓存是否存在且不超过1天
        if os.path.exists(cache_file):
            file_time = os.path.getmtime(cache_file)
            current_time = datetime.now().timestamp()

            # 如果文件不超过24小时，直接读取缓存
            if (current_time - file_time) < 24 * 3600:
                print(f"📁 从缓存读取 {ticker} 数据")
                try:
                    data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
                    return data
                except Exception as e:
                    print(f"缓存读取失败: {e}，将重新下载")

        # 下载新数据
        print(f"🌐 下载 {ticker} 数据...")
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            # 保存到缓存
            data.to_csv(cache_file)
            print(f"💾 数据已缓存到: {cache_file}")

            return data

        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return None

    # 演示缓存功能
    if YFINANCE_AVAILABLE:
        print("\n缓存功能演示：")
        try:
            # 第一次调用（下载）
            cached_data = get_stock_data_with_cache("AAPL", "2025-06-01", "2025-08-01")
            if cached_data is not None:
                print(f"✅ 获取到 {len(cached_data)} 行数据")

                # 第二次调用（从缓存读取）
                cached_data2 = get_stock_data_with_cache(
                    "AAPL",
                    "2025-06-01",
                    "2025-08-01",
                )
                if cached_data2 is not None:
                    print("✅ 缓存功能正常工作")

        except Exception as e:
            print(f"缓存演示失败: {e}")

    print("\n4. 错误处理和重试机制")
    print("-" * 25)

    # 带重试的数据获取函数
    def download_with_retry(ticker, max_retries=3, retry_delay=2, **kwargs):
        """
        带重试机制的数据下载函数

        Args:
            ticker: 股票代码
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
            **kwargs: yf.download的其他参数

        Returns:
            pandas.DataFrame or None: 股票数据
        """
        import time

        for attempt in range(max_retries):
            try:
                print(f"🔄 尝试下载 {ticker} (第{attempt + 1}次)")
                data = yf.download(ticker, progress=False, **kwargs)

                if not data.empty:
                    print(f"✅ {ticker} 下载成功")
                    return data
                else:
                    print(f"⚠️ {ticker} 返回空数据")

            except Exception as e:
                print(f"❌ 第{attempt + 1}次尝试失败: {e}")

                if attempt < max_retries - 1:
                    print(f"⏳ {retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避
                else:
                    print(f"💔 {ticker} 下载最终失败")
                    return None

        return None

    # 演示重试机制
    if YFINANCE_AVAILABLE:
        print("\n重试机制演示：")
        try:
            # 使用一个可能不存在的股票代码测试
            test_data = download_with_retry(
                "INVALID_TICKER",
                start="2025-06-01",
                end="2025-08-01",
                max_retries=2,
            )

            if test_data is None:
                print("✅ 重试机制正常工作（正确处理了无效代码）")

        except Exception as e:
            print(f"重试演示过程中出错: {e}")

    print("\n5. 批量下载优化策略")
    print("-" * 25)

    def download_multiple_stocks_optimized(tickers, **kwargs):
        """
        优化的批量股票数据下载

        Features:
        - 并发下载
        - 错误处理
        - 进度显示
        - 结果验证
        """
        import time
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = {}
        failed_tickers = []

        def download_single(ticker):
            try:
                data = yf.download(ticker, progress=False, **kwargs)
                if not data.empty:
                    return ticker, data
                else:
                    return ticker, None
            except Exception as e:
                print(f"❌ {ticker} 下载失败: {e}")
                return ticker, None

        print(f"🚀 开始批量下载 {len(tickers)} 只股票...")
        start_time = time.time()

        # 使用线程池并发下载
        with ThreadPoolExecutor(max_workers=5) as executor:
            # 提交所有下载任务
            future_to_ticker = {
                executor.submit(download_single, ticker): ticker for ticker in tickers
            }

            # 收集结果
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    ticker_result, data = future.result()
                    if data is not None:
                        results[ticker_result] = data
                        print(f"✅ {ticker_result}: {len(data)} 行数据")
                    else:
                        failed_tickers.append(ticker_result)
                        print(f"❌ {ticker_result}: 下载失败")
                except Exception as e:
                    failed_tickers.append(ticker)
                    print(f"❌ {ticker}: 处理失败 - {e}")

        end_time = time.time()
        print(f"⏱️  批量下载完成，用时 {end_time - start_time:.2f} 秒")
        print(f"📊 成功: {len(results)}, 失败: {len(failed_tickers)}")

        return results, failed_tickers

    # 演示批量下载优化
    if YFINANCE_AVAILABLE:
        print("\n批量下载优化演示：")
        try:
            test_tickers = ["AAPL", "GOOGL", "INVALID_TICKER"]  # 包含一个无效代码
            results, failed = download_multiple_stocks_optimized(
                test_tickers,
                start="2025-06-01",
                end="2025-08-01",
            )

            print("✅ 批量下载优化功能演示完成")

        except Exception as e:
            print(f"批量下载演示失败: {e}")

else:
    print("跳过真实数据示例，因为 yfinance 未安装")
    print("如需使用真实数据，请运行：pip install yfinance")

# --------------------------- 第十一部分：双均线交易系统模拟案例 ---------------------------

print("\n" + "=" * 60)
print("第十一部分：双均线交易系统模拟案例")
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
print("第十二部分：yfinance 进阶技巧和数据源对比")
print("=" * 60)

if YFINANCE_AVAILABLE:
    print("\n1. yfinance 高级功能")
    print("-" * 20)

    # 获取股票基本信息
    try:
        print("获取 AAPL 公司信息...")
        aapl_info = yf.Ticker("AAPL")
        info = aapl_info.info

        print("公司基本信息：")
        key_info = {
            "公司名称": info.get("longName", "N/A"),
            "所属行业": info.get("industry", "N/A"),
            "员工数量": info.get("fullTimeEmployees", "N/A"),
            "市值": info.get("marketCap", "N/A"),
            "股价": info.get("regularMarketPrice", "N/A"),
            "52周最高": info.get("fiftyTwoWeekHigh", "N/A"),
            "52周最低": info.get("fiftyTwoWeekLow", "N/A"),
        }

        for key, value in key_info.items():
            print(f"{key}: {value}")

        # 获取财务数据
        print("\n财务数据获取：")
        # 损益表
        try:
            income_stmt = aapl_info.income_stmt
            if not income_stmt.empty:
                print("✅ 损益表数据可用")
                print(f"最新年度营收: {income_stmt.loc['Total Revenue'].iloc[0]:,.0f}")
            else:
                print("❌ 损益表数据不可用")
        except Exception:
            print("❌ 损益表数据获取失败")

        # 资产负债表
        try:
            balance_sheet = aapl_info.balance_sheet
            if not balance_sheet.empty:
                print("✅ 资产负债表数据可用")
            else:
                print("❌ 资产负债表数据不可用")
        except Exception:
            print("❌ 资产负债表数据获取失败")

        # 现金流量表
        try:
            cash_flow = aapl_info.cashflow
            if not cash_flow.empty:
                print("✅ 现金流量表数据可用")
            else:
                print("❌ 现金流量表数据不可用")
        except Exception:
            print("❌ 现金流量表数据获取失败")

    except Exception as e:
        print(f"公司信息获取失败: {e}")

    print("\n2. 不同时间频率的数据")
    print("-" * 25)

    # 获取不同频率的数据
    try:
        # 分钟级数据（最近7天）
        print("获取分钟级数据...")
        minute_data = yf.download("AAPL", period="7d", interval="1m", progress=False)
        print(f"分钟数据形状: {minute_data.shape}")

        # 小时级数据
        print("获取小时级数据...")
        hourly_data = yf.download("AAPL", period="60d", interval="1h", progress=False)
        print(f"小时数据形状: {hourly_data.shape}")

        # 周级数据
        print("获取周级数据...")
        weekly_data = yf.download("AAPL", period="2y", interval="1wk", progress=False)
        print(f"周数据形状: {weekly_data.shape}")

        # 月级数据
        print("获取月级数据...")
        monthly_data = yf.download("AAPL", period="10y", interval="1mo", progress=False)
        print(f"月数据形状: {monthly_data.shape}")

        print("\n不同频率数据的应用场景：")
        print("📊 分钟数据: 日内交易、高频策略")
        print("📈 小时数据: 短期交易、市场微观结构分析")
        print("📉 日数据: 中长期投资、技术分析")
        print("📋 周/月数据: 长期趋势分析、资产配置")

    except Exception as e:
        print(f"多频率数据获取失败: {e}")

    print("\n3. 批量数据获取技巧")
    print("-" * 20)

    # 批量获取多只股票
    try:
        print("批量获取道琼斯成分股数据...")
        dow_tickers = [
            "AAPL",
            "MSFT",
            "JPM",
            "V",
            "JNJ",
            "WMT",
            "PG",
            "HD",
            "CVX",
            "MRK",
        ]

        # 方法1：循环获取
        dow_data = {}
        for ticker in dow_tickers[:3]:  # 只获取前3只以节省时间
            try:
                data = yf.download(
                    ticker,
                    start="2025-06-01",
                    end="2024-01-01",
                    progress=False,
                )
                dow_data[ticker] = data["Close"]
                print(f"✅ {ticker}: {len(data)} 个交易日")
            except Exception:
                print(f"❌ {ticker}: 获取失败")

        # 方法2：一次性获取多只股票
        print("\n一次性获取多只股票...")
        multi_stocks = yf.download(
            ["AAPL", "GOOGL", "MSFT"],
            start="2025-06-01",
            end="2024-01-01",
            progress=False,
        )

        if not multi_stocks.empty:
            print("✅ 批量获取成功")
            print(f"数据形状: {multi_stocks.shape}")
            print("可用数据类型:", multi_stocks.columns.levels[0].tolist())

            # 提取收盘价
            close_prices = multi_stocks["Close"]
            print("收盘价数据：")
            print(close_prices.head())

    except Exception as e:
        print(f"批量数据获取失败: {e}")

else:
    print("跳过 yfinance 进阶功能，因为库未安装")

print("\n4. 数据源对比和选择建议")
print("-" * 25)

print("金融数据源对比（2024最新）：")
print("""
🚀 推荐：yfinance (最新版) - 首选方案
├── ✅ 完全免费，无API限制
├── ✅ 数据质量高，覆盖全球主要市场
├── ✅ 支持多种数据频率（1m-1mo）
├── ✅ 自动复权处理，开箱即用
├── ✅ 支持并发下载，性能优异
├── ✅ 包含基本面数据（财报、公司信息）
├── ✅ 活跃的开源社区，持续更新
└── 🎯 适合：个人投资、量化研究、教育学习、中小型项目

📊 其他免费数据源：
├── Alpha Vantage
│   ✅ 官方API支持
│   ❌ 免费版限制500次/天
│   🎯 适合：需要官方API的小型应用
│
├── Quandl/Nasdaq Data Link
│   ✅ 宏观经济数据丰富
│   ❌ 股票数据大多需付费
│   🎯 适合：学术研究、经济分析
│
└── FRED (美联储经济数据)
│   ✅ 权威宏观经济数据
│   ❌ 仅限美国经济数据
│   🎯 适合：宏观经济研究

💰 专业级数据源：
├── Bloomberg Terminal ($2000+/月)
├── Refinitiv Eikon ($1000+/月)
├── Wind万得 (中国市场)
└── 券商API (各券商提供)

🏆 yfinance 最新版优势：
- 零成本获取专业级数据质量
- 无需注册API Key
- 支持全球60+交易所
- 历史数据可追溯20+年
- 分钟级数据覆盖
- Python生态完美集成
""")

print("\n2024年最佳数据源选择指南：")
print("""
🎯 不同场景推荐：

📚 学习和个人投资 (推荐方案)
└── yfinance (最新版) + pandas
    💡 完全满足需求，零成本，高质量

🔬 量化研究和策略开发 (推荐方案)
└── yfinance (主力) + FRED (宏观数据)
    💡 覆盖95%的研究需求

💼 中小型量化基金
├── yfinance (历史数据 + 回测)
├── 券商API (实时交易)
└── Wind/Bloomberg (补充数据)

🏛️ 大型机构
├── Bloomberg/Refinitiv (主要数据源)
├── 自建数据团队
└── yfinance (备用/验证)

🌟 特别推荐 yfinance 的原因：
- 数据质量已达到商业级标准
- 覆盖面广：股票、ETF、期货、外汇、加密货币
- 更新及时：通常T+1日更新
- 社区活跃：问题响应快，功能持续改进
- 零门槛：无需注册、无使用限制
""")

print("\n" + "=" * 60)
print("第十三部分：常见问题和最佳实践")
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
print("6. 💾 学习数据存储和管理（SQLite、PostgreSQL、HDF5）")
print("7. ⚡ 学习并行计算和性能优化（multiprocessing、numba）")

print("\n实用资源：")
print("📖 文档资源：")
print("- pandas官方文档：https://pandas.pydata.org/docs/")
print("- yfinance文档：https://pypi.org/project/yfinance/")
print("- quantlib：https://www.quantlib.org/")

print("\n💰 数据源推荐：")
print("- 免费：yfinance, alpha_vantage, quandl")
print("- 付费：Bloomberg API, Refinitiv, Wind")
print("- 加密货币：ccxt, binance-python")

print("\n🔧 分析工具：")
print("- 回测框架：backtrader, zipline, vectorbt")
print("- 技术指标：ta-lib, pandas-ta")
print("- 可视化：plotly, bokeh, dash")
print("- 机器学习：scikit-learn, tensorflow, pytorch")

print("\n📊 实战项目建议：")
print("1. 构建个人股票筛选系统")
print("2. 开发多因子选股模型")
print("3. 建立投资组合管理系统")
print("4. 创建市场情绪分析工具")
print("5. 设计量化交易策略回测平台")

print("\n" + "=" * 60)
print("🎉 教程完成！")
print("=" * 60)

print("\n📝 学习成果总结：")
print("✅ 掌握了pandas在金融数据分析中的核心应用")
print("✅ 熟练使用最新版yfinance获取多种金融数据")
print("✅ 构建了完整的量化分析工作流程")
print("✅ 实现了真实数据驱动的交易策略回测")
print("✅ 建立了数据缓存和错误处理的最佳实践")
print("✅ 掌握了并发下载和性能优化技巧")

print("\n🎯 核心技能掌握检验：")
print("现在你应该能够：")
print("1. 🚀 高效获取全球市场的实时和历史数据")
print("2. 📊 构建专业级的技术分析指标体系")
print("3. 💼 开发完整的量化投资策略")
print("4. 🔍 进行多维度的风险和收益分析")
print("5. ⚡ 优化数据处理性能和系统稳定性")
print("6. 🏗️ 搭建可扩展的量化分析框架")

print("\n💡 yfinance 最新版现代化使用示例：")

# 示例1：一行代码获取多维度数据
print("\n🔥 现代化写法示例：")
print("""
# 传统写法 vs 现代化写法对比

# ❌ 旧式写法（繁琐）
data = yf.download('AAPL', start='2025-06-01', end='2025-08-01', auto_adjust=True, progress=False)
close_price = data['Close']
returns = close_price.pct_change()

# ✅ 现代化写法（链式调用）
returns = (yf.download('AAPL', period='1y', progress=False)['Close']
           .pct_change()
           .dropna())

# ✅ 批量获取多股票（自动并发）
stocks = yf.download(['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
                    period='6mo',
                    group_by='ticker')

# ✅ 获取期权数据（新功能）
aapl_ticker = yf.Ticker('AAPL')
options_dates = aapl_ticker.options
options_chain = aapl_ticker.option_chain(options_dates[0])
""")

print("\n⚡ 最新版性能优化技巧：")
print("- 默认复权处理，数据质量更高")
print("- 自动并发下载，速度提升3-5倍")
print("- 智能重试机制，网络稳定性更好")
print("- 内存优化，支持更大数据集")
print("- 多线程安全，适合生产环境")

print("\n🚀 yfinance 2024年新特性应用：")

if YFINANCE_AVAILABLE:
    print("\n📊 现代化数据获取演示：")
    try:
        # 新特性1：快速获取多市场数据
        print("1. 全球市场一次性获取：")
        global_etfs = yf.download(
            ["SPY", "QQQ", "IWM", "EFA", "EEM"],
            period="1mo",
            progress=False,
        )["Close"]
        print(f"✅ 获取 {len(global_etfs.columns)} 个全球ETF数据")

        # 新特性2：Ticker对象的高级功能
        print("\n2. 高级Ticker对象功能：")
        aapl = yf.Ticker("AAPL")

        # 获取实时报价
        fast_info = aapl.fast_info
        print(f"✅ 实时价格: ${fast_info.get('lastPrice', 'N/A')}")

        # 获取历史分红
        dividends = aapl.dividends.tail(5)
        if not dividends.empty:
            print(f"✅ 最近5次分红数据: {len(dividends)} 条记录")

        print("\n3. 现代化数据分析链：")
        # 演示现代化分析流程
        analysis_result = (
            aapl.history(period="3mo")
            .assign(
                Returns=lambda x: x["Close"].pct_change(),
                MA20=lambda x: x["Close"].rolling(20).mean(),
                Volatility=lambda x: x["Returns"].rolling(20).std(),
            )
            .dropna()
        )

        print(f"✅ 完成现代化分析链，处理 {len(analysis_result)} 个交易日")

    except Exception as e:
        print(f"演示失败: {e}")

print("\n🎯 推荐项目实战：")
print("📊 多资产组合分析：同时分析股票、ETF、商品、外汇")
print("⏰ 实时监控系统：结合定时任务自动更新数据")
print("🤖 智能选股：基于财务指标和技术指标筛选股票")
print("📈 因子投资：构建多因子选股模型")
print("🔄 自动化回测：建立策略自动化测试框架")
print("📱 投资仪表板：开发个人投资监控面板")

print("\n🌟 yfinance + AI 融合应用：")
print("- 结合ChatGPT API进行智能市场分析")
print("- 使用机器学习预测股价趋势")
print("- 构建基于NLP的情绪分析系统")
print("- 开发智能投顾助手")

print("\n" + "=" * 60)
print("💪 记住：实践是最好的老师！")
print("现在就开始获取一只你感兴趣的股票数据，动手分析吧！")
print("=" * 60)
