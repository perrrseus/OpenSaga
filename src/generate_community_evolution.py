#!/usr/bin/env python3
# 生成社区演化数据，包含网络级指标

import pandas as pd
import networkx as nx
import os
import sys

def generate_community_evolution():
    """生成社区演化数据"""
    print("=" * 60)
    print("生成社区演化数据")
    print("=" * 60)
    
    # 获取项目根目录
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 定义文件路径
collab_path = os.path.join(project_path, 'data', 'collaborations_temporal.csv')
    developers_path = os.path.join(project_path, 'data', 'developers.csv')
    output_dir = os.path.join(project_path, 'data')
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("1. 加载数据...")
    try:
        collab_df = pd.read_csv(collab_path)
        developers_df = pd.read_csv(developers_path)
        print(f"   协作数据：{len(collab_df)} 条记录")
        print(f"   开发者数据：{len(developers_df)} 条记录")
    except Exception as e:
        print(f"加载数据失败：{e}")
        sys.exit(1)
    
    print("\n2. 检查依赖...")
    try:
        import community as community_louvain
        use_louvain = True
        print("   使用Louvain算法进行社区检测")
    except ImportError:
        use_louvain = False
        print("未安装python-louvain，使用连通组件作为社区")
    
    # 初始化结果
community_evolution = []
    monthly_summary = []
    
    # 按月份分组（按时间排序）
    print("\n3. 按月份分析网络结构演化...")
    monthly_groups = sorted(collab_df.groupby('year_month'), key=lambda x: x[0])
    
    for month_idx, (month, month_data) in enumerate(monthly_groups):
        print(f"   {month}: ", end="")
        
        # 创建该月的网络
        G_month = nx.DiGraph()
        
        # 添加该月活跃的开发者
        active_devs = set(month_data['source']).union(set(month_data['target']))
        for dev_id in active_devs:
            dev_info = developers_df[developers_df['developer_id'] == dev_id]
            if not dev_info.empty:
                G_month.add_node(dev_id, 
                               name=dev_info.iloc[0]['name'],
                               tech=dev_info.iloc[0]['primary_tech'])
        
        # 添加该月的协作关系
        for _, edge in month_data.iterrows():
            G_month.add_edge(edge['source'], edge['target'], weight=edge['weight'])
        
        num_active = len(active_devs)
        num_edges = G_month.number_of_edges()
        
        # 检测社区
        if num_edges > 0:
            if use_louvain:
                # 使用Louvain算法
                G_undir = G_month.to_undirected()
                partition = community_louvain.best_partition(G_undir)
                
                # 重组社区结构
                communities_dict = {}
                for node, comm_id in partition.items():
                    communities_dict.setdefault(comm_id, []).append(node)
                communities = list(communities_dict.values())
                num_communities = len(communities)
                
            else:
                # 使用连通组件
                G_undir = G_month.to_undirected()
                components = list(nx.connected_components(G_undir))
                communities = components
                num_communities = len(components)
                partition = {}
                for comm_id, nodes in enumerate(components):
                    for node in nodes:
                        partition[node] = comm_id
            
            # 记录社区信息
            for comm_id, comm_nodes in enumerate(communities):
                for node in comm_nodes:
                    community_evolution.append({
                        'year_month': month,
                        'month_index': month_idx,
                        'developer_id': node,
                        'community_id': comm_id,
                        'community_size': len(comm_nodes)
                    })
            
            # 计算网络级指标
            G_undir = G_month.to_undirected()
            network_density = nx.density(G_month) if num_active > 1 else 0
            
            # 计算平均聚类系数
            try:
                avg_clustering = nx.average_clustering(G_undir)
            except:
                avg_clustering = 0
            
            # 计算连通分量数
            num_connected_components = nx.number_connected_components(G_undir) if num_active > 0 else 0
            
            # 记录月度汇总
            avg_community_size = sum(len(c) for c in communities) / len(communities) if communities else 0
            
            # 计算社区规模的标准差
            if len(communities) > 1:
                import numpy as np
                community_sizes = [len(c) for c in communities]
                community_size_std = np.std(community_sizes)
            else:
                community_size_std = 0
            
            # 计算平均协作强度
            avg_collab_strength = month_data['weight'].mean() if len(month_data) > 0 else 0
            
            monthly_summary.append({
                'year_month': month,
                'month_index': month_idx,
                'num_active_developers': num_active,
                'num_collaborations': len(month_data),
                'num_edges': num_edges,
                'avg_collab_strength': round(avg_collab_strength, 4),
                'num_communities': num_communities,
                'avg_community_size': round(avg_community_size, 1),
                'community_size_std': round(community_size_std, 2),
                'network_density': round(network_density, 4),
                'avg_clustering_coefficient': round(avg_clustering, 4),
                'num_connected_components': num_connected_components
            })
            
            print(f"{num_active}活跃开发者, {num_edges}条边, {num_communities}个社区")
        else:
            # 当没有边时，设置默认值
            monthly_summary.append({
                'year_month': month,
                'month_index': month_idx,
                'num_active_developers': num_active,
                'num_collaborations': len(month_data),
                'num_edges': num_edges,
                'avg_collab_strength': 0,
                'num_communities': 0,
                'avg_community_size': 0,
                'community_size_std': 0,
                'network_density': 0,
                'avg_clustering_coefficient': 0,
                'num_connected_components': num_active if num_active > 0 else 0
            })
            print(f"{num_active}活跃开发者, 0条边, 0个社区")
    
    # 处理结果
    print("\n4. 处理结果...")
    if community_evolution:
        community_evolution_df = pd.DataFrame(community_evolution)
        monthly_summary_df = pd.DataFrame(monthly_summary)
        
        print(f"社区演化分析完成:")
        print(f"   覆盖 {len(monthly_summary_df)} 个月份")
        print(f"   总记录数: {len(community_evolution_df)} 条")
        print(f"   平均每月社区数: {monthly_summary_df['num_communities'].mean():.1f}")
        
        # 保存数据
        community_evolution_df.to_csv(os.path.join(output_dir, 'community_evolution_detail.csv'), index=False, encoding='utf-8')
        monthly_summary_df.to_csv(os.path.join(output_dir, 'community_evolution_monthly.csv'), index=False, encoding='utf-8')
        
        # 保存用于可视化的数据
        viz_dir = os.path.join(project_path, 'viz')
        os.makedirs(viz_dir, exist_ok=True)
        viz_monthly_path = os.path.join(viz_dir, 'for_viz_community_monthly.csv')
        monthly_summary_df.to_csv(viz_monthly_path, index=False, encoding='utf-8')
        
        print(f"\n数据已保存:")
        print(f"   data/community_evolution_detail.csv")
        print(f"   data/community_evolution_monthly.csv")
        print(f"   viz/for_viz_community_monthly.csv")
        
        print("\n社区演化趋势摘要:")
        print(monthly_summary_df[[
            'year_month', 'num_communities', 'avg_community_size', 'num_active_developers',
            'network_density', 'avg_clustering_coefficient', 'num_connected_components'
        ]].to_string(index=False))
        
        return monthly_summary_df
    else:
        print("未生成有效的社区演化数据")
        return None

if __name__ == "__main__":
    generate_community_evolution()
