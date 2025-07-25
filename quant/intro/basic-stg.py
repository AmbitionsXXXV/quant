"""
动量策略主程序 - 重构版
基于模块化架构的动量策略实现
"""

import asyncio
import sys
import warnings
from typing import List

# 导入重构后的模块 - 使用绝对路径
from quant.intro.strategy import MomentumStrategy
from quant.intro.backtest import BacktestManager, BacktestConfig

# 忽略警告信息
warnings.filterwarnings("ignore")

# 尝试导入 uvloop（仅在非 Windows 系统）
try:
    if sys.platform != "win32":
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        print("✓ 使用 uvloop 加速异步处理")
    else:
        print("ℹ️ Windows 系统，使用默认事件循环")
except ImportError:
    print("ℹ️ uvloop 未安装，使用默认事件循环")


def demo_single_strategy():
    """演示单个策略分析"""
    print("\n" + "=" * 50)
    print("🎯 单策略演示")
    print("=" * 50)

    tech_stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

    # 60天动量策略
    print("\n📊 60天动量策略分析...")
    strategy = MomentumStrategy(lookback_period=60, top_n=3)

    try:
        # 同步获取数据
        strategy.fetch_data_sync(tech_stocks)

        # 获取推荐股票
        top_stocks = strategy.get_top_stocks()

        if top_stocks:
            print("\n🎯 推荐关注股票:")
            for i, (ticker, score) in enumerate(top_stocks, 1):
                print(f"   {i}. {ticker}: {score * 100:+.2f}%")

            # 生成报告
            report = strategy.generate_report()
            print("\n" + report)

            # 生成图表
            chart_path = strategy.create_visualization()
            if chart_path:
                print(f"\n📈 图表已保存: {chart_path}")
        else:
            print("❌ 未找到符合条件的推荐股票")

    except Exception as e:
        print(f"❌ 策略分析失败: {str(e)}")


async def demo_async_strategy():
    """演示异步策略分析"""
    print("\n" + "=" * 50)
    print("🚀 异步策略演示")
    print("=" * 50)

    tech_stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

    # 创建多个不同周期的策略
    strategies = [
        ("1个月", MomentumStrategy(lookback_period=30, top_n=3)),
        ("3个月", MomentumStrategy(lookback_period=90, top_n=3)),
        ("1年", MomentumStrategy(lookback_period=365, top_n=3)),
    ]

    for period_name, strategy in strategies:
        print(f"\n📊 {period_name}策略分析...")

        try:
            # 异步获取数据
            await strategy.fetch_data_async(tech_stocks, max_workers=3)

            # 获取推荐股票
            top_stocks = strategy.get_top_stocks()

            if top_stocks:
                print(f"🎯 {period_name}推荐:")
                for i, (ticker, score) in enumerate(top_stocks, 1):
                    print(f"   {i}. {ticker}: {score * 100:+.2f}%")
            else:
                print(f"❌ {period_name}无推荐股票")

        except Exception as e:
            print(f"❌ {period_name}策略失败: {str(e)}")


async def demo_batch_backtest():
    """演示批量回测"""
    print("\n" + "=" * 50)
    print("🔄 批量回测演示")
    print("=" * 50)

    tech_stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

    # 创建回测管理器
    backtest_manager = BacktestManager()

    try:
        # 运行默认回测配置
        results = await backtest_manager.run_default_backtest(
            tickers=tech_stocks, output_dir="backtest_results",
        )

        # 显示成功结果
        successful_results = [r for r in results if r.success]

        if successful_results:
            print(f"\n🎉 成功生成 {len(successful_results)} 个回测图表")
            print("所有图表已保存到 backtest_results/ 目录")
        else:
            print("\n❌ 未能生成任何图表")

    except Exception as e:
        print(f"❌ 批量回测失败: {str(e)}")


def demo_custom_backtest():
    """演示自定义回测配置"""
    print("\n" + "=" * 50)
    print("⚙️ 自定义回测演示")
    print("=" * 50)

    # 自定义回测周期
    custom_periods = [
        (30, "短期动量"),
        (180, "中期动量"),
        ("2021-01-01", "疫情后恢复"),
        ("2022-01-01", "近期表现"),
    ]

    # 自定义股票池
    custom_stocks = ["AAPL", "GOOGL", "AMZN", "TSLA"]

    # 创建自定义配置
    config = BacktestConfig(
        periods=custom_periods,
        tickers=custom_stocks,
        top_n=2,  # 只选前2只
        output_dir="custom_backtest",
        max_workers=2,
    )

    print("📋 自定义配置:")
    print(f"   周期数: {len(config.periods)}")
    print(f"   股票池: {', '.join(config.tickers)}")
    print(f"   推荐数: {config.top_n}")
    print("   (实际运行需要在异步环境中)")


async def main_async():
    """异步主函数"""
    print("🚀 启动动量策略分析系统...")
    print("🔧 基于模块化架构的重构版本")

    # 选择演示模式
    print("\n选择演示模式:")
    print("1. 单策略演示 (同步)")
    print("2. 异步策略演示")
    print("3. 批量回测演示")
    print("4. 自定义回测演示")

    # 为了演示，我们运行所有模式
    try:
        # 1. 单策略演示
        demo_single_strategy()

        # 2. 异步策略演示
        await demo_async_strategy()

        # 3. 批量回测演示
        await demo_batch_backtest()

        # 4. 自定义回测演示
        demo_custom_backtest()

        print("\n🎉 所有演示完成！")

    except Exception as e:
        print(f"❌ 程序执行出错: {str(e)}")


def main():
    """主函数"""
    try:
        # 运行异步主函数
        asyncio.run(main_async())

    except KeyboardInterrupt:
        print("\n👋 用户中断程序")
    except Exception as e:
        print(f"❌ 程序异常: {str(e)}")
        print("请检查网络连接和股票代码是否正确")


# 便捷函数供外部调用
def quick_analysis(
    tickers: List[str] = None, lookback_period: int = 60, top_n: int = 3,
) -> MomentumStrategy:
    """
    快速分析函数

    Args:
        tickers: 股票代码列表
        lookback_period: 回看期间
        top_n: 推荐股票数

    Returns:
        配置好的策略实例
    """
    if tickers is None:
        tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

    strategy = MomentumStrategy(lookback_period=lookback_period, top_n=top_n)

    try:
        strategy.fetch_data_sync(tickers)
        top_stocks = strategy.get_top_stocks()

        if top_stocks:
            print("🎯 快速分析结果:")
            for i, (ticker, score) in enumerate(top_stocks, 1):
                print(f"   {i}. {ticker}: {score * 100:+.2f}%")
        else:
            print("❌ 未找到推荐股票")

        return strategy

    except Exception as e:
        print(f"❌ 快速分析失败: {str(e)}")
        return strategy


async def quick_backtest(tickers: List[str] = None) -> List:
    """
    快速回测函数

    Args:
        tickers: 股票代码列表

    Returns:
        回测结果列表
    """
    if tickers is None:
        tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

    backtest_manager = BacktestManager()

    try:
        results = await backtest_manager.run_default_backtest(tickers)
        return results
    except Exception as e:
        print(f"❌ 快速回测失败: {str(e)}")
        return []


if __name__ == "__main__":
    main()
