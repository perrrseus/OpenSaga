import pandas as pd
import numpy as np
import os


node_csv_path = r"C:\Users\31802\Desktop\OpenSaga\viz\for_viz_nodes.csv"
edge_csv_path = r"C:\Users\31802\Desktop\OpenSaga\viz\for_viz_edges.csv"

output_dir = r"C:\Users\31802\Desktop\OpenSaga\data"
output_csv_path = os.path.join(output_dir, "协作网络_合并表.csv")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"📁 自动创建文件夹：{output_dir}")

df_node = pd.read_csv(node_csv_path, encoding='utf-8')
df_edge = pd.read_csv(edge_csv_path, encoding='utf-8')

df_node['developer_id'] = df_node['developer_id'].astype(str).str.strip()
df_edge['source'] = df_edge['source'].astype(str).str.strip()
df_edge['target'] = df_edge['target'].astype(str).str.strip()


df_merge = pd.merge(
    df_edge,  # 主表：协作关系
    df_node,  # 关联表：开发者信息
    left_on='source',  # edge的source匹配node的developer_id
    right_on='developer_id',
    how='left'  # 保留所有协作关系，即使无匹配的开发者
)


# 创建target开发者信息的临时表
df_node_target = df_node.rename(columns={
    'developer_id': 'target_developer_id',
    'name': 'target_name',
    'primary_tech': 'target_primary_tech'
})
# 关联target信息
df_merge = pd.merge(
    df_merge,
    df_node_target,
    left_on='target',
    right_on='target_developer_id',
    how='left'
)


# 标记协作方向（outgoing=主动，incoming=被动）
df_merge['direction'] = 'outgoing'  # 原source→target（主动）
# 生成反向记录（被动视角）
df_reverse = df_merge.copy()
# 交换source/target，标记为incoming
df_reverse['source'], df_reverse['target'] = df_reverse['target'], df_reverse['source']
df_reverse['direction'] = 'incoming'
# 同步更新反向记录的开发者信息
df_reverse['developer_id'] = df_reverse['target_developer_id'].fillna('')
df_reverse['name'] = df_reverse['target_name'].fillna('')
df_reverse['primary_tech'] = df_reverse['target_primary_tech'].fillna('')

# 合并正向+反向记录
df_final = pd.concat([df_merge, df_reverse], ignore_index=True)

# 过滤空值（保留有source/target/weight的记录）
df_final = df_final.dropna(subset=['source', 'target', 'weight'])
# 重置索引
df_final = df_final.reset_index(drop=True)

df_final.to_csv(output_csv_path, encoding='utf-8-sig', index=False)

print("="*50)
print(f"✅ 合并完成！")
print(f"📂 输出文件路径：{output_csv_path}")
print(f"📊 数据统计：")
print(f"   - 总记录数：{len(df_final)} 条")
print(f"   - 正向（主动）记录：{len(df_merge)} 条")
print(f"   - 反向（被动）记录：{len(df_reverse)} 条")
print(f"🔧 包含字段：direction（协作方向）、developer_id、name、source、target、weight等")
print("="*50)