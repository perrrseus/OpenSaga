#!/usr/bin/env python3
import csv
from collections import defaultdict


def generate_diverse_collaboration_data():
    input_file = 'viz/for_viz_edges_two_directions_processed.csv'
    collaboration_map = defaultdict(float)
    
    # 读取并处理文件
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            source = row['source']
            target = row['target']
            weight = float(row['weight'])
            
            # 确保合作关系唯一，使用较小的ID作为键的第一个元素
            if int(source) < int(target):
                key = (source, target)
            else:
                key = (target, source)
            
            # 只保留最大的权重值
            if weight > collaboration_map[key]:
                collaboration_map[key] = weight
    
    # 转换为列表并按权重排序
    collaboration_list = [(k[0], k[1], v) for k, v in collaboration_map.items()]
    collaboration_list.sort(key=lambda x: x[2], reverse=True)
    
    print("前50个合作关系的权重值分布：")
    top_50 = collaboration_list[:50]
    
    for i, (source, target, weight) in enumerate(top_50, 1):
        print(f"{i}. 开发者{source} - 开发者{target}: {weight:.2f}")
    
    print("\n\n权重值低于1.50的合作关系：")
    diverse_weights = [item for item in top_50 if item[2] < 1.50]
    
    for i, (source, target, weight) in enumerate(diverse_weights[:20], 1):
        print(f"{i}. 开发者{source} - 开发者{target}: {weight:.2f}")
    
    print("\n\n前端所需的JavaScript代码（多样化权重）：")
    print("const collaborationData = [")
    
    # 生成多样化的数据，包含前10强和10个低于1.50的合作关系
    diverse_data = collaboration_list[:10] + diverse_weights[:10]
    
    for source, target, weight in diverse_data:
        print(f"    {{ developer1: '开发者{source}', developer2: '开发者{target}', strength: {weight:.2f} }},")
    
    print("];")


if __name__ == "__main__":
    generate_diverse_collaboration_data()