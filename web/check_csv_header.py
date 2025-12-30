#!/usr/bin/env python3

# 读取CSV文件的前几行
file_path = 'viz/for_viz_edges_two_directions.csv'
print(f"正在读取文件: {file_path}")

with open(file_path, 'r', encoding='utf-8') as f:
    # 读取所有行
    lines = f.readlines()
    print(f"文件共有 {len(lines)} 行")
    
    # 显示前3行
    for i in range(min(3, len(lines))):
        line = lines[i]
        print(f"\n第{i+1}行原始内容:")
        print(repr(line))
        
        # 显示分割后的内容
        parts = line.strip().split(',')
        print(f"分割后共有 {len(parts)} 列:")
        for j, part in enumerate(parts):
            print(f"  列{j+1}: {repr(part)}")