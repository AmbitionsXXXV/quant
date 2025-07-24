import yfinance as yf
import matplotlib.pyplot as plt

"""
获取特斯拉(TSLA)2020年至今的日线数据
计算20日移动平均线并绘制价格对比图
统计收益率分布的峰度
比较不同窗口长度（20日 vs 60日）均线的平滑效果差异
"""
tsla = yf.download("TSLA", start="2020-01-01")["Close"]

ma_20 = tsla.rolling(window=20).mean()
ma_60 = tsla.rolling(window=60).mean()

# 绘图比较
plt.figure(figsize=(12,6))
plt.plot(tsla, label='Price')
plt.plot(ma_20, label='20-day MA')
plt.plot(ma_60, label='60-day MA')
plt.legend()
plt.show()

# 计算统计量
returns = tsla.pct_change().dropna()
# 使用 iloc[0] 获取 Series 中的标量值，避免 FutureWarning
kurtosis_val = returns.kurt().iloc[0] if hasattr(returns.kurt(), 'iloc') else float(returns.kurt())
print(f"峰度系数: {kurtosis_val:.2f}")
