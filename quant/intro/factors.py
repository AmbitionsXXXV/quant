"""
因子计算模块 - 技术指标和动量因子计算
"""

import pandas as pd
from typing import Dict, Optional
import warnings

warnings.filterwarnings("ignore")


class TechnicalFactors:
    """技术指标计算器"""

    @staticmethod
    def calculate_moving_average(data: pd.DataFrame, window: int = 20) -> pd.Series:
        """计算移动平均线"""
        return data["Close"].rolling(window=window).mean()

    @staticmethod
    def calculate_daily_return(data: pd.DataFrame) -> pd.Series:
        """计算日收益率"""
        return data["Close"].pct_change()

    @staticmethod
    def calculate_volatility(data: pd.DataFrame, window: int = 20) -> pd.Series:
        """计算波动率"""
        daily_returns = TechnicalFactors.calculate_daily_return(data)
        return daily_returns.rolling(window=window).std()

    @staticmethod
    def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
        """计算 RSI 相对强弱指数"""
        delta = data["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def add_all_indicators(data: pd.DataFrame) -> pd.DataFrame:
        """
        为数据添加所有技术指标

        Args:
            data: 原始股票数据

        Returns:
            包含技术指标的数据
        """
        try:
            # 创建副本避免修改原数据
            enriched_data = data.copy()

            # 添加移动平均线
            enriched_data["MA_5"] = TechnicalFactors.calculate_moving_average(data, 5)
            enriched_data["MA_20"] = TechnicalFactors.calculate_moving_average(data, 20)

            # 添加收益率
            enriched_data["Daily_Return"] = TechnicalFactors.calculate_daily_return(
                data,
            )

            # 添加波动率
            enriched_data["Volatility"] = TechnicalFactors.calculate_volatility(
                data, 20,
            )

            # 添加 RSI
            enriched_data["RSI"] = TechnicalFactors.calculate_rsi(data, 14)

            return enriched_data

        except Exception as e:
            print(f"添加技术指标时出错: {str(e)}")
            return data


class MomentumFactors:
    """动量因子计算器"""

    @staticmethod
    def calculate_price_momentum(
        data: pd.DataFrame,
        lookback_days: int,
        period_type: str = "days",
        start_date: Optional[pd.Timestamp] = None,
    ) -> float:
        """
        计算价格动量

        Args:
            data: 股票数据
            lookback_days: 回看天数
            period_type: 期间类型
            start_date: 开始日期

        Returns:
            动量得分
        """
        try:
            closes = data["Close"].dropna()

            if len(closes) < 2:
                return 0.0

            # 根据期间类型调整计算方式
            if period_type == "date" and start_date:
                # 时间戳模式：使用实际的开始和结束价格
                start_price = float(closes.iloc[0])
                end_price = float(closes.iloc[-1])
            else:
                # 天数模式：使用指定回看期间
                if len(closes) < lookback_days:
                    # 如果数据不足，使用所有可用数据
                    start_price = float(closes.iloc[0])
                    end_price = float(closes.iloc[-1])
                else:
                    start_price = float(closes.iloc[-lookback_days])
                    end_price = float(closes.iloc[-1])

            # 计算动量得分
            momentum = (
                (end_price - start_price) / start_price if start_price != 0 else 0.0
            )
            return momentum

        except Exception as e:
            print(f"计算价格动量时出错: {str(e)}")
            return 0.0

    @staticmethod
    def calculate_volume_momentum(data: pd.DataFrame, window: int = 20) -> float:
        """计算成交量动量"""
        try:
            volumes = data["Volume"].dropna()
            if len(volumes) < window:
                return 0.0

            recent_volume = volumes.tail(window).mean()
            historical_volume = volumes.head(len(volumes) - window).mean()

            if historical_volume == 0:
                return 0.0

            return (recent_volume - historical_volume) / historical_volume

        except Exception as e:
            print(f"计算成交量动量时出错: {str(e)}")
            return 0.0

    @staticmethod
    def calculate_rsi_momentum(data: pd.DataFrame) -> float:
        """基于 RSI 计算动量指标"""
        try:
            if "RSI" not in data.columns:
                return 0.0

            rsi_values = data["RSI"].dropna()
            if len(rsi_values) == 0:
                return 0.0

            latest_rsi = rsi_values.iloc[-1]

            # RSI 动量：50以上为正，50以下为负
            rsi_momentum = (latest_rsi - 50) / 50
            return rsi_momentum

        except Exception as e:
            print(f"计算RSI动量时出错: {str(e)}")
            return 0.0

    @staticmethod
    def calculate_composite_momentum(
        data: pd.DataFrame,
        lookback_days: int,
        period_type: str = "days",
        start_date: Optional[pd.Timestamp] = None,
    ) -> float:
        """
        计算综合动量得分

        Args:
            data: 股票数据
            lookback_days: 回看天数
            period_type: 期间类型
            start_date: 开始日期

        Returns:
            综合动量得分
        """
        try:
            # 价格动量 (权重: 0.7)
            price_momentum = MomentumFactors.calculate_price_momentum(
                data, lookback_days, period_type, start_date,
            )

            # 成交量动量 (权重: 0.2)
            volume_momentum = MomentumFactors.calculate_volume_momentum(data, 20)

            # RSI 动量 (权重: 0.1)
            rsi_momentum = MomentumFactors.calculate_rsi_momentum(data)

            # 加权综合
            composite_score = (
                price_momentum * 0.7 + volume_momentum * 0.2 + rsi_momentum * 0.1
            )

            return composite_score

        except Exception as e:
            print(f"计算综合动量时出错: {str(e)}")
            return 0.0


class FactorValidator:
    """因子数据验证器"""

    @staticmethod
    def validate_data_quality(data: pd.DataFrame, min_records: int = 10) -> bool:
        """
        验证数据质量

        Args:
            data: 股票数据
            min_records: 最小记录数

        Returns:
            是否通过验证
        """
        try:
            if data is None or data.empty:
                return False

            # 检查记录数量
            if len(data) < min_records:
                return False

            # 检查必要列
            required_columns = ["Open", "High", "Low", "Close", "Volume"]
            if not all(col in data.columns for col in required_columns):
                return False

            # 检查数据完整性
            if data[required_columns].isnull().all().any():
                return False

            return True

        except Exception as e:
            print(f"数据质量验证出错: {str(e)}")
            return False

    @staticmethod
    def get_data_summary(data: pd.DataFrame) -> Dict:
        """
        获取数据摘要

        Args:
            data: 股票数据

        Returns:
            数据摘要字典
        """
        try:
            if data is None or data.empty:
                return {"error": "数据为空"}

            summary = {
                "records_count": len(data),
                "date_range": {
                    "start": data.index.min().strftime("%Y-%m-%d")
                    if not data.index.empty
                    else None,
                    "end": data.index.max().strftime("%Y-%m-%d")
                    if not data.index.empty
                    else None,
                },
                "price_info": {
                    "latest_close": float(data["Close"].iloc[-1])
                    if "Close" in data.columns
                    else None,
                    "max_high": float(data["High"].max())
                    if "High" in data.columns
                    else None,
                    "min_low": float(data["Low"].min())
                    if "Low" in data.columns
                    else None,
                },
                "technical_indicators": {},
                "data_quality": {
                    "null_count": data.isnull().sum().sum(),
                    "completeness": 1
                    - (data.isnull().sum().sum() / (len(data) * len(data.columns))),
                },
            }

            # 添加技术指标信息
            if "RSI" in data.columns and not data["RSI"].empty:
                summary["technical_indicators"]["latest_rsi"] = float(
                    data["RSI"].iloc[-1],
                )

            if "Volatility" in data.columns and not data["Volatility"].empty:
                summary["technical_indicators"]["latest_volatility"] = float(
                    data["Volatility"].iloc[-1],
                )

            return summary

        except Exception as e:
            return {"error": str(e)}
