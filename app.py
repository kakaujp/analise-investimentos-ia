import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuração da Página para Melhor Visualização em Celular
st.set_page_config(
    page_title="Investidor Pro AI", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Começa fechado para ganhar espaço no celular
)

# Estilo CSS para ajustar fontes em telas pequenas
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - Menu de Navegação
st.sidebar.title("🚀 Menu Investidor")
aba_selecionada = st.sidebar.radio("Ir para:", ["Dashboard Principal", "Análise de Dividendos", "Checklist de Saúde"])

ticker_input = st.sidebar.text_input("Ticker (Ex: BBSE3, SAPR11, AAPL):", "BBSE3").strip().upper()
ticker = f"{ticker_input}.SA" if len(ticker_input) >= 5 and "." not in ticker_input else ticker_input

try:
    acao = yf.Ticker(ticker)
    info = acao.info
    hist = acao.history(period="5y")

    # --- ABA 1: DASHBOARD PRINCIPAL ---
    if aba_selecionada == "Dashboard Principal":
        st.header(f"📊 {info.get('shortName', ticker)}")
        
        # No celular, colunas se empilham automaticamente
        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)
        
        c1.metric("Preço", f"R$ {info.get('currentPrice', 0):.2f}")
        c2.metric("P/L", f"{info.get('forwardPE', 0):.2f}")
        c3.metric("P/VP", f"{info.get('priceToBook', 0):.2f}")
        c4.metric("DY", f"{info.get('dividendYield', 0)*100:.2f}%")

        st.subheader("Evolução (5 Anos)")
        # use_container_width=True é essencial para responsividade
        fig = px.line(hist, x=hist.index, y='Close', template="plotly_dark")
        fig.update_traces(line_color='#00FF00')
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300)
        st.plotly_chart(fig, use_container_width=True)

    # --- ABA 2: ANÁLISE DE DIVIDENDOS ---
    elif aba_selecionada == "Análise de Dividendos":
        st.header("💰 Renda Passiva")
        
        preco_atual = info.get('currentPrice', 1)
        dps = info.get('dividendRate', 0) or (preco_atual * info.get('dividendYield', 0))
        preco_teto = dps / 0.06

        st.write(f"**Dividendos/Ação:** R$ {dps:.2f}")
        st.write(f"**Preço Teto (6%):** R$ {preco_teto:.2f}")
        
        margem = (preco_teto / preco_atual - 1) * 100
        st.metric("Margem de Segurança", f"{margem:.2f}%", delta=f"{margem:.2f}%")

    # --- ABA 3: CHECKLIST DE SAÚDE ---
    elif aba_selecionada == "Checklist de Saúde":
        st.header("✅ Checklist de Valor")
        
        preco_atual = info.get('currentPrice', 0)
        dps = info.get('dividendRate', 0) or (preco_atual * info.get('dividendYield', 0))
        preco_teto = dps / 0.06
        
        def check(condicao, texto):
            if condicao:
                st.success(f"✅ {texto}")
            else:
                st.error(f"❌ {texto}")

        # Parâmetros com foco em leitura rápida no celular
        check(preco_atual <= preco_teto, f"Preço Teto: R$ {preco_teto:.2f} (Atual: R$ {preco_atual:.2f})")
        check(info.get('returnOnEquity', 0) > 0.15, f"ROE: {info.get('returnOnEquity', 0)*100:.1f}% (>15%)")
        check(info.get('profitMargins', 0) > 0.10, f"Margem: {info.get('profitMargins', 0)*100:.1f}% (>10%)")
        check(info.get('debtToEquity', 0) < 100, f"Dívida/Patrimônio: {info.get('debtToEquity', 0):.1f}% (<100%)")

except Exception as e:
    st.error("Ativo não encontrado. Verifique o Ticker.")
