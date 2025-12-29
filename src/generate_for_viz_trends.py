#!/usr/bin/env python3
"""
生成符合要求格式的for_viz_trends.csv文件
将monthly_metrics.csv转换为包含unique、non_unique和total三种协作类型的格式
"""

import pandas as pd
import os

def generate_for_viz_trends():
    """
    生成符合要求格式的for_viz_trends.csv文件
    """
    print("=" * 60)
    print("生成符合要求格式的for_viz_trends.csv文件")
    print("=" * 60)
    
    # 获取项目根目录
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 定义文件路径
    input_path = os.path.join(project_path, 'data', 'monthly_metrics.csv')
    output_dir = os.path.join(project_path, 'viz')
    output_path = os.path.join(output_dir, 'for_viz_trends.csv')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载数据
    print("1. 加载数据...")
    try:
        df = pd.read_csv(input_path)
        print(f"   ✅ 原始数据：{len(df)} 条记录")
        print(f"   ✅ 数据字段：{list(df.columns)}")
    except Exception as e:
        print(f"❌ 加载数据失败：{e}")
        return None
    
    # 处理数据
    print("\n2. 处理数据...")
    
    # 创建结果列表
    result = []
    
    # 遍历每个月份的数据
    for _, row in df.iterrows():
        # 计算non_unique值
        non_unique = row['num_collaborations'] - row['unique_pairs']
        
        # 添加三种类型的记录
        # 1. unique类型
        result.append({
            'year_month': row['year_month'],
            'num_collaborations': row['num_collaborations'],
            'num_active_developers': row['num_active_developers'],
            'avg_collab_weight': row['avg_collab_weight'],
            'unique_pairs': row['unique_pairs'],
            'collab_type': 'unique',
            'non_unique': non_unique,
            'target_value': row['unique_pairs']
        })
        
        # 2. non_unique类型
        result.append({
            'year_month': row['year_month'],
            'num_collaborations': row['num_collaborations'],
            'num_active_developers': row['num_active_developers'],
            'avg_collab_weight': row['avg_collab_weight'],
            'unique_pairs': row['unique_pairs'],
            'collab_type': 'non_unique',
            'non_unique': non_unique,
            'target_value': non_unique
        })
        
        # 3. total类型
        result.append({
            'year_month': row['year_month'],
            'num_collaborations': row['num_collaborations'],
            'num_active_developers': row['num_active_developers'],
            'avg_collab_weight': row['avg_collab_weight'],
            'unique_pairs': row['unique_pairs'],
            'collab_type': 'total',
            'non_unique': non_unique,
            'target_value': row['num_collaborations']
        })
    
    # 转换为DataFrame
    df_result = pd.DataFrame(result)
    print(f"   ✅ 处理后数据：{len(df_result)} 条记录")
    
    # 保存结果
    print("\n3. 保存结果...")
    df_result.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"   ✅ 结果已保存到：{output_path}")
    
    # 显示样本数据
    print("\n📊 样本数据：")
    print(df_result.head(9))  # 显示前3个月的数据
    
    print("\n" + "=" * 60)
    print("✅ for_viz_trends.csv 文件生成完成！")
    print("=" * 60)
    
    return df_result

if __name__ == "__main__":
    generate_for_viz_trends()
