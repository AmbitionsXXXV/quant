"""
可视化模块 - 图表生成和报告输出
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 设置图表样式
plt.style.use("default")


class ChartGenerator:
    """图表生成器"""

    @staticmethod
    def create_momentum_chart(
        top_stocks: List[Tuple[str, float]],
        stock_data: Dict[str, pd.DataFrame],
        analysis_config: Dict,
        output_path: str = None,
    ) -> str:
        """
        创建动量分析图表

        Args:
            top_stocks: 排序后的股票列表
            stock_data: 股票数据字典
            analysis_config: 分析配置
            output_path: 输出路径

        Returns:
            保存的图片路径
        """
        try:
            # 创建图表
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            fig.suptitle(
                ChartGenerator._generate_chart_title(analysis_config),
                fontsize=16,
                fontweight="bold",
            )

            # 1. 动量得分柱状图
            ChartGenerator._create_momentum_bar_chart(ax1, top_stocks)

            # 2. 价格走势图
            ChartGenerator._create_price_trend_chart(
                ax2,
                top_stocks,
                stock_data,
                analysis_config,
            )

            # 调整布局
            plt.tight_layout()

            # 保存图片
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                plt.savefig(output_path, dpi=300, bbox_inches="tight")
                chart_path = output_path
            else:
                # 生成默认文件名
                chart_path = ChartGenerator._generate_default_filename(analysis_config)
                os.makedirs("charts", exist_ok=True)
                plt.savefig(chart_path, dpi=300, bbox_inches="tight")

            # 释放内存
            plt.close(fig)

            return chart_path

        except Exception as e:
            print(f"生成图表时出错: {str(e)}")
            plt.close("all")
            return None

    @staticmethod
    def _generate_chart_title(analysis_config: Dict) -> str:
        """生成图表标题"""
        lookback_period = analysis_config.get("lookback_period", 60)
        period_type = analysis_config.get("period_type", "days")
        start_date = analysis_config.get("start_date")

        if period_type == "date" and start_date:
            title = f"动量策略分析 - 从 {start_date.strftime('%Y年%m月%d日')} 开始"
        else:
            title = f"动量策略分析 - {lookback_period} 天回看期"

        return title

    @staticmethod
    def _create_momentum_bar_chart(ax, top_stocks: List[Tuple[str, float]]):
        """创建动量得分柱状图"""
        if not top_stocks:
            ax.text(
                0.5,
                0.5,
                "无数据",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )
            return

        tickers = [stock[0] for stock in top_stocks]
        scores = [stock[1] * 100 for stock in top_stocks]  # 转换为百分比

        # 根据得分设置颜色
        colors = ["green" if score > 0 else "red" for score in scores]

        bars = ax.bar(
            tickers,
            scores,
            color=colors,
            alpha=0.7,
            edgecolor="black",
            linewidth=0.8,
        )

        # 添加数值标签
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + (1 if height > 0 else -3),
                f"{score:+.2f}%",
                ha="center",
                va="bottom" if height > 0 else "top",
                fontweight="bold",
                fontsize=10,
            )

        ax.set_title("股票动量得分排名", fontsize=14, fontweight="bold", pad=20)
        ax.set_ylabel("动量得分 (%)", fontsize=12)
        ax.grid(True, alpha=0.3, axis="y")
        ax.axhline(y=0, color="black", linestyle="-", linewidth=0.8)

        # 设置y轴范围
        if scores:
            y_max = max(max(scores), 5)
            y_min = min(min(scores), -5)
            ax.set_ylim(y_min - 2, y_max + 2)

    @staticmethod
    def _create_price_trend_chart(
        ax,
        top_stocks: List[Tuple[str, float]],
        stock_data: Dict,
        analysis_config: Dict,
    ):
        """创建价格走势图"""
        if not top_stocks or not stock_data:
            ax.text(
                0.5,
                0.5,
                "无数据",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )
            return

        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

        for i, (ticker, score) in enumerate(top_stocks[:5]):  # 最多显示前5只
            if ticker in stock_data:
                data = stock_data[ticker]
                if not data.empty and "Close" in data.columns:
                    # 计算归一化价格 (以第一个价格为基准)
                    prices = data["Close"].dropna()
                    normalized_prices = (prices / prices.iloc[0] - 1) * 100

                    color = colors[i % len(colors)]
                    ax.plot(
                        normalized_prices.index,
                        normalized_prices.values,
                        label=f"{ticker} ({score * 100:+.2f}%)",
                        color=color,
                        linewidth=2,
                        alpha=0.8,
                    )

        ax.set_title("股价相对表现 (归一化)", fontsize=14, fontweight="bold", pad=20)
        ax.set_ylabel("相对涨跌幅 (%)", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color="black", linestyle="-", linewidth=0.8)
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

        # 格式化x轴日期
        ax.tick_params(axis="x", rotation=45)

    @staticmethod
    def _generate_default_filename(analysis_config: Dict) -> str:
        """生成默认文件名"""
        lookback_period = analysis_config.get("lookback_period", 60)
        timestamp = datetime.now().strftime("%H%M%S")
        return f"charts/momentum_analysis_{lookback_period}d_{timestamp}.png"


class ReportGenerator:
    """报告生成器"""

    @staticmethod
    def generate_strategy_report(
        top_stocks: List[Tuple[str, float]],
        stock_data: Dict[str, pd.DataFrame],
        analysis_config: Dict,
        tickers: List[str],
    ) -> str:
        """
        生成策略分析报告

        Args:
            top_stocks: 推荐股票列表
            stock_data: 股票数据
            analysis_config: 分析配置
            tickers: 原始股票列表

        Returns:
            报告字符串
        """
        try:
            report_lines = []

            # 报告标题
            report_lines.append("=" * 50)
            report_lines.append("动量策略分析报告")
            report_lines.append("=" * 50)

            # 基本信息
            lookback_period = analysis_config.get("lookback_period", 60)
            period_type = analysis_config.get("period_type", "days")
            start_date = analysis_config.get("start_date")

            report_lines.append(
                f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            )

            if period_type == "date" and start_date:
                report_lines.append(
                    f"分析期间: 从 {start_date.strftime('%Y-%m-%d')} 开始",
                )
            else:
                report_lines.append(f"回看期: {lookback_period} 天")

            report_lines.append(f"分析股票数: {len(tickers)}")
            report_lines.append(f"推荐股票数: {len(top_stocks)}")
            report_lines.append("")

            # 推荐股票详情
            if top_stocks:
                report_lines.append("推荐股票排名:")
                report_lines.append("-" * 30)

                for i, (ticker, score) in enumerate(top_stocks, 1):
                    report_lines.append(f"{i}. {ticker}: {score * 100:+.2f}%")

                    # 添加详细信息
                    if ticker in stock_data:
                        data = stock_data[ticker]
                        latest = data.iloc[-1] if not data.empty else None

                        if latest is not None:
                            report_lines.append(
                                f"   当前价格: ${latest.get('Close', 0):.2f}",
                            )

                            if "RSI" in data.columns and not pd.isna(latest.get("RSI")):
                                report_lines.append(f"   RSI: {latest['RSI']:.1f}")

                            if "Volatility" in data.columns and not pd.isna(
                                latest.get("Volatility"),
                            ):
                                report_lines.append(
                                    f"   波动率: {latest['Volatility'] * 100:.2f}%",
                                )

                    report_lines.append("")
            else:
                report_lines.append("未找到符合条件的推荐股票")

            return "\n".join(report_lines)

        except Exception as e:
            return f"生成报告时出错: {str(e)}"

    @staticmethod
    def generate_backtest_summary(results: List) -> str:
        """
        生成回测总结报告

        Args:
            results: 回测结果列表

        Returns:
            总结报告字符串
        """
        try:
            successful_results = [
                r for r in results if hasattr(r, "success") and r.success
            ]

            report_lines = []
            report_lines.append("=" * 60)
            report_lines.append("批量回测总结报告")
            report_lines.append("=" * 60)
            report_lines.append(f"总测试数: {len(results)}")
            report_lines.append(f"成功测试数: {len(successful_results)}")
            report_lines.append(
                f"成功率: {len(successful_results) / len(results) * 100:.1f}%"
                if results
                else "0%",
            )
            report_lines.append("")

            if successful_results:
                report_lines.append("成功的回测:")
                report_lines.append("-" * 40)
                for result in successful_results:
                    report_lines.append(f"✓ {result.period_name}")
                    if hasattr(result, "top_stocks") and result.top_stocks:
                        top_stock = result.top_stocks[0]
                        report_lines.append(
                            f"  最佳股票: {top_stock[0]} ({top_stock[1] * 100:+.2f}%)",
                        )
                    report_lines.append("")

            failed_results = [
                r for r in results if hasattr(r, "success") and not r.success
            ]
            if failed_results:
                report_lines.append("失败的回测:")
                report_lines.append("-" * 40)
                for result in failed_results:
                    report_lines.append(
                        f"✗ {result.period_name}: {getattr(result, 'error_message', '未知错误')}",
                    )
                report_lines.append("")

            return "\n".join(report_lines)

        except Exception as e:
            return f"生成回测总结时出错: {str(e)}"


class VisualizationManager:
    """可视化管理器"""

    def __init__(self, output_dir: str = "charts"):
        """
        初始化可视化管理器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        self.chart_generator = ChartGenerator()
        self.report_generator = ReportGenerator()

        # 创建输出目录
        Path(self.output_dir).mkdir(exist_ok=True)

    def create_strategy_visualization(
        self,
        top_stocks: List[Tuple[str, float]],
        stock_data: Dict[str, pd.DataFrame],
        analysis_config: Dict,
        filename: Optional[str] = None,
    ) -> Tuple[Optional[str], str]:
        """
        创建策略可视化

        Args:
            top_stocks: 推荐股票列表
            stock_data: 股票数据
            analysis_config: 分析配置
            filename: 自定义文件名

        Returns:
            (图表路径, 报告内容)
        """
        try:
            # 生成图表
            if filename:
                chart_path = os.path.join(self.output_dir, filename)
            else:
                chart_path = None

            saved_chart_path = self.chart_generator.create_momentum_chart(
                top_stocks=top_stocks,
                stock_data=stock_data,
                analysis_config=analysis_config,
                output_path=chart_path,
            )

            # 生成报告
            report = self.report_generator.generate_strategy_report(
                top_stocks=top_stocks,
                stock_data=stock_data,
                analysis_config=analysis_config,
                tickers=list(stock_data.keys()),
            )

            return saved_chart_path, report

        except Exception as e:
            error_msg = f"创建可视化时出错: {str(e)}"
            return None, error_msg

    def clear_output_dir(self):
        """清空输出目录"""
        try:
            if os.path.exists(self.output_dir):
                for file in os.listdir(self.output_dir):
                    file_path = os.path.join(self.output_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            print(f"已清空输出目录: {self.output_dir}")
        except Exception as e:
            print(f"清空输出目录时出错: {str(e)}")

    def get_output_info(self) -> Dict:
        """
        获取输出目录信息

        Returns:
            输出目录信息字典
        """
        try:
            info = {
                "output_dir": self.output_dir,
                "exists": os.path.exists(self.output_dir),
                "file_count": 0,
                "files": [],
            }

            if os.path.exists(self.output_dir):
                files = [
                    f
                    for f in os.listdir(self.output_dir)
                    if os.path.isfile(os.path.join(self.output_dir, f))
                ]
                info["file_count"] = len(files)
                info["files"] = files

            return info

        except Exception as e:
            return {"error": str(e)}
