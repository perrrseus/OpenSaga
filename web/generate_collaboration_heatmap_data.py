#!/usr/bin/env python3
import csv
from collections import defaultdict

# 读取处理后的双向协作数据
input_file = 'viz/for_viz_edges_two_directions_processed.csv'

# 用于存储去重后的合作关系
collaboration_map = defaultdict(float)

with open(input_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        source = row['source']
        target = row['target']
        weight = float(row['weight'])
        
        # 确保source < target，避免重复计算双向合作
        if int(source) < int(target):
            key = (source, target)
        else:
            key = (target, source)
        
        # 取最大值作为合作强度
        if weight > collaboration_map[key]:
            collaboration_map[key] = weight

# 将合作关系转换为列表并按照权重降序排序
collaboration_list = [(k[0], k[1], v) for k, v in collaboration_map.items()]
collaboration_list.sort(key=lambda x: x[2], reverse=True)

# 提取前20个最强的合作关系
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