#!/usr/bin/env python3
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def generate_network_visualizations():
    print("=" * 60)
    print("生成网络结构可视化图")
    print("=" * 60)
    
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_path, 'data')
    viz_dir = os.path.join(project_path, 'viz')
    graph_dir = os.path.join(project_path, 'graph')
    os.makedirs(graph_dir, exist_ok=True)
    
    print("1. 加载数据...")
    try:
        developers_df = pd.read_csv(os.path.join(data_dir, 'developers.csv'))
        latest_network_df = pd.read_csv(os.path.join(data_dir, 'latest_network.csv'))
        node_df = pd.read_csv(os.path.join(viz_dir, 'for_viz_nodes.csv'))
        print(f"    开发者数据: {len(developers_df)} 位开发者")
        print(f"    最新网络数据: {len(latest_network_df)} 条边")
        print(f"    节点数据: {len(node_df)} 个节点")
    except Exception as e:
        print(f"    加载数据失败: {e}")
        return None
    
    print("\n2. 生成开发者协作网络图...")
    generate_developer_collaboration_graph(developers_df, latest_network_df, node_df, graph_dir)
    
    print("\n3. 生成核心开发者影响力图...")
    generate_core_developer_influence_graph(developers_df, latest_network_df, node_df, graph_dir)
    
    print("\n4. 生成技术栈协作网络...")
    generate_tech_stack_collaboration_graph(developers_df, latest_network_df, graph_dir)
    
    print("\n" + "=" * 60)
    print(" 所有网络可视化图生成完成！")
    print(f" 图像已保存到: {graph_dir}")
    print("=" * 60)


def generate_developer_collaboration_graph(developers_df, latest_network_df, node_df, output_dir):
    G = nx.DiGraph()
    
    tech_colors = {
        'Python': '#4285F4',
        'JavaScript': '#EA4335',
        'Java': '#FBBC05',
        'Go': '#34A853',
        'Rust': '#000000',
        'C++': '#00599C',
        'TypeScript': '#3178C6'
    }
    
    for _, dev in node_df.iterrows():
        G.add_node(dev['developer_id'],
                  name=dev['name'],
                  tech=dev['primary_tech'],
                  pagerank=dev['pagerank_score'],
                  color=tech_colors.get(dev['primary_tech'], '#9AA0A6'))
    
    for _, edge in latest_network_df.iterrows():
        if edge['source'] in G and edge['target'] in G:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    node_sizes = [G.nodes[node]['pagerank'] * 10000 for node in G.nodes()]
    edge_widths = [G.edges[edge]['weight'] * 2 for edge in G.edges()]
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    
    plt.figure(figsize=(12, 10), dpi=150)
    pos = nx.spring_layout(G, k=0.5, iterations=20)
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3, edge_color='#9AA0A6')
    
    core_devs = node_df[node_df['is_core_developer']]
    core_labels = {dev['developer_id']: dev['name'] for _, dev in core_devs.iterrows()}
    nx.draw_networkx_labels(G, pos, core_labels, font_size=8, font_weight='bold', alpha=0.9)
    
    plt.title('开发者协作网络图', fontsize=24, fontweight='bold', pad=20)
    
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=tech)
                      for tech, color in tech_colors.items()]
    plt.legend(handles=legend_elements, title='技术栈', loc='best', fontsize=10, title_fontsize=12)
    
    plt.axis('off')
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'developer_collaboration_graph.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    print(f"    已保存: {output_path}")


def generate_core_developer_influence_graph(developers_df, latest_network_df, node_df, output_dir):
    G = nx.DiGraph()
    
    core_devs = node_df[node_df['is_core_developer']]
    core_dev_ids = set(core_devs['developer_id'])
    
    node_colors = []
    for _, dev in node_df.iterrows():
        if dev['is_core_developer']:
            node_colors.append('#EA4335')
        else:
            node_colors.append('#4285F4')
    
    for _, dev in node_df.iterrows():
        G.add_node(dev['developer_id'],
                  name=dev['name'],
                  pagerank=dev['pagerank_score'],
                  is_core=dev['is_core_developer'])
    
    for _, edge in latest_network_df.iterrows():
        if edge['source'] in G and edge['target'] in G:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    node_sizes = []
    for node in G.nodes():
        if G.nodes[node]['is_core']:
            node_sizes.append(G.nodes[node]['pagerank'] * 15000)
        else:
            node_sizes.append(G.nodes[node]['pagerank'] * 5000)
    
    edge_widths = [G.edges[edge]['weight'] * 2 for edge in G.edges()]
    
    plt.figure(figsize=(12, 10), dpi=150)
    pos = nx.spring_layout(G, k=0.5, iterations=20)
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3, edge_color='#9AA0A6')
    
    core_labels = {dev['developer_id']: dev['name'] for _, dev in core_devs.iterrows()}
    nx.draw_networkx_labels(G, pos, core_labels, font_size=10, font_weight='bold', alpha=0.9, font_color='white')
    
    plt.title('核心开发者影响力图', fontsize=24, fontweight='bold', pad=20)
    
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#EA4335', markersize=10, label='核心开发者'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4285F4', markersize=10, label='普通开发者')
    ]
    plt.legend(handles=legend_elements, loc='best', fontsize=12, title_fontsize=14)
    
    plt.axis('off')
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'core_developer_influence_graph.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    print(f"    已保存: {output_path}")


def generate_tech_stack_collaboration_graph(developers_df, latest_network_df, output_dir):
    tech_stack_counts = developers_df['primary_tech'].value_counts()
    tech_stacks = tech_stack_counts.index.tolist()
    tech_to_id = {tech: i for i, tech in enumerate(tech_stacks)}
    
    tech_collab_matrix = pd.DataFrame(0, index=tech_stacks, columns=tech_stacks, dtype=float)
    
    for _, edge in latest_network_df.iterrows():
        source_tech = developers_df[developers_df['developer_id'] == edge['source']]['primary_tech'].iloc[0]
        target_tech = developers_df[developers_df['developer_id'] == edge['target']]['primary_tech'].iloc[0]
        tech_collab_matrix.loc[source_tech, target_tech] += edge['weight']
    
    G_tech = nx.DiGraph()
    
    for tech in tech_stacks:
        G_tech.add_node(tech, size=tech_stack_counts[tech])
    
    for source_tech in tech_stacks:
        for target_tech in tech_stacks:
            weight = tech_collab_matrix.loc[source_tech, target_tech]
            if weight > 0:
                G_tech.add_edge(source_tech, target_tech, weight=weight)
    
    tech_colors = {
        'Python': '#4285F4',
        'JavaScript': '#EA4335',
        'Java': '#FBBC05',
        'Go': '#34A853',
        'Rust': '#000000',
        'C++': '#00599C',
        'TypeScript': '#3178C6'
    }
    
    node_sizes = [G_tech.nodes[tech]['size'] * 100 for tech in G_tech.nodes()]
    edge_widths = [G_tech.edges[edge]['weight'] * 0.5 for edge in G_tech.edges()]
    node_colors = [tech_colors.get(tech, '#9AA0A6') for tech in G_tech.nodes()]
    
    plt.figure(figsize=(12, 10), dpi=150)
    pos = nx.spring_layout(G_tech, k=0.8, iterations=20)
    
    nx.draw_networkx_nodes(G_tech, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(G_tech, pos, width=edge_widths, alpha=0.5, edge_color='#9AA0A6')
    nx.draw_networkx_labels(G_tech, pos, font_size=12, font_weight='bold', alpha=0.9, font_color='white')
    
    edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G_tech.edges(data=True) if d['weight'] > 2}
    nx.draw_networkx_edge_labels(G_tech, pos, edge_labels=edge_labels, font_size=8, alpha=0.7)
    
    plt.title('技术栈协作网络', fontsize=24, fontweight='bold', pad=20)
    
    plt.text(0.02, 0.02, f'节点大小表示技术栈开发者数量\n边粗细表示技术栈间合作强度',
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='bottom',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    plt.axis('off')
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'tech_stack_collaboration_graph.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    print(f"    已保存: {output_path}")


if __name__ == "__main__":
    generate_network_visualizations()