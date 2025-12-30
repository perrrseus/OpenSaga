#!/usr/bin/env python3
"""
生成网络结构可视化图
包括：
1. 开发者协作网络图：节点大小表示PageRank，边粗细表示合作强度，颜色区分技术栈
2. 核心开发者影响力图：突出核心开发者的连接作用
3. 技术栈协作网络：展示不同技术栈之间的合作关系
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def generate_network_visualizations():
    """
    生成三个网络结构可视化图
    """
    print("=" * 60)
    print("生成网络结构可视化图")
    print("=" * 60)
    
    # 获取项目根目录
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 定义文件路径
    data_dir = os.path.join(project_path, 'data')
    viz_dir = os.path.join(project_path, 'viz')
    graph_dir = os.path.join(project_path, 'graph')
    
    # 确保输出目录存在
    os.makedirs(graph_dir, exist_ok=True)
    
    # 1. 加载数据
    print("1. 加载数据...")
    try:
        developers_df = pd.read_csv(os.path.join(data_dir, 'developers.csv'))
        latest_network_df = pd.read_csv(os.path.join(data_dir, 'latest_network.csv'))
        node_df = pd.read_csv(os.path.join(viz_dir, 'for_viz_nodes.csv'))
        
        print(f"   ✅ 开发者数据: {len(developers_df)} 位开发者")
        print(f"   ✅ 最新网络数据: {len(latest_network_df)} 条边")
        print(f"   ✅ 节点数据: {len(node_df)} 个节点")
    except Exception as e:
        print(f"   ❌ 加载数据失败: {e}")
        return None
    
    # 2. 生成开发者协作网络图
    print("\n2. 生成开发者协作网络图...")
    generate_developer_collaboration_graph(developers_df, latest_network_df, node_df, graph_dir)
    
    # 3. 生成核心开发者影响力图
    print("\n3. 生成核心开发者影响力图...")
    generate_core_developer_influence_graph(developers_df, latest_network_df, node_df, graph_dir)
    
    # 4. 生成技术栈协作网络
    print("\n4. 生成技术栈协作网络...")
    generate_tech_stack_collaboration_graph(developers_df, latest_network_df, graph_dir)
    
    print("\n" + "=" * 60)
    print("✅ 所有网络可视化图生成完成！")
    print(f"✅ 图像已保存到: {graph_dir}")
    print("=" * 60)

def generate_developer_collaboration_graph(developers_df, latest_network_df, node_df, output_dir):
    """
    生成开发者协作网络图
    节点大小表示PageRank，边粗细表示合作强度，颜色区分技术栈
    """
    # 构建网络
    G = nx.DiGraph()
    
    # 定义技术栈颜色映射
    tech_colors = {
        'Python': '#3776AB',
        'JavaScript': '#F7DF1E',
        'Java': '#ED8B00',
        'Go': '#00ADD8',
        'Rust': '#DEA584',
        'C++': '#00599C',
        'TypeScript': '#3178C6'
    }
    
    # 添加节点，直接使用node_df
    for _, dev in node_df.iterrows():
        G.add_node(dev['developer_id'],
                  name=dev['name'],
                  tech=dev['primary_tech'],
                  pagerank=dev['pagerank_score'],
                  color=tech_colors.get(dev['primary_tech'], '#808080'))
    
    # 添加边
    for _, edge in latest_network_df.iterrows():
        if edge['source'] in G and edge['target'] in G:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    # 设置节点大小（基于PageRank）
    node_sizes = [G.nodes[node]['pagerank'] * 10000 for node in G.nodes()]
    
    # 设置边宽度（基于合作强度）
    edge_widths = [G.edges[edge]['weight'] * 2 for edge in G.edges()]
    
    # 设置节点颜色
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    
    # 绘制图形
    plt.figure(figsize=(12, 10), dpi=150)
    
    # 使用spring_layout布局，减少迭代次数加快速度
    pos = nx.spring_layout(G, k=0.5, iterations=20)
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3, edge_color='#888888', arrowsize=10)
    
    # 绘制标签（只显示核心开发者）
    core_devs = node_df[node_df['is_core_developer']]
    core_labels = {dev['developer_id']: dev['name'] for _, dev in core_devs.iterrows()}
    nx.draw_networkx_labels(G, pos, core_labels, font_size=8, font_weight='bold', alpha=0.9)
    
    # 添加标题和图例
    plt.title('开发者协作网络图', fontsize=24, fontweight='bold', pad=20)
    
    # 创建技术栈图例
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=tech)
                      for tech, color in tech_colors.items()]
    plt.legend(handles=legend_elements, title='技术栈', loc='best', fontsize=10, title_fontsize=12)
    
    # 隐藏坐标轴
    plt.axis('off')
    
    # 调整布局并保存
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'developer_collaboration_graph.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    
    print(f"   ✅ 已保存: {output_path}")

def generate_core_developer_influence_graph(developers_df, latest_network_df, node_df, output_dir):
    """
    生成核心开发者影响力图
    突出核心开发者的连接作用
    """
    # 构建网络
    G = nx.DiGraph()
    
    # 筛选核心开发者，直接使用node_df
    core_devs = node_df[node_df['is_core_developer']]
    core_dev_ids = set(core_devs['developer_id'])
    
    # 定义节点颜色：核心开发者为红色，其他为灰色
    node_colors = []
    for _, dev in node_df.iterrows():
        if dev['is_core_developer']:
            node_colors.append('#FF5733')
        else:
            node_colors.append('#808080')
    
    # 添加节点，直接使用node_df
    for _, dev in node_df.iterrows():
        G.add_node(dev['developer_id'],
                  name=dev['name'],
                  pagerank=dev['pagerank_score'],
                  is_core=dev['is_core_developer'])
    
    # 添加边
    for _, edge in latest_network_df.iterrows():
        if edge['source'] in G and edge['target'] in G:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    # 设置节点大小（基于PageRank，核心开发者放大）
    node_sizes = []
    for node in G.nodes():
        if G.nodes[node]['is_core']:
            node_sizes.append(G.nodes[node]['pagerank'] * 15000)
        else:
            node_sizes.append(G.nodes[node]['pagerank'] * 5000)
    
    # 设置边宽度（基于合作强度）
    edge_widths = [G.edges[edge]['weight'] * 2 for edge in G.edges()]
    
    # 绘制图形
    plt.figure(figsize=(12, 10), dpi=150)
    
    # 使用spring_layout布局，减少迭代次数加快速度
    pos = nx.spring_layout(G, k=0.5, iterations=20)
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3, edge_color='#888888', arrowsize=10)
    
    # 绘制标签（只显示核心开发者）
    core_labels = {dev['developer_id']: dev['name'] for _, dev in core_devs.iterrows()}
    nx.draw_networkx_labels(G, pos, core_labels, font_size=10, font_weight='bold', alpha=0.9, font_color='#000000')
    
    # 添加标题
    plt.title('核心开发者影响力图', fontsize=24, fontweight='bold', pad=20)
    
    # 添加图例
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF5733', markersize=15, label='核心开发者'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#808080', markersize=10, label='普通开发者')
    ]
    plt.legend(handles=legend_elements, loc='best', fontsize=12, title_fontsize=14)
    
    # 隐藏坐标轴
    plt.axis('off')
    
    # 调整布局并保存
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'core_developer_influence_graph.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    
    print(f"   ✅ 已保存: {output_path}")

def generate_tech_stack_collaboration_graph(developers_df, latest_network_df, output_dir):
    """
    生成技术栈协作网络
    展示不同技术栈之间的合作关系
    """
    # 构建技术栈合作矩阵
    tech_stack_counts = developers_df['primary_tech'].value_counts()
    tech_stacks = tech_stack_counts.index.tolist()
    
    # 创建技术栈映射
    tech_to_id = {tech: i for i, tech in enumerate(tech_stacks)}
    
    # 计算技术栈之间的合作强度
    tech_collab_matrix = pd.DataFrame(0, index=tech_stacks, columns=tech_stacks, dtype=float)
    
    # 遍历所有边，计算技术栈之间的合作强度
    for _, edge in latest_network_df.iterrows():
        source_tech = developers_df[developers_df['developer_id'] == edge['source']]['primary_tech'].iloc[0]
        target_tech = developers_df[developers_df['developer_id'] == edge['target']]['primary_tech'].iloc[0]
        tech_collab_matrix.loc[source_tech, target_tech] += edge['weight']
    
    # 构建技术栈合作网络
    G_tech = nx.DiGraph()
    
    # 添加节点（技术栈）
    for tech in tech_stacks:
        G_tech.add_node(tech, size=tech_stack_counts[tech])
    
    # 添加边（技术栈之间的合作）
    for source_tech in tech_stacks:
        for target_tech in tech_stacks:
            weight = tech_collab_matrix.loc[source_tech, target_tech]
            if weight > 0:
                G_tech.add_edge(source_tech, target_tech, weight=weight)
    
    # 定义技术栈颜色映射
    tech_colors = {
        'Python': '#3776AB',
        'JavaScript': '#F7DF1E',
        'Java': '#ED8B00',
        'Go': '#00ADD8',
        'Rust': '#DEA584',
        'C++': '#00599C',
        'TypeScript': '#3178C6'
    }
    
    # 设置节点大小（基于该技术栈的开发者数量）
    node_sizes = [G_tech.nodes[tech]['size'] * 100 for tech in G_tech.nodes()]
    
    # 设置边宽度（基于技术栈之间的合作强度）
    edge_widths = [G_tech.edges[edge]['weight'] * 0.5 for edge in G_tech.edges()]
    
    # 设置节点颜色
    node_colors = [tech_colors.get(tech, '#808080') for tech in G_tech.nodes()]
    
    # 绘制图形
    plt.figure(figsize=(12, 10), dpi=150)
    
    # 使用spring_layout布局，减少迭代次数加快速度
    pos = nx.spring_layout(G_tech, k=0.8, iterations=20)
    
    # 绘制节点
    nx.draw_networkx_nodes(G_tech, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    
    # 绘制边
    nx.draw_networkx_edges(G_tech, pos, width=edge_widths, alpha=0.5, edge_color='#555555', arrowsize=15)
    
    # 绘制标签
    nx.draw_networkx_labels(G_tech, pos, font_size=12, font_weight='bold', alpha=0.9, font_color='#000000')
    
    # 绘制边权重
    edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G_tech.edges(data=True) if d['weight'] > 2}
    nx.draw_networkx_edge_labels(G_tech, pos, edge_labels=edge_labels, font_size=8, alpha=0.7)
    
    # 添加标题
    plt.title('技术栈协作网络', fontsize=24, fontweight='bold', pad=20)
    
    # 添加图例说明
    plt.text(0.02, 0.02, f'节点大小表示技术栈开发者数量\n边粗细表示技术栈间合作强度', 
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='bottom',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    # 隐藏坐标轴
    plt.axis('off')
    
    # 调整布局并保存
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'tech_stack_collaboration_graph.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    
    print(f"   ✅ 已保存: {output_path}")

if __name__ == "__main__":
    generate_network_visualizations()
