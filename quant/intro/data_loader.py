"""
数据获取模块 - 股票数据的同步和异步获取
"""

import yfinance as yf
import pandas as pd
import asyncio
import sys
from datetime import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from quant.intro.factors import TechnicalFactors, FactorValidator

# 尝试导入 uvloop（仅在非 Windows 系统）
try:
    if sys.platform != "win32":
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class DataPeriodCalculator:
    """数据周期计算器"""

    @staticmethod
    def calculate_period(lookback_days: int) -> str:
        """
        根据回测天数计算合适的数据获取周期

        Args:
            lookback_days: 回看天数

        Returns:
            yfinance 支持的周期字符串
        """
        # 为了确保有足够的数据，我们获取比回测天数多 50% 的数据
        required_days = int(lookback_days * 1.5)

        if required_days <= 5:
            return "5d"
        elif required_days <= 30:
            return "1mo"
        elif required_days <= 90:
            return "3mo"
        elif required_days <= 180:
            return "6mo"
        elif required_days <= 365:
            return "1y"
        elif required_days <= 730:
            return "2y"
        elif required_days <= 1095:  # 3年
            return "5y"
        elif required_days <= 1825:  # 5年
            return "5y"
        elif required_days <= 3650:  # 10年
            return "10y"
        else:
            return "max"  # 获取所有可用数据


class StockDataLoader:
    """股票数据加载器"""

    def __init__(
        self, period_type: str = "days", start_date: Optional[pd.Timestamp] = None,
    ):
        """
        初始化数据加载器

        Args:
            period_type: 期间类型 ("days" 或 "date")
            start_date: 开始日期（时间戳模式）
        """
        self.period_type = period_type
        self.start_date = start_date

    def fetch_single_stock(
        self, ticker: str, period: str, lookback_days: int, max_retries: int = 2,
    ) -> Optional[pd.DataFrame]:
        """
        获取单只股票数据

        Args:
            ticker: 股票代码
            period: 数据周期
            lookback_days: 回看天数
            max_retries: 最大重试次数

        Returns:
            处理后的股票数据或 None
        """
        for attempt in range(max_retries):
            try:
                # 根据期间类型获取数据
                if self.period_type == "date" and self.start_date:
                    # 使用具体开始日期
                    end_date = datetime.now()
                    raw_data = yf.download(
                        ticker,
                        start=self.start_date.strftime("%Y-%m-%d"),
                        end=end_date.strftime("%Y-%m-%d"),
                        progress=False,
                    )
                else:
                    # 使用相对周期，对于长期回测，尝试获取更多数据
                    if lookback_days >= 365:
                        # 长期回测，强制获取最大可用数据
                        try:
                            print(f"  长期回测 {ticker}，获取最大历史数据...")
                            raw_data = yf.download(ticker, period="max", progress=False)
                            print(f"  {ticker} 获取到 {len(raw_data)} 条历史记录")

                            # 对于长期回测，如果数据仍不足，尝试不同的策略
                            if len(raw_data) < lookback_days:
                                print(
                                    f"  {ticker} 历史数据不足({len(raw_data)}天)，尝试获取可用的最大范围",
                                )
                                # 即使数据不足，也尝试使用所有可用数据
                                if len(raw_data) >= 30:  # 至少需要30天数据
                                    print(
                                        f"  {ticker} 使用可用的 {len(raw_data)} 天数据进行分析",
                                    )
                                else:
                                    print(
                                        f"  {ticker} 数据过少({len(raw_data)}天)，跳过",
                                    )
                                    if attempt < max_retries - 1:
                                        continue
                                    return None
                        except Exception as e:
                            print(
                                f"  {ticker} 获取max数据失败: {str(e)}，回退到指定周期",
                            )
                            # 如果max失败，使用指定周期
                            raw_data = yf.download(
                                ticker, period=period, progress=False,
                            )
                    else:
                        # 短期回测，使用指定周期
                        raw_data = yf.download(ticker, period=period, progress=False)

                # 验证数据
                if raw_data.empty:
                    if attempt < max_retries - 1:
                        print(f"  重试获取 {ticker} 数据 (第{attempt + 1}次)")
                        continue
                    return None

                # 数据清洗和处理
                raw_data = raw_data.dropna()

                # 确保数据有足够的记录
                if not FactorValidator.validate_data_quality(raw_data, min_records=2):
                    if attempt < max_retries - 1:
                        print(f"  {ticker} 数据质量不足，重试 (第{attempt + 1}次)")
                        continue
                    return None

                # 添加技术指标
                processed_data = TechnicalFactors.add_all_indicators(raw_data)

                return processed_data

            except Exception as e:
                if attempt < max_retries - 1:
                    print(
                        f"  获取 {ticker} 数据出错，重试 (第{attempt + 1}次): {str(e)}",
                    )
                    continue
                else:
                    print(f"获取 {ticker} 单只股票数据时出错: {str(e)}")
                    return None

        return None

    def fetch_stocks_sync(
        self, tickers: List[str], lookback_days: int, period: str = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        同步获取多只股票数据

        Args:
            tickers: 股票代码列表
            lookback_days: 回看天数
            period: 数据获取周期

        Returns:
            包含各股票数据的字典
        """
        try:
            if period is None:
                period = DataPeriodCalculator.calculate_period(lookback_days)

            print(f"正在获取 {len(tickers)} 只股票的数据 (周期: {period})...")

            # 根据期间类型获取数据
            if self.period_type == "date" and self.start_date:
                # 使用具体开始日期
                end_date = datetime.now()
                raw_data = yf.download(
                    tickers,
                    start=self.start_date.strftime("%Y-%m-%d"),
                    end=end_date.strftime("%Y-%m-%d"),
                    group_by="ticker",
                    progress=False,
                )
            else:
                # 使用相对周期
                raw_data = yf.download(
                    tickers,
                    period=period,
                    group_by="ticker",
                    progress=False,
                )

            if raw_data.empty:
                raise ValueError("无法获取股票数据，请检查股票代码是否正确")

            # 使用 pandas 处理数据
            processed_data = {}
            for ticker in tickers:
                try:
                    if len(tickers) == 1:
                        ticker_data = raw_data
                    else:
                        ticker_data = raw_data[ticker]

                    # 数据清洗和处理
                    ticker_data = ticker_data.dropna()

                    # 验证数据质量
                    if not FactorValidator.validate_data_quality(ticker_data):
                        print(f"✗ {ticker} 数据质量不符合要求，跳过")
                        continue

                    # 添加技术指标
                    ticker_data = TechnicalFactors.add_all_indicators(ticker_data)

                    processed_data[ticker] = ticker_data
                    print(f"✓ 成功获取 {ticker} 数据: {len(ticker_data)} 条记录")

                except Exception as e:
                    print(f"✗ 获取 {ticker} 数据失败: {str(e)}")
                    continue

            if not processed_data:
                raise ValueError("所有股票数据获取失败")

            return processed_data

        except Exception as e:
            if "No data found" in str(e):
                raise ValueError(f"未找到股票数据，请检查股票代码: {tickers}")
            elif "Connection" in str(e):
                raise ConnectionError(f"网络连接失败: {str(e)}")
            else:
                raise ValueError(f"数据获取失败: {str(e)}")

    async def fetch_stocks_async(
        self,
        tickers: List[str],
        lookback_days: int,
        period: str = None,
        max_workers: int = 5,
    ) -> Dict[str, pd.DataFrame]:
        """
        异步获取多只股票数据

        Args:
            tickers: 股票代码列表
            lookback_days: 回看天数
            period: 数据获取周期
            max_workers: 最大并发数

        Returns:
            包含各股票数据的字典
        """
        try:
            if period is None:
                period = DataPeriodCalculator.calculate_period(lookback_days)

            print(
                f"正在异步获取 {len(tickers)} 只股票的数据 (周期: {period}, 并发数: {max_workers})...",
            )

            # 使用线程池执行器进行并发下载
            loop = asyncio.get_event_loop()

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 创建异步任务
                tasks = []
                for ticker in tickers:
                    task = loop.run_in_executor(
                        executor, self.fetch_single_stock, ticker, period, lookback_days,
                    )
                    tasks.append((ticker, task))

                # 等待所有任务完成
                processed_data = {}
                for ticker, task in tasks:
                    try:
                        result = await task
                        if result is not None:
                            processed_data[ticker] = result
                            print(f"✓ 成功获取 {ticker} 数据: {len(result)} 条记录")
                        else:
                            print(f"✗ 获取 {ticker} 数据失败")
                    except Exception as e:
                        print(f"✗ 获取 {ticker} 数据异常: {str(e)}")

            if not processed_data:
                raise ValueError("所有股票数据获取失败")

            return processed_data

        except Exception as e:
            raise ValueError(f"异步数据获取失败: {str(e)}")


class DataManager:
    """数据管理器 - 统一的数据获取接口"""

    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}

    def get_data_loader(
        self, period_type: str = "days", start_date: Optional[pd.Timestamp] = None,
    ) -> StockDataLoader:
        """
        获取数据加载器实例

        Args:
            period_type: 期间类型
            start_date: 开始日期

        Returns:
            数据加载器实例
        """
        return StockDataLoader(period_type=period_type, start_date=start_date)

    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()

    def get_cache_info(self) -> Dict:
        """
        获取缓存信息

        Returns:
            缓存信息字典
        """
        return {
            "cached_tickers": list(self.cache.keys()),
            "cache_size": len(self.cache),
            "total_records": sum(len(data) for data in self.cache.values()),
        }
