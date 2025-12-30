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

print(f"总共有 {len(collaboration_list)} 个独特的合作关系")

# 提取前100强和最后100弱的合作关系
top_100 = collaboration_list[:100]
bottom_100 = collaboration_list[-100:]

# 合并两部分数据，先显示最后100弱，再显示前100强
# 这样可以形成从弱到强的趋势
combined_data = bottom_100 + top_100

# 打印统计信息
print(f"\n前100强合作关系的权重范围: {top_100[0][2]:.2f} - {top_100[-1][2]:.2f}")
print(f"最后100弱合作关系的权重范围: {bottom_100[0][2]:.2f} - {bottom_100[-1][2]:.2f}")

# 生成前端所需的JavaScript代码
print("\n\n前端所需的JavaScript代码：")
print("const collaborationData = [")
for source, target, weight in combined_data:
    print(f"    {{ developer1: '开发者{source}', developer2: '开发者{target}', strength: {weight:.2f} }},")
print("];")

# 生成简化版的JavaScript代码（只包含强度值）
print("\n\n简化版JavaScript代码（只包含强度值）：")
print("const collaborationStrengths = [")
for _, _, weight in combined_data:
    print(f"    {weight:.2f},")
print("];")