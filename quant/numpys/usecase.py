"""
NumPy 在量化金融中的应用实例
=================================

本文件展示了 NumPy 在量化分析中的核心应用，包括：
1. 数组基础操作和索引切片
2. 数学函数应用和统计计算
3. 缺失值处理技术
4. 投资组合分析和风险计算
5. 线性代数在金融中的应用

参考资料：WQU Guru - Quantopia量化分析56讲 第3讲：NumPy入门
"""

import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")  # 忽略警告信息

print("=" * 80)
print("NumPy 量化金融应用实例")
print("=" * 80)

# ============================================================================
# 一、NumPy 数组基础
# ============================================================================
print("\n一、NumPy 数组基础")
print("-" * 50)

# 1.1 创建数组
print("1.1 创建数组")
stock_list = [3.5, 5, 2, 8, 4.2]  # 原始股票收益率数据（百分比）
returns = np.array(stock_list)  # 使用 np.array() 将 Python 列表转换为 NumPy 数组
print(f"股票收益率数组: {returns}")
print(f"数组类型: {type(returns)}")
print(f"数组形状: {returns.shape}")
print(f"数组维度: {returns.ndim}")
print(f"数组大小: {returns.size}")

# 创建二维数组示例
A = np.array([[1, 2], [3, 4]])
print(f"\n二维数组 A:\n{A}")
print(f"A 的形状: {A.shape}")  # (行数, 列数)

# 1.2 数组索引与切片
print("\n1.2 数组索引与切片")
print(f"returns[1:3]: {returns[1:3]}")  # 切片操作：获取索引1到2的元素
print(f"A[0, :]: {A[0, :]}")  # 获取第0行的所有列
print(f"A[:, 0]: {A[:, 0]}")  # 获取第0列的所有行

# ============================================================================
# 二、数组运算与统计
# ============================================================================
print("\n\n二、数组运算与统计")
print("-" * 50)

# 2.1 数学函数应用
print("2.1 数学函数应用")
log_returns = np.log(returns[1:3])  # 对数收益率计算，金融中常用于连续复利计算
print(f"对数收益率 ln(returns[1:3]): {log_returns}")
print(f"最大收益率: {np.max(returns)}")

# 更多数学函数示例
print(f"指数函数 exp(returns): {np.exp(returns[:3])}")  # 只显示前3个避免输出过长
print(f"平方根 sqrt(returns): {np.sqrt(returns)}")
print(f"绝对值 abs(returns-5): {np.abs(returns - 5)}")

# 2.2 统计计算
print("\n2.2 统计计算")

# 均值计算 - 数学公式详解：μ = (1/n) * Σxi
# 其中：
# μ (mu) = 总体均值或样本均值
# n = 样本数量（观测值个数）
# Σ (sigma) = 求和符号，表示对所有 i 从 1 到 n 求和
# xi = 第 i 个观测值
#
# 具体展开：μ = (x1 + x2 + x3 + ... + xn) / n
# 在金融中，这通常表示资产的平均收益率或期望收益率
# 例如：如果股票在5天的收益率分别为 [3.5%, 5%, 2%, 8%, 4.2%]
# 那么平均收益率 = (3.5 + 5 + 2 + 8 + 4.2) / 5 = 22.7 / 5 = 4.54%
mean_return = np.mean(returns)
print(f"平均收益率: {mean_return:.4f}")

# 标准差计算 - 数学公式详解：σ = √[(1/n) * Σ(xi - μ)²]
# 其中：
# σ (sigma) = 标准差
# n = 样本数量
# Σ = 求和符号，对所有 i 从 1 到 n 求和
# xi = 第 i 个观测值
# μ = 样本均值
#
# 计算步骤：
# 1. 计算每个观测值与均值的差：(xi - μ)
# 2. 将差值平方：(xi - μ)²
# 3. 对所有平方差求和：Σ(xi - μ)²
# 4. 除以样本数量：(1/n) * Σ(xi - μ)²  (这就是方差)
# 5. 开平方根：√[(1/n) * Σ(xi - μ)²]  (得到标准差)
#
# 在金融中，标准差表示波动率（风险）：
# - 标准差越大，收益率波动越大，风险越高
# - 标准差越小，收益率波动越小，风险越低
# 例如：对于收益率 [3.5, 5, 2, 8, 4.2]，均值 μ = 4.54
# 计算过程：
# (3.5-4.54)² + (5-4.54)² + (2-4.54)² + (8-4.54)² + (4.2-4.54)²
# = 1.0816 + 0.2116 + 6.4516 + 11.9716 + 0.1156
# = 19.832 / 5 = 3.9664
# σ = √3.9664 = 1.9916
std_return = np.std(returns)
print(f"收益率标准差（波动率）: {std_return:.4f}")

# 方差计算 - 数学公式详解：σ² = (1/n) * Σ(xi - μ)²
# 其中：
# σ² (sigma squared) = 方差
# n = 样本数量
# Σ = 求和符号，对所有 i 从 1 到 n 求和
# xi = 第 i 个观测值
# μ = 样本均值
#
# 计算步骤：
# 1. 计算每个观测值与均值的差：(xi - μ)
# 2. 将差值平方：(xi - μ)²
# 3. 对所有平方差求和：Σ(xi - μ)²
# 4. 除以样本数量：(1/n) * Σ(xi - μ)²
#
# 方差与标准差的关系：
# - 方差 = 标准差的平方：σ² = σ × σ
# - 标准差 = 方差的平方根：σ = √σ²
#
# 在金融中，方差同样衡量风险：
# - 方差的单位是收益率的平方，不太直观
# - 因此通常使用标准差（与收益率同单位）来表示风险
# 例如：对于上面的例子，方差 = 3.9664，标准差 = √3.9664 = 1.9916
var_return = np.var(returns)
print(f"收益率方差: {var_return:.4f}")
print(f"验证关系：标准差² = 方差: {std_return**2:.4f} ≈ {var_return:.4f}")

# 其他统计量
print(f"最小值: {np.min(returns):.4f}")
print(f"最大值: {np.max(returns):.4f}")
print(f"中位数: {np.median(returns):.4f}")
print(f"百分位数（25%）: {np.percentile(returns, 25):.4f}")
print(f"百分位数（75%）: {np.percentile(returns, 75):.4f}")

# ============================================================================
# 三、缺失值处理
# ============================================================================
print("\n\n三、缺失值处理")
print("-" * 50)

# 创建包含缺失值的数组
v = np.array([1, 2, np.nan, 4, 5])
print(f"包含 NaN 的数组: {v}")

# 方法1：过滤 NaN 值
# np.isnan() 返回布尔数组，标识哪些元素是 NaN
# ~ 是按位取反运算符，将 True 变为 False，False 变为 True
print(f"NaN 位置标识: {np.isnan(v)}")
print(f"非 NaN 位置标识: {~np.isnan(v)}")

clean_v = v[~np.isnan(v)]  # 布尔索引，只保留非 NaN 的元素
print(f"过滤后的数组: {clean_v}")
print(f"过滤后的均值: {np.mean(clean_v):.4f}")

# 方法2：使用 NumPy 的 nan 函数族
# 这些函数会自动忽略 NaN 值进行计算
print(f"使用 np.nanmean(): {np.nanmean(v):.4f}")
print(f"使用 np.nanstd(): {np.nanstd(v):.4f}")
print(f"使用 np.nanmax(): {np.nanmax(v):.4f}")
print(f"使用 np.nanmin(): {np.nanmin(v):.4f}")

# ============================================================================
# 四、投资组合分析
# ============================================================================
print("\n\n四、投资组合分析")
print("-" * 50)

# 4.1 生成模拟资产数据
print("4.1 生成模拟资产数据")
N = 10  # 投资组合中资产的数量
days = 100  # 观察期的交易日数量

# 创建二维数组存储收益率数据
# 行：资产，列：时间（交易日）
returns_matrix = np.zeros((N, days))
print(f"收益率矩阵形状: {returns_matrix.shape}")

# 设置随机种子以确保结果可重现
np.random.seed(42)

# 生成基准资产的收益率
# 假设基准资产（如市场指数）的日收益率服从正态分布
# 均值 1.01 表示平均日收益率为 1%，标准差 0.03 表示波动率为 3%
base_returns = np.random.normal(1.01, 0.03, days)
returns_matrix[0] = base_returns
print(f"基准资产收益率（前5天）: {base_returns[:5]}")

# 生成其他相关资产的收益率
# 每个资产都与基准资产相关，但有各自的随机扰动
for i in range(1, N):
    # 相关资产 = 基准资产 + 随机噪声
    # 这种方法确保了资产间的相关性
    noise = np.random.normal(0.001, 0.02, days)  # 均值为 0.1%，标准差为 2% 的噪声
    returns_matrix[i] = base_returns + noise

print(f"所有资产收益率矩阵（前3个资产，前5天）:\n{returns_matrix[:3, :5]}")

# 4.2 计算投资组合收益
print("\n4.2 计算投资组合收益")

# 生成随机权重并归一化
# 在实际应用中，权重可能来自优化算法或投资策略
weights = np.random.uniform(0, 1, N)  # 生成 [0,1] 区间的随机权重
weights = weights / weights.sum()  # 归一化：确保权重和为1
print(f"投资组合权重: {weights}")
print(f"权重和验证: {weights.sum():.6f}")

# 计算每个资产的平均收益率
asset_mean_returns = np.array([np.mean(returns_matrix[i]) for i in range(N)])
print(f"各资产平均收益率: {asset_mean_returns}")

# 投资组合期望收益率计算
# 公式：E(Rp) = Σ(wi * E(Ri))，其中 wi 是权重，E(Ri) 是资产 i 的期望收益率
portfolio_expected_return = np.dot(weights, asset_mean_returns)
print(f"投资组合期望收益率: {portfolio_expected_return:.6f}")
print(f"投资组合期望收益率（百分比）: {portfolio_expected_return * 100:.4f}%")

# ============================================================================
# 五、线性代数核心应用
# ============================================================================
print("\n\n五、线性代数核心应用")
print("-" * 50)

# 5.1 矩阵运算基础
print("5.1 矩阵运算基础")

# 创建示例矩阵
np.random.seed(123)  # 设置种子确保结果一致
matrix_A = np.random.rand(3, 5)  # 3×5 矩阵
matrix_B = np.random.rand(5, 2)  # 5×2 矩阵

print(f"矩阵 A 形状: {matrix_A.shape}")
print(f"矩阵 B 形状: {matrix_B.shape}")

# 矩阵乘法：A(m×n) × B(n×p) = C(m×p)
# 要求：A 的列数必须等于 B 的行数
matrix_C = np.dot(matrix_A, matrix_B)  # 或使用 matrix_A @ matrix_B
print(f"矩阵乘积 C = A × B 的形状: {matrix_C.shape}")

# 其他矩阵运算
print(f"矩阵 A 的转置形状: {matrix_A.T.shape}")
print("矩阵 A 的行列式（需要方阵）: 跳过（非方阵）")

# 5.2 投资组合风险计算（协方差矩阵应用）
print("\n5.2 投资组合风险计算")

# 计算协方差矩阵
# 协方差矩阵 Σ 是 N×N 的对称矩阵
# Σij = Cov(Ri, Rj) = E[(Ri - E(Ri))(Rj - E(Rj))]
# 对角线元素是各资产的方差，非对角线元素是资产间的协方差
covariance_matrix = np.cov(returns_matrix)
print(f"协方差矩阵形状: {covariance_matrix.shape}")
print(f"协方差矩阵（前3×3子矩阵）:\n{covariance_matrix[:3, :3]}")

# 验证协方差矩阵的对称性
print(f"协方差矩阵是否对称: {np.allclose(covariance_matrix, covariance_matrix.T)}")

# 提取方差（对角线元素）
asset_variances = np.diag(covariance_matrix)
asset_volatilities = np.sqrt(asset_variances)
print(f"各资产方差: {asset_variances}")
print(f"各资产波动率: {asset_volatilities}")

# 投资组合方差计算
# 公式：σp² = w^T × Σ × w
# 其中 w 是权重向量，Σ 是协方差矩阵
weights_column = weights.reshape(-1, 1)  # 转换为列向量 (N×1)
print(f"权重向量形状: {weights_column.shape}")

# 执行矩阵乘法：w^T × Σ × w
# 步骤1：w^T (1×N) × Σ (N×N) = temp (1×N)
# 步骤2：temp (1×N) × w (N×1) = portfolio_variance (1×1)
portfolio_variance = weights_column.T @ covariance_matrix @ weights_column
print(f"投资组合方差: {portfolio_variance[0, 0]:.8f}")

# 投资组合波动率（标准差）
portfolio_volatility = np.sqrt(portfolio_variance[0, 0])
print(f"投资组合波动率: {portfolio_volatility:.6f}")
print(f"投资组合波动率（百分比）: {portfolio_volatility * 100:.4f}%")

# ============================================================================
# 六、投资组合理论验证
# ============================================================================
print("\n\n六、投资组合理论验证")
print("-" * 50)

# 验证分散化效应：组合风险 < 加权平均风险
weighted_avg_volatility = np.dot(weights, asset_volatilities)
print(f"加权平均波动率: {weighted_avg_volatility:.6f}")
print(f"投资组合波动率: {portfolio_volatility:.6f}")
print(f"分散化效应: {weighted_avg_volatility - portfolio_volatility:.6f}")

if portfolio_volatility < weighted_avg_volatility:
    print("✓ 分散化降低了投资组合风险")
else:
    print("✗ 未观察到明显的分散化效应")

# 计算相关系数矩阵
correlation_matrix = np.corrcoef(returns_matrix)
print(f"\n相关系数矩阵（前3×3子矩阵）:\n{correlation_matrix[:3, :3]}")

# 平均相关系数
upper_triangle = np.triu(correlation_matrix, k=1)  # 上三角矩阵（不包括对角线）
non_zero_correlations = upper_triangle[upper_triangle != 0]
avg_correlation = np.mean(non_zero_correlations)
print(f"资产间平均相关系数: {avg_correlation:.4f}")

# ============================================================================
# 七、高级应用示例
# ============================================================================
print("\n\n七、高级应用示例")
print("-" * 50)

# 7.1 等权重组合 vs 当前组合比较
equal_weights = np.ones(N) / N  # 等权重：每个资产权重为 1/N
equal_portfolio_return = np.dot(equal_weights, asset_mean_returns)
equal_portfolio_variance = equal_weights.T @ covariance_matrix @ equal_weights
equal_portfolio_volatility = np.sqrt(equal_portfolio_variance)

print("7.1 等权重组合 vs 随机权重组合比较")
print(f"等权重组合收益率: {equal_portfolio_return * 100:.4f}%")
print(f"等权重组合波动率: {equal_portfolio_volatility * 100:.4f}%")
print(f"随机权重组合收益率: {portfolio_expected_return * 100:.4f}%")
print(f"随机权重组合波动率: {portfolio_volatility * 100:.4f}%")

# 7.2 夏普比率计算（假设无风险利率为 2%）
risk_free_rate = 0.02 / 252  # 年化 2% 转换为日收益率
equal_sharpe = (equal_portfolio_return - risk_free_rate) / equal_portfolio_volatility
random_sharpe = (portfolio_expected_return - risk_free_rate) / portfolio_volatility

print("\n7.2 夏普比率比较（风险调整后收益）")
print(f"等权重组合夏普比率: {equal_sharpe:.4f}")
print(f"随机权重组合夏普比率: {random_sharpe:.4f}")

# 7.3 VaR (Value at Risk) 计算示例
print("\n7.3 风险价值（VaR）计算")
confidence_level = 0.05  # 95% 置信水平
# 假设收益率服从正态分布
var_95 = portfolio_expected_return + portfolio_volatility * np.percentile(
    np.random.standard_normal(10000),
    confidence_level * 100,
)
print(f"95% 置信水平下的 VaR: {var_95 * 100:.4f}%")

# ============================================================================
# 八、性能优化提示
# ============================================================================
print("\n\n八、NumPy 性能优化提示")
print("-" * 50)

# 8.1 向量化操作 vs 循环
print("8.1 向量化操作性能优势")

# 低效的循环方式（仅作演示，不建议使用）


start_time = time.time()
loop_result = []
for i in range(len(asset_mean_returns)):
    loop_result.append(asset_mean_returns[i] * weights[i])
loop_sum = sum(loop_result)
loop_time = time.time() - start_time

# 高效的向量化操作
start_time = time.time()
vectorized_result = np.dot(weights, asset_mean_returns)
vectorized_time = time.time() - start_time

print(f"循环方式结果: {loop_sum:.8f}, 耗时: {loop_time:.6f}秒")
print(f"向量化结果: {vectorized_result:.8f}, 耗时: {vectorized_time:.6f}秒")
print(f"性能提升: {loop_time / vectorized_time:.2f}倍")

# ============================================================================
# 九、总结和最佳实践
# ============================================================================
print("\n\n九、总结和最佳实践")
print("-" * 50)

print("NumPy 在量化金融中的关键应用：")
print("1. 数组操作：高效处理大规模金融时间序列数据")
print("2. 统计计算：快速计算收益率、波动率等关键指标")
print("3. 线性代数：投资组合优化和风险管理的数学基础")
print("4. 随机模拟：蒙特卡洛方法和情景分析")
print("5. 缺失值处理：清洗和预处理真实市场数据")

print("\n最佳实践建议：")
print("• 优先使用向量化操作而非循环")
print("• 注意矩阵维度匹配，避免广播错误")
print("• 合理使用随机种子确保结果可重现")
print("• 利用 NumPy 的数学函数库进行复杂计算")
print("• 结合 Pandas 处理带标签的金融数据")

print("\n" + "=" * 80)
print("NumPy 量化金融应用实例完成")
print("=" * 80)

if __name__ == "__main__":
    print("\n程序执行完成！")
    print("这个实例展示了 NumPy 在量化金融中的核心应用。")
    print("建议结合实际市场数据进一步练习和探索。")
