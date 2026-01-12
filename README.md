# OpenSaga

An interactive visualization platform for open-source collaboration networks, leveraging graph theory and temporal analysis to uncover insights from developer collaboration data.

##  项目概述

OpenSaga 是一个开源协作网络的交互式可视化平台，旨在帮助用户理解和分析开源社区中的开发者协作模式、社区演化和核心开发者影响力。该平台使用图计算引擎（EasyGraph/NetworkX）进行网络分析，并提供直观的Web可视化界面。

##  核心功能

### 1. 图计算引擎
- **双引擎支持**：自动切换 EasyGraph 和 NetworkX，确保最佳性能
- **社区检测**：基于 Louvain 算法的社区划分
- **中心性分析**：支持 PageRank 和度中心性计算
- **灵活的图构建**：支持有向图和无向图创建

### 2. 数据获取与处理
- **OpenDigger 集成**：从 OpenDigger 获取真实的开源项目协作数据
- **时间演化分析**：生成月度协作网络数据
- **数据预处理**：节点和边的合并与清洗
- **多维度指标计算**：活跃度、技术匹配度等

### 3. 可视化生成
- **网络可视化**：生成用于可视化的节点、边和社区数据
- **时间演化**：生成社区和协作模式的时间序列数据
- **热力图数据**：生成协作热度和多样性分析数据
- **趋势分析**：生成各种指标的趋势数据

### 4. Web 交互界面
- **交互式网络图**：可视化开发者协作关系
- **社区演化视图**：展示社区的形成、合并和分裂
- **核心开发者分析**：识别和展示核心贡献者
- **协作热度图**：直观展示协作强度和模式

##  技术栈

### 核心技术
- **Python 3.7+**：主要开发语言
- **图计算引擎**：EasyGraph (优先) / NetworkX (备选)
- **社区检测**：python-louvain
- **数据处理**：pandas, numpy
- **可视化**：matplotlib, Jupyter Notebook
- **Web 技术**：HTML, JavaScript (前端可视化)

### 依赖项
查看 `requirements.txt` 文件获取完整依赖列表：
```
easygraph==0.2.1
networkx
python-louvain
pandas
numpy
matplotlib
jupyter
seaborn  
```

##  安装说明

### 1. 克隆仓库
```bash
git clone https://github.com/your-username/OpenSaga.git
cd OpenSaga
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

##  快速开始

### 1. 测试图计算引擎
```bash
python src/graph_engine.py
```

### 2. 生成示例数据
```bash
python src/fetch_opendigger_data.py
```

### 3. 运行社区演化分析
```bash
python src/generate_community_evolution.py
```

### 4. 生成可视化数据
```bash
python src/generate_for_viz_data.py
```

### 5. 启动 Web 界面
在浏览器中打开 `web/index.html` 文件，即可查看交互式可视化界面。

##  项目结构

```
OpenSaga/
├── data/                 # 原始和处理后的数据
│   ├── collaborations_temporal.csv
│   ├── developers.csv
│   └── community_evolution_detail.csv
├── examples/             # 示例脚本和笔记本
│   ├── generate_network_graph.py
│   └── temporal_analysis.ipynb
├── src/                  # 核心源代码
│   ├── graph_engine.py   # 图计算引擎
│   ├── fetch_opendigger_data.py
│   └── generate_community_evolution.py
├── viz/                  # 可视化数据
│   ├── for_viz_nodes.csv
│   ├── for_viz_edges.csv
│   └── for_viz_communities.csv
├── web/                  # Web 界面和脚本
│   ├── index.html
│   └── generate_heatmap_data.py
├── requirements.txt      # 依赖列表
├── LICENSE               # 许可证
└── README.md             # 项目文档
```

##  使用指南

### 1. 数据获取

#### 生成模拟数据
```bash
python src/fetch_opendigger_data.py
```

#### 获取真实数据
```bash
python src/fetch_real_opendigger_data.py
```

### 2. 网络分析

#### 社区检测
```bash
python src/generate_community_evolution.py
```

#### 网络可视化
```bash
python src/generate_network_visualizations.py
```

### 3. 时间演化分析

```bash
python src/generate_time_evolution_visualizations.py
```

### 4. Web 可视化

1. 生成可视化数据：
   ```bash
   python src/generate_for_viz_data.py
   ```

2. 处理 Web 数据：
   ```bash
   python web/generate_heatmap_data.py
   ```

3. 在浏览器中打开 `web/index.html`

##  数据说明

### 数据格式

#### 开发者数据 (`developers.csv`)
| 字段名 | 描述 |
|--------|------|
| developer_id | 开发者唯一标识 |
| name | 开发者名称 |
| primary_tech | 主要技术栈 |
| join_date | 加入日期 |
| activity_level | 活跃度 |

#### 协作数据 (`collaborations_temporal.csv`)
| 字段名 | 描述 |
|--------|------|
| source | 源开发者ID |
| target | 目标开发者ID |
| weight | 协作权重 |
| year_month | 年份-月份 |
| source_tech | 源开发者技术栈 |
| target_tech | 目标开发者技术栈 |

#### 社区数据 (`community_evolution_detail.csv`)
| 字段名 | 描述 |
|--------|------|
| community_id | 社区ID |
| developer_id | 开发者ID |
| year_month | 年份-月份 |
| role | 角色（核心/边缘） |

##  自定义配置

### 修改数据源
在 `src/fetch_opendigger_data.py` 中修改：
```python
platform = "github"
org = "pandas-dev"
repo = "pandas"
```

### 调整图计算引擎
在 `src/graph_engine.py` 中修改：
```python
default_engine = GraphEngine(backend='easygraph')  # 或 'networkx'
```

### 修改可视化参数
在相应的可视化生成脚本中调整参数，例如 `src/generate_network_visualizations.py`。

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件获取详细信息。

##  致谢

- 感谢 [OpenDigger](https://github.com/X-lab2017/open-digger) 提供开源数据支持
- 感谢 [EasyGraph](https://github.com/easy-graph/EasyGraph) 和 [NetworkX](https://networkx.org/) 提供图计算支持

---

**OpenSaga** - 探索开源协作网络的无限可能！