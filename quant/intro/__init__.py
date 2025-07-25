"""
动量策略包 - 模块化架构的量化交易策略实现

主要模块:
- strategy: 策略核心实现
- factors: 因子计算
- data_loader: 数据获取
- backtest: 回测引擎
- visualization: 可视化
"""

# 导入核心类 - 使用绝对路径
from quant.intro.strategy import MomentumStrategy
from quant.intro.backtest import (
    BacktestManager,
    BacktestConfig,
    BacktestResult,
    BacktestAnalyzer,
)
from quant.intro.factors import TechnicalFactors, MomentumFactors, FactorValidator
from quant.intro.data_loader import DataManager, StockDataLoader, DataPeriodCalculator
from quant.intro.visualization import (
    VisualizationManager,
    ChartGenerator,
    ReportGenerator,
)

# 版本信息
__version__ = "2.0.0"
__author__ = "Quant Team"
__description__ = "模块化动量策略系统"

# 导出的公共接口
__all__ = [
    # 核心策略
    "MomentumStrategy",
    # 回测相关
    "BacktestManager",
    "BacktestConfig",
    "BacktestResult",
    "BacktestAnalyzer",
    # 因子计算
    "TechnicalFactors",
    "MomentumFactors",
    "FactorValidator",
    # 数据获取
    "DataManager",
    "StockDataLoader",
    "DataPeriodCalculator",
    # 可视化
    "VisualizationManager",
    "ChartGenerator",
    "ReportGenerator",
    # 便捷函数
    "quick_analysis",
    "quick_backtest",
]
