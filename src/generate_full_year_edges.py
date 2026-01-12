#!/usr/bin/env python3
import pandas as pd
import os



def generate_full_year_edges():
    print("=" * 60)
    print("生成完整年度的开发者协作边数据")
    print("=" * 60)
    
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("1. 加载数据文件...")
    developers_df = pd.read_csv(os.path.join(project_path, 'data', 'developers.csv'))
    collab_df = pd.read_csv(os.path.join(project_path, 'data', 'collaborations_temporal.csv'))
    
    print(f"    开发者数据: {len(developers_df)} 位开发者")
    print(f"    协作记录: {len(collab_df)} 条时序记录")
    
    print("\n2. 聚合整年协作关系...")
    
    def get_sorted_edge(row):
        if row['source'] < row['target']:
            return (row['source'], row['target'])
        else:
            return (row['target'], row['source'])
    
    collab_df['unique_edge'] = collab_df.apply(get_sorted_edge, axis=1)
    aggregated_edges = collab_df.groupby('unique_edge')['weight'].sum().reset_index()
    aggregated_edges[['source', 'target']] = pd.DataFrame(aggregated_edges['unique_edge'].tolist(), index=aggregated_edges.index)
    edge_data = aggregated_edges[['source', 'target', 'weight']].copy()
    edge_data['weight'] = edge_data['weight'].round(2)
    
    print(f"    聚合后边数: {len(edge_data)} 条")
    print(f"    平均每条边权重: {edge_data['weight'].mean():.2f}")
    print(f"    最大边权重: {edge_data['weight'].max():.2f}")
    
    print("\n3. 添加技术栈信息...")
    if 'primary_tech' in developers_df.columns:
        edge_data = pd.merge(edge_data,
                             developers_df[['developer_id', 'primary_tech']],
                             left_on='source', right_on='developer_id',
                             how='left')
        edge_data = edge_data.rename(columns={'primary_tech': 'source_tech'})
        edge_data = edge_data.drop(columns=['developer_id'])
        
        edge_data = pd.merge(edge_data,
                             developers_df[['developer_id', 'primary_tech']],
                             left_on='target', right_on='developer_id',
                             how='left')
        edge_data = edge_data.rename(columns={'primary_tech': 'target_tech'})
        edge_data = edge_data.drop(columns=['developer_id'])
        
        edge_data['tech_match'] = edge_data['source_tech'] == edge_data['target_tech']
        edge_data['tech_match_type'] = edge_data.apply(
            lambda x: 'Same Tech' if x['source_tech'] == x['target_tech'] else 'Cross-Tech',
            axis=1
        )
    else:
        edge_data['tech_match'] = False
        edge_data['tech_match_type'] = 'Unknown'
    
    edge_data['strength_level'] = pd.qcut(edge_data['weight'], q=3,
                                           labels=['Low', 'Medium', 'High'])
    
    print("\n4. 保存边数据...")
    viz_dir = os.path.join(project_path, 'viz')
    os.makedirs(viz_dir, exist_ok=True)
    
    output_path = os.path.join(viz_dir, 'for_viz_edges.csv')
    edge_data.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"    边数据已保存到: {output_path}")
    print(f"    数据行数: {len(edge_data)} 条")
    print(f"    数据列名: {list(edge_data.columns)}")
    
    print("\n📊 数据统计:")
    print(f"   总边数: {len(edge_data)}")
    print(f"   相同技术栈协作: {(edge_data['tech_match_type'] == 'Same Tech').sum()} 条")
    print(f"   跨技术栈协作: {(edge_data['tech_match_type'] == 'Cross-Tech').sum()} 条")
    print(f"   协作强度分布:")
    print(edge_data['strength_level'].value_counts().to_string())
    
    print("\n" + "=" * 60)
    print(" 完整年度边数据生成完成!")
    print("=" * 60)
    
    return edge_data


if __name__ == "__main__":
    generate_full_year_edges()