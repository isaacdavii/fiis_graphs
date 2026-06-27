"""
Estes são os passos recomendados para rodar este painel:
1 - Instale o Python 3.10 ou superior (recomendado: 3.11)
2 - Crie um ambiente virtual (recomendado: venv ou conda)
3 - Instale as dependências do projeto:
        pip install -r requirements.txt
4 - Ative com o ambiente virtual:
        # Windows
        .\venv\Scripts\activate
        # Linux / MacOS
        source venv/bin/activate        
5 - Execute o painel com:
        streamlit run app.py
6 - Para encerrar o painel, pressione Ctrl+C no terminal ou feche a aba do navegador.
7 - Para desativar o ambiente virtual, use:
        deactivate
"""

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import networkx.algorithms.community as nx_comm
import pandas as pd
import numpy as np

# Importando os nossos módulos matemáticos criados anteriormente na pasta src/
from src.data_processor import carregar_dados_historicos, limpar_dados_fiis, gerar_matriz_distancias
from src.network_model import construir_pmfg, calcular_metricas_rede

# ===============================================
# 1. CONFIGURAÇÕES DA PÁGINA E REGRA DE NEGÓCIOS
# ===============================================
st.set_page_config(page_title = "Moira Analytics Terminal | IFIX", layout = "wide", page_icon = "📊")

# Dicionário de Setores Mapeados Manualmente (A "Realidade" da B3)
setores_reais = {
    'HGLG11.SA': 'Logística', 'BTLG11.SA': 'Logística', 'XPLG11.SA': 'Logística', 'VILG11.SA': 'Logística', 'LVBI11.SA': 'Logística', 'BRCO11.SA': 'Logística',
    'MXRF11.SA': 'Papel', 'KNCR11.SA': 'Papel', 'IRDM11.SA': 'Papel', 'CPTS11.SA': 'Papel', 'KNIP11.SA': 'Papel', 'HCTR11.SA': 'Papel', 'RECR11.SA': 'Papel',
    'VISC11.SA': 'Shoppings', 'XPML11.SA': 'Shoppings', 'HGBS11.SA': 'Shoppings', 'HSML11.SA': 'Shoppings',
    'BRCR11.SA': 'Lajes Corp.', 'VINO11.SA': 'Lajes Corp.', 'HGRE11.SA': 'Lajes Corp.', 'PVBI11.SA': 'Lajes Corp.',
    'SDIL11.SA': 'Logística', 'HTMX11.SA': 'Renda Urbana', 'FIIB11.SA': 'Logística',
    'HGRU11.SA': 'Renda Urbana', 'TRXF11.SA': 'Renda Urbana', 'BBPO11.SA': 'Renda Urbana', 'NVHO11.SA': 'Renda Urbana',
    'RZTR11.SA': 'Fiagro', 'BTAL11.SA': 'Fiagro', 'BCRI11.SA': 'Papel', 'RBRR11.SA': 'Papel', 'FIGS11.SA': 'Shoppings',
    'MCCI11.SA': 'FoF', 'KFOF11.SA': 'FoF', 'HGFF11.SA': 'FoF',
    'ALZR11.SA': 'Híbrido', 'TGAR11.SA': 'Desenvolvimento', 'BARI11.SA': 'Papel',
    'BCIA11.SA': 'FoF', 'CARE11.SA': 'Renda Urbana',
    'CBOP11.SA': 'Lajes Corp.', 'CPFF11.SA': 'FoF', 'CXCE11.SA': 'Lajes Corp.',
    'FLMA11.SA': 'Híbrido', 'FVPQ11.SA': 'Shoppings', 'GGRC11.SA': 'Logística', 'GTWR11.SA': 'Lajes Corp.',
    'HABT11.SA': 'Papel', 'HGCR11.SA': 'Papel', 'HGPO11.SA': 'Lajes Corp.', 'HPDP11.SA': 'Shoppings',
    'HRDF11.SA': 'Desenvolvimento', 'HUSC11.SA': 'Renda Urbana',
    'JSRE11.SA': 'Lajes Corp.', 'KNHY11.SA': 'Papel', 'KNRE11.SA': 'Desenvolvimento', 'KNRI11.SA': 'Híbrido',
    'MBRF11.SA': 'Renda Urbana', 'MFII11.SA': 'Desenvolvimento', 'NEWL11.SA': 'Logística',
    'OUJP11.SA': 'Papel', 'PABY11.SA': 'Híbrido', 'PATC11.SA': 'Lajes Corp.', 'PLCR11.SA': 'Papel',
    'PORD11.SA': 'Papel', 'PQDP11.SA': 'Shoppings', 'RBOP11.SA': 'Lajes Corp.', 'RBRF11.SA': 'FoF',
    'RBRP11.SA': 'Híbrido', 'RBRY11.SA': 'Papel', 'RBVA11.SA': 'Renda Urbana',
    'RCFA11.SA': 'Híbrido', 'RCRB11.SA': 'Lajes Corp.', 'RECT11.SA': 'Lajes Corp.', 'RNDP11.SA': 'Papel',
    'RNGO11.SA': 'Lajes Corp.', 'SARE11.SA': 'Híbrido', 'SPTW11.SA': 'Lajes Corp.', 'VGIP11.SA': 'Papel',
    'VGIR11.SA': 'Papel', 'VRTA11.SA': 'Papel', 'XPIN11.SA': 'Logística', 'XPSF11.SA': 'FoF',
}

# Paleta Neon de Alto Contraste (Para os Setores da B3)
paleta_cores = {
    'Logística': '#00F3FF', 'Papel': '#FF0055', 'Shoppings': '#FFF000',
    'Lajes Corp.': '#00FF41', 'Renda Urbana': '#FF9100', 'Fiagro': '#2E5BFF',
    'FoF': '#FFFFFF', 'Híbrido': '#D100FF', 'Desenvolvimento': '#FF00F7',
    'Outros': '#444444'
}

paleta_ia = ['#00F3FF', '#FF0055', '#FFF000', '#00FF41', '#FF9100', '#D100FF', '#FF00F7', '#FFFFFF', '#4ECDC4']

tickers_ifix = list(setores_reais.keys()) 

# =====================================
# 2. MOTOR DE RENDERIZAÇÃO 2D DINÂMICO
# =====================================
def renderizar_grafo_2d(grafo, modo_cor, metrica_nome, atributo_metrica, algoritmo_nome):
    pos_2d = nx.spring_layout(grafo, dim = 2, seed = 42)
    edge_x, edge_y = [], []
    for u, v in grafo.edges():
        x0, y0 = pos_2d[u]
        x1, y1 = pos_2d[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    trace_arestas = go.Scatter(
        x = edge_x, 
        y = edge_y, 
        mode = 'lines',
        line = dict(color = 'rgba(150,150,150,0.3)', width = 1), 
        hoverinfo = 'none'
    )

    n_x, n_y, n_color, n_size, n_text = [], [], [], [], []
    
    # Extrai os valores da métrica escolhida pelo usuário
    valores_metrica = nx.get_node_attributes(grafo, atributo_metrica)
    max_val = max(valores_metrica.values()) if valores_metrica else 1

    # Roteamento dos Algoritmos de Machine Learning
    if "Inteligência Artificial" in modo_cor:
        if algoritmo_nome == "Louvain":
            comunidades = nx_comm.louvain_communities(grafo, weight = 'sim_louvain', seed = 42)
        elif algoritmo_nome == "Greedy":
            comunidades = list(nx_comm.greedy_modularity_communities(grafo, weight = 'sim_louvain'))
        elif algoritmo_nome == "Label Propagation":
            comunidades = list(nx_comm.asyn_lpa_communities(grafo, weight = 'sim_louvain', seed = 42))
        elif algoritmo_nome == "Girvan-Newman":
            def aresta_mais_valiosa(g):
                cent = nx.edge_betweenness_centrality(g, weight = 'weight')
                return max(cent, key = cent.get)
            comunidades = next(nx_comm.girvan_newman(grafo, most_valuable_edge = aresta_mais_valiosa))
            
        mapa_comunidades = {}
        for id_com, com in enumerate(comunidades):
            for no in com:
                mapa_comunidades[no] = id_com

    for node in grafo.nodes():
        x, y = pos_2d[node]
        n_x.append(x); n_y.append(y)
        
        c_val = valores_metrica.get(node, 0)
        # Escala dinâmica do tamanho da bolinha com base no max_val
        n_size.append(10 + ((c_val / max_val) * 80)) 
        
        setor = setores_reais.get(node, 'Outros')
        
        if "Inteligência Artificial" in modo_cor:
            id_cluster = mapa_comunidades.get(node, 0)
            n_color.append(paleta_ia[id_cluster % len(paleta_ia)])
            n_text.append(f"Ticker: {node.replace('.SA','')}<br><b>Cluster IA: {id_cluster} ({algoritmo_nome})</b><br>Setor B3: {setor}<br>{metrica_nome}: {c_val:.4f}")
        else:
            n_color.append(paleta_cores.get(setor, '#444444'))
            n_text.append(f"Ticker: {node.replace('.SA','')}<br>Setor: {setor}<br>{metrica_nome}: {c_val:.4f}")

    trace_nos = go.Scatter(
        x = n_x,
        y = n_y,
        mode = 'markers', 
        text = n_text,
        hoverinfo = 'text',
        marker = dict(size = n_size,
                      color = n_color,
                      opacity = 0.9,
                      line = dict(color = 'black', width = 1))
    )

    fig = go.Figure(data = [trace_arestas, trace_nos])
    fig.update_layout(
        template = "plotly_dark", paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
        showlegend = False, margin = dict(t = 0, b = 0, l = 0, r = 0), height = 600,
        xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
        yaxis = dict(showgrid = False, zeroline = False, showticklabels = False)
    )
    return fig

# =========================
# 3. INTERFACE E CONTROLES
# =========================
st.warning("⚠️ **AVISO LEGAL:** Este painel é o resultado de uma pesquisa acadêmica em Teoria dos Grafos. **NENHUMA informação aqui apresentada constitui recomendação de compra, venda ou alocação de ativos financeiros.**")

st.title("🌐 Moira Analytics Terminal | IFIX")

with st.sidebar:
    st.header("⚙️ Parâmetros do Modelo")
    data_inicio = st.date_input("Data de Início", value = pd.to_datetime("2020-01-01"))
    data_fim = st.date_input("Data Final", value = pd.to_datetime("2025-01-01"))
    taxa_sobrevivencia = st.slider("Filtro de Sobrevivência (%)", 50, 100, 75)
    st.markdown("---")
    botao_executar = st.button("Construir Topologia PMFG", type = "primary", width = 'stretch')

# ======================================
# 4. GATILHO DE EXECUÇÃO E REATIVIDADE
# ======================================
if 'analise_pronta' not in st.session_state:
    st.session_state.analise_pronta = False

if botao_executar:
    st.session_state.analise_pronta = True

if st.session_state.analise_pronta:
    
    @st.cache_data(show_spinner = False)
    def calcular_tudo(d_inicio, d_fim, tx_sobrevivencia):
        precos, volumes = carregar_dados_historicos(tickers_ifix, d_inicio.strftime("%Y-%m-%d"), d_fim.strftime("%Y-%m-%d"))
        df_limpo = limpar_dados_fiis(precos, volumes, taxa_sobrevivencia = (tx_sobrevivencia/100.0))
        matriz_dist = gerar_matriz_distancias(df_limpo)
        pmfg = construir_pmfg(matriz_dist)
        pmfg_com_metricas = calcular_metricas_rede(pmfg)
        return pmfg, pmfg_com_metricas

    with st.spinner("Mapeando ecossistema de risco e aplicando as topologias e IAs..."):
        pmfg_global, pmfg_metricas_global = calcular_tudo(data_inicio, data_fim, taxa_sobrevivencia)
        
    # --- MÉTRICAS GLOBAIS NO TOPO DO DASHBOARD ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Vértices (FIIs Líquidos)", len(pmfg_global.nodes()))
    col2.metric("Arestas Planificadas", len(pmfg_global.edges()))
    
    # Encontra o maior hub sistêmico baseado na centralidade Eigenvector (padrão)
    influencias_dict = nx.get_node_attributes(pmfg_metricas_global, 'cent_eigen')
    maior_hub = max(influencias_dict, key = influencias_dict.get).replace('.SA', '')
    
    col3.metric("Maior Hub Sistêmico", maior_hub)
    st.markdown("---")
    # ---------------------------------------------    

    # O Dicionário de Mapeamento para a Interface UI
    mapa_metricas = {
        "Eigenvector (Contágio Dominó)": "cent_eigen",
        "Betweenness (Pontes de Liquidez)": "cent_betw",
        "PageRank (Acúmulo Aleatório)": "cent_page",
        "Closeness (Velocidade de Choque)": "cent_close"
    }

    aba1, aba2, aba3, aba4 = st.tabs(["🕸️ Topologia e Risco", "🛡️ Estratégia e Perfis", "📚 Resumo Metodológico", "🔬 Artigo Científico e Benchmarking"])

    with aba1:
        # CONTROLES SUPERIORES (AS 3 COLUNAS MÁGICAS)
        col_modo, col_cent, col_alg = st.columns(3)
        
        with col_modo:
            modo_cor = st.radio("🎨 Agrupamento Visual:", ["🏢 Setores Oficiais (B3)", "🤖 Inteligência Artificial"])
            
        with col_cent:
            metrica_escolhida = st.selectbox("📏 Métrica de Risco (Tamanho do Nó):", list(mapa_metricas.keys()))
            
        with col_alg:
            algoritmo_escolhido = st.selectbox(
                "🧠 Motor de IA (Comunidades):", 
                ["Louvain", "Greedy", "Label Propagation", "Girvan-Newman"],
                disabled=("Inteligência Artificial" not in modo_cor)
            )

        st.markdown(f"**Legenda:** Os nós maiores representam os FIIs com o maior índice de **{metrica_escolhida.split(' ')[0]}** sob as condições atuais.")
        
        # O Atributo interno que o Python vai ler baseado na escolha do usuário
        atributo_atual = mapa_metricas[metrica_escolhida]
        
        # Renderização dinâmica com base nas escolhas
        fig_2d = renderizar_grafo_2d(pmfg_metricas_global, modo_cor, metrica_escolhida, atributo_atual, algoritmo_escolhido)
        st.plotly_chart(fig_2d, width = 'stretch', config = {'displayModeBar': False})
        
        # ==============================================================
        # DATAFRAMES REATIVOS (Atualizam sozinhos baseados na Métrica)
        # ==============================================================
        metricas_dict = nx.get_node_attributes(pmfg_metricas_global, atributo_atual)
        df_metricas = pd.DataFrame(list(metricas_dict.items()), columns = ['Ticker', metrica_escolhida])
        df_metricas['Setor'] = df_metricas['Ticker'].map(lambda x: setores_reais.get(x, 'Outros'))
        df_metricas['Ticker'] = df_metricas['Ticker'].str.replace('.SA', '')
        
        df_hubs = df_metricas.sort_values(by = metrica_escolhida, ascending = False).reset_index(drop = True)
        df_folhas = df_metricas.sort_values(by = metrica_escolhida, ascending = True).reset_index(drop = True)

        st.subheader(f"🚨 Top 10 Hubs Sistêmicos ({metrica_escolhida.split(' ')[0]})")
        st.dataframe(df_hubs.head(10), width = 'stretch')

    with aba2:
        st.header("Estudo de Alocação e Diversificação")
        st.markdown("**Regra de Ouro da Diversificação:** Analistas de mercado apontam que não é necessário possuir dezenas de títulos para blindar um portfólio. Uma diversificação estruturada exige entre **8 e 15 FIIs**. O ideal é que cada FII represente entre 5% e 10% do capital destinado a essa classe.")
        
        st.markdown("### Selecione o seu Perfil de Risco Teórico:")
        perfil = st.radio("Perfis:", ["Conservador 🟢", "Moderado 🟡", "Agressivo 🔴"], horizontal = True)

        if "Conservador" in perfil:
            st.success("**Perfil Conservador:** Foco na preservação de capital. Renda variável deve ser mínima (0% a 10%). Priorize ativos *High Grade* ou fundos de tijolo consolidados. Evite fundos de desenvolvimento.")
        elif "Moderado" in perfil:
            st.warning("**Perfil Moderado:** Busca de equilíbrio entre segurança e rentabilidade (15% a 30% em RV). Permite mesclar ativos *High Grade* com uma pequena exposição a Lajes Corporativas *Prime* e Logística.")
        else:
            st.error("**Perfil Agressivo:** Foco no crescimento com tolerância à volatilidade (40% a 70% em RV). Há espaço para fundos de Desenvolvimento ou *High Yield* (maior retorno, maior risco).")

        st.markdown("---")
        st.subheader(f"🍃 Top 10 Folhas Topológicas (Menor {metrica_escolhida.split(' ')[0]})")
        st.markdown("Segundo a métrica selecionada, os ativos abaixo operam na margem da rede topológica, sendo considerados 'Bunkers' estruturais para proteção.")
        st.dataframe(df_folhas.head(10), width = 'stretch')
        
        st.markdown("### 📚 Dê o próximo passo: Due Diligence")
        st.markdown("""
        * 🔍 [StatusInvest](https://statusinvest.com.br/fundos-imobiliarios)
        * 🏢 [ClubeFII](https://www.clubefii.com.br/)
        * 📊 [FundsExplorer](https://www.fundsexplorer.com.br/ranking)
        """)

    with aba3:
        st.header("Transparência Algorítmica (Resumo)")
        st.markdown("Este painel não é uma caixa-preta. Abaixo, detalhamos a arquitetura matemática básica. Para ver o estudo científico completo, acesse a próxima aba.")

        with st.expander("1. Econofísica: De Correlação para Distância"):
            st.markdown("""
            A Teoria dos Grafos entende "distância e custo". Para transformar a correlação de Pearson ($\rho$) em uma distância euclidiana topológica ($d$), aplicamos:
            """)
            st.latex(r"d = \sqrt{2(1 - \rho)}")

        with st.expander("2. Topologia: O Algoritmo PMFG"):
            st.markdown("""
            Utilizamos o **Planar Maximally Filtered Graph (PMFG)**. Ele ordena as conexões mais fortes e as desenha sob a regra da **Planaridade**.
            Isso permite extrair até $3N - 6$ arestas, mantendo os triângulos de risco sem cruzar as linhas.
            """)

        with st.expander("3. Risco Sistêmico (As 4 Centralidades)"):
            st.markdown("""
            O painel permite alternar entre 4 lógicas de risco:
            * **Eigenvector:** O Efeito Dominó ($Ax = \lambda x$).
            * **Betweenness:** Pontes que ligam setores opostos.
            * **PageRank:** A probabilidade do choque parar neste fundo.
            * **Closeness:** A velocidade com que a queda de um fundo atinge os demais.
            """)
        
        with st.expander("4. Algoritmos de Comunidades (Inteligência Artificial)"):
            st.markdown("""
            O usuário pode explorar as quebras estruturais usando 4 IA's distintas:
            1. **Louvain:** Otimização heurística em múltiplas fases (Melhor Custo-Benefício).
            2. **Greedy Modularity:** Otimização gulosa passo-a-passo.
            3. **Label Propagation:** Votação epidêmica local.
            4. **Girvan-Newman:** Modelo divisivo cortando as pontes mais sensíveis.
            """)

    with aba4:
        st.header("Pesquisa e Modelagem Topológica do IFIX")
        st.markdown("""
        Bem-vindo à seção científica deste projeto. Aqui detalhamos as provas matemáticas e os testes de estresse computacional que justificam as escolhas tecnológicas deste terminal, utilizando os critérios internacionais de Benchmarking de Raj Jain.
        """)
        
        st.markdown("---")
        st.subheader("1. A Dinâmica de Percolação e a Superioridade do PMFG")
        st.markdown("""
        Para validar a robustez da nossa arquitetura topológica, implementamos um grupo de controle utilizando o método de **Rede de Limiar (*Threshold Network*)**. O objetivo era responder a um questionamento técnico comum: *"Por que não simplificar a abordagem e apenas deletar as arestas com correlações mais fracas?"*

        Ao testarmos 50 limiares progressivos, provamos estatisticamente que não existe um "ponto ideal":
        * **Limiares Baixos:** A rede vira um "novelo de lã" denso com mais de 2.000 arestas e muito ruído estatístico.
        * **Limiares Altos:** A rede sofre uma Transição de Fase drástica. Próximo ao limiar de correlação 0.16, o mercado entra em colapso e se estilhaça em dezenas de componentes órfãos.

        O algoritmo PMFG, operando sob a restrição de Euler ($E \le 3V - 6$), filtra matematicamente o mercado preservando apenas as 225 conexões mais vitais, garantindo um mercado sempre **100% conectado** e viabilizando os cálculos de risco.
        """)
        
        # Espaço reservado para a imagem gerada no Jupyter Notebook (Curva de Percolação)
        # O usuário precisará salvar a imagem do Plotly como 'percolacao_threshold.png' na pasta raiz
        try:
            st.image("img/percolacao_threshold.png", caption = "Fig 1. Análise de Percolação: O Colapso Topológico do Método Threshold", width = 'stretch')
        except:
            st.info("📌 [Espaço reservado para a imagem 'percolacao_threshold.png'.]")

        st.markdown("---")
        st.subheader("2. Benchmarking Algorítmico (Metodologia Raj Jain)")
        st.markdown("""
        Para garantir o rigor científico da Inteligência Artificial aplicada no agrupamento de FIIs, testamos **4 matrizes matemáticas distintas** na tarefa de clusterização:

        1. **Louvain:** Agrupamento Bottom-up ($O(N \log N)$).
        2. **Greedy Modularity:** Otimização gulosa ($O(N \log^2 N)$).
        3. **Label Propagation:** Votação epidêmica local ($O(E)$).
        4. **Girvan-Newman:** Divisão Top-down baseada em intermediação ($O(E^2 N)$).

        Para avaliar o vencedor absoluto, calculamos o **Score de Eficiência Sistêmica (0-100)**, uma métrica ponderada que cruza:
        * **Modularidade ($Q$) [Peso 35%]:** Avalia a otimização global da rede e a densidade máxima das aglomerações.
        * **Cobertura Topológica (Coverage) [Peso 30%]:** Mede o grau de retenção do risco sistêmico. Um cluster eficiente deve "aprisionar" a maior proporção possível de arestas dentro da sua própria fronteira, minimizando o vazamento de contágio para o restante do mercado.
        * **Informação Mútua Normalizada (NMI) [Peso 20%]:** A métrica de dissimilaridade. Avalia o quanto a Inteligência Artificial consegue descobrir correlações ocultas rentáveis sem se descolar completamente dos macro-setores oficiais da B3.
        * **Contraste de Centralidade [Peso 15%]:** Calculado através do Coeficiente de Variação ($\sigma/\mu$). Avalia matematicamente se a métrica de centralidade possui a clareza estatística necessária para separar e destacar os "Super-Hubs" da massa de fundos secundários.
        """)

        try:
            st.image("img/benchmarking_raj_jain.png", caption = "Fig 2. Relatório Técnico de Eficiência Multi-Algoritmo.", width = 'stretch')
        except:
            st.info("📌 [Espaço reservado para a imagem 'benchmarking_raj_jain.png'.]")

        st.success("🏆 **A Conclusão Matemática:** Conforme demonstrado nos gráficos de avaliação, o algoritmo **Greedy Modularity**, quando combinado à centralidade **Betweenness**, demonstrou o maior grau de Eficiência Sistêmica, provando-se como a arquitetura metodológica definitiva para a versão em produção deste sistema.")

else:
    st.info("👈 Defina as datas na barra lateral e clique no botão para computar a Inteligência Artificial.")