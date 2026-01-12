#!/usr/bin/env python3
import csv
from collections import defaultdict


def generate_collaboration_heatmap_data():
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
    
    # 输出前20个最强的合作关系
    print("前20个最强的合作关系：")
    top_20 = collaboration_list[:20]
    
    for i, (source, target, weight) in enumerate(top_20, 1):
        print(f"{i}. 开发者{source} - 开发者{target}: {weight:.2f}")
    
    # 生成前端所需的JavaScript代码
    print("\n\n前端所需的JavaScript代码：")
    print("const collaborationData = [")
    
    for source, target, weight in top_20:
        print(f"    {{ developer1: '开发者{source}', developer2: '开发者{target}', strength: {weight:.2f} }},")
    
    print("];")


if __name__ == "__main__":
    generate_collaboration_heatmap_data()