#!/usr/bin/env python3
import pandas as pd
import os
import sys


def generate_bidirectional_collaboration_data():
    print("=" * 60)
    print("生成包含整年协作关系的双向协作数据")
    print("=" * 60)
    
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    node_csv_path = os.path.join(project_path, 'viz', 'for_viz_nodes.csv')
    edge_csv_path = os.path.join(project_path, 'viz', 'for_viz_edges.csv')
    output_dir = os.path.join(project_path, 'data')
    output_csv_path = os.path.join(output_dir, '协作网络_合并表.csv')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 自动创建文件夹：{output_dir}")
    
    print("1. 加载数据文件...")
    try:
        df_node = pd.read_csv(node_csv_path, encoding='utf-8')
        df_edge = pd.read_csv(edge_csv_path, encoding='utf-8')
        print(f"    节点数据：{len(df_node)} 条")
        print(f"    边数据（整年）：{len(df_edge)} 条")
    except Exception as e:
        print(f" 加载数据失败：{e}")
        sys.exit(1)
    
    print("\n2. 数据预处理...")
    df_node['developer_id'] = df_node['developer_id'].astype(str).str.strip()
    df_edge['source'] = df_edge['source'].astype(str).str.strip()
    df_edge['target'] = df_edge['target'].astype(str).str.strip()
    print("    数据类型转换完成")
    
    print("\n3. 合并源开发者信息...")
    df_merge = pd.merge(
        df_edge,
        df_node,
        left_on='source',
        right_on='developer_id',
        how='left'
    )
    print(f"    源开发者信息合并完成，记录数：{len(df_merge)}")
    
    print("\n4. 合并目标开发者信息...")
    df_node_target = df_node.rename(columns={
        'developer_id': 'target_developer_id',
        'name': 'target_name',
        'primary_tech': 'target_primary_tech',
        'activity_level': 'target_activity_level',
        'pagerank_score': 'target_pagerank_score',
        'degree_centrality': 'target_degree_centrality',
        'betweenness_centrality': 'target_betweenness_centrality',
        'is_core_developer': 'target_is_core_developer'
    })
    
    df_merge = pd.merge(
        df_merge,
        df_node_target,
        left_on='target',
        right_on='target_developer_id',
        how='left'
    )
    print(f"    目标开发者信息合并完成，记录数：{len(df_merge)}")
    
    print("\n5. 生成双向协作数据...")
    df_merge['direction'] = 'outgoing'
    df_reverse = df_merge.copy()
    df_reverse['source'], df_reverse['target'] = df_reverse['target'], df_reverse['source']
    df_reverse['direction'] = 'incoming'
    df_reverse['developer_id'] = df_reverse['target_developer_id'].fillna('')
    df_reverse['name'] = df_reverse['target_name'].fillna('')
    df_reverse['primary_tech'] = df_reverse['target_primary_tech'].fillna('')
    df_reverse['activity_level'] = df_reverse['target_activity_level'].fillna(0)
    df_reverse['pagerank_score'] = df_reverse['target_pagerank_score'].fillna(0)
    df_reverse['degree_centrality'] = df_reverse['target_degree_centrality'].fillna(0)
    df_reverse['betweenness_centrality'] = df_reverse['target_betweenness_centrality'].fillna(0)
    df_reverse['is_core_developer'] = df_reverse['target_is_core_developer'].fillna(False)
    
    print(f"    正向记录：{len(df_merge)} 条")
    print(f"    反向记录：{len(df_reverse)} 条")
    
    print("\n6. 合并正向和反向记录...")
    df_final = pd.concat([df_merge, df_reverse], ignore_index=True)
    
    print("\n7. 数据清洗...")
    df_final = df_final.dropna(subset=['source', 'target', 'weight'])
    df_final = df_final.reset_index(drop=True)
    print(f"    数据清洗完成，最终记录数：{len(df_final)} 条")
    
    print("\n8. 保存结果...")
    viz_output_path = os.path.join(project_path, 'viz', '协作网络_合并表.csv')
    df_final.to_csv(viz_output_path, encoding='utf-8-sig', index=False)
    print(f"    双向协作数据已保存：{viz_output_path}")
    
    print("\n📊 数据统计：")
    print(f"   总记录数：{len(df_final)} 条")
    print(f"   正向（主动）记录：{len(df_merge)} 条")
    print(f"   反向（被动）记录：{len(df_reverse)} 条")
    print(f"   边数据来源：包含整年协作关系")
    print(f"   包含字段：direction（协作方向）、developer_id、name、source、target、weight等")
    
    print("\n" + "=" * 60)
    print(" 包含整年协作关系的双向协作数据生成完成！")
    print(" 所有修改后的数据已保存到viz文件夹")
    print("=" * 60)
    
    return df_final


if __name__ == "__main__":
    generate_bidirectional_collaboration_data()