import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from datetime import datetime
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

def create_network_graph():
    """创建协作网络图"""
    print("开始生成协作网络图...")
    
    nodes_df = pd.read_csv('../viz/for_viz_nodes.csv')
    edges_df = pd.read_csv('../viz/for_viz_edges.csv')
    
    print(f"  加载 {len(nodes_df)} 个节点, {len(edges_df)} 条边")
    
    G = nx.DiGraph()
    
    node_size_scaling = 2000  # 节点大小缩放因子
    for _, row in nodes_df.iterrows():
        G.add_node(row['developer_id'],
                  name=row['name'],
                  tech=row['primary_tech'],
                  pagerank=row['pagerank_score'],
                  degree=row['degree_centrality'])
    
    for _, row in edges_df.iterrows():
        G.add_edge(row['source'], row['target'],
                  weight=row['weight'],
                  tech_match=row['tech_match'])
    
    print("  计算力导向布局...")
    # 使用Spring布局，基于权重
    pos = nx.spring_layout(G, k=2, iterations=50, weight='weight', seed=42)
    
    # 节点大小基于PageRank
    pagerank_values = [G.nodes[n]['pagerank'] for n in G.nodes()]
    pagerank_min, pagerank_max = min(pagerank_values), max(pagerank_values)
    node_sizes = [(p - pagerank_min) / (pagerank_max - pagerank_min) * 800 + 200 
                  for p in pagerank_values]
    
    # 节点颜色基于技术栈
    tech_colors = {
        'Python': '#FF6B6B',     
        'JavaScript': '#4ECDC4', 
        'Java': '#45B7D1',       
        'Go': '#96CEB4',         
        'Rust': '#FFEAA7',       
        'C++': '#DDA0DD',       
        'TypeScript': '#F8B195'  
    }
    node_colors = [tech_colors.get(G.nodes[n]['tech'], '#999999') for n in G.nodes()]
    
    # 边透明度基于权重
    edge_alphas = [G[u][v]['weight'] * 0.7 + 0.3 for u, v in G.edges()]
    edge_widths = [G[u][v]['weight'] * 2 + 0.5 for u, v in G.edges()]
    
    print("  绘制图形...")
    plt.figure(figsize=(16, 12))
    
    edges = nx.draw_networkx_edges(G, pos,
                                   edge_color='#555555',
                                   width=edge_widths,
                                   alpha=0.6,  
                                   arrowstyle='-|>',
                                   arrowsize=10,
                                   connectionstyle="arc3,rad=0.1")
    
    # 绘制节点
    nodes = nx.draw_networkx_nodes(G, pos,
                                   node_size=node_sizes,
                                   node_color=node_colors,
                                   edgecolors='white',
                                   linewidths=1.5,
                                   alpha=0.9)
    
    # 添加标签（只显示核心节点）
    # 计算度中心性，只标注高度连接的节点
    degrees = dict(G.degree())
    high_degree_nodes = [n for n in G.nodes() if degrees[n] >= 3]
    
    labels = {n: G.nodes[n]['name'] for n in high_degree_nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
    
    from matplotlib.patches import Patch
    legend_elements = []
    for tech, color in tech_colors.items():
        # 计算该技术栈有多少开发者
        count = sum(1 for n in G.nodes() if G.nodes[n]['tech'] == tech)
        if count > 0:
            legend_elements.append(Patch(facecolor=color, edgecolor='white',
                                        label=f'{tech} ({count}人)'))
    
    plt.legend(handles=legend_elements, loc='upper left', 
               title='技术栈分布', frameon=True, fancybox=True)
    
    plt.title('开源协作网络关系图 (力导向布局)', fontsize=18, fontweight='bold', pad=20)
    plt.text(0.02, 0.02,
            f'   节点大小 ≈ PageRank影响力\\n'
            f'   边粗细 ≈ 协作强度\\n'
            f'   共 {len(G.nodes())} 位开发者, {len(G.edges())} 条协作关系\\n'
            f'   生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
            transform=plt.gca().transAxes,
            fontsize=10,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.axis('off')
    plt.tight_layout()
    
    output_path = '../data/network_graph.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f" 网络图已保存至: {output_path}")
    print(f"   文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, node_size=30, node_color=node_colors, 
            width=0.5, alpha=0.6, with_labels=False)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('../data/network_graph_small.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f" 缩略图已保存至: ../data/network_graph_small.png")
    
    return output_path

def create_network_metrics_table():
    """生成网络指标表格（也可在DataEase中展示）"""
    nodes_df = pd.read_csv('../data/for_viz_nodes.csv')
    edges_df = pd.read_csv('../data/for_viz_edges.csv')
    
    metrics = {
        'metric': ['开发者总数', '协作关系总数', '平均协作强度', 
                   '技术栈数量', '网络密度', '核心开发者(PageRank>0.01)'],
        'value': [
            len(nodes_df),
            len(edges_df),
            f"{edges_df['weight'].mean():.3f}",
            nodes_df['primary_tech'].nunique(),
            f"{len(edges_df) / (len(nodes_df) * (len(nodes_df)-1)):.4f}",
            len(nodes_df[nodes_df['pagerank_score'] > 0.01])
        ]
    }
    
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv('../data/network_metrics.csv', index=False, encoding='utf-8-sig')
    print(f" 网络指标已保存至: ../data/network_metrics.csv")
    
    return metrics_df

if __name__ == "__main__":
    print("=" * 60)
    print("生成开源协作网络可视化文件")
    print("=" * 60)
    
    os.makedirs('../data', exist_ok=True)
    
    graph_path = create_network_graph()
    
    metrics_df = create_network_metrics_table()
