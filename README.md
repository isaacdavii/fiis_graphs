---

# 🌐 Moira Analytics: Terminal Analítico de Risco Sistêmico (IFIX)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Econophysics](https://img.shields.io/badge/Econophysics-Graph_Theory-success)
![Machine Learning](https://img.shields.io/badge/AI-Unsupervised-orange)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://seu-link-do-streamlit-aqui.streamlit.app/)

> **🔴 Demo Online:** Clique no selo "Streamlit" acima ou acesse o dashboard para interagir com a topologia do mercado em tempo real. *(Insira o link após o deploy)*

> **"Investir é um jogo de ligar os pontos. A parte boa é que, quanto mais tempo você passa no mercado e mais curioso intelectualmente você é, maior fica a sua coleção de dados e pontos para conectar." — Ted Weschler, gestor de investimentos da Berkshire Hathaway**

## 📖 Sobre o Projeto

O **Moira Analytics** é um terminal de *Data Science* e Inteligência Artificial focado na modelagem do mercado brasileiro de Fundos de Investimento Imobiliário (IFIX) utilizando a **Teoria das Redes Complexas** e a **Econofísica**.

O objetivo do sistema é transpor a análise fundamentalista tradicional (estática) para uma abordagem topológica (dinâmica). Ao invés de tratar o mercado como uma lista de FIIs, o Moira Analytics mapeia as interdependências de liquidez, identificando gargalos, "bunkers" de proteção e calculando o efeito dominó em cenários de estresse financeiro.

---

## 📉 Motivação: A Ilusão dos Rótulos Setoriais

Muitos investidores acreditam estar diversificados por possuírem fundos de "Shoppings" e "Lajes Corporativas". No entanto, em momentos de crise, fundos de setores nominais distintos frequentemente colapsam juntos devido a correlações ocultas.

O Moira Analytics busca responder: **Como blindar uma carteira mapeando o fluxo do pânico?**
* **Filtro Topológico:** Extrair apenas o "Sinal" (as correlações vitais) em meio ao "Ruído" da bolsa de valores.
* **Inteligência Artificial:** Agrupar FIIs pelo seu comportamento real de risco, ignorando os rótulos oficiais da B3.
* **Teste de Estresse:** Simular ataques direcionados aos "Super-Hubs" para visualizar a fragmentação da liquidez.

---

## 🛠️ Tecnologias e Arquitetura Matemática

Este projeto orquestra algoritmos de ponta em ciência da computação e física estatística:

* **PMFG (*Planar Maximally Filtered Graph*):** Algoritmo de filtragem que preserva a integridade geométrica do mercado (planaridade), superior à tradicional Árvore Geradora Mínima (MST) por permitir ciclos de retroalimentação.
* **Centralidades (Risco):** Avaliação de *Eigenvector* (Efeito Dominó), *Betweenness* (Pontes de Liquidez), *PageRank* e *Closeness*.
* **Machine Learning (Clustering):** Algoritmos não-supervisionados de detecção de comunidades (*Greedy Modularity*, *Louvain*, *Label Propagation* e *Girvan-Newman*).
* **Metodologia Raj Jain:** *Cross-benchmarking* determinístico para validação do modelo, cruzando Modularidade, Cobertura (*Coverage*), NMI e Contraste de Risco.

---

## 📂 Estrutura do Repositório

```text
fiis_graphs(moira-analytics)/
├── docs/                            # Documentação técnica e científica do projeto
├── html/                            # Artefatos visuais e renderizações dinâmicas (PyVis)
│   ├── centralidades/               # Grafos interativos mapeando as 4 dimensões de risco
│   │   ├── pmfg_risco_betweenness.html
│   │   ├── pmfg_risco_closeness.html
│   │   ├── pmfg_risco_eigenvector.html
│   │   └── pmfg_risco_pagerank.html
│   ├── comunidades/                  # Grafos interativos mapeando as 4 metodologias de clustering
│   │   ├── pmfg_comunidade_girvan_newman.html
│   │   ├── pmfg_comunidade_greedy_modularity.html
│   │   ├── pmfg_comunidade_label_propagation.html
│   │   └── pmfg_comunidade_louvain.html
│   └── estresse/                    # Resultados do simulador de colapso (Targeted Attack)
│       └── pmfg_pos_colapso.html
├── img/                             # Imagens estáticas do artigo e gráficos de benchmarking
├── paper/                           # Contém o nosso artigo completo em PDF
├── src/
|   ├── data_processor.py            # Módulo de ingestão e ETL de dados históricos do IFIX  
|   └── network_model.py             # Módulo de construção e análise da rede topológica do mercado  
├── .gitignore                       # Arquivos ocultos (ignora o .venv311 e caches do VS Code)
├── app.py                           # Código-fonte principal do Terminal Web (Streamlit)
├── graphs.ipynb                     # Jupyter Notebook detalhado com a pesquisa matemática
├── LICENSE                          # Licença Creative Commons Atribuição-NãoComercial 4.0 Internacional (CC BY-NC 4.0)
├── README.md                        # Documentação oficial do projeto (este arquivo)
└── requirements.txt                 # Lista de dependências e motores (yfinance, networkx, etc.)
```

O ecossistema do projeto está dividido em duas frentes de operação:

### 1. [O Motor Científico (Jupyter Notebook)](graphs.ipynb)
O coração da pesquisa. Onde os dados brutos se transformam em geometria.
* **Ingestão e ETL:** Extração de séries temporais históricas com `yfinance` e conversão da correlação de Pearson em Distância Euclidiana.
* **Análise de Percolação:** Prova matemática do colapso topológico do método de Limiar (*Threshold*).
* **Benchmarking Determinístico:** O laboratório de testes da IA, elegendo a combinação **Greedy Modularity + Betweenness** como motor principal.
* **Teste de Estresse (*Targeted Attack*):** Simulação computacional deletando os 5 maiores Hubs do mercado para mapear a quebra do componente gigante e isolamento de órfãos.

### 2. [O Terminal Web Interativo (Streamlit App)](app.py)
A interface pronta para produção. Permite que investidores e pesquisadores interajam com o modelo de IA.
* Renderização 2D dinâmica da rede com `Plotly`.
* Ajuste em tempo real de sobrevivência de mercado e recorte temporal.
* Módulo de alocação de carteira (identificação de "Folhas" topológicas para *Hedge*).
* Documentação metodológica e científica embutida.

---

## 📊 Resultados Visuais e Descobertas

> **Nota:** As imagens estáticas abaixo são recortes do artigo. O terminal interativo possui renderização fluida no navegador.

### 1. Transição de Fase (Percolação vs PMFG)
A prova de que cortar correlações fracas arbitrariamente destrói a coesão do mercado. O PMFG preserva as 225 arestas vitais.
![Curva de Percolação](img/percolacao_threshold.png) ### 2. Benchmarking Algorítmico (Raj Jain)
A matriz de decisão matemática provando o "Sweet Spot" de inteligência do algoritmo *Greedy* ao encontrar o equilíbrio perfeito entre descoberta de novas correlações (NMI) e coesão interna.
![Benchmarking Raj Jain](img/benchmarking_raj_jain.png)

### 3. O Colapso dos Super-Hubs (Stress Test)
O mercado financeiro após o *Targeted Attack*. O Grupo Ciano conseguiu manter rotas secundárias de liquidez, enquanto os pontos vermelhos sofreram congelamento isolado.
![Anatomia do Colapso](img/pmfg_pos_colapso.png) ---

## 🚀 Como Executar o App (Ambiente Local)

Siga o passo a passo abaixo para iniciar o Terminal CRISP-NET na sua máquina local.

**1. Clone o repositório:**
```bash
git clone [https://github.com/seu-usuario/crisp-net-ifix.git](https://github.com/seu-usuario/crisp-net-ifix.git)
cd crisp-net-ifix
```

**2. Crie e ative um Ambiente Virtual (Recomendado)**

*Para usuários de Windows:*
```bash
python -m venv .venv
.\.venv\Scripts\activate
```
*Para usuários de Linux/Mac:*
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as Dependências do Projeto**
```bash
pip install -r requirements.txt
```

**4. Execute o Dashboard no Terminal**
```bash
streamlit run app.py
```

**5. Encerre a Sessão**

Após fechar o navegador e parar o servidor no terminal (`Ctrl + C`), desative o ambiente virtual para retornar ao Python global do seu sistema:
```bash
deactivate
```

---

🎓 Equipe de Pesquisa
Projeto desenvolvido na Universidade Federal de Itajubá (UNIFEI) Disciplina: CMAC03 - Algoritmos em Grafos | Professor: Prof. Rafael Frinhani
Pesquisador(a) Matrícula
Ana Paula Gomes Jacó 2025015633
Bianca Salvador 2022012137
Isaac Davi Mendonça Viana 2023000650
Laura Raimundi Dias Jesus 2022002097

---

## ⚖️ Licença e Aviso Legal
Copyright (c) 2026 Ana Paula Gomes Jacó, Bianca Salvador, Isaac Davi Mendonça Viana, Laura Raimundi Dias Jesus.
Este projeto acadêmico e seus artefatos são disponibilizados sob a licença Creative Commons Atribuição-NãoComercial 4.0 Internacional (CC BY-NC 4.0).
É permitido compartilhar e adaptar o material para fins acadêmicos e educacionais.
É terminantemente proibido utilizar este código, seus gráficos ou dados derivados para fins comerciais, plataformas de assinatura, relatórios pagos ou vídeos monetizados sem a autorização expressa dos autores.
⚠️ ISENÇÃO DE RESPONSABILIDADE FINANCEIRA (DISCLAIMER)
ESTE SOFTWARE E OS DADOS NELE CONTIDOS SÃO ESTRITAMENTE DE CARÁTER ACADÊMICO E CIENTÍFICO. NENHUMA INFORMAÇÃO, GRÁFICO OU MÉTRICA AQUI APRESENTADA CONSTITUI RECOMENDAÇÃO DE COMPRA, VENDA, MANUTENÇÃO OU ALOCAÇÃO DE ATIVOS FINANCEIROS. OS AUTORES, O PROFESSOR ORIENTADOR E A INSTITUIÇÃO DE ENSINO NÃO SE RESPONSABILIZAM POR QUAISQUER PREJUÍZOS (DIRETOS OU INDIRETOS) DECORRENTES DA INTERPRETAÇÃO OU USO DO CÓDIGO DESTE PROJETO. O MERCADO DE RENDA VARIÁVEL ENVOLVE ALTO RISCO. O USO DESTA FERRAMENTA É DE INTEIRA RESPONSABILIDADE DO USUÁRIO.