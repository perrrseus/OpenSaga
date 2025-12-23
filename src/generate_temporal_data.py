"""
生成开源协作网络时序数据
生成过去12个月的模拟协作数据,用于时序可视化分析
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_temporal_network_data(months=12, num_developers=50):
    """
    生成时序网络数据
    
    参数:
        months: 生成几个月的数据
        num_developers: 开发者数量
    """
    print("=" * 60)
    print("生成开源协作网络时序数据...")
    print("=" * 60)
    
    # 创建数据目录
    os.makedirs('../data', exist_ok=True)
    
    # 生成开发者信息（静态属性）
    print("1. 生成开发者信息...")
    developers = []
    tech_stacks = ['Python', 'JavaScript', 'Java', 'Go', 'Rust', 'C++', 'TypeScript']
    
    for i in range(num_developers):
        dev = {
            'developer_id': i + 1,
            'name': f'Dev_{i+1:03d}',
            'primary_tech': random.choice(tech_stacks),
            'join_date': datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365)),
            'activity_level': random.uniform(0.3, 1.0)  # 活跃度
        }
        developers.append(dev)
    
    developers_df = pd.DataFrame(developers)
    
    # 生成时序协作关系（动态网络）
    print("2. 生成时序协作关系...")
    all_edges = []
    
    # 基础网络结构（谁倾向于和谁合作）
    base_network = {}
    for dev in developers:
        # 每个开发者有2-5个常合作对象
        num_partners = random.randint(2, 5)
        partners = random.sample([d['developer_id'] for d in developers if d['developer_id'] != dev['developer_id']], 
                                min(num_partners, num_developers-1))
        base_network[dev['developer_id']] = partners
    
    # 生成每个月的数据
    end_date = datetime.now()
    
    for month_offset in range(months-1, -1, -1):
        month_date = end_date - timedelta(days=30*month_offset)
        year_month = month_date.strftime('%Y-%m')
        print(f"  生成 {year_month} 月数据...")
        
        # 每月的协作关系
        for source_id, usual_partners in base_network.items():
            # 开发者本月的活跃度
            source_dev = developers_df[developers_df['developer_id'] == source_id].iloc[0]
            base_activity = source_dev['activity_level']
            
            # 每月协作事件数量
            num_collabs = random.randint(1, 5) if random.random() < base_activity else 0
            
            for _ in range(num_collabs):
                # 80%概率与常合作对象协作，20%概率随机协作
                if random.random() < 0.8 and usual_partners:
                    target_id = random.choice(usual_partners)
                else:
                    target_id = random.choice([d['developer_id'] for d in developers 
                                             if d['developer_id'] != source_id])
                
                # 协作权重（基于技术栈匹配度和活跃度）
                source_tech = source_dev['primary_tech']
                target_dev = developers_df[developers_df['developer_id'] == target_id].iloc[0]
                target_tech = target_dev['primary_tech']
                
                tech_match = 1.0 if source_tech == target_tech else 0.3
                weight = round(tech_match * random.uniform(0.5, 1.5), 2)
                
                edge = {
                    'source': source_id,
                    'target': target_id,
                    'weight': weight,
                    'timestamp': month_date.strftime('%Y-%m-%d'),
                    'year_month': year_month,
                    'source_tech': source_tech,
                    'target_tech': target_tech
                }
                all_edges.append(edge)
    
    edges_df = pd.DataFrame(all_edges)
    
    # 生成月度聚合指标（为DataEase准备）
    print("3. 生成月度聚合指标...")
    monthly_metrics = []
    
    for year_month in sorted(edges_df['year_month'].unique()):
        month_edges = edges_df[edges_df['year_month'] == year_month]
        
        metrics = {
            'year_month': year_month,
            'num_collaborations': len(month_edges),
            'num_active_developers': len(set(month_edges['source'].tolist() + month_edges['target'].tolist())),
            'avg_collab_weight': month_edges['weight'].mean(),
            'unique_pairs': month_edges[['source', 'target']].drop_duplicates().shape[0]
        }
        monthly_metrics.append(metrics)
    
    monthly_df = pd.DataFrame(monthly_metrics)
    
    # 保存所有数据文件
    print("4. 保存数据文件...")
    
    # 开发者信息
    developers_df.to_csv('../data/developers.csv', index=False)
    print(f"   ✅ developers.csv: {len(developers_df)} 位开发者")
    
    # 详细协作关系（时序）
    edges_df.to_csv('../data/collaborations_temporal.csv', index=False)
    print(f"   ✅ collaborations_temporal.csv: {len(edges_df)} 条协作记录")
    
    # 月度聚合指标
    monthly_df.to_csv('../data/monthly_metrics.csv', index=False)
    print(f"   ✅ monthly_metrics.csv: {len(monthly_df)} 个月度指标")
    
    # 最新一个月的数据快照（用于网络图）
    latest_month = edges_df['year_month'].max()
    latest_edges = edges_df[edges_df['year_month'] == latest_month]
    latest_edges[['source', 'target', 'weight']].to_csv('../data/latest_network.csv', index=False)
    print(f"   ✅ latest_network.csv: {latest_month} 月网络快照，{len(latest_edges)} 条边")
    
    print("\n" + "=" * 60)
    print("数据生成完成！")
    print("=" * 60)
    print("\n生成的文件:")
    print("  data/developers.csv          - 开发者属性信息")
    print("  data/collaborations_temporal.csv - 详细时序协作数据")
    print("  data/monthly_metrics.csv     - 月度聚合指标（用于趋势图）")
    print("  data/latest_network.csv      - 最新网络快照（用于网络图）")
    print("\n下一步: 运行 examples/network_analysis.ipynb 进行分析")
    
    return developers_df, edges_df, monthly_df

if __name__ == "__main__":
    # 生成数据
    dev_df, edges_df, monthly_df = generate_temporal_network_data(months=12, num_developers=50)
    
    # 显示数据摘要
    print("\n📊 数据摘要:")
    print(f"• 时间范围: {edges_df['year_month'].min()} 到 {edges_df['year_month'].max()}")
    print(f"• 总协作事件: {len(edges_df):,} 次")
    print(f"• 活跃开发者: {len(dev_df)} 人")
    print(f"• 技术栈分布:")
    print(dev_df['primary_tech'].value_counts().to_string())