import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import warnings

# 忽略 yfinance 的警告信息
warnings.filterwarnings("ignore")


class MomentumStrategy:
    """
    动量策略类 - 基于历史价格动量选择股票
    """

    def __init__(self, lookback_days: int = 60, top_n: int = 3):
        """
        初始化动量策略

        Args:
            lookback_days: 回看天数，用于计算动量
            top_n: 选择排名前 N 的股票
        """
        self.lookback_days = lookback_days
        self.top_n = top_n
        self.stock_data: Dict[str, pd.DataFrame] = {}
        self.momentum_scores: Dict[str, float] = {}

    def fetch_stock_data(
        self, tickers: List[str], period: str = "1y",
    ) -> Dict[str, pd.DataFrame]:
        """
        获取多只股票的历史数据并使用 pandas 处理

        Args:
            tickers: 股票代码列表
            period: 数据获取周期

        Returns:
            包含各股票数据的字典

        Raises:
            ValueError: 当无法获取股票数据时
            ConnectionError: 当网络连接失败时
        """
        try:
            print(f"正在获取 {len(tickers)} 只股票的数据...")

            # 使用 yfinance 批量下载数据
            raw_data = yf.download(
                tickers, period=period, group_by="ticker", progress=False,
            )

            if raw_data.empty:
                raise ValueError("无法获取股票数据，请检查股票代码是否正确")

            # 使用 pandas 处理数据
            processed_data = {}
            for ticker in tickers:
                try:
                    if len(tickers) == 1:
                        # 单只股票的情况
                        ticker_data = raw_data
                    else:
                        # 多只股票的情况
                        ticker_data = raw_data[ticker]

                    # 数据清洗和处理
                    ticker_data = ticker_data.dropna()  # 删除缺失值

                    # 添加技术指标
                    ticker_data = self._add_technical_indicators(ticker_data)

                    processed_data[ticker] = ticker_data
                    print(f"✓ 成功获取 {ticker} 数据: {len(ticker_data)} 条记录")

                except Exception as e:
                    print(f"✗ 获取 {ticker} 数据失败: {str(e)}")
                    continue

            if not processed_data:
                raise ValueError("所有股票数据获取失败")

            self.stock_data = processed_data
            return processed_data

        except Exception as e:
            if "No data found" in str(e):
                raise ValueError(f"未找到股票数据，请检查股票代码: {tickers}")
            elif "Connection" in str(e):
                raise ConnectionError(f"网络连接失败: {str(e)}")
            else:
                raise ValueError(f"数据获取失败: {str(e)}")

    def _add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        使用 pandas 添加技术指标

        Args:
            data: 原始股票数据

        Returns:
            添加技术指标后的数据
        """
        try:
            # 计算移动平均线
            data["MA_5"] = data["Close"].rolling(window=5).mean()
            data["MA_20"] = data["Close"].rolling(window=20).mean()

            # 计算收益率
            data["Daily_Return"] = data["Close"].pct_change()

            # 计算波动率 (20日滚动标准差)
            data["Volatility"] = data["Daily_Return"].rolling(window=20).std()

            # 计算 RSI (相对强弱指数)
            data["RSI"] = self._calculate_rsi(data["Close"])

            return data
        except Exception as e:
            print(f"添加技术指标时出错: {str(e)}")
            return data

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        计算 RSI 指标

        Args:
            prices: 价格序列
            period: 计算周期

        Returns:
            RSI 值序列
        """
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception:
            return pd.Series(index=prices.index, dtype=float)

    def calculate_momentum(self, tickers: List[str]) -> Dict[str, float]:
        """
        计算股票动量得分

        Args:
            tickers: 股票代码列表

        Returns:
            股票动量得分字典
        """
        if not self.stock_data:
            self.fetch_stock_data(tickers)

        momentum_scores = {}

        for ticker in tickers:
            try:
                if ticker not in self.stock_data:
                    print(f"警告: {ticker} 数据不存在，跳过")
                    continue

                data = self.stock_data[ticker]
                closes = data["Close"]

                if len(closes) < self.lookback_days:
                    print(f"警告: {ticker} 数据不足 {self.lookback_days} 天，跳过")
                    continue

                # 计算动量得分 (价格变化率)
                start_price = closes.iloc[-self.lookback_days]
                end_price = closes.iloc[-1]
                momentum = (end_price - start_price) / start_price

                momentum_scores[ticker] = momentum

            except Exception as e:
                print(f"计算 {ticker} 动量时出错: {str(e)}")
                continue

        self.momentum_scores = momentum_scores
        return momentum_scores

    def get_top_stocks(self, tickers: List[str]) -> List[Tuple[str, float]]:
        """
        获取动量排名前 N 的股票

        Args:
            tickers: 股票代码列表

        Returns:
            排序后的股票列表 (股票代码, 动量得分)
        """
        try:
            momentum_scores = self.calculate_momentum(tickers)

            if not momentum_scores:
                raise ValueError("无法计算任何股票的动量得分")

            # 按动量得分排序
            sorted_stocks = sorted(
                momentum_scores.items(), key=lambda x: x[1], reverse=True,
            )

            return sorted_stocks[: self.top_n]

        except Exception as e:
            print(f"获取顶级股票时出错: {str(e)}")
            return []

    def visualize_strategy(
        self, tickers: List[str], save_path: Optional[str] = None,
    ) -> None:
        """
        可视化策略结果

        Args:
            tickers: 股票代码列表
            save_path: 图片保存路径 (可选)
        """
        try:
            # 设置中文字体
            plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei"]
            plt.rcParams["axes.unicode_minus"] = False

            # 获取顶级股票
            top_stocks = self.get_top_stocks(tickers)

            if not top_stocks:
                print("无法生成可视化图表: 没有有效的股票数据")
                return

            # 创建子图
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle(
                f"动量策略分析 (回看期: {self.lookback_days} 天)",
                fontsize=16,
                fontweight="bold",
            )

            # 1. 动量得分柱状图
            ax1 = axes[0, 0]
            stocks, scores = zip(*top_stocks) if top_stocks else ([], [])
            colors = ["green" if score > 0 else "red" for score in scores]
            bars = ax1.bar(
                stocks, [score * 100 for score in scores], color=colors, alpha=0.7,
            )
            ax1.set_title("动量得分排名 (%)")
            ax1.set_ylabel("动量得分 (%)")
            ax1.tick_params(axis="x", rotation=45)

            # 添加数值标签
            for bar, score in zip(bars, scores):
                height = bar.get_height()
                ax1.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + (0.5 if height > 0 else -1.5),
                    f"{score * 100:.1f}%",
                    ha="center",
                    va="bottom" if height > 0 else "top",
                )

            # 2. 价格走势图 (前3只股票)
            ax2 = axes[0, 1]
            for i, (ticker, _) in enumerate(top_stocks[:3]):
                if ticker in self.stock_data:
                    data = self.stock_data[ticker]["Close"].tail(60)  # 最近60天
                    ax2.plot(data.index, data.values, label=ticker, linewidth=2)

            ax2.set_title("前3只股票价格走势 (近60天)")
            ax2.set_ylabel("价格 ($)")
            ax2.legend()
            ax2.tick_params(axis="x", rotation=45)

            # 3. 波动率对比
            ax3 = axes[1, 0]
            volatilities = []
            stock_names = []

            for ticker, _ in top_stocks:
                if (
                    ticker in self.stock_data
                    and "Volatility" in self.stock_data[ticker].columns
                ):
                    vol = self.stock_data[ticker]["Volatility"].iloc[-1]
                    if not pd.isna(vol):
                        volatilities.append(vol * 100)
                        stock_names.append(ticker)

            if volatilities:
                ax3.bar(stock_names, volatilities, color="orange", alpha=0.7)
                ax3.set_title("股票波动率对比 (%)")
                ax3.set_ylabel("波动率 (%)")
                ax3.tick_params(axis="x", rotation=45)

            # 4. RSI 指标
            ax4 = axes[1, 1]
            for i, (ticker, _) in enumerate(top_stocks[:3]):
                if (
                    ticker in self.stock_data
                    and "RSI" in self.stock_data[ticker].columns
                ):
                    rsi_data = self.stock_data[ticker]["RSI"].tail(30)  # 最近30天
                    ax4.plot(rsi_data.index, rsi_data.values, label=ticker, linewidth=2)

            # 添加 RSI 参考线
            ax4.axhline(y=70, color="r", linestyle="--", alpha=0.5, label="超买线(70)")
            ax4.axhline(y=30, color="g", linestyle="--", alpha=0.5, label="超卖线(30)")
            ax4.set_title("RSI 指标对比 (近30天)")
            ax4.set_ylabel("RSI")
            ax4.legend()
            ax4.tick_params(axis="x", rotation=45)
            ax4.set_ylim(0, 100)

            plt.tight_layout()

            # 保存图片
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")
                print(f"图表已保存至: {save_path}")
            else:
                # 默认保存到当前目录
                default_path = (
                    f"momentum_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                plt.savefig(default_path, dpi=300, bbox_inches="tight")
                print(f"图表已保存至: {default_path}")

            plt.close()  # 关闭图形以释放内存

        except Exception as e:
            print(f"可视化过程中出错: {str(e)}")

    def generate_report(self, tickers: List[str]) -> str:
        """
        生成策略分析报告

        Args:
            tickers: 股票代码列表

        Returns:
            分析报告字符串
        """
        try:
            top_stocks = self.get_top_stocks(tickers)

            if not top_stocks:
                return "无法生成报告: 没有有效的股票数据"

            report = []
            report.append("=" * 50)
            report.append("动量策略分析报告")
            report.append("=" * 50)
            report.append(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"回看期: {self.lookback_days} 天")
            report.append(f"分析股票数: {len(tickers)}")
            report.append(f"推荐股票数: {len(top_stocks)}")
            report.append("")

            report.append("推荐股票排名:")
            report.append("-" * 30)

            for i, (ticker, score) in enumerate(top_stocks, 1):
                report.append(f"{i}. {ticker}: {score * 100:+.2f}%")

                # 添加额外信息
                if ticker in self.stock_data:
                    data = self.stock_data[ticker]
                    current_price = data["Close"].iloc[-1]

                    # 获取技术指标
                    rsi = (
                        data["RSI"].iloc[-1]
                        if "RSI" in data.columns and not pd.isna(data["RSI"].iloc[-1])
                        else None
                    )
                    volatility = (
                        data["Volatility"].iloc[-1]
                        if "Volatility" in data.columns
                        and not pd.isna(data["Volatility"].iloc[-1])
                        else None
                    )

                    report.append(f"   当前价格: ${current_price:.2f}")
                    if rsi is not None:
                        report.append(f"   RSI: {rsi:.1f}")
                    if volatility is not None:
                        report.append(f"   波动率: {volatility * 100:.2f}%")
                    report.append("")

            return "\n".join(report)

        except Exception as e:
            return f"生成报告时出错: {str(e)}"


def main():
    """主函数 - 演示策略使用"""
    try:
        print("🚀 启动动量策略分析...")

        # 创建策略实例
        strategy = MomentumStrategy(lookback_days=60, top_n=3)

        # 定义要分析的股票
        tech_stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOG", "META"]

        print(f"\n📊 分析股票: {', '.join(tech_stocks)}")

        # 获取股票数据
        stock_data = strategy.fetch_stock_data(tech_stocks)

        # 获取推荐股票
        top_stocks = strategy.get_top_stocks(tech_stocks)

        if top_stocks:
            print("\n🎯 推荐关注股票:")
            for i, (ticker, score) in enumerate(top_stocks, 1):
                print(f"   {i}. {ticker}: {score * 100:+.2f}%")

        # 生成分析报告
        report = strategy.generate_report(tech_stocks)
        print(f"\n{report}")

        # 可视化结果
        print("\n📈 生成可视化图表...")
        strategy.visualize_strategy(tech_stocks)

        # 展示苹果公司详细数据
        if "AAPL" in stock_data:
            print("\n🍎 苹果公司最近5个交易日详细数据:")
            aapl_data = stock_data["AAPL"].tail()[
                ["Open", "High", "Low", "Close", "Volume", "Daily_Return"]
            ]
            print(aapl_data.round(2))

    except Exception as e:
        print(f"❌ 程序执行出错: {str(e)}")
        print("请检查网络连接和股票代码是否正确")


if __name__ == "__main__":
    main()
