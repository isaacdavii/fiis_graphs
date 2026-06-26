import yfinance as yf
import pandas as pd
import numpy as np

def carregar_dados_historicos(tickers, data_inicio, data_fim):
    """
    Baixa os dados históricos de preços e volumes do Yahoo Finance.
    """
    print(f"Baixando dados para {len(tickers)} fundos de {data_inicio} a {data_fim}...")
    
    # yfinance já aplica auto_adjust=True por padrão nas versões mais recentes
    dados = yf.download(tickers, 
                        start = data_inicio,
                        end = data_fim,
                        progress = False)
    
    # Retorna as tabelas de fechamento ajustado e volume
    return dados['Close'], dados['Volume']

def limpar_dados_fiis(precos, volumes, taxa_sobrevivencia = 0.75):
    """
    Aplica os filtros de liquidez e tempo de existência (Data Preparation).
    Remove FIIs que não possuem histórico suficiente ou que ficaram
    muitos dias com volume de negociação zerado.
    """
    print("\nIniciando limpeza e filtragem dos dados...")
    
    # Remove colunas que vieram 100% vazias da API
    precos = precos.dropna(axis = 1, how = 'all')
    volumes = volumes.dropna(axis = 1, how = 'all')
    
    dias_totais = len(precos)
    limite_minimo_dias = dias_totais * taxa_sobrevivencia
    
    # Filtro 1: Sobrevivência ao Tempo (Fundos que existem na maior parte da janela)
    fundos_vivos = precos.dropna(thresh = limite_minimo_dias, axis = 1).columns
    print(f"-> Sobreviveram ao tempo de existência: {len(fundos_vivos)} fundos.")
    
    # Filtro 2: Liquidez Contínua (Ignora dias com 0 negócios)
    volumes_filtrados = volumes[fundos_vivos].replace(0, np.nan)
    fundos_liquidos = volumes_filtrados.dropna(thresh = limite_minimo_dias, axis = 1).columns
    print(f"-> Sobreviveram ao teste de liquidez severa: {len(fundos_liquidos)} fundos.")
    
    # Preenche pequenos buracos de 1 a 2 dias (forward fill) e limpa resquícios
    df_final = precos[fundos_liquidos].ffill().dropna(axis = 0)
    
    print(f"Limpeza concluída! Vértices finais para o grafo: {len(df_final.columns)} FIIs.")
    return df_final

def gerar_matriz_distancias(df_precos_limpos):
    """
    Converte a série de preços em retornos logarítmicos e, em seguida,
    em uma Matriz de Distâncias Euclidianas baseada na Correlação de Pearson.
    """
    print("\nCalculando Retornos Logarítmicos e Matriz de Distâncias...")
    
    # R = ln(Preço_Hoje / Preço_Ontem)
    retornos = np.log(df_precos_limpos / df_precos_limpos.shift(1)).dropna()
    
    # Matriz de Correlação
    matriz_correlacao = retornos.corr()
    
    # Fórmula: d = sqrt(2 * (1 - correlacao))
    # Correlação +1 vira distância 0; Correlação -1 vira distância 2.
    matriz_distancias = np.sqrt(2 * (1 - matriz_correlacao))
    
    return matriz_distancias