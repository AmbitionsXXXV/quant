"""均值（Means）示例与金融数据演示

参考与灵感来源：
- 第 6 讲：均值 (Means)（提炼自示例代码）
  链接: https://wqu.guru/blog/quantopia-quantitative-analysis-56-lectures/means

运行方式（推荐使用 uv）：
- 作为模块运行：uv run -m quant.means_demo
- 作为脚本运行：uv run quant/means_demo.py

本脚本包含：
1) 基础统计量示例：算术平均、几何平均、调和平均、众数、中位数
2) 金融数据示例：下载 SPY 日线，计算收益率均值/中位数/众数与几何平均收益率

═══════════════════════════════════════════════════════════════════════════════
                              数学概念详解
═══════════════════════════════════════════════════════════════════════════════

1. 算术平均数 (Arithmetic Mean)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   公式：μ = (1/n) × Σ(xi)，其中 i 从 1 到 n

   数学意义：
   - 所有观测值的总和除以观测值个数
   - 数据的"重心"位置，使得各点到该点距离的平方和最小
   - 对异常值敏感，一个极端值会显著影响结果

   应用场景：
   - 描述数据的典型水平
   - 正态分布数据的最佳中心估计
   - 线性回归中的基础统计量

2. 中位数 (Median)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   定义：将数据排序后位于中间位置的值

   数学特性：
   - 50% 分位数，将数据分为两等份
   - 对异常值不敏感（稳健统计量）
   - 偏态分布的更好中心度量

   计算方法：
   - 奇数个数据：取中间值
   - 偶数个数据：取中间两个值的平均

3. 众数 (Mode)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   定义：出现频率最高的数值

   特点：
   - 唯一能用于分类数据的集中趋势度量
   - 可能不存在（无重复值）或存在多个
   - 描述数据的"最常见"特征

   类型：
   - 单峰分布：一个众数
   - 双峰分布：两个众数
   - 多峰分布：多个众数

4. 几何平均数 (Geometric Mean)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   公式：G = ⁿ√(x₁ × x₂ × ... × xₙ) = (∏xi)^(1/n)

   数学特性：
   - 所有值乘积的 n 次方根
   - 始终 ≤ 算术平均数（AM-GM 不等式）
   - 对数变换后等于算术平均数的指数

   适用条件：
   - 所有数值必须为正数
   - 数据具有乘性关系
   - 比率和增长率的平均化

5. 调和平均数 (Harmonic Mean)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   公式：H = n / Σ(1/xi)

   数学特性：
   - 倒数的算术平均数的倒数
   - 三种平均数中最小：H ≤ G ≤ A
   - 对小数值更敏感

   典型应用：
   - 速度的平均（时间固定，距离变化）
   - 价格的平均（P/E 比率等）
   - 电阻并联计算

═══════════════════════════════════════════════════════════════════════════════
                              金融概念详解
═══════════════════════════════════════════════════════════════════════════════

1. 收益率 (Return)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   简单收益率：R = (P_t - P_{t-1}) / P_{t-1}

   金融意义：
   - 衡量投资在单位时间内的相对收益
   - 消除了价格水平的影响，便于比较不同资产
   - 可以直接加总计算组合收益率

   特点：
   - 范围：-1 到 +∞
   - 不具备时间可加性
   - 适合短期分析和横截面比较

2. 几何平均收益率 (Geometric Mean Return)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   公式：R_g = [(1+R₁)(1+R₂)...(1+Rₙ)]^(1/n) - 1

   金融意义：
   - 复合增长率，考虑了复利效应
   - 真实反映长期投资的平均收益水平
   - 用于计算年化收益率

   重要性：
   - 时间加权收益率的基础
   - 消除了波动性对平均收益的影响
   - 投资业绩评估的标准指标

   验证公式：
   最终价值 = 初始价值 × (1 + R_g)^T
   其中 T 为投资期数

3. SPY ETF
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   全称：SPDR S&P 500 ETF Trust

   特点：
   - 跟踪标普 500 指数的交易所交易基金
   - 包含美国 500 家最大上市公司
   - 代表美国股市的整体表现
   - 流动性极高，交易成本低

   分析价值：
   - 市场基准，用于比较其他投资的表现
   - 系统性风险的代表
   - 宏观经济趋势的反映

4. 收益率分布特征
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   均值 vs 中位数：
   - 均值 > 中位数：右偏分布（正偏态）
   - 均值 < 中位数：左偏分布（负偏态）
   - 均值 ≈ 中位数：对称分布

   众数的意义：
   - 最常出现的收益率水平
   - 市场"正常"状态的指示
   - 连续数据需要分组处理

   实际应用：
   - 风险评估：分布形状影响风险度量
   - 投资决策：了解收益率的典型特征
   - 模型选择：选择合适的概率分布模型

═══════════════════════════════════════════════════════════════════════════════
                            数值解释与直觉理解
═══════════════════════════════════════════════════════════════════════════════

为什么几何平均数 < 算术平均数？
- 几何平均考虑复利效应，更保守
- 波动性会降低几何平均收益率
- 体现了"波动拖累"效应

为什么使用不同的平均数？
- 算术平均：期望收益率，用于资产配置
- 几何平均：实际增长率，用于业绩评估
- 调和平均：特殊比率计算，如平均P/E

金融数据的特殊性：
- 收益率通常呈现尖峰厚尾分布
- 存在波动性聚集现象
- 极端值（黑天鹅事件）影响显著
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Union

import numpy as np
from scipy import stats

try:
    import yfinance as yf

    YFINANCE_AVAILABLE = True
except Exception:  # 明确仅捕获导入失败等异常
    YFINANCE_AVAILABLE = False


Number = Union[int, float, np.floating]


def calculate_mode(values: Sequence[Number]) -> Union[str, List[Number]]:
    """计算众数（与参考代码一致的直观实现）。

    众数（Mode）数学定义：
    - 在一组数据中出现频率最高的数值
    - 对于连续数据，通常需要先分组（分箱）处理
    - 是唯一可以用于分类数据的集中趋势度量

    金融应用：
    - 识别最常见的收益率水平
    - 发现市场的"正常"状态
    - 多峰分布可能暗示市场存在不同的运行状态

    统计特性：
    - 可能不存在（所有值都不同）
    - 可能存在多个（多峰分布）
    - 对异常值不敏感

    参数：
        values: 数值序列

    返回：
        str: "No mode" 表示无众数
        List[Number]: 众数列表（可能有多个）

    当存在多个众数时返回列表；若没有众数（所有频次相同且>1 之前的实现会返回 'No mode'），
    这里约定：当每个值只出现一次且元素数量>1 时，返回 'No mode'。
    """
    counts: dict[Number, int] = {}
    for element in values:
        counts[element] = counts.get(element, 0) + 1

    if not counts:
        return "No mode"

    max_count = max(counts.values(), default=0)
    # 与参考实现保持一致的语义：当 max_count < 1（不会发生）或没有重复元素时返回 No mode
    if max_count <= 1 and len(values) > 1:
        return "No mode"

    modes = [k for k, v in counts.items() if v == max_count]
    return modes if modes else "No mode"


@dataclass
class BasicMeansResult:
    mean_x1: float
    mean_x2: float
    median_x1: Number
    median_x2: Number
    mode_x1: Union[str, List[Number]]
    mode_x2: Union[str, List[Number]]
    gmean_x1: float
    gmean_x2: float
    hmean_x1: float
    hmean_x2: float


def demo_basic_means() -> BasicMeansResult:
    """基础统计量演示，提炼自参考示例。

    本函数演示五种重要的集中趋势度量：

    1. 算术平均数 (Arithmetic Mean)：
       - 数学期望的无偏估计
       - 公式：μ = Σxi / n
       - 特点：对异常值敏感，适合正态分布数据

    2. 中位数 (Median)：
       - 50% 分位数，稳健统计量
       - 特点：对异常值不敏感，适合偏态分布

    3. 众数 (Mode)：
       - 最频繁出现的值
       - 特点：可用于分类数据，可能不存在或有多个

    4. 几何平均数 (Geometric Mean)：
       - 增长率的平均，考虑复利效应
       - 公式：G = (∏xi)^(1/n)
       - 特点：适合比率数据，G ≤ 算术平均

    5. 调和平均数 (Harmonic Mean)：
       - 倒数的算术平均的倒数
       - 公式：H = n / Σ(1/xi)
       - 特点：对小值敏感，H ≤ G ≤ A

    演示数据：
    - x1 = [1,2,2,3,4,5,5,7]：正常分布，有众数
    - x2 = x1 + [100]：添加异常值，观察各统计量的变化

    返回：
        BasicMeansResult: 包含所有统计量的结果对象
    """
    x1 = [1, 2, 2, 3, 4, 5, 5, 7]
    x2 = x1 + [100]

    mean_x1 = float(np.mean(x1))
    mean_x2 = float(np.mean(x2))

    median_x1 = np.median(x1)
    median_x2 = np.median(x2)

    mode_x1 = calculate_mode(x1)
    mode_x2 = calculate_mode(x2)

    gmean_x1 = float(stats.gmean(x1))
    gmean_x2 = float(stats.gmean(x2))

    hmean_x1 = float(stats.hmean(x1))
    hmean_x2 = float(stats.hmean(x2))

    return BasicMeansResult(
        mean_x1=mean_x1,
        mean_x2=mean_x2,
        median_x1=median_x1,
        median_x2=median_x2,
        mode_x1=mode_x1,
        mode_x2=mode_x2,
        gmean_x1=gmean_x1,
        gmean_x2=gmean_x2,
        hmean_x1=hmean_x1,
        hmean_x2=hmean_x2,
    )


@dataclass
class FinanceMeansResult:
    mean: float
    median: float
    mode: Union[str, List[Number]]
    geometric_mean_return: float
    actual_final_price: float
    gmean_check_price: float
    periods: int


def demo_finance_means(
    ticker: str = "SPY",
    start: str = "2014-01-01",
    end: str = "2015-01-01",
) -> FinanceMeansResult:
    """下载金融数据并计算收益率的均值/中位数/众数与几何平均收益率。

    金融时间序列分析的核心概念：

    1. 简单收益率计算：
       - 公式：R_t = (P_t - P_{t-1}) / P_{t-1}
       - 意义：单期相对收益，便于不同资产比较
       - 特点：可加性，适合组合分析

    2. 收益率统计特征：
       - 均值：期望收益率，用于资产配置决策
       - 中位数：稳健的中心趋势，不受极端值影响
       - 众数：最常见的收益率，反映市场"正常"状态

    3. 几何平均收益率：
       - 公式：R_g = [(1+R₁)(1+R₂)...(1+Rₙ)]^(1/n) - 1
       - 意义：复合年增长率，考虑复利效应
       - 应用：业绩评估、长期投资规划

    4. 验证机制：
       - 通过几何平均收益率反推最终价格
       - 公式：P_T = P_0 × (1 + R_g)^T
       - 目的：确保计算的准确性和一致性

    5. SPY ETF 特点：
       - 跟踪标普500指数，代表美国大盘股表现
       - 高流动性，低费用，是理想的基准资产
       - 包含500家大型企业，分散化程度高

    金融直觉：
    - 几何平均 < 算术平均：波动拖累效应
    - 中位数接近均值：收益率分布相对对称
    - 众数的存在：市场存在"正常"收益率区间

    参数：
        ticker: 股票/ETF代码，默认SPY
        start: 开始日期，格式'YYYY-MM-DD'
        end: 结束日期，格式'YYYY-MM-DD'

    返回：
        FinanceMeansResult: 包含各种统计量和验证结果

    异常：
        RuntimeError: yfinance未安装或数据获取失败

    返回值中包含用几何平均收益率反推的价格检验，以对照验证计算。
    """
    if not YFINANCE_AVAILABLE:
        raise RuntimeError(
            "yfinance 未安装，无法执行金融数据示例。请先安装：uv add yfinance",
        )

    data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=True,  # 显式指定以避免默认值变更告警
    )
    if data.empty:
        raise RuntimeError("下载到的行情数据为空，请检查代码或网络环境。")

    prices = data["Close"].astype(float)
    returns = prices.pct_change().dropna()

    if returns.empty:
        raise RuntimeError("收益率序列为空，请检查时间范围或数据可用性。")

    # ═══════════════════════════════════════════════════════════════════════════
    #                           收益率统计量计算
    # ═══════════════════════════════════════════════════════════════════════════

    # 1. 算术平均收益率 (期望收益率)
    # 公式：E[R] = (1/n) × Σ R_i
    # 金融意义：未来收益率的期望值，用于资产配置和风险调整
    # 特点：对极端值敏感，可能高估或低估长期收益
    mean_value = float(np.mean(returns.to_numpy()))

    # 2. 中位数收益率 (稳健中心趋势)
    # 定义：将收益率排序后的中位数
    # 金融意义：50%的交易日收益率低于此值，50%高于此值
    # 特点：对异常值不敏感，更稳健的中心度量
    median_value = float(np.median(returns.to_numpy()))

    # 3. 众数收益率 (最常见收益率)
    # 为了分组更稳定，对收益率四舍五入到 4 位小数 (0.01% 精度)
    # 金融意义：市场"正常"状态下最可能出现的收益率水平
    # 应用：识别市场的典型表现，发现多峰分布(多种市场状态)
    mode_array = np.asarray(returns.round(4).to_numpy(), dtype=float).reshape(-1)
    mode_value = calculate_mode(mode_array.tolist())

    # ═══════════════════════════════════════════════════════════════════════════
    #                        几何平均收益率计算与验证
    # ═══════════════════════════════════════════════════════════════════════════

    # 4. 几何平均收益率 (复合增长率)
    # 公式：R_g = [(1+R₁)(1+R₂)...(1+Rₙ)]^(1/n) - 1
    #      = [∏(1+R_i)]^(1/n) - 1
    # 等价于：gmean(1 + r) - 1
    #
    # 数学原理：
    # - 将乘性过程转换为几何平均
    # - 考虑复利效应，反映真实的长期增长率
    # - 总是 ≤ 算术平均收益率 (AM-GM不等式)
    #
    # 金融意义：
    # - 时间加权收益率，消除现金流时间影响
    # - 长期投资的实际年化收益率
    # - 复利增长的平均速度
    gmean_val = stats.gmean(returns.to_numpy() + 1.0)
    gmean_scalar = np.squeeze(np.asarray(gmean_val)).item()
    geo_mean_return = gmean_scalar - 1.0

    # ═══════════════════════════════════════════════════════════════════════════
    #                            价格路径验证
    # ═══════════════════════════════════════════════════════════════════════════

    # 提取关键价格点进行验证
    initial_price = np.asarray(prices.to_numpy()[0]).item()  # 期初价格
    final_price = np.asarray(prices.to_numpy()[-1]).item()  # 期末价格
    T = returns.shape[0]  # 交易期数

    # 几何平均收益率验证公式：
    # P_T = P_0 × (1 + R_g)^T
    #
    # 验证逻辑：
    # - 如果几何平均收益率计算正确，反推的价格应该等于实际最终价格
    # - 误差来源：数值精度、复利计算的累积误差
    # - 通常误差应该很小 (< 0.01%)
    calculated_price = float(initial_price * (1.0 + geo_mean_return) ** T)

    # 验证说明：
    # calculated_price ≈ final_price 说明几何平均收益率计算正确
    # 如果差异较大，可能存在：
    # 1. 数据质量问题（分红、拆股等未调整）
    # 2. 计算精度问题
    # 3. 时间序列不连续

    return FinanceMeansResult(
        mean=mean_value,
        median=median_value,
        mode=mode_value,
        geometric_mean_return=geo_mean_return,
        actual_final_price=final_price,
        gmean_check_price=calculated_price,
        periods=T,
    )


def _print_basic_result(result: BasicMeansResult) -> None:
    print("\n" + "=" * 60)
    print("基础统计量示例结果分析")
    print("=" * 60)

    print("\n📊 数据集对比：")
    print("   x1 = [1,2,2,3,4,5,5,7] (正常数据)")
    print("   x2 = x1 + [100] (添加异常值)")

    print("\n📈 算术平均数 (对异常值敏感)：")
    print(f"   x1: {result.mean_x1:.2f} | x2: {result.mean_x2:.2f}")
    print(
        f"   📝 异常值影响：{result.mean_x2 - result.mean_x1:.2f} (+{(result.mean_x2 / result.mean_x1 - 1) * 100:.0f}%)",
    )

    print("\n📊 中位数 (对异常值稳健)：")
    print(f"   x1: {result.median_x1} | x2: {result.median_x2}")
    print("   📝 稳健性：几乎不受异常值影响")

    print("\n🎯 众数 (最频繁值)：")
    print(f"   x1: {result.mode_x1} | x2: {result.mode_x2}")
    print("   📝 解释：[2,5] 表示有两个众数，都出现2次")

    print("\n📐 几何平均数 (增长率平均)：")
    print(f"   x1: {result.gmean_x1:.2f} | x2: {result.gmean_x2:.2f}")
    print("   📝 特性：G < 算术平均 (AM-GM不等式)")

    print("\n⚖️  调和平均数 (倒数的平均)：")
    print(f"   x1: {result.hmean_x1:.2f} | x2: {result.hmean_x2:.2f}")
    print("   📝 关系：调和 ≤ 几何 ≤ 算术 平均")

    print("\n🔍 数学关系验证：")
    print(
        f"   x1: {result.hmean_x1:.2f} ≤ {result.gmean_x1:.2f} ≤ {result.mean_x1:.2f}",
    )
    print(
        f"   x2: {result.hmean_x2:.2f} ≤ {result.gmean_x2:.2f} ≤ {result.mean_x2:.2f}",
    )

    print("\n💡 关键洞察：")
    print(
        f"   • 异常值对算术平均影响最大 (+{(result.mean_x2 / result.mean_x1 - 1) * 100:.0f}%)",
    )
    print("   • 中位数最稳健，几乎不变")
    print("   • 几何平均介于两者之间")
    print("   • 三种平均数的大小关系始终成立")


def _print_finance_result(result: FinanceMeansResult) -> None:
    print("\n" + "=" * 60)
    print("SPY ETF 收益率分析结果")
    print("=" * 60)

    # 计算年化指标
    annual_mean = result.mean * 252
    annual_geom = ((1 + result.geometric_mean_return) ** 252) - 1
    price_error = abs(result.actual_final_price - result.gmean_check_price)
    price_error_pct = (price_error / result.actual_final_price) * 100

    print("\n📊 收益率统计特征：")
    print(f"   样本期数: {result.periods} 个交易日")
    print(f"   数据期间: 约 {result.periods / 252:.1f} 年")

    print("\n📈 日收益率分析：")
    print(f"   算术平均: {result.mean:.4f} ({result.mean * 100:.2f}%)")
    print(f"   中 位 数: {result.median:.4f} ({result.median * 100:.2f}%)")
    print(f"   众    数: {result.mode}")
    print(
        f"   几何平均: {result.geometric_mean_return:.4f} ({result.geometric_mean_return * 100:.2f}%)",
    )

    print("\n📅 年化收益率 (252个交易日)：")
    print(f"   算术平均年化: {annual_mean:.4f} ({annual_mean * 100:.2f}%)")
    print(f"   几何平均年化: {annual_geom:.4f} ({annual_geom * 100:.2f}%)")
    print(f"   📝 差异: {(annual_mean - annual_geom) * 100:.2f}% (波动拖累效应)")

    print("\n💰 价格验证：")
    print(f"   实际最终价格: ${result.actual_final_price:.2f}")
    print(f"   几何平均验证: ${result.gmean_check_price:.2f}")
    print(f"   绝对误差: ${price_error:.2f}")
    print(f"   相对误差: {price_error_pct:.4f}%")
    if price_error_pct < 0.01:
        print("   ✅ 验证通过：误差极小，计算正确")
    else:
        print("   ⚠️  验证警告：误差较大，请检查数据质量")

    print("\n🔍 金融直觉解读：")
    if result.mean > result.median:
        print("   • 均值 > 中位数：收益率呈右偏分布 (正偏态)")
        print("   • 解释：存在少数大涨日拉高平均收益")
    elif result.mean < result.median:
        print("   • 均值 < 中位数：收益率呈左偏分布 (负偏态)")
        print("   • 解释：存在少数大跌日拉低平均收益")
    else:
        print("   • 均值 ≈ 中位数：收益率分布相对对称")

    print(f"   • 几何平均 < 算术平均：{(annual_mean - annual_geom) * 100:.2f}%")
    print("   • 这是'波动拖累'：波动性降低复合增长率")
    print("   • 众数显示最常见的收益率水平")

    print("\n💡 投资启示：")
    if annual_geom > 0:
        print(f"   ✅ 长期趋势：年化复合收益率 +{annual_geom * 100:.2f}%")
        print("   📈 投资建议：适合长期持有的优质资产")
    else:
        print(f"   ❌ 长期趋势：年化复合收益率 {annual_geom * 100:.2f}%")
        print("   📉 投资警示：该期间表现不佳")

    print("   • 几何平均更适合评估长期投资表现")
    print("   • 算术平均更适合短期期望收益估算")
    print("   • 中位数提供稳健的收益率预期")


def main() -> None:
    # 1) 基础统计量演示
    basic = demo_basic_means()
    _print_basic_result(basic)

    # 2) 金融数据演示
    if YFINANCE_AVAILABLE:
        try:
            finance = demo_finance_means()
            _print_finance_result(finance)
        except Exception as exc:  # 避免裸 except，打印明确错误
            print(f"\n金融数据示例运行失败: {exc}")
            print("提示：检查网络或使用 'uv add yfinance' 安装依赖后重试。")
    else:
        print("\n跳过金融数据示例：未安装 yfinance，运行 'uv add yfinance' 后重试。")


if __name__ == "__main__":
    main()
