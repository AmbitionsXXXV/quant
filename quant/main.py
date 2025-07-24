import numpy as np  # 数值计算
import matplotlib.pyplot as plt  # 可视化
import yfinance as yf


def main():
    start_date = "2022-01-01"
    end_date = "2025-07-24"
    tickers = ["AAPL", "MSFT"]

    stock_data = yf.download(tickers, start=start_date, end=end_date)

    aapl_close = stock_data["Close"]["AAPL"].dropna()
    # msft_close = stock_data["Close"]["MSFT"].dropna()

    # figsize 参数用于设置图表的尺寸，单位是英寸
    # plt.figure(figsize=(10,6))
    # 第一个参数是x轴，第二个参数是y轴
    # plt.plot(aapl_close.index, aapl_close.values)
    # plt.ylabel('Price (USD)')
    # plt.title('AAPL Closing Price 2022-2025');
    # plt.show()

    # pct_change 计算每日收益率
    # dropna 删除缺失值
    daily_returns = aapl_close.pct_change().dropna()
    print(daily_returns)

    # 绘制直方图
    # 怎么看分布？
    # bins 直方图的柱子数量
    # 收益分析计算说明：
    # 1. daily_returns = aapl_close.pct_change() 计算每日收益率
    #    公式：(今日价格 - 昨日价格) / 昨日价格
    # 2. 例如：昨日100元，今日105元，收益率 = (105-100)/100 = 5%

    plt.hist(daily_returns, bins=50, density=True)
    plt.xlabel('Daily Return')
    plt.ylabel('Frequency')
    plt.title('AAPL Daily Returns Distribution')
    plt.show()

    # 计算均值和标准差
    return_mean = np.mean(daily_returns)
    # 标准差 标准差越大，数据越分散，波动越大（波动率）
    # 公式：sqrt(sum((x - mean)^2) / n)
    return_std = np.std(daily_returns)
    print(f"日均收益率: {return_mean:.4%}")
    print(f"日收益波动率: {return_std:.4%}")

    # 交易策略逻辑说明：
    # 这个代码目前只是做收益分析，没有实际的交易策略
    # 但可以基于收益分布制定策略：
    # 1. 均值回归策略：当收益率偏离均值超过1个标准差时，预期会回归
    # 2. 风险管理：利用标准差设置止损点，如超过2倍标准差就止损
    # 3. 正态分布假设：如果收益率服从正态分布，可以计算VaR（风险价值）
    print("\n策略建议:")
    print(f"买入信号阈值: {return_mean - return_std:.4%} (均值-1标准差)")
    print(f"卖出信号阈值: {return_mean + return_std:.4%} (均值+1标准差)")
    print(f"止损阈值: {return_mean - 2*return_std:.4%} (均值-2标准差)")

    # normal_returns = np.random.normal(return_mean, return_std, size=1000)
    # plt.hist(daily_returns, bins=50, density=True, alpha=0.6, label='Actual')
    # plt.hist(normal_returns, bins=50, density=True, alpha=0.5, label='Normal')
    # plt.legend()
    # plt.title('Actual vs Normal Distribution');
    # plt.show()

    # ma_60 = aapl_close.rolling(window=60).mean()
    # ma_200 = aapl_close.rolling(window=200).mean()
    # plt.figure(figsize=(10,6))
    # plt.plot(aapl_close.index, aapl_close.values, label='AAPL')
    # plt.plot(ma_60.index, ma_60.values, label='MA 60')
    # plt.plot(ma_200.index, ma_200.values, label='MA 200')
    # plt.legend()
    # plt.show()


if __name__ == "__main__":
    main()
