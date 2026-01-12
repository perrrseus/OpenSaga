#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def generate_time_evolution_visualizations():
    print("=" * 60)
    print("生成时间演化可视化图")
    print("=" * 60)
    
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_path, 'data')
    graph_dir = os.path.join(project_path, 'graph')
    os.makedirs(graph_dir, exist_ok=True)
    
    print("1. 加载数据...")
    try:
        monthly_df = pd.read_csv(os.path.join(data_dir, 'monthly_metrics.csv'))
        community_monthly_df = pd.read_csv(os.path.join(data_dir, 'community_evolution_monthly.csv'))
        print(f"    月度指标数据: {len(monthly_df)} 个月份")
        print(f"    社区演化月度数据: {len(community_monthly_df)} 个月份")
    except Exception as e:
        print(f"    加载数据失败: {e}")
        return None
    
    print("\n2. 生成月度活跃开发者趋势图...")
    generate_active_developers_trend(monthly_df, graph_dir)
    
    print("\n3. 生成合作次数与强度趋势图...")
    generate_collaboration_trend(monthly_df, graph_dir)
    
    print("\n4. 生成社区数量与规模演化图...")
    generate_community_evolution(community_monthly_df, graph_dir)
    
    print("\n5. 生成网络健康指标趋势图...")
    generate_network_health_trend(community_monthly_df, graph_dir)
    
    print("\n6. 生成分析文件...")
    generate_analysis_file(graph_dir)
    
    print("\n" + "=" * 60)
    print(" 所有时间演化可视化图生成完成！")
    print(f" 图像已保存到: {graph_dir}")
    print(f" 分析文件已保存到: {os.path.join(graph_dir, 'time_evolution_analysis.md')}")
    print("=" * 60)


def generate_active_developers_trend(monthly_df, output_dir):
    monthly_df = monthly_df.sort_values('year_month')
    plt.figure(figsize=(12, 6), dpi=150)
    plt.plot(monthly_df['year_month'], monthly_df['num_active_developers'],
             marker='o', linestyle='-', linewidth=2, markersize=6, color='#4285F4')
    plt.title('月度活跃开发者趋势', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('月份', fontsize=12, labelpad=10)
    plt.ylabel('活跃开发者数量', fontsize=12, labelpad=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'active_developers_trend.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    print(f"    已保存: {output_path}")


def generate_collaboration_trend(monthly_df, output_dir):
    monthly_df = monthly_df.sort_values('year_month')
    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=150)
    
    ax1.plot(monthly_df['year_month'], monthly_df['num_collaborations'],
             marker='o', linestyle='-', linewidth=2, markersize=6, color='#4285F4')
    ax1.set_xlabel('月份', fontsize=12, labelpad=10)
    ax1.set_ylabel('合作次数', fontsize=12, labelpad=10, color='#4285F4')
    ax1.tick_params(axis='y', labelcolor='#4285F4')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    ax2 = ax1.twinx()
    ax2.plot(monthly_df['year_month'], monthly_df['avg_collab_weight'],
             marker='s', linestyle='--', linewidth=2, markersize=6, color='#EA4335')
    ax2.set_ylabel('平均合作强度', fontsize=12, labelpad=10, color='#EA4335')
    ax2.tick_params(axis='y', labelcolor='#EA4335')
    
    plt.title('合作次数与强度趋势', fontsize=16, fontweight='bold', pad=20)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, ['合作次数', '平均合作强度'], loc='upper left', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'collaboration_trend.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    print(f"    已保存: {output_path}")


def generate_community_evolution(community_monthly_df, output_dir):
    community_monthly_df = community_monthly_df.sort_values('year_month')
    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=150)
    
    ax1.plot(community_monthly_df['year_month'], community_monthly_df['num_communities'],
             marker='o', linestyle='-', linewidth=2, markersize=6, color='#4285F4')
    ax1.set_xlabel('月份', fontsize=12, labelpad=10)
    ax1.set_ylabel('社区数量', fontsize=12, labelpad=10, color='#4285F4')
    ax1.tick_params(axis='y', labelcolor='#4285F4')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    ax2 = ax1.twinx()
    ax2.plot(community_monthly_df['year_month'], community_monthly_df['avg_community_size'],
             marker='s', linestyle='--', linewidth=2, markersize=6, color='#EA4335')
    ax2.set_ylabel('平均社区规模', fontsize=12, labelpad=10, color='#EA4335')
    ax2.tick_params(axis='y', labelcolor='#EA4335')
    
    plt.title('社区数量与规模演化', fontsize=16, fontweight='bold', pad=20)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, ['社区数量', '平均社区规模'], loc='upper left', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'community_evolution.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    print(f"    已保存: {output_path}")


def generate_network_health_trend(community_monthly_df, output_dir):
    community_monthly_df = community_monthly_df.sort_values('year_month')
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), dpi=150, sharex=True)
    
    ax1.plot(community_monthly_df['year_month'], community_monthly_df['network_density'],
             marker='o', linestyle='-', linewidth=2, markersize=6, color='#4285F4')
    ax1.set_ylabel('网络密度', fontsize=12, labelpad=10)
    ax1.set_title('网络密度', fontsize=14, fontweight='bold', pad=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    ax2.plot(community_monthly_df['year_month'], community_monthly_df['avg_clustering_coefficient'],
             marker='s', linestyle='--', linewidth=2, markersize=6, color='#EA4335')
    ax2.set_ylabel('平均聚类系数', fontsize=12, labelpad=10)
    ax2.set_title('平均聚类系数', fontsize=14, fontweight='bold', pad=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    ax3.plot(community_monthly_df['year_month'], community_monthly_df['num_connected_components'],
             marker='^', linestyle='-.', linewidth=2, markersize=6, color='#FBBC05')
    ax3.set_xlabel('月份', fontsize=12, labelpad=10)
    ax3.set_ylabel('连通分量数', fontsize=12, labelpad=10)
    ax3.set_title('连通分量数', fontsize=14, fontweight='bold', pad=10)
    ax3.grid(True, alpha=0.3, linestyle='--')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.suptitle('网络健康指标趋势', fontsize=18, fontweight='bold', y=0.98)
    
    output_path = os.path.join(output_dir, 'network_health_trend.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    print(f"    已保存: {output_path}")


def generate_analysis_file(output_dir):
    analysis_content = "# 时间演化分析报告\n\n## 1. 活跃开发者趋势\n\n## 2. 合作模式变化\n\n## 3. 社区演化分析\n\n## 4. 网络健康评估\n"
    output_path = os.path.join(output_dir, 'time_evolution_analysis.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(analysis_content)
    print(f"    已保存: {output_path}")


if __name__ == "__main__":
    generate_time_evolution_visualizations()