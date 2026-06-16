# 足球比赛预测系统 - Football Prediction System

一个综合的足球比赛数据分析、统计和预测系统，包含数据可视化和后续的视频分析功能。

## 🎯 项目目标

- ✅ **数据分析** - 从 StatsBomb、football.json 等公开数据源获取和分析足球数据
- ✅ **统计分析** - 球队表现、球员数据、历史对战分析
- ✅ **机器学习预测** - 预测比赛结果、进球数等
- ✅ **数据可视化** - 交互式仪表盘、图表和报告
- 🔄 **实时 API 集成** - 后期集成实时数据源
- 🎬 **视频分析** - 后期加入 YOLO 和 OpenCV 的视频分析功能

## 📁 项目结构

```
football-match-prediction/
├── README.md                          # 项目说明
├── requirements.txt                   # Python 依赖
├── setup.py                           # 项目配置
├── config.yaml                        # 配置文件
│
├── data/
│   ├── raw/                           # 原始数据
│   ├── processed/                     # 处理后的数据
│   └── sample_data.csv                # 样本数据
│
├── src/
│   ├── __init__.py
│   ├── config.py                      # 配置管理
│   │
│   ├── data_sources/
│   │   ├── __init__.py
│   │   ├── base_loader.py             # 基础加载器
│   │   ├── statsbomb_loader.py        # StatsBomb 数据加载
│   │   └── football_json_loader.py    # football.json 数据加载
│   │
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── data_cleaner.py            # 数据清洗
│   │   └── feature_engineer.py        # 特征工程
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── stats_analyzer.py          # 统计分析
│   │
│   ├── prediction/
│   │   ├── __init__.py
│   │   ├── ml_predictor.py            # ML 预测模块
│   │   └── models/                    # 预训练模型
│   │
│   └── visualization/
│       ├── __init__.py
│       └── charts.py                  # 图表生成
│
├── notebooks/
│   ├── 01_fetch_data.ipynb            # 数据获取演示
│   ├── 02_data_analysis.ipynb         # 数据分析演示
│   ├── 03_prediction_demo.ipynb       # 预测演示
│   └── 04_visualization.ipynb         # 可视化演示
│
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_analyzer.py
│   └── test_predictor.py
│
└── scripts/
    ├── fetch_data.py                  # 数据获取脚本
    ├── train_model.py                 # 模型训练脚本
    └── generate_report.py             # 报告生成脚本
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/ming-chen4697/football-match-prediction.git
cd football-match-prediction
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 获取数据

```bash
python scripts/fetch_data.py
```

### 4. 运行分析

```bash
jupyter notebook notebooks/02_data_analysis.ipynb
```

### 5. 生成预测

```bash
python scripts/train_model.py
```

## 📊 主要功能

### 数据分析
- 球队进攻/防守能力分析
- 球员表现评分
- 历史对战数据分析
- 进球趋势分析

### 机器学习预测
- 比赛结果预测（胜/平/负）
- 进球数预测
- 球队排名预测
- 伤病影响评估

### 数据可视化
- 交互式仪表盘（Plotly）
- 球队对比图表
- 进球热力图
- 赛季趋势图

## 📈 数据源

- **StatsBomb** - 专业足球数据（通过 API）
- **football.json** - 开放的比赛数据
- **Kaggle** - 历史足球数据集
- **实时 API** - 后期集成（ESPN、FootAPI等）

## 🛠️ 技术栈

- **数据处理**: Pandas, NumPy
- **机器学习**: Scikit-learn, XGBoost, LightGBM
- **可视化**: Plotly, Matplotlib, Seaborn
- **Web 框架**: Dash, Flask
- **数据库**: SQLite/PostgreSQL（可选）
- **视频分析**: OpenCV, YOLOv8（后期）

## 📚 学习资源

- [StatsBomb 官方文档](https://statsbomb.com/what-we-do/our-work/research-projects/)
- [football-analytics](https://github.com/eddwebster/football_analytics)
- [awesome-football-analytics](https://github.com/diegopastor/awesome-football-analytics)
- [Football_Prediction_Project](https://github.com/James-Luckhurst/Football_Prediction_Project)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**开始探索足球数据的奥秘吧！** ⚽🔍📊
