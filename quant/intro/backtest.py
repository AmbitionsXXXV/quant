"""
回测引擎模块 - 批量异步回测功能
"""

import asyncio
import os
from datetime import datetime
from typing import List, Dict, Union, Optional, Tuple
from pathlib import Path


from quant.intro.strategy import MomentumStrategy


class BacktestConfig:
    """回测配置类"""

    def __init__(
        self,
        periods: List[Tuple[Union[int, str], str]] = None,
        tickers: List[str] = None,
        top_n: int = 3,
        output_dir: str = "backtest_results",
        max_workers: int = 3,
    ):
        """
        初始化回测配置

        Args:
            periods: 回测周期列表 [(周期, 名称), ...]
            tickers: 股票代码列表
            top_n: 推荐股票数量
            output_dir: 输出目录
            max_workers: 最大并发数
        """
        self.periods = periods or self._get_default_periods()
        self.tickers = tickers or ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
        self.top_n = top_n
        self.output_dir = output_dir
        self.max_workers = max_workers

    def _get_default_periods(self) -> List[Tuple[Union[int, str], str]]:
        """获取默认回测周期"""
        return [
            (30, "1个月"),
            (60, "2个月"),
            (90, "3个月"),
            (180, "6个月"),
            (365, "1年"),
            (730, "2年"),
            ("2020-01-01", "从2020年开始"),
            ("2021-01-01", "从2021年开始"),
            ("2022-01-01", "从2022年开始"),
        ]


class BacktestResult:
    """回测结果类"""

    def __init__(
        self,
        period: Union[int, str],
        period_name: str,
        success: bool,
        chart_path: Optional[str] = None,
        top_stocks: List[Tuple[str, float]] = None,
        error_message: Optional[str] = None,
    ):
        """
        初始化回测结果

        Args:
            period: 回测周期
            period_name: 周期名称
            success: 是否成功
            chart_path: 图表路径
            top_stocks: 推荐股票
            error_message: 错误信息
        """
        self.period = period
        self.period_name = period_name
        self.success = success
        self.chart_path = chart_path
        self.top_stocks = top_stocks or []
        self.error_message = error_message
        self.timestamp = datetime.now()


class SingleBacktestRunner:
    """单个回测任务运行器"""

    @staticmethod
    async def run_single_backtest(
        period: Union[int, str],
        period_name: str,
        tickers: List[str],
        output_dir: str,
        top_n: int = 3,
        max_workers: int = 3,
    ) -> BacktestResult:
        """
        运行单个回测任务

        Args:
            period: 回测周期
            period_name: 周期名称
            tickers: 股票代码列表
            output_dir: 输出目录
            top_n: 推荐股票数量
            max_workers: 最大并发数

        Returns:
            回测结果
        """
        try:
            print(f"\n📊 开始 {period_name} 回测...")

            # 创建策略实例
            strategy = MomentumStrategy(lookback_period=period, top_n=top_n)

            # 获取数据
            try:
                await strategy.fetch_data_async(tickers, max_workers=max_workers)
            except Exception as e:
                print(f"  异步获取数据失败，回退到同步方法: {str(e)}")
                strategy.fetch_data_sync(tickers)

            # 获取推荐股票
            top_stocks = strategy.get_top_stocks()

            if top_stocks:
                print("  推荐股票:")
                for i, (ticker, score) in enumerate(top_stocks, 1):
                    print(f"    {i}. {ticker}: {score * 100:+.2f}%")

                # 生成图表
                filename = SingleBacktestRunner._generate_filename(period)
                chart_path = os.path.join(output_dir, filename)
                saved_path = strategy.create_visualization(chart_path)

                if saved_path:
                    print(f"  ✓ {period_name} 图表已保存")
                    return BacktestResult(
                        period=period,
                        period_name=period_name,
                        success=True,
                        chart_path=saved_path,
                        top_stocks=top_stocks,
                    )
            else:
                print(f"  ❌ {period_name} 无有效推荐")
                return BacktestResult(
                    period=period,
                    period_name=period_name,
                    success=False,
                    error_message="无有效推荐股票",
                )

        except Exception as e:
            error_msg = f"{period_name} 回测失败: {str(e)}"
            print(f"  ❌ {error_msg}")
            return BacktestResult(
                period=period,
                period_name=period_name,
                success=False,
                error_message=error_msg,
            )

    @staticmethod
    def _generate_filename(period: Union[int, str]) -> str:
        """生成文件名"""
        if isinstance(period, str):
            return f"backtest_{period.replace('-', '')}.png"
        else:
            return f"backtest_{period}days.png"


class BatchBacktestEngine:
    """批量回测引擎"""

    def __init__(self, config: BacktestConfig):
        """
        初始化回测引擎

        Args:
            config: 回测配置
        """
        self.config = config
        self.results: List[BacktestResult] = []

    async def run_batch_backtest(self) -> List[BacktestResult]:
        """
        运行批量回测

        Returns:
            回测结果列表
        """
        print("🔄 异步回测周期演示")
        print("=" * 60)

        # 创建输出目录
        Path(self.config.output_dir).mkdir(exist_ok=True)

        # 创建异步任务列表
        tasks = []
        for period, period_name in self.config.periods:
            task = asyncio.create_task(
                SingleBacktestRunner.run_single_backtest(
                    period=period,
                    period_name=period_name,
                    tickers=self.config.tickers,
                    output_dir=self.config.output_dir,
                    top_n=self.config.top_n,
                    max_workers=self.config.max_workers,
                ),
            )
            tasks.append(task)

        # 并发执行所有回测
        self.results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理异常结果
        processed_results = []
        for i, result in enumerate(self.results):
            period, period_name = self.config.periods[i]
            if isinstance(result, Exception):
                processed_results.append(
                    BacktestResult(
                        period=period,
                        period_name=period_name,
                        success=False,
                        error_message=str(result),
                    ),
                )
            else:
                processed_results.append(result)

        self.results = processed_results
        return self.results

    def get_summary(self) -> Dict:
        """
        获取回测总结

        Returns:
            回测总结字典
        """
        successful_results = [r for r in self.results if r.success]
        failed_results = [r for r in self.results if not r.success]

        return {
            "total_tests": len(self.results),
            "successful_tests": len(successful_results),
            "failed_tests": len(failed_results),
            "success_rate": len(successful_results) / len(self.results)
            if self.results
            else 0,
            "successful_charts": [
                r.chart_path for r in successful_results if r.chart_path
            ],
            "failed_test_details": [
                (r.period_name, r.error_message) for r in failed_results
            ],
        }

    def print_summary(self):
        """打印回测总结"""
        summary = self.get_summary()

        print("\n📊 回测完成总结:")
        print(f"  ✓ 成功生成图表: {summary['successful_tests']} 个")
        print(f"  ✗ 失败的测试: {summary['failed_tests']} 个")
        print(f"  📈 成功率: {summary['success_rate']:.1%}")

        if summary["successful_charts"]:
            print("\n📁 图表保存位置:")
            for chart_path in summary["successful_charts"]:
                print(f"  - {chart_path}")

        if summary["failed_test_details"]:
            print("\n❌ 失败的测试:")
            for test_name, error in summary["failed_test_details"]:
                print(f"  - {test_name}: {error}")

    def get_best_performers(
        self, top_n: int = 3,
    ) -> List[Tuple[str, List[Tuple[str, float]]]]:
        """
        获取各周期的最佳表现股票

        Args:
            top_n: 返回前N个周期

        Returns:
            [(周期名称, 推荐股票列表), ...]
        """
        successful_results = [r for r in self.results if r.success and r.top_stocks]

        # 按推荐股票的平均得分排序
        period_scores = []
        for result in successful_results:
            if result.top_stocks:
                avg_score = sum(score for _, score in result.top_stocks) / len(
                    result.top_stocks,
                )
                period_scores.append((result.period_name, result.top_stocks, avg_score))

        # 排序并返回前N个
        period_scores.sort(key=lambda x: x[2], reverse=True)
        return [(name, stocks) for name, stocks, _ in period_scores[:top_n]]


class BacktestAnalyzer:
    """回测结果分析器"""

    @staticmethod
    def analyze_stock_performance(results: List[BacktestResult]) -> Dict[str, Dict]:
        """
        分析股票在不同周期的表现

        Args:
            results: 回测结果列表

        Returns:
            股票表现分析字典
        """
        stock_performance = {}

        for result in results:
            if result.success and result.top_stocks:
                for ticker, score in result.top_stocks:
                    if ticker not in stock_performance:
                        stock_performance[ticker] = {
                            "appearances": 0,
                            "total_score": 0.0,
                            "periods": [],
                            "rankings": [],
                        }

                    stock_performance[ticker]["appearances"] += 1
                    stock_performance[ticker]["total_score"] += score
                    stock_performance[ticker]["periods"].append(result.period_name)

                    # 找到排名
                    ranking = next(
                        (
                            i + 1
                            for i, (t, _) in enumerate(result.top_stocks)
                            if t == ticker
                        ),
                        None,
                    )
                    if ranking:
                        stock_performance[ticker]["rankings"].append(ranking)

        # 计算平均分和其他统计信息
        for ticker, data in stock_performance.items():
            data["avg_score"] = (
                data["total_score"] / data["appearances"]
                if data["appearances"] > 0
                else 0
            )
            data["avg_ranking"] = (
                sum(data["rankings"]) / len(data["rankings"]) if data["rankings"] else 0
            )
            data["consistency"] = data["appearances"] / len(
                [r for r in results if r.success],
            )

        return stock_performance

    @staticmethod
    def generate_performance_report(results: List[BacktestResult]) -> str:
        """
        生成性能分析报告

        Args:
            results: 回测结果列表

        Returns:
            性能分析报告字符串
        """
        stock_performance = BacktestAnalyzer.analyze_stock_performance(results)

        if not stock_performance:
            return "无法生成性能报告：没有成功的回测结果"

        report = []
        report.append("=" * 60)
        report.append("回测性能分析报告")
        report.append("=" * 60)
        report.append(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"分析周期数: {len(results)}")
        report.append("")

        # 按一致性排序
        sorted_stocks = sorted(
            stock_performance.items(),
            key=lambda x: (x[1]["consistency"], x[1]["avg_score"]),
            reverse=True,
        )

        report.append("股票表现排名 (按一致性和平均得分):")
        report.append("-" * 50)

        for i, (ticker, data) in enumerate(sorted_stocks, 1):
            report.append(f"{i}. {ticker}")
            report.append(f"   出现次数: {data['appearances']} 次")
            report.append(f"   一致性: {data['consistency']:.1%}")
            report.append(f"   平均得分: {data['avg_score'] * 100:+.2f}%")
            report.append(f"   平均排名: {data['avg_ranking']:.1f}")
            report.append(f"   出现周期: {', '.join(data['periods'])}")
            report.append("")

        return "\n".join(report)


class BacktestManager:
    """回测管理器 - 统一的回测接口"""

    def __init__(self):
        self.engines: List[BatchBacktestEngine] = []
        self.current_engine: Optional[BatchBacktestEngine] = None

    def create_engine(self, config: BacktestConfig) -> BatchBacktestEngine:
        """
        创建回测引擎

        Args:
            config: 回测配置

        Returns:
            回测引擎实例
        """
        engine = BatchBacktestEngine(config)
        self.engines.append(engine)
        self.current_engine = engine
        return engine

    async def run_default_backtest(
        self, tickers: List[str] = None, output_dir: str = "backtest_results",
    ) -> List[BacktestResult]:
        """
        运行默认配置的回测

        Args:
            tickers: 股票代码列表
            output_dir: 输出目录

        Returns:
            回测结果列表
        """
        config = BacktestConfig(
            tickers=tickers or ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"],
            output_dir=output_dir,
        )

        engine = self.create_engine(config)
        results = await engine.run_batch_backtest()
        engine.print_summary()

        return results

    def get_all_results(self) -> List[BacktestResult]:
        """获取所有回测结果"""
        all_results = []
        for engine in self.engines:
            all_results.extend(engine.results)
        return all_results

    def clear_history(self):
        """清空历史记录"""
        self.engines.clear()
        self.current_engine = None


# 测试函数（当作为主程序运行时）
async def main():
    """测试回测模块功能"""
    print("🧪 测试回测引擎模块...")

    try:
        # 创建回测管理器
        manager = BacktestManager()
        print("✓ 回测管理器创建成功")

        # 创建简单配置进行测试
        config = BacktestConfig(
            periods=[(30, "短期测试"), (60, "中期测试")],
            tickers=["AAPL", "MSFT"],
            top_n=2,
            output_dir="test_backtest",
        )
        print(f"✓ 回测配置创建成功: {len(config.periods)} 个周期")

        # 创建引擎
        engine = manager.create_engine(config)
        print("✓ 回测引擎创建成功")

        # 运行小规模回测
        print("🚀 开始运行测试回测...")
        results = await engine.run_batch_backtest()
        print(results)

        # 显示结果
        summary = engine.get_summary()
        print(
            f"✓ 回测完成: 成功 {summary['successful_tests']}/{summary['total_tests']}",
        )

        print("🎉 回测模块测试通过！")

    except Exception as e:
        print(f"❌ 回测模块测试失败: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
