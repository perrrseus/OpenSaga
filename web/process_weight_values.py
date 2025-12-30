#!/usr/bin/env python3
import csv
import os

# 定义weight的合理范围
MIN_WEIGHT = 0
MAX_WEIGHT = 1.5

# 函数：处理单个CSV文件中的weight值
def process_csv_file(input_path, output_path):
    print(f"\n正在处理文件: {input_path}")
    
    # 读取原始文件
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        print(f"文件 {input_path} 为空")
        return
    
    # 确定weight列的索引
    header = rows[0]
    if 'weight' in header:
        weight_col = header.index('weight')
    else:
        print(f"文件 {input_path} 中没有 'weight' 列")
        return
    
    # 统计原始数据
    original_weights = []
    for row in rows[1:]:
        if len(row) > weight_col:
            try:
                weight = float(row[weight_col])
                original_weights.append(weight)
            except ValueError:
                continue
    
    if not original_weights:
        print(f"文件 {input_path} 中没有有效的weight值")
        return
    
    # 打印统计信息
    print(f"原始数据统计:")
    print(f"  总行数: {len(rows) - 1}")
    print(f"  weight最小值: {min(original_weights):.2f}")
    print(f"  weight最大值: {max(original_weights):.2f}")
    print(f"  weight平均值: {sum(original_weights)/len(original_weights):.2f}")
    
    # 统计异常值
    low_outliers = len([w for w in original_weights if w < MIN_WEIGHT])
    high_outliers = len([w for w in original_weights if w > MAX_WEIGHT])
    print(f"  低于 {MIN_WEIGHT} 的异常值数量: {low_outliers}")
    print(f"  高于 {MAX_WEIGHT} 的异常值数量: {high_outliers}")
    
    # 处理数据
    processed_rows = [header]
    for row in rows[1:]:
        if len(row) > weight_col:
            try:
                weight = float(row[weight_col])
                # 限制weight在合理范围内
                processed_weight = max(MIN_WEIGHT, min(weight, MAX_WEIGHT))
                row[weight_col] = str(processed_weight)
            except ValueError:
                pass
        processed_rows.append(row)
    
    # 写入处理后的文件
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(processed_rows)
    
    print(f"处理完成，结果已保存到: {output_path}")
    print(f"  处理后总行数: {len(processed_rows) - 1}")

# 处理collaborations_temporal.csv
process_csv_file(
    'data/collaborations_temporal.csv', 
    'data/collaborations_temporal_processed.csv'
)

# 处理双向协作数据
process_csv_file(
    'viz/for_viz_edges_two_directions.csv', 
    'viz/for_viz_edges_two_directions_processed.csv'
)

print("\n所有文件处理完成!")