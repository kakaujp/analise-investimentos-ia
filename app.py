import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Investidor Pro AI", layout="wide")

# Sidebar - Menu de Navegação
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
        st.header(f"📊 Panorama: {info.get('longName', ticker)}")
        
        # Cards de Destaque
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Preço Atual", f"R$ {info.get('currentPrice', 0):.2f}")
        c2.metric("P/L", f"{info.get('forwardPE', 0):.2f}")
        c3.metric("P/VP", f"{info.get('priceToBook', 0):.2f}")
        c4.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%")

        # Gráfico de Preço Interativo
        st.subheader("Evolução Patrimonial (5 Anos)")
        fig = px.line(hist, x=hist.index, y='Close', labels={'Close': 'Preço', 'Date': 'Data'})
        fig.update_traces(line_color='#00FF00')
        st.plotly_chart(fig, use_container_width=True)

    # --- ABA 2: ANÁLISE DE DIVIDENDOS ---
    elif aba_selecionada == "Análise de Dividendos":
        st.header("💰 Estratégia de Renda Passiva")
        
        preco_atual = info.get('currentPrice', 1)
        dps = info.get('dividendRate', 0) or (preco_atual * info.get('dividendYield', 0))
        preco_teto = dps / 0.06

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Dividendos por Ação (12m):** R$ {dps:.2f}")
            st.write(f"**Preço Teto (Método Barsi - 6%):** R$ {preco_teto:.2f}")
        
        with col2:
            margem = (preco_teto / preco_atual - 1) * 100
            st.metric("Margem de Segurança", f"{margem:.2f}%", delta=f"{margem:.2f}%")

    # --- ABA 3: CHECKLIST DE SAÚDE ---
    elif aba_selecionada == "Checklist de Saúde":
        st.header("✅ Critérios de Qualidade e Valor")
        
        # Cálculos Necessários para o Checklist
        preco_atual = info.get('currentPrice', 0)
        dps = info.get('dividendRate', 0) or (preco_atual * info.get('dividendYield', 0))
        preco_teto = dps / 0.06
        
        def check(condicao, texto):
            if condicao:
                st.success(f"✅ {texto}")
            else:
                st.error(f"❌ {texto}")

        # Parâmetro de Preço Teto (Novo)
        check(preco_atual <= preco_teto, f"Preço Teto: R$ {preco_teto:.2f} (Preço atual R$ {preco_atual:.2f} {'abaixo' if preco_atual <= preco_teto else 'acima'} do teto)")
        
        # Demais Parâmetros
        check(info.get('returnOnEquity', 0) > 0.15, f"ROE de {info.get('returnOnEquity', 0)*100:.2f}% (Acima de 15% ideal)")
        check(info.get('profitMargins', 0) > 0.10, f"Margem Líquida de {info.get('profitMargins', 0)*100:.2f}% (Acima de 10% ideal)")
        check(info.get('debtToEquity', 0) < 100, f"Dívida/Patrimônio de {info.get('debtToEquity', 0):.2f}% (Abaixo de 100% ideal)")
        check(info.get('dividendYield', 0) > 0.05, f"Dividend Yield de {info.get('dividendYield', 0)*100:.2f}% (Acima de 5% ideal)")

except Exception as e:
    st.error(f"Erro ao processar dados: {e}")
