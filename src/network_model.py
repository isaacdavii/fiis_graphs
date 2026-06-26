import networkx as nx

def construir_pmfg(matriz_distancias):
    """
    Constrói o Grafo Planar Filtrado Maximamente (PMFG)
    a partir da matriz de distâncias euclidianas.
    """
    
    print("Construindo o PMFG (Verificação de Planaridade)...")
    
    # 1. Cria o grafo completo e ordena as arestas da mais forte para a mais fraca
    G_completo = nx.from_pandas_adjacency(matriz_distancias)
    todas_arestas = sorted(G_completo.edges(data = True), key = lambda x: x[2]['weight'])
    
    # 2. Inicializa o PMFG vazio
    PMFG = nx.Graph()
    PMFG.add_nodes_from(G_completo.nodes())
    
    # Limite matemático de arestas para um grafo planar (3N - 6)
    limite_arestas = 3 * len(PMFG.nodes()) - 6
    arestas_adicionadas = 0
    
    # 3. Filtragem Topológica
    for u, v, data in todas_arestas:
        if arestas_adicionadas >= limite_arestas:
            break
            
        PMFG.add_edge(u, v, weight = data['weight'])
        
        is_planar, _ = nx.check_planarity(PMFG)
        
        if is_planar:
            arestas_adicionadas += 1
        else:
            PMFG.remove_edge(u, v)
            
    print(f"PMFG concluído: {len(PMFG.edges())} conexões ótimas estabelecidas.")
    return PMFG

def calcular_metricas_rede(grafo):
    """
    Calcula MÚLTIPLAS métricas de Risco Sistêmico (Centralidades) e injeta no grafo.
    """
    
    print("Calculando múltiplas métricas de influência de mercado...")
    
    # 1. Preparar pesos de Similaridade para os algoritmos de contágio e IA
    for u, v, d in grafo.edges(data = True):
        distancia = d.get('weight', 1.0)
        grafo[u][v]['sim_louvain'] = max(0.0, 2.0 - distancia)
        
    # 2. Computar as 4 matrizes de Centralidade
    cent_eigen = nx.eigenvector_centrality(grafo, max_iter = 1000, weight = 'sim_louvain')
    cent_betw = nx.betweenness_centrality(grafo, weight = 'weight')
    cent_page = nx.pagerank(grafo, weight = 'sim_louvain')
    cent_close = nx.closeness_centrality(grafo, distance = 'weight')
    
    # 3. Injetar como atributos de nó na topologia
    nx.set_node_attributes(grafo, cent_eigen, 'cent_eigen')
    nx.set_node_attributes(grafo, cent_betw, 'cent_betw')
    nx.set_node_attributes(grafo, cent_page, 'cent_page')
    nx.set_node_attributes(grafo, cent_close, 'cent_close')
    
    return grafo