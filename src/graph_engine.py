"""
智能图计算引擎适配器
"""

import warnings
import pandas as pd

class GraphEngine:
    """统一的图计算接口,自动选择后端引擎"""
    
    def __init__(self, backend='auto'):
        """
        初始化图引擎
        
        参数:
            backend: 'auto', 'easygraph', 或 'networkx'
        """
        self.backend = backend
        self.engine = None
        self._init_engine()
        
    def _init_engine(self):
        """初始化后端引擎"""
        if self.backend == 'easygraph' or self.backend == 'auto':
            try:
                import easygraph as eg
                self.engine = eg
                self.engine_name = 'EasyGraph'
                print(f"✅ 成功加载 {self.engine_name}")
                return
            except ImportError as e:
                print(f"⚠️ EasyGraph 加载失败: {e}")
                if self.backend == 'easygraph':
                    raise RuntimeError("指定使用EasyGraph但加载失败")
        
        # 回退到 NetworkX
        try:
            import networkx as nx
            self.engine = nx
            self.engine_name = 'NetworkX'
            
            # 为 NetworkX 添加 EasyGraph 风格的函数别名
            if not hasattr(self.engine, 'DiGraph'):
                self.engine.DiGraph = nx.DiGraph
            if not hasattr(self.engine, 'Graph'):
                self.engine.Graph = nx.Graph
                
            print(f"✅ 使用备用引擎: {self.engine_name}")
        except ImportError as e:
            raise RuntimeError(f"所有图引擎加载失败: {e}")
    
    def create_graph(self, directed=True):
        """创建图对象"""
        if directed:
            return self.engine.DiGraph()
        else:
            return self.engine.Graph()
    
    def add_community_detection(self, G):
        """添加社区检测功能"""
        if self.engine_name == 'EasyGraph':
            # EasyGraph 内置社区检测
            return self.engine.louvain(G.to_undirected()) if hasattr(G, 'to_undirected') else self.engine.louvain(G)
        else:
            # NetworkX 需要 python-louvain 包
            try:
                import community as community_louvain
                # 转换为无向图
                if G.is_directed():
                    G_undir = G.to_undirected()
                else:
                    G_undir = G
                partition = community_louvain.best_partition(G_undir)
                # 将分区格式转换为与EasyGraph一致: [[node1, node2,...], ...]
                communities_dict = {}
                for node, comm_id in partition.items():
                    communities_dict.setdefault(comm_id, []).append(node)
                return list(communities_dict.values())
            except ImportError:
                warnings.warn("未安装python-louvain,使用简单的连通组件作为社区")
                return list(self.engine.connected_components(G.to_undirected()))
    
    def calculate_pagerank(self, G, alpha=0.85):
        """计算PageRank"""
        if self.engine_name == 'EasyGraph':
            return self.engine.pagerank(G, alpha=alpha)
        else:
            return self.engine.pagerank(G, alpha=alpha)
    
    def calculate_degree_centrality(self, G):
        """计算度中心性"""
        if self.engine_name == 'EasyGraph':
            return self.engine.degree_centrality(G)
        else:
            return self.engine.degree_centrality(G)
    
    def get_info(self):
        """获取引擎信息"""
        return {
            'backend': self.engine_name,
            'version': self.engine.__version__ if hasattr(self.engine, '__version__') else '未知'
        }

# 全局默认引擎实例
default_engine = GraphEngine(backend='auto')

def test_engine():
    """测试引擎功能"""
    print("=" * 50)
    print("测试图计算引擎...")
    engine = GraphEngine()
    info = engine.get_info()
    print(f"当前使用引擎: {info['backend']} (版本: {info['version']})")
    
    # 创建测试图
    G = engine.create_graph(directed=True)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 1)
    
    print(f"图节点数: {G.number_of_nodes()}")
    print(f"图边数: {G.number_of_edges()}")
    
    # 计算PageRank
    pagerank = engine.calculate_pagerank(G)
    print(f"PageRank计算成功: {pagerank}")
    
    print("✅ 引擎测试通过！")
    print("=" * 50)
    return engine

if __name__ == "__main__":
    test_engine()