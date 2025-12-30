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

# 提取前50个合作关系，以便找到更多样化的权重值
print("前50个合作关系的权重值分布：")
top_50 = collaboration_list[:50]
for i, (source, target, weight) in enumerate(top_50, 1):
    print(f"{i}. 开发者{source} - 开发者{target}: {weight:.2f}")

# 寻找权重值低于1.50的合作关系
print("\n\n权重值低于1.50的合作关系：")
diverse_weights = [item for item in top_50 if item[2] < 1.50]
for i, (source, target, weight) in enumerate(diverse_weights[:20], 1):
    print(f"{i}. 开发者{source} - 开发者{target}: {weight:.2f}")

# 生成前端所需的JavaScript代码，使用更多样化的权重值
print("\n\n前端所需的JavaScript代码（多样化权重）：")
print("const collaborationData = [")
# 结合一些1.50的记录和一些低于1.50的记录
diverse_data = collaboration_list[:10] + diverse_weights[:10]
for source, target, weight in diverse_data:
    print(f"    {{ developer1: '开发者{source}', developer2: '开发者{target}', strength: {weight:.2f} }},")
print("];")