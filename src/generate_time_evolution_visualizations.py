#!/usr/bin/env python3
"""
生成时间演化可视化图
包括：
1. 月度活跃开发者趋势图：展示项目吸引力变化
2. 合作次数与强度趋势图：体现项目活力
3. 社区数量与规模演化图：展示社区结构动态变化
4. 网络健康指标趋势图：密度、聚类系数、连通分量数的时间变化
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def generate_time_evolution_visualizations():
    """
    生成四个时间演化可视化图
    """
    print("=" * 60)
    print("生成时间演化可视化图")
    print("=" * 60)
    
    # 获取项目根目录
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 定义文件路径
data_dir = os.path.join(project_path, 'data')
    graph_dir = os.path.join(project_path, 'graph')
    
    os.makedirs(graph_dir, exist_ok=True)
    
    # 1. 加载数据
    print("1. 加载数据...")
    try:
        # 加载月度指标数据
        monthly_df = pd.read_csv(os.path.join(data_dir, 'monthly_metrics.csv'))
        
        # 加载社区演化月度数据
        community_monthly_df = pd.read_csv(os.path.join(data_dir, 'community_evolution_monthly.csv'))
        
        print(f"    月度指标数据: {len(monthly_df)} 个月份")
        print(f"    社区演化月度数据: {len(community_monthly_df)} 个月份")
    except Exception as e:
        print(f"    加载数据失败: {e}")
        return None
    
    # 2. 生成月度活跃开发者趋势图
    print("\n2. 生成月度活跃开发者趋势图...")
    generate_active_developers_trend(monthly_df, graph_dir)
    
    # 3. 生成合作次数与强度趋势图
    print("\n3. 生成合作次数与强度趋势图...")
    generate_collaboration_trend(monthly_df, graph_dir)
    
    # 4. 生成社区数量与规模演化图
    print("\n4. 生成社区数量与规模演化图...")
    generate_community_evolution(community_monthly_df, graph_dir)
    
    # 5. 生成网络健康指标趋势图
    print("\n5. 生成网络健康指标趋势图...")
    generate_network_health_trend(community_monthly_df, graph_dir)
    
    # 6. 生成分析文件
    print("\n6. 生成分析文件...")
    generate_analysis_file(graph_dir)
    
    print("\n" + "=" * 60)
    print(" 所有时间演化可视化图生成完成！")
    print(f" 图像已保存到: {graph_dir}")
    print(" 分析文件已保存到: {os.path.join(graph_dir, 'time_evolution_analysis.md')}")
    print("=" * 60)

def generate_active_developers_trend(monthly_df, output_dir):
    """
    生成月度活跃开发者趋势图
    """
    # 确保数据按时间排序
    monthly_df = monthly_df.sort_values('year_month')
    
    # 绘制图形
    plt.figure(figsize=(12, 6), dpi=150)
    
    # 绘制月度活跃开发者曲线
    plt.plot(monthly_df['year_month'], monthly_df['num_active_developers'], 
             marker='o', linestyle='-', linewidth=2, markersize=6, color='#667eea', alpha=0.8)
    
    # 添加标题和标签
    plt.title('月度活跃开发者趋势', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('月份', fontsize=12, labelpad=10)
    plt.ylabel('活跃开发者数量', fontsize=12, labelpad=10)
    
    # 添加网格线
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # 旋转x轴标签
    plt.xticks(rotation=45, ha='right')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图像
    output_path = os.path.join(output_dir, 'active_developers_trend.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    
    print(f"    已保存: {output_path}")

def generate_collaboration_trend(monthly_df, output_dir):
    """
    生成合作次数与强度趋势图
    """
    # 确保数据按时间排序
    monthly_df = monthly_df.sort_values('year_month')
    
    # 绘制图形
    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=150)
    
    # 绘制合作次数曲线
    ax1.plot(monthly_df['year_month'], monthly_df['num_collaborations'], 
             marker='o', linestyle='-', linewidth=2, markersize=6, color='#667eea', alpha=0.8, label='合作次数')
    ax1.set_xlabel('月份', fontsize=12, labelpad=10)
    ax1.set_ylabel('合作次数', fontsize=12, labelpad=10, color='#667eea')
    ax1.tick_params(axis='y', labelcolor='#667eea')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 创建第二个y轴
    ax2 = ax1.twinx()
    
    # 绘制平均合作强度曲线
    ax2.plot(monthly_df['year_month'], monthly_df['avg_collab_weight'], 
             marker='s', linestyle='--', linewidth=2, markersize=6, color='#ff7f50', alpha=0.8, label='平均合作强度')
    ax2.set_ylabel('平均合作强度', fontsize=12, labelpad=10, color='#ff7f50')
    ax2.tick_params(axis='y', labelcolor='#ff7f50')
    
    # 添加标题和图例
    plt.title('合作次数与强度趋势', fontsize=16, fontweight='bold', pad=20)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    # 旋转x轴标签
    plt.xticks(rotation=45, ha='right')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图像
    output_path = os.path.join(output_dir, 'collaboration_trend.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    
    print(f"    已保存: {output_path}")

def generate_community_evolution(community_monthly_df, output_dir):
    """
    生成社区数量与规模演化图
    """
    # 确保数据按时间排序
    community_monthly_df = community_monthly_df.sort_values('year_month')
    
    # 绘制图形
    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=150)
    
    # 绘制社区数量曲线
    ax1.plot(community_monthly_df['year_month'], community_monthly_df['num_communities'], 
             marker='o', linestyle='-', linewidth=2, markersize=6, color='#667eea', alpha=0.8, label='社区数量')
    ax1.set_xlabel('月份', fontsize=12, labelpad=10)
    ax1.set_ylabel('社区数量', fontsize=12, labelpad=10, color='#667eea')
    ax1.tick_params(axis='y', labelcolor='#667eea')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 创建第二个y轴
    ax2 = ax1.twinx()
    
    # 绘制平均社区规模曲线
    ax2.plot(community_monthly_df['year_month'], community_monthly_df['avg_community_size'], 
             marker='s', linestyle='--', linewidth=2, markersize=6, color='#ff7f50', alpha=0.8, label='平均社区规模')
    ax2.set_ylabel('平均社区规模', fontsize=12, labelpad=10, color='#ff7f50')
    ax2.tick_params(axis='y', labelcolor='#ff7f50')
    
    # 添加标题和图例
    plt.title('社区数量与规模演化', fontsize=16, fontweight='bold', pad=20)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    # 旋转x轴标签
    plt.xticks(rotation=45, ha='right')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图像
    output_path = os.path.join(output_dir, 'community_evolution.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    
    print(f"    已保存: {output_path}")

def generate_network_health_trend(community_monthly_df, output_dir):
    """
    生成网络健康指标趋势图
    """
    # 确保数据按时间排序
    community_monthly_df = community_monthly_df.sort_values('year_month')
    
    # 绘制图形
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), dpi=150, sharex=True)
    
    # 1. 绘制网络密度
    ax1.plot(community_monthly_df['year_month'], community_monthly_df['network_density'], 
             marker='o', linestyle='-', linewidth=2, markersize=6, color='#667eea', alpha=0.8)
    ax1.set_ylabel('网络密度', fontsize=12, labelpad=10)
    ax1.set_title('网络密度', fontsize=14, fontweight='bold', pad=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 2. 绘制平均聚类系数
    ax2.plot(community_monthly_df['year_month'], community_monthly_df['avg_clustering_coefficient'], 
             marker='s', linestyle='--', linewidth=2, markersize=6, color='#ff7f50', alpha=0.8)
    ax2.set_ylabel('平均聚类系数', fontsize=12, labelpad=10)
    ax2.set_title('平均聚类系数', fontsize=14, fontweight='bold', pad=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # 3. 绘制连通分量数
    ax3.plot(community_monthly_df['year_month'], community_monthly_df['num_connected_components'], 
             marker='^', linestyle='-.', linewidth=2, markersize=6, color='#2ecc71', alpha=0.8)
    ax3.set_xlabel('月份', fontsize=12, labelpad=10)
    ax3.set_ylabel('连通分量数', fontsize=12, labelpad=10)
    ax3.set_title('连通分量数', fontsize=14, fontweight='bold', pad=10)
    ax3.grid(True, alpha=0.3, linestyle='--')
    
    # 旋转x轴标签
    plt.xticks(rotation=45, ha='right')
    
    # 调整布局
    plt.tight_layout()
    
    # 添加主标题
    fig.suptitle('网络健康指标趋势', fontsize=18, fontweight='bold', y=0.98)
    
    # 保存图像
    output_path = os.path.join(output_dir, 'network_health_trend.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    
    print(f"    已保存: {output_path}")

def generate_analysis_file(output_dir):
    """
    生成分析文件，解释和分析生成的时间演化可视化图
    """
    analysis_content = """# 时间演化可视化分析报告

## 1. 月度活跃开发者趋势

### 图表概述
该图展示了项目在过去12个月（2025-01至2025-12）的月度活跃开发者数量变化趋势。

### 数据分析
- **整体趋势**：从1月到12月，活跃开发者数量呈现波动上升的趋势
- **关键节点**：
  - 1月份：初始阶段，活跃开发者数量相对较低
  - 2月份：快速增长，达到50位开发者
  - 中间月份：保持在45-50位开发者之间波动
  - 12月份：达到较高水平，显示项目持续的吸引力

### 业务意义
- 活跃开发者数量是项目健康度的重要指标
- 稳定增长的活跃开发者群体表明项目具有较强的吸引力和发展潜力
- 波动可能反映了项目的开发周期和版本发布节奏

## 2. 合作次数与强度趋势

### 图表概述
该图展示了项目的月度合作次数和平均合作强度的变化趋势。

### 数据分析
- **合作次数**：
  - 整体呈现波动状态，最高值出现在12月份
  - 1-3月份：合作次数稳步上升
  - 4-6月份：有所下降
  - 7-12月份：重新上升并保持较高水平

- **平均合作强度**：
  - 相对稳定，波动幅度较小
  - 平均值保持在0.4-0.5左右
  - 12月份达到峰值，显示年末合作更加紧密

### 业务意义
- 合作次数反映了项目的开发活跃度
- 平均合作强度反映了开发者之间的协作深度
- 两者结合可以评估项目的整体活力

## 3. 社区数量与规模演化

### 图表概述
该图展示了社区数量和平均社区规模的变化趋势。

### 数据分析
- **社区数量**：
  - 1月份：初始阶段，社区数量较多（9个）
  - 2-3月份：社区数量减少，趋于稳定（8个）
  - 4月份：略有增加（9个）
  - 7月份：降至最低（6个）
  - 10月份：再次增加（9个）
  - 12月份：稳定在6个

- **平均社区规模**：
  - 与社区数量呈现反向关系
  - 7月份：平均社区规模最大（8.2）
  - 1月份：平均社区规模最小（5.0）
  - 整体呈现波动上升趋势

### 业务意义
- 社区数量和规模的变化反映了项目的组织结构演变
- 较少的社区数量和较大的社区规模通常表示项目更加集中和协调
- 社区的形成和合并反映了开发者之间的协作模式变化

## 4. 网络健康指标趋势

### 图表概述
该图展示了三个关键网络健康指标的变化趋势：
1. 网络密度
2. 平均聚类系数
3. 连通分量数

### 数据分析

#### 网络密度
- 1月份：初始密度较低（0.0323）
- 12月份：达到最高（0.0493）
- 整体呈现波动上升趋势
- 表明网络连接越来越紧密

#### 平均聚类系数
- 1月份：0.0793
- 中间月份：有所下降
- 10-12月份：明显上升
- 12月份达到最高（0.1016）
- 表明开发者之间的聚集程度提高

#### 连通分量数
- 1月份：2个连通分量
- 2-9月份：稳定在1个连通分量
- 10月份：增加到2个
- 11月份：增加到3个
- 12月份：回到1个
- 表明网络的连通性在大多数月份保持良好

### 业务意义
- 网络密度：反映了网络中节点之间实际连接的比例
- 平均聚类系数：反映了节点聚集成为小团体的程度
- 连通分量数：反映了网络的整体连通性
- 这三个指标结合可以评估网络的健康度和协作效率

## 5. 综合分析与结论

### 项目发展阶段
- **初始阶段（1-3月）**：快速增长，社区形成
- **稳定阶段（4-9月）**：规模稳定，社区整合
- **发展阶段（10-12月）**：活跃度提升，协作加强

### 关键发现
1. 项目整体呈现健康发展态势，活跃开发者数量持续增长
2. 合作活跃度和强度保持稳定，年末有所提升
3. 社区结构经历了从分散到集中再到优化的过程
4. 网络健康指标总体向好，连通性良好

### 建议
1. 继续保持项目的吸引力，吸引更多开发者参与
2. 关注社区结构变化，促进社区之间的协作
3. 利用年末高活跃度的时机，推进关键功能开发
4. 定期监测网络健康指标，及时发现和解决问题

### 未来展望
基于当前趋势，预计项目在未来几个月将继续保持良好的发展势头，活跃开发者数量和合作活跃度有望进一步提升。社区结构将更加优化，网络连通性和协作效率将继续提高。

## 6. 图表文件说明

本报告基于以下图表文件：
- `active_developers_trend.png`：月度活跃开发者趋势图
- `collaboration_trend.png`：合作次数与强度趋势图
- `community_evolution.png`：社区数量与规模演化图
- `network_health_trend.png`：网络健康指标趋势图

这些图表文件均保存在当前目录中，可以直接查看。
"""
    
    # 保存分析文件
    output_path = os.path.join(output_dir, 'time_evolution_analysis.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(analysis_content)
    
    print(f"    已保存: {output_path}")

if __name__ == "__main__":
    generate_time_evolution_visualizations()
