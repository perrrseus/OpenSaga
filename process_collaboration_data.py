#!/usr/bin/env python3

# 读取CSV文件
file_path = 'viz/for_viz_edges_two_directions.csv'

# 用于存储去重后的合作关系
collaboration_map = {}

with open(file_path, 'r', encoding='utf-8-sig') as f:
    # 跳过第一行（列名）
    f.readline()
    
    # 读取剩余行
    for line in f:
        # 分割行
        parts = line.strip().split(',')
        if len(parts) < 3:
            continue
        
        source = parts[0]
        target = parts[1]
        weight = float(parts[2])
        
        # 确保source < target，避免重复计算双向合作
        if int(source) < int(target):
            key = (source, target)
        else:
            key = (target, source)
        
        # 取最大值作为合作强度
        if key not in collaboration_map or weight > collaboration_map[key]:
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
    # 确保权重值不超过1.5
    normalized_weight = min(weight, 1.5)
    print(f"    {{ developer1: '开发者{source}', developer2: '开发者{target}', strength: {normalized_weight:.2f} }},")
print("];")