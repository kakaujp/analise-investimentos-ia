import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Configuração de Estilo
st.set_page_config(page_title="Inabalável Score", layout="wide")

# Tese de Boas-vindas (Baseada no seu Copywriting Cultural)
st.title("🛡️ Sistema de Análise Inabalável")
st.markdown("""
### O mercado foca no preço. Nós focamos no valor.
*Enquanto a maioria joga dinheiro na bolsa como se fosse um cassino, os verdadeiros donos do mundo usam a matemática do 'Preço Teto'. Este app não prevê o futuro, ele revela o preço da sua liberdade.*
""")
st.divider()

# Entrada do Usuário
ticker = st.sidebar.text_input("Digite o Ticker (Ex: SAPR11.SA, BBSE3.SA):", "SAPR11.SA")

if ticker:
    try:
        acao = yf.Ticker(ticker)
        hist = acao.history(period="5y")
        info = acao.info

        # 1. Gráfico de 5 Anos (Crescimento)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Preço', line=dict(color='#00FF00')))
        fig.update_layout(title=f"Histórico de 5 Anos: {ticker}", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # 2. Métricas de Ouro
        col1, col2, col3 = st.columns(3)
        
        preco_atual = info.get('currentPrice', 1)
        # Estimativa de dividendos dos últimos 12 meses
        dps = info.get('dividendRate', 0) if info.get('dividendRate') else (preco_atual * info.get('dividendYield', 0))
        preco_teto = dps / 0.06

        col1.metric("Preço Atual", f"R$ {preco_atual:.2f}")
        col2.metric("Preço Teto (6%)", f"R$ {preco_teto:.2f}", delta=f"{(preco_teto/preco_atual-1)*100:.1f}% Margem")
        
        lpa = info.get('trailingEps', 1)
        vpa = info.get('bookValue', 1)
        preco_justo = np.sqrt(22.5 * lpa * vpa) if lpa > 0 and vpa > 0 else 0
        col3.metric("Preço Justo (Graham)", f"R$ {preco_justo:.2f}")

        # 3. Fatos Relevantes e Checklist
        st.subheader("📋 Checklist de Segurança (Método BEST)")
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Setor:** {info.get('sectorDisp')}")
            st.write(f"**ROE:** {info.get('returnOnEquity', 0)*100:.2f}%")
        with c2:
            st.write(f"**Dívida/EBITDA:** {info.get('debtToEquity', 0)/100:.2f}x")
            st.write(f"**Margem Líquida:** {info.get('profitMargins', 0)*100:.2f}%")

    except:
        st.error("Ticker não encontrado. Tente adicionar '.SA' ao final (ex: PETR4.SA)")
