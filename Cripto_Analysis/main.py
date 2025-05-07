import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

st.set_page_config(page_title="Dashboard Cripto", layout="wide")

st.title("📊 Dashboard de Criptomoedas - CoinGecko API")

# --- Funções ---

@st.cache_data
def listar_moedas():
    url = "https://api.coingecko.com/api/v3/coins/list"
    resposta = requests.get(url)
    return resposta.json()

@st.cache_data
def obter_dados_historicos(coin_id, dias=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": dias}
    resposta = requests.get(url, params=params).json()
    precos = resposta["prices"]
    df = pd.DataFrame(precos, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

@st.cache_data
def obter_preco_atual(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin_id, "vs_currencies": "usd,brl"}
    resposta = requests.get(url, params=params).json()
    return resposta[coin_id]

# --- Interface ---

moedas = listar_moedas()
moedas_ordenadas = sorted(moedas, key=lambda x: x["name"])

opcoes = [f'{m["name"]} ({m["symbol"].upper()})' for m in moedas_ordenadas]
moeda_escolhida = st.selectbox("Escolha a criptomoeda", opcoes)

moeda_id = next(m["id"] for m in moedas_ordenadas if f'{m["name"]} ({m["symbol"].upper()})' == moeda_escolhida)

col1, col2 = st.columns([1, 3])

with col1:
    dias = st.selectbox("Intervalo de dias", [1, 7, 30, 90, 180, 365, "max"])

with col2:
    preco = obter_preco_atual(moeda_id)
    st.metric(label="💰 Preço Atual (USD)", value=f'${preco["usd"]:.2f}')
    st.metric(label="💰 Preço Atual (BRL)", value=f'R${preco["brl"]:.2f}')

# --- Gráfico ---
df = obter_dados_historicos(moeda_id, dias)

grafico = go.Figure()
grafico.add_trace(go.Scatter(x=df["date"], y=df["price"], mode="lines", name="Preço USD"))
grafico.update_layout(title=f"Variação de Preço: {moeda_escolhida}", xaxis_title="Data", yaxis_title="Preço (USD)")

st.plotly_chart(grafico, use_container_width=True)