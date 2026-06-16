# 网页版足球预测系统 - Web Application Guide

## 📱 功能介绍

这个网页应用提供了一个现代化的用户界面来使用足球比赛预测系统。

### ✨ 主要功能

1. **仪表盘 Dashboard**
   - 关键指标卡片（总比赛数、球队数、平均进球、主场胜率）
   - 球队排名图表
   - 比赛结果分布

2. **球队排名 Teams**
   - 完整的球队排名表
   - 详细的统计数据（场次、胜平负、进失球、球差、积分）
   - 查看球队详情

3. **比赛预测 Prediction**
   - 选择两支球队
   - 获得实时预测
   - 显示胜平负概率
   - 显示预期进球数

4. **统计数据 Statistics**
   - 整体比赛统计
   - 最近比赛记录
   - 结果分析

## 🚀 安装和运行

### 1. 安装依赖

```bash
pip install -r web/requirements.txt
```

### 2. 准备数据

确保已经运行过数据处理脚本：

```bash
python scripts/fetch_data.py
```

### 3. 启动 Web 应用

```bash
python run_web.py
```

或者直接运行：

```bash
python -m web.app
```

### 4. 访问应用

打开浏览器，访问：
```
http://localhost:5000
```

## 🏗️ 项目结构

```
web/
├── app.py                 # Flask 主应用
├── requirements.txt       # Python 依赖
├── templates/
│   └── index.html        # 主页面 HTML
└── static/
    ├── css/
    │   └── style.css     # 样式文件
    └── js/
        └── main.js       # 前端 JavaScript
```

## 📡 API 端点

### 获取仪表盘数据
```
GET /api/dashboard
Response: {
    "total_matches": int,
    "total_teams": int,
    "avg_goals": float
}
```

### 获取球队列表
```
GET /api/teams
Response: {
    "teams": [
        {
            "team": string,
            "matches": int,
            "wins": int,
            "draws": int,
            "losses": int,
            "goals_for": int,
            "goals_against": int,
            "points": int,
            ...
        }
    ]
}
```

### 获取球队详情
```
GET /api/team/<team_name>
Response: {
    "team": string,
    "matches": int,
    "form": {...},
    ...
}
```

### 预测比赛
```
POST /api/predict
Request: {
    "team1": string,
    "team2": string
}
Response: {
    "team1": string,
    "team2": string,
    "team1_win_prob": float,
    "draw_prob": float,
    "team2_win_prob": float,
    "expected_goals": {
        "team1": float,
        "team2": float
    }
}
```

### 获取统计数据
```
GET /api/statistics
Response: {
    "total_matches": int,
    "home_wins": int,
    "draws": int,
    "away_wins": int,
    "avg_goals": float,
    "home_win_rate": float,
    ...
}
```

### 获取最近比赛
```
GET /api/matches
Response: {
    "matches": [
        {
            "date": string,
            "home_team": string,
            "home_goals": int,
            "away_goals": int,
            "away_team": string,
            "result": string
        }
    ]
}
```

## 🎨 UI 功能

### 响应式设计
- ✅ 自适应布局
- ✅ 手机、平板、桌面支持
- ✅ 触摸友好

### 交互功能
- ✅ 实时数据加载
- ✅ 交互式图表（使用 Plotly）
- ✅ 表格排序和筛选
- ✅ 平滑滚动导航

### 可视化
- ✅ 球队排名柱状图
- ✅ 比赛结果饼图
- ✅ 预测概率卡片
- ✅ 统计数据仪表板

## 🔧 自定义

### 修改样式
编辑 `web/static/css/style.css` 来自定义配色和布局

### 添加新功能
1. 在 `web/app.py` 中添加新的 API 端点
2. 在 `web/templates/index.html` 中添加新的 HTML 元素
3. 在 `web/static/js/main.js` 中添加对应的 JavaScript 逻辑

### 连接数据库
目前使用 CSV 文件，可以扩展为：
- SQLite
- PostgreSQL
- MongoDB

## 📊 数据流

```
用户界面 (HTML/CSS/JS)
        ↓
  Flask API (Python)
        ↓
  数据处理模块 (Pandas)
        ↓
   数据文件 (CSV)
```

## 🚀 部署

### 开发环境
```bash
python run_web.py
```

### 生产环境

使用 Gunicorn：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web.app:app
```

使用 Docker：
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "run_web.py"]
```

## 🐛 故障排除

### 无法加载数据
- ✅ 检查 `data/processed/matches.csv` 是否存在
- ✅ 运行 `python scripts/fetch_data.py`

### CORS 错误
- ✅ 已在 Flask 中启用 CORS
- ✅ 检查浏览器控制台错误

### 端口已被占用
- ✅ 修改 `run_web.py` 中的端口号
- ✅ 或关闭占用该端口的应用

## 📝 许可证

MIT License
