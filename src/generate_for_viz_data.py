#!/usr/bin/env python3
"""
生成viz文件夹下的四个数据文件：
1. for_viz_nodes.csv - 节点数据
2. for_viz_trends.csv - 趋势数据
3. for_viz_communities.csv - 社区数据
4. for_viz_core_developers.csv - 核心开发者数据
"""

import pandas as pd
import networkx as nx
import os
import sys
import subprocess


def generate_for_viz_data():
    """
    生成viz文件夹下的四个数据文件
    """
    print("=" * 60)
    print("生成viz文件夹下的四个数据文件")
    print("=" * 60)
    
    # 获取项目根目录
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 定义文件路径
    data_dir = os.path.join(project_path, 'data')
    viz_dir = os.path.join(project_path, 'viz')
    
    # 确保输出目录存在
    os.makedirs(viz_dir, exist_ok=True)
    
    # 1. 加载数据
    print("1. 加载数据...")
    try:
        developers_df = pd.read_csv(os.path.join(data_dir, 'developers.csv'))
        collab_df = pd.read_csv(os.path.join(data_dir, 'collaborations_temporal.csv'))
        monthly_df = pd.read_csv(os.path.join(data_dir, 'monthly_metrics.csv'))
        latest_network_df = pd.read_csv(os.path.join(data_dir, 'latest_network.csv'))
        community_df = pd.read_csv(os.path.join(data_dir, 'community_evolution_detail.csv'))
        
        print(f"   ✅ 开发者数据: {len(developers_df)} 位开发者")
        print(f"   ✅ 协作记录: {len(collab_df)} 条时序记录")
        print(f"   ✅ 月度指标: {len(monthly_df)} 个月份")
        print(f"   ✅ 最新网络: {len(latest_network_df)} 条边")
        print(f"   ✅ 社区数据: {len(community_df)} 条记录")
    except Exception as e:
        print(f"   ❌ 加载数据失败: {e}")
        return None
    
    # 2. 生成节点数据 (for_viz_nodes.csv)
    print("\n2. 生成节点数据 (for_viz_nodes.csv)...")
    
    # 构建网络
    G = nx.DiGraph()
    
    # 添加节点
    for _, dev in developers_df.iterrows():
        G.add_node(dev['developer_id'], 
                  name=dev['name'],
                  tech=dev['primary_tech'],
                  activity=dev['activity_level'])
    
    # 添加边
    for _, edge in latest_network_df.iterrows():
        if edge['source'] in G and edge['target'] in G:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    print(f"   ✅ 构建了 {G.number_of_nodes()} 个节点, {G.number_of_edges()} 条边的网络")
    
    # 计算网络指标
    pagerank = nx.pagerank(G, alpha=0.85)
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    
    print(f"   ✅ 计算了 PageRank, 度中心性, 介数中心性")
    
    # 准备节点数据
    node_data = []
    for node in G.nodes():
        dev_info = developers_df[developers_df['developer_id'] == node].iloc[0]
        node_data.append({
            'developer_id': node,
            'name': dev_info['name'],
            'primary_tech': dev_info['primary_tech'],
            'activity_level': dev_info['activity_level'],
            'pagerank_score': pagerank[node],
            'degree_centrality': degree_centrality[node],
            'betweenness_centrality': betweenness_centrality[node]
        })
    
    node_df = pd.DataFrame(node_data)
    
    # 计算分位数
    for col in ['pagerank_score', 'degree_centrality', 'betweenness_centrality', 'activity_level']:
        node_df[f'{col}_percentile'] = node_df[col].rank(pct=True) * 100
    
    # 标记核心开发者（PageRank前20%）
    pagerank_threshold = node_df['pagerank_score'].quantile(0.8)
    node_df['is_core_developer'] = node_df['pagerank_score'] >= pagerank_threshold
    
    # 处理浮点数字段，仅对异常浮点数保留两位小数
    print(f"   ✅ 处理浮点数字段，仅对异常浮点数保留两位小数...")
    float_columns = [
        'pagerank_score', 'degree_centrality', 'betweenness_centrality',
        'pagerank_score_percentile', 'degree_centrality_percentile', 
        'betweenness_centrality_percentile', 'activity_level_percentile'
    ]
    
    # 自定义函数：仅对异常浮点数保留两位小数
    def fix_abnormal_floats(x):
        # 检查x是否为浮点数
        if isinstance(x, float):
            # 计算四舍五入到两位小数的值
            rounded = round(x, 2)
            # 检查原始值与四舍五入后的值之差是否小于一个极小值（1e-9）
            # 这个极小值用于判断是否是浮点数精度问题导致的异常值
            if abs(x - rounded) < 1e-9:
                # 是异常浮点数，返回两位小数
                return rounded
        # 正常数值保持原样
        return x
    
    # 对每个浮点数字段应用自定义处理
    for col in float_columns:
        node_df[col] = node_df[col].apply(fix_abnormal_floats)
    
    # 保存节点数据到viz文件夹
    node_output_path = os.path.join(viz_dir, 'for_viz_nodes.csv')
    node_df.to_csv(node_output_path, index=False, encoding='utf-8')
    print(f"   ✅ 节点数据已保存到: {node_output_path}")
    print(f"   ✅ 数据行数: {len(node_df)}")
    
    # 3. 生成趋势数据 (for_viz_trends.csv)
    print("\n3. 生成趋势数据 (for_viz_trends.csv)...")
    
    # 调用现有的generate_for_viz_trends.py脚本
    subprocess.run([sys.executable, os.path.join(project_path, 'src', 'generate_for_viz_trends.py')], 
                   cwd=project_path, check=True)
    print(f"   ✅ 趋势数据已保存到: {os.path.join(viz_dir, 'for_viz_trends.csv')}")
    
    # 4. 生成社区数据 (for_viz_communities.csv)
    print("\n4. 生成社区数据 (for_viz_communities.csv)...")
    
    # 保存社区数据到viz文件夹
    community_output_path = os.path.join(viz_dir, 'for_viz_communities.csv')
    community_df.to_csv(community_output_path, index=False, encoding='utf-8')
    print(f"   ✅ 社区数据已保存到: {community_output_path}")
    print(f"   ✅ 数据行数: {len(community_df)}")
    
    # 5. 生成核心开发者数据 (for_viz_core_developers.csv)
    print("\n5. 生成核心开发者数据 (for_viz_core_developers.csv)...")
    
    # 获取核心开发者
    core_developers = node_df[node_df['is_core_developer']]
    
    # 准备核心开发者汇总数据
    core_developers_summary = core_developers[[
        'developer_id', 'name', 'primary_tech', 'pagerank_score', 
        'degree_centrality', 'betweenness_centrality', 'activity_level'
    ]].sort_values('pagerank_score', ascending=False)
    
    # 保存核心开发者数据到viz文件夹
    core_output_path = os.path.join(viz_dir, 'for_viz_core_developers.csv')
    core_developers_summary.to_csv(core_output_path, index=False, encoding='utf-8')
    print(f"   ✅ 核心开发者数据已保存到: {core_output_path}")
    print(f"   ✅ 数据行数: {len(core_developers_summary)}")
    
    # 6. 显示生成的文件
    print("\n" + "=" * 60)
    print("生成的数据文件:")
    print("=" * 60)
    
    # 检查并显示生成的文件
    for file_name in ['for_viz_nodes.csv', 'for_viz_trends.csv', 
                     'for_viz_communities.csv', 'for_viz_core_developers.csv']:
        file_path = os.path.join(viz_dir, file_name)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / 1024  # KB
            df = pd.read_csv(file_path)
            print(f"✅ {file_name}")
            print(f"   路径: {file_path}")
            print(f"   行数: {len(df)}")
            print(f"   大小: {file_size:.2f} KB")
            print(f"   列名: {list(df.columns)}")
            print()
        else:
            print(f"❌ {file_name} - 生成失败")
            print()
    
    print("=" * 60)
    print("✅ 所有数据文件生成完成！")
    print("✅ 数据已保存到 viz 文件夹")
    print("=" * 60)
    
    return node_df, monthly_df, community_df, core_developers_summary


if __name__ == "__main__":
    import sys
    generate_for_viz_data()
