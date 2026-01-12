#!/usr/bin/env python3
import csv
from collections import defaultdict


def generate_heatmap_data():
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
    
    print(f"总共有 {len(collaboration_list)} 个独特的合作关系")
    
    # 获取前100强和最后100弱的合作关系
    top_100 = collaboration_list[:100]
    bottom_100 = collaboration_list[-100:]
    combined_data = bottom_100 + top_100
    
    print(f"\n前100强合作关系的权重范围: {top_100[0][2]:.2f} - {top_100[-1][2]:.2f}")
    print(f"最后100弱合作关系的权重范围: {bottom_100[0][2]:.2f} - {bottom_100[-1][2]:.2f}")
    
    # 生成前端所需的JavaScript代码
    print("\n\n前端所需的JavaScript代码：")
    print("const collaborationData = [")
    
    for source, target, weight in combined_data:
        print(f"    {{ developer1: '开发者{source}', developer2: '开发者{target}', strength: {weight:.2f} }},")
    
    print("];")
    
    print("\n\n简化版JavaScript代码（只包含强度值）：")
    print("const collaborationStrengths = [")
    
    for _, _, weight in combined_data:
        print(f"    {weight:.2f},")
    
    print("];")


if __name__ == "__main__":
    generate_heatmap_data()