# 动量策略增强功能文档

## 概述

本文档记录了对 `basic-stg.py` 文件的四项重要增强功能，旨在提升代码的功能性、可视化能力、封装性和健壮性。

## 增强功能详情

### 1. 使用 pandas 处理股票数据

#### 新增功能

- **数据清洗**: 使用 `dropna()` 自动删除缺失值
- **技术指标计算**:
  - 5 日和 20 日移动平均线 (`MA_5`, `MA_20`)
  - 日收益率 (`Daily_Return`)
  - 20 日滚动波动率 (`Volatility`)
  - RSI 相对强弱指数 (`RSI`)
- **数据处理优化**: 支持单只股票和多只股票的批量处理

#### 代码示例

```python
def _add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
    data['MA_5'] = data['Close'].rolling(window=5).mean()
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['Daily_Return'] = data['Close'].pct_change()
    data['Volatility'] = data['Daily_Return'].rolling(window=20).std()
    data['RSI'] = self._calculate_rsi(data['Close'])
    return data
```

### 2. 策略函数可视化

#### 新增功能

- **多维度图表**: 包含 4 个子图的综合分析面板
  - 动量得分柱状图
  - 前 3 只股票价格走势图
  - 股票波动率对比图
  - RSI 指标对比图
- **图表美化**: 支持中文显示、颜色编码、数值标签
- **保存功能**: 支持将图表保存为高清图片

#### 主要方法

```python
def visualize_strategy(self, tickers: List[str], save_path: Optional[str] = None) -> None:
    # 创建 2x2 子图布局
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    # 绘制各种分析图表
```

### 3. 使用类封装策略逻辑

#### 类设计

- **类名**: `MomentumStrategy`
- **主要属性**:
  - `lookback_days`: 回看天数
  - `top_n`: 推荐股票数量
  - `stock_data`: 股票数据存储
  - `momentum_scores`: 动量得分缓存

#### 主要方法

- `fetch_stock_data()`: 获取和处理股票数据
- `calculate_momentum()`: 计算动量得分
- `get_top_stocks()`: 获取排名前 N 的股票
- `visualize_strategy()`: 生成可视化图表
- `generate_report()`: 生成分析报告

#### 封装优势

- **代码复用**: 避免重复代码，提高维护性
- **状态管理**: 缓存数据和计算结果，提高效率
- **扩展性**: 便于添加新的策略方法和指标

### 4. 异常处理增强代码健壮性

#### 异常处理策略

- **网络异常**: 捕获 yfinance 连接失败和数据获取失败
- **数据异常**: 处理空数据、格式错误、计算异常
- **用户输入异常**: 验证股票代码有效性
- **系统异常**: 处理文件操作和内存不足等问题

#### 异常类型

```python
# 自定义异常处理
try:
    raw_data = yf.download(tickers, period=period, group_by='ticker', progress=False)
    if raw_data.empty:
        raise ValueError("无法获取股票数据，请检查股票代码是否正确")
except Exception as e:
    if "No data found" in str(e):
        raise ValueError(f"未找到股票数据，请检查股票代码: {tickers}")
    elif "Connection" in str(e):
        raise ConnectionError(f"网络连接失败: {str(e)}")
    else:
        raise ValueError(f"数据获取失败: {str(e)}")
```

## 新增功能

### 分析报告生成

- **详细报告**: 包含时间戳、参数设置、推荐股票详情
- **技术指标**: 显示当前价格、RSI、波动率等关键指标
- **格式化输出**: 清晰的报告格式，便于阅读和保存

### 主函数演示

- **完整流程**: 从数据获取到可视化的完整演示
- **错误处理**: 友好的错误提示和处理建议
- **多样化输出**: 控制台输出 + 图表显示 + 详细数据展示

## 使用方法

### 基本使用

```python
# 创建策略实例
strategy = MomentumStrategy(lookback_days=60, top_n=3)

# 分析股票
tech_stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
top_stocks = strategy.get_top_stocks(tech_stocks)

# 生成可视化
strategy.visualize_strategy(tech_stocks)

# 生成报告
report = strategy.generate_report(tech_stocks)
print(report)
```

### 高级功能

```python
# 自定义参数
strategy = MomentumStrategy(lookback_days=90, top_n=5)

# 保存图表
strategy.visualize_strategy(tech_stocks, save_path="analysis_chart.png")

# 获取详细数据
stock_data = strategy.fetch_stock_data(tech_stocks)
```

## 技术特性

### 类型提示

- 使用 Python 类型提示增强代码可读性
- 支持 IDE 智能提示和静态类型检查

### 性能优化

- 数据缓存机制，避免重复计算
- 批量数据处理，提高执行效率
- 异常处理不影响程序主流程

### 扩展性设计

- 模块化设计，便于添加新的技术指标
- 可配置参数，适应不同的分析需求
- 标准化接口，便于集成到更大的系统中

## 依赖项

确保已安装以下 Python 包：

- `yfinance`: 股票数据获取
- `pandas`: 数据处理和分析
- `matplotlib`: 图表绘制
- `numpy`: 数值计算
- `typing`: 类型提示支持

## 注意事项

1. **网络连接**: 需要稳定的网络连接获取股票数据
2. **数据延迟**: yfinance 数据可能有 15-20 分钟延迟
3. **图表显示**: 某些环境可能需要配置 matplotlib 后端
4. **中文字体**: 可视化中文显示需要系统支持相应字体

## 更新日志

- **2024-12-20**: 完成四项核心功能增强
  - ✅ pandas 数据处理集成
  - ✅ 可视化功能实现
  - ✅ 类封装重构完成
  - ✅ 异常处理机制建立
