"""
策略核心模块 - 动量策略的主要实现
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Union

from quant.intro.data_loader import DataManager
from quant.intro.factors import MomentumFactors, FactorValidator
from quant.intro.visualization import VisualizationManager


class MomentumStrategy:
    """
    动量策略核心类
    整合数据获取、因子计算和可视化功能
    """

    def __init__(self, lookback_period: Union[int, str] = 60, top_n: int = 3):
        """
        初始化动量策略

        Args:
            lookback_period: 回看期间，可以是天数(int)或时间戳字符串(如 '2020-11-01')
            top_n: 选择排名前 N 的股票
        """
        self.lookback_period = lookback_period
        self.top_n = top_n
        self.stock_data: Dict[str, pd.DataFrame] = {}
        self.momentum_scores: Dict[str, float] = {}
        self.tickers: List[str] = []

        # 解析回看期间参数
        self._parse_lookback_period()

        # 初始化组件
        self.data_manager = DataManager()
        self.visualization_manager = VisualizationManager()

        # 获取数据加载器
        self.data_loader = self.data_manager.get_data_loader(
            period_type=self.period_type, start_date=self.start_date,
        )

    def _parse_lookback_period(self) -> None:
        """解析回看期间参数"""
        if isinstance(self.lookback_period, int):
            self.lookback_days = self.lookback_period
            self.start_date = None
            self.period_type = "days"
        elif isinstance(self.lookback_period, str):
            try:
                self.start_date = pd.to_datetime(self.lookback_period)
                actual_days = (datetime.now() - self.start_date).days
                self.lookback_days = actual_days
                self.period_type = "date"
            except Exception:
                raise ValueError(
                    f"无效的时间戳格式: {self.lookback_period}. 请使用 'YYYY-MM-DD' 格式",
                )
        else:
            raise ValueError("lookback_period 必须是整数（天数）或时间戳字符串")

    async def fetch_data_async(
        self, tickers: List[str], max_workers: int = 5,
    ) -> Dict[str, pd.DataFrame]:
        """
        异步获取股票数据

        Args:
            tickers: 股票代码列表
            max_workers: 最大并发数

        Returns:
            股票数据字典
        """
        self.tickers = tickers
        self.stock_data = await self.data_loader.fetch_stocks_async(
            tickers=tickers, lookback_days=self.lookback_days, max_workers=max_workers,
        )
        return self.stock_data

    def fetch_data_sync(self, tickers: List[str]) -> Dict[str, pd.DataFrame]:
        """
        同步获取股票数据

        Args:
            tickers: 股票代码列表

        Returns:
            股票数据字典
        """
        self.tickers = tickers
        self.stock_data = self.data_loader.fetch_stocks_sync(
            tickers=tickers, lookback_days=self.lookback_days,
        )
        return self.stock_data

    def calculate_momentum_scores(self) -> Dict[str, float]:
        """
        计算所有股票的动量得分

        Returns:
            动量得分字典
        """
        if not self.stock_data:
            raise ValueError("请先获取股票数据")

        momentum_scores = {}

        for ticker in self.tickers:
            try:
                if ticker not in self.stock_data:
                    print(f"警告: {ticker} 数据不存在，跳过")
                    continue

                data = self.stock_data[ticker]

                # 验证数据质量
                if not self._validate_stock_data(ticker, data):
                    continue

                # 计算动量得分
                momentum = MomentumFactors.calculate_price_momentum(
                    data=data,
                    lookback_days=self.lookback_days,
                    period_type=self.period_type,
                    start_date=self.start_date,
                )

                momentum_scores[ticker] = momentum

                # 输出调试信息
                if self.lookback_days >= 365 and len(data) < self.lookback_days:
                    print(
                        f"  {ticker} 使用 {len(data)} 天数据计算动量（原计划{self.lookback_days}天）",
                    )

            except Exception as e:
                print(f"计算 {ticker} 动量时出错: {str(e)}")
                continue

        self.momentum_scores = momentum_scores
        return momentum_scores

    def _validate_stock_data(self, ticker: str, data: pd.DataFrame) -> bool:
        """
        验证股票数据是否满足计算要求

        Args:
            ticker: 股票代码
            data: 股票数据

        Returns:
            是否通过验证
        """
        closes = data["Close"]

        # 修复数据长度检查逻辑
        if self.period_type == "date" and self.start_date:
            # 时间戳模式：只要有数据就可以计算
            if len(closes) < 2:
                print(f"警告: {ticker} 数据不足（少于2条记录），跳过")
                return False
        else:
            # 天数模式：对长期回测使用更灵活的要求
            if self.lookback_days >= 365:
                # 长期回测：如果数据不足，但有至少30天，也尝试计算
                if len(closes) < 30:
                    print(
                        f"警告: {ticker} 数据过少（需要至少30天，实际{len(closes)}天），跳过",
                    )
                    return False
                elif len(closes) < self.lookback_days:
                    print(
                        f"注意: {ticker} 数据不足目标天数（目标{self.lookback_days}天，实际{len(closes)}天），使用可用数据",
                    )
            else:
                # 短期回测：需要足够的回看天数
                if len(closes) < self.lookback_days:
                    print(
                        f"警告: {ticker} 数据不足（需要{self.lookback_days}天，实际{len(closes)}天），跳过",
                    )
                    return False

        return True

    def get_top_stocks(self) -> List[Tuple[str, float]]:
        """
        获取动量排名前 N 的股票

        Returns:
            排序后的股票列表 (股票代码, 动量得分)
        """
        try:
            if not self.momentum_scores:
                self.calculate_momentum_scores()

            if not self.momentum_scores:
                raise ValueError("无法计算任何股票的动量得分")

            # 按动量得分排序
            sorted_stocks = sorted(
                self.momentum_scores.items(),
                key=lambda x: x[1],
                reverse=True,
            )

            return sorted_stocks[: self.top_n]

        except Exception as e:
            print(f"获取顶级股票时出错: {str(e)}")
            return []

    def create_visualization(self, save_path: Optional[str] = None) -> str:
        """
        创建可视化图表

        Args:
            save_path: 保存路径

        Returns:
            保存的图片路径
        """
        try:
            top_stocks = self.get_top_stocks()

            if not top_stocks:
                print("无法生成可视化图表: 没有有效的股票数据")
                return ""

            # 准备分析配置
            analysis_config = {
                "period_type": self.period_type,
                "start_date": self.start_date,
                "lookback_days": self.lookback_days,
            }

            # 生成文件名
            filename = None
            if save_path:
                filename = save_path.split("/")[-1] if "/" in save_path else save_path

            # 创建可视化
            chart_path, report = (
                self.visualization_manager.create_strategy_visualization(
                    top_stocks=top_stocks,
                    stock_data=self.stock_data,
                    analysis_config=analysis_config,
                    filename=filename,
                )
            )

            return chart_path

        except Exception as e:
            print(f"创建可视化时出错: {str(e)}")
            return ""

    def generate_report(self) -> str:
        """
        生成策略分析报告

        Returns:
            分析报告字符串
        """
        try:
            top_stocks = self.get_top_stocks()

            if not top_stocks:
                return "无法生成报告: 没有有效的股票数据"

            # 准备分析配置
            analysis_config = {
                "period_type": self.period_type,
                "start_date": self.start_date,
                "lookback_days": self.lookback_days,
            }

            # 生成报告
            report = (
                self.visualization_manager.report_generator.generate_strategy_report(
                    top_stocks=top_stocks,
                    stock_data=self.stock_data,
                    analysis_config=analysis_config,
                    tickers=self.tickers,
                )
            )

            return report

        except Exception as e:
            return f"生成报告时出错: {str(e)}"

    def get_stock_summary(self, ticker: str) -> Dict:
        """
        获取单只股票的详细信息

        Args:
            ticker: 股票代码

        Returns:
            股票信息字典
        """
        if ticker not in self.stock_data:
            return {"error": f"股票 {ticker} 数据不存在"}

        try:
            data = self.stock_data[ticker]

            # 基础信息
            summary = FactorValidator.get_data_summary(data)

            # 动量信息
            if ticker in self.momentum_scores:
                summary["momentum_score"] = self.momentum_scores[ticker]
                summary["momentum_rank"] = None

                # 计算排名
                sorted_scores = sorted(
                    self.momentum_scores.items(), key=lambda x: x[1], reverse=True,
                )
                for i, (t, _) in enumerate(sorted_scores, 1):
                    if t == ticker:
                        summary["momentum_rank"] = i
                        break

            # 技术指标
            if len(data) > 0:
                latest = data.iloc[-1]
                summary["latest_indicators"] = {
                    "rsi": float(latest.get("RSI", 0))
                    if not pd.isna(latest.get("RSI", float("nan")))
                    else None,
                    "volatility": float(latest.get("Volatility", 0)) * 100
                    if not pd.isna(latest.get("Volatility", float("nan")))
                    else None,
                    "ma_5": float(latest.get("MA_5", 0))
                    if not pd.isna(latest.get("MA_5", float("nan")))
                    else None,
                    "ma_20": float(latest.get("MA_20", 0))
                    if not pd.isna(latest.get("MA_20", float("nan")))
                    else None,
                }

            return summary

        except Exception as e:
            return {"error": f"获取 {ticker} 信息时出错: {str(e)}"}

    def get_strategy_summary(self) -> Dict:
        """
        获取策略整体摘要

        Returns:
            策略摘要字典
        """
        try:
            top_stocks = self.get_top_stocks()

            return {
                "strategy_config": {
                    "lookback_period": self.lookback_period,
                    "lookback_days": self.lookback_days,
                    "period_type": self.period_type,
                    "start_date": self.start_date.strftime("%Y-%m-%d")
                    if self.start_date
                    else None,
                    "top_n": self.top_n,
                },
                "data_summary": {
                    "total_tickers": len(self.tickers),
                    "successful_tickers": len(self.stock_data),
                    "calculated_scores": len(self.momentum_scores),
                },
                "top_recommendations": [
                    {
                        "ticker": ticker,
                        "momentum_score": score,
                        "momentum_pct": f"{score * 100:+.2f}%",
                    }
                    for ticker, score in top_stocks
                ],
                "cache_info": self.data_manager.get_cache_info(),
                "visualization_info": self.visualization_manager.get_output_info(),
            }

        except Exception as e:
            return {"error": f"获取策略摘要时出错: {str(e)}"}

    def clear_data(self):
        """清空所有数据"""
        self.stock_data.clear()
        self.momentum_scores.clear()
        self.tickers.clear()
        self.data_manager.clear_cache()

    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"MomentumStrategy("
            f"lookback_period={self.lookback_period}, "
            f"top_n={self.top_n}, "
            f"tickers_count={len(self.tickers)}, "
            f"data_loaded={len(self.stock_data) > 0}"
            f")"
        )


# 测试函数（当作为主程序运行时）
def main():
    """测试策略模块功能"""
    print("🧪 测试动量策略模块...")

    try:
        # 创建策略实例
        strategy = MomentumStrategy(lookback_period=30, top_n=2)
        print(f"✓ 策略实例创建成功: {strategy}")

        # 测试数据获取
        test_tickers = ["AAPL", "MSFT"]
        strategy.fetch_data_sync(test_tickers)
        print(f"✓ 数据获取成功: {len(strategy.stock_data)} 只股票")

        # 测试动量计算
        top_stocks = strategy.get_top_stocks()
        print(f"✓ 动量计算成功: {len(top_stocks)} 个推荐")

        for i, (ticker, score) in enumerate(top_stocks, 1):
            print(f"   {i}. {ticker}: {score * 100:+.2f}%")

        print("🎉 策略模块测试通过！")

    except Exception as e:
        print(f"❌ 策略模块测试失败: {str(e)}")


if __name__ == "__main__":
    main()
