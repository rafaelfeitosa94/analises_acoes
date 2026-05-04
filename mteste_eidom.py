# dashboard_eidom.py - Versão com fonte Excel local
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import hashlib
import os

# Configuração da página
st.set_page_config(
    page_title="Análise de vendas - Eindom",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CAMINHO DO ARQUIVO ====================
# Altere o caminho abaixo conforme necessário
EXCEL_PATH = "dados_eidom.xlsx"

# ==================== SISTEMA DE LOGIN ====================
USUARIOS = {
    "admin":     hashlib.sha256("admin123".encode()).hexdigest(),
    "eidom":     hashlib.sha256("eidom2024".encode()).hexdigest(),
    "consultor": hashlib.sha256("consultor".encode()).hexdigest()
}

def verificar_login(usuario, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    return USUARIOS.get(usuario) == senha_hash

def tela_login():
    st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; max-width: 100% !important; }
    header, footer { visibility: hidden; }
    .login-wrapper { display: flex; justify-content: center; padding-top: 80px; }
    .login-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px; border-radius: 20px; text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3); max-width: 420px; width: 100%;
    }
    .login-card h2 { color: white; margin-bottom: 10px; }
    .login-card p  { color: rgba(255,255,255,0.8); margin-bottom: 25px; }
    .stTextInput input { background-color: rgba(255,255,255,0.95) !important; color: black !important; border-radius: 10px; }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border-radius: 25px; font-weight: bold; width: 100%; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="login-card">
        <h2>🔐 Acesso ao Dashboard</h2>
        <p>Análise de vendas - Eindom</p>
    </div>
    """, unsafe_allow_html=True)

    usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário", key="login_usuario")
    senha   = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha", key="login_senha")

    if st.button("📊 Entrar", use_container_width=True):
        if usuario and senha:
            if verificar_login(usuario, senha):
                st.session_state["logado"]  = True
                st.session_state["usuario"] = usuario
                st.rerun()
            else:
                st.error("❌ Usuário ou senha inválidos!")
        else:
            st.warning("⚠️ Por favor, preencha usuário e senha!")

    st.markdown("</div></div>", unsafe_allow_html=True)

def logout():
    if st.sidebar.button("🚪 Sair", use_container_width=True):
        for key in ["logado", "usuario"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ==================== CSS CUSTOMIZADO ====================
st.markdown("""
<style>
.notice-board {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    border-radius: 15px; padding: 20px; margin: 20px 0;
    color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.notice-title {
    font-size: 1.5rem; font-weight: bold; margin-bottom: 15px;
    display: flex; align-items: center; gap: 10px;
    border-bottom: 2px solid rgba(255,255,255,0.3); padding-bottom: 10px;
}
.notice-item {
    display: flex; align-items: center; gap: 15px; padding: 12px;
    margin: 10px 0; background: rgba(255,255,255,0.1); border-radius: 10px;
}
.notice-item:hover { background: rgba(255,255,255,0.15); }
.notice-icon  { font-size: 2rem; }
.notice-text  { font-size: 1rem; line-height: 1.4; }
.notice-highlight {
    font-weight: bold; color: #ffd700;
    background: rgba(0,0,0,0.3); padding: 2px 8px; border-radius: 5px;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 15px; border-radius: 10px; text-align: center; color: white;
}
.metric-value { font-size: 1.8rem; font-weight: bold; }
.user-info {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 10px; border-radius: 10px; color: white;
    text-align: center; margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==================== CARREGAMENTO DOS DADOS ====================
@st.cache_data(ttl=300)
def carregar_dados():
    """
    Lê o arquivo Excel e reproduz as 3 queries originais:
      - df             → query principal  (STATUS = Ativo, sem nulos essenciais)
      - df_kpi         → métricas agregadas
      - df_maior_venda → TOP 1 por TOTAL À VISTA
    """
    if not os.path.exists(EXCEL_PATH):
        st.error(f"❌ Arquivo não encontrado em: {EXCEL_PATH}")
        st.info("Verifique o caminho definido em EXCEL_PATH no topo do script.")
        return None, None, None

    try:
        raw = pd.read_excel(EXCEL_PATH)

        # ---------- Renomeia colunas para os aliases usados no código ----------
        raw.rename(columns={
            "TOTAL À VISTA":         "TOTAL_VISTA",
            "PROMOTOR DE MARKETING": "promotor",
            "PONTO DE CAPTAÇÃO":     "ponto_captacao",
        }, inplace=True)
        # GERENTE DE SALA e CLOSER já chegam com o nome original — sem rename necessário

        # ---------- Replica WHERE STATUS = 'Ativo' ----------
        df = raw[raw["STATUS"].str.strip() == "Ativo"].copy()

        # ---------- Replica filtros NOT NULL / NOT '' ----------
        for col in ["ESTADO", "CIDADE", "PRODUTO"]:
            df = df[df[col].notna() & (df[col].astype(str).str.strip() != "")]

        # ---------- Garante tipo numérico em TOTAL_VISTA ----------
        df["TOTAL_VISTA"] = pd.to_numeric(df["TOTAL_VISTA"], errors="coerce")

        # ---------- Garante colunas opcionais ----------
        for col in ["promotor", "CLOSER", "GERENTE DE SALA", "ponto_captacao", "COTA", "DATA"]:
            if col not in df.columns:
                df[col] = "Não informado"

        # ---------- df_kpi ----------
        df_num = df[df["TOTAL_VISTA"].notna()]
        df_kpi = pd.DataFrame({
            "total_contratos": [len(df)],
            "ticket_medio":    [df_num["TOTAL_VISTA"].mean()],
            "receita_total":   [df_num["TOTAL_VISTA"].sum()],
            "cidades_ativas":  [df["CIDADE"].nunique()],
            "estados_ativos":  [df["ESTADO"].nunique()],
            "maior_venda":     [df_num["TOTAL_VISTA"].max()],
        })

        # ---------- df_maior_venda (TOP 1) ----------
        df_maior_venda = (
            df_num[["promotor", "TOTAL_VISTA"]]
            .sort_values("TOTAL_VISTA", ascending=False)
            .head(1)
            .reset_index(drop=True)
        )

        return df, df_kpi, df_maior_venda

    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {str(e)}")
        return None, None, None

# ==================== FUNÇÕES AUXILIARES ====================
def processar_cota(cota):
    if pd.isna(cota) or str(cota).strip() == "":
        return None
    try:
        s = str(cota)
        if "/" in s:
            return int(s.split("/")[1])
        return int(float(s))
    except:
        return None

# ==================== DASHBOARD PRINCIPAL ====================
def dashboard_principal():
    # --- Sidebar ---
    with st.sidebar:
        st.markdown(f"""
        <div class="user-info">
            👋 Olá, <strong>{st.session_state["usuario"]}</strong><br>
            📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
        </div>
        """, unsafe_allow_html=True)
        logout()
        st.markdown("---")

    # --- Título ---
    st.markdown("""
    <h1 style='text-align: center; color: #667eea;'>📊 Análise de vendas - Eindom</h1>
    <hr>
    """, unsafe_allow_html=True)

    # --- Aviso fixo ---
    st.markdown("""
    <div class="notice-board">
        <div class="notice-title"><span>📢</span><span>Pontos à serem ressaltados</span></div>
        <div class="notice-item">
            <div class="notice-icon">📊</div>
            <div class="notice-text">
                <span class="notice-highlight">A cidade com maior número de contratos fechados é Salvador e o estado é a Bahia</span>,
                com 14 das 15 cidades que mais venderam no ranking
            </div>
        </div>
        <div class="notice-item">
            <div class="notice-icon">🏪</div>
            <div class="notice-text">
                Embora não tenha sido o que mais vendeu, o promotor
                <span class="notice-highlight">Marcelo José foi o responsável pela maior venda</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Carrega dados ---
    with st.spinner("🔄 Carregando dados..."):
        df, df_kpi, df_maior_venda = carregar_dados()

    if df is None or df.empty:
        st.error("❌ Nenhum dado encontrado.")
        return

    # --- KPIs ---
    st.subheader("📈 Indicadores Gerais")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""<div class="metric-card"><div>📋 Total Contratos</div>
            <div class="metric-value">{df_kpi['total_contratos'].iloc[0]:,.0f}</div></div>""",
            unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><div>💰 Ticket Médio</div>
            <div class="metric-value">R$ {df_kpi['ticket_medio'].iloc[0]:,.2f}</div></div>""",
            unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><div>💵 Receita Total</div>
            <div class="metric-value">R$ {df_kpi['receita_total'].iloc[0]:,.2f}</div></div>""",
            unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><div>🏙️ Cidades</div>
            <div class="metric-value">{df_kpi['cidades_ativas'].iloc[0]}</div></div>""",
            unsafe_allow_html=True)
    with col5:
        st.markdown(f"""<div class="metric-card"><div>🗺️ Estados</div>
            <div class="metric-value">{df_kpi['estados_ativos'].iloc[0]}</div></div>""",
            unsafe_allow_html=True)

    # --- Filtros na sidebar ---
    st.sidebar.markdown("## 🔍 Filtros")
    estados_lista = sorted(df["ESTADO"].unique())
    estado_filtro = st.sidebar.selectbox("Estado", ["Todos"] + estados_lista)

    df_filtrado = df[df["ESTADO"] == estado_filtro].copy() if estado_filtro != "Todos" else df.copy()
    cidade_options = ["Todas"] + sorted(df_filtrado["CIDADE"].unique())
    cidade_filtro  = st.sidebar.selectbox("Cidade", cidade_options)

    produto_options = ["Todos"] + sorted(df_filtrado["PRODUTO"].unique())
    produto_filtro  = st.sidebar.selectbox("Produto", produto_options)

    if cidade_filtro  != "Todas": df_filtrado = df_filtrado[df_filtrado["CIDADE"]  == cidade_filtro]
    if produto_filtro != "Todos": df_filtrado = df_filtrado[df_filtrado["PRODUTO"] == produto_filtro]

    # ===== GRÁFICOS =====
    st.subheader("📊 Análises")
    col1, col2 = st.columns(2)

    with col1:
        top_estados = df_filtrado.groupby("ESTADO").size().sort_values(ascending=False).head(10).reset_index()
        top_estados.columns = ["Estado", "Quantidade"]
        fig1 = px.bar(top_estados, x="Estado", y="Quantidade",
                      title="Top 10 Estados por Contratos",
                      color="Quantidade", color_continuous_scale="Blues", text="Quantidade")
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        top_produtos = df_filtrado.groupby("PRODUTO").size().sort_values(ascending=False).head(10).reset_index()
        top_produtos.columns = ["Produto", "Quantidade"]
        fig2 = px.bar(top_produtos, x="Produto", y="Quantidade",
                      title="Top 10 Produtos",
                      color="Quantidade", color_continuous_scale="Greens", text="Quantidade")
        fig2.update_traces(textposition="outside")
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🏙️ Top Cidades")
    top_cidades = df_filtrado.groupby(["CIDADE", "ESTADO"]).size().reset_index()
    top_cidades.columns = ["Cidade", "Estado", "Quantidade"]
    top_cidades = top_cidades.sort_values("Quantidade", ascending=False).head(15)
    fig3 = px.bar(top_cidades, x="Cidade", y="Quantidade", color="Estado",
                  title="Top 15 Cidades por Contratos", text="Quantidade")
    fig3.update_traces(textposition="outside")
    fig3.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)

    # --- Análise de Cotas ---
    st.subheader("🔢 Análise de Cotas")
    df_filtrado = df_filtrado.copy()
    df_filtrado["numero_cota"] = df_filtrado["COTA"].apply(processar_cota)
    df_cotas = df_filtrado[df_filtrado["numero_cota"].notna()]

    if not df_cotas.empty:
        col1, col2 = st.columns(2)
        with col1:
            cota_counts = df_cotas["numero_cota"].value_counts().sort_index().reset_index()
            cota_counts.columns = ["Número da Cota", "Frequência"]
            fig4 = px.bar(cota_counts, x="Número da Cota", y="Frequência",
                          title="Distribuição dos Números de Cota",
                          color="Frequência", color_continuous_scale="Viridis")
            fig4.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig4, use_container_width=True)

        with col2:
            top_prod_cotas = df_cotas["PRODUTO"].value_counts().head(8).index.tolist()
            media_cota_prod = (
                df_cotas[df_cotas["PRODUTO"].isin(top_prod_cotas)]
                .groupby("PRODUTO")["numero_cota"].mean()
                .sort_values(ascending=False).reset_index()
            )
            media_cota_prod.columns = ["Produto", "Média da Cota"]
            fig5 = px.bar(media_cota_prod, x="Produto", y="Média da Cota",
                          title="Média de Cotas por Produto",
                          color="Média da Cota", color_continuous_scale="Oranges",
                          text="Média da Cota")
            fig5.update_traces(textposition="outside")
            fig5.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig5, use_container_width=True)

        st.subheader("📊 Distribuição por Faixas de Cota")
        bins   = [0, 10, 20, 30, 50, 100, float("inf")]
        labels = ["1-10", "11-20", "21-30", "31-50", "51-100", "100+"]
        df_cotas = df_cotas.copy()
        df_cotas["faixa_cota"] = pd.cut(df_cotas["numero_cota"], bins=bins, labels=labels, right=False)
        faixa_counts = df_cotas["faixa_cota"].value_counts().reset_index()
        faixa_counts.columns = ["Faixa da Cota", "Quantidade"]
        fig6 = px.bar(faixa_counts, x="Faixa da Cota", y="Quantidade",
                      title="Distribuição por Faixas de Cota",
                      color="Quantidade", color_continuous_scale="RdPu", text="Quantidade")
        fig6.update_traces(textposition="outside")
        st.plotly_chart(fig6, use_container_width=True)

    # --- Gerente de Sala e Closer ---
    st.subheader("🏆 Gerente de Sala & Closer")
    col1, col2 = st.columns(2)

    with col1:
        if "GERENTE DE SALA" in df_filtrado.columns:
            top_gerentes = (
                df_filtrado.groupby("GERENTE DE SALA").size()
                .sort_values(ascending=False).head(10).reset_index()
            )
            top_gerentes.columns = ["Gerente de Sala", "Quantidade"]
            fig_ger = px.bar(
                top_gerentes, x="Gerente de Sala", y="Quantidade",
                title="Top 10 Gerentes de Sala por Contratos",
                color="Quantidade", color_continuous_scale="Teal", text="Quantidade"
            )
            fig_ger.update_traces(textposition="outside")
            fig_ger.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_ger, use_container_width=True)

    with col2:
        if "CLOSER" in df_filtrado.columns:
            top_closers = (
                df_filtrado.groupby("CLOSER").size()
                .sort_values(ascending=False).head(10).reset_index()
            )
            top_closers.columns = ["Closer", "Quantidade"]
            fig_clo = px.bar(
                top_closers, x="Closer", y="Quantidade",
                title="Top 10 Closers por Contratos",
                color="Quantidade", color_continuous_scale="Purples", text="Quantidade"
            )
            fig_clo.update_traces(textposition="outside")
            fig_clo.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_clo, use_container_width=True)

    # --- Promotores ---
    st.subheader("👥 Análise por Promotor")
    top_promotores = df_filtrado.groupby("promotor").size().sort_values(ascending=False).head(10).reset_index()
    top_promotores.columns = ["Promotor", "Quantidade"]
    fig7 = px.bar(top_promotores, x="Promotor", y="Quantidade",
                  title="Top 10 Promotores",
                  color="Quantidade", color_continuous_scale="Viridis", text="Quantidade")
    fig7.update_traces(textposition="outside")
    fig7.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig7, use_container_width=True)

    # --- Pontos de Captação ---
    st.subheader("📍 Pontos de Captação")
    top_pontos = df_filtrado.groupby("ponto_captacao").size().sort_values(ascending=False).head(10).reset_index()
    top_pontos.columns = ["Ponto de Captação", "Quantidade"]
    fig8 = px.bar(top_pontos, x="Ponto de Captação", y="Quantidade",
                  title="Top 10 Pontos de Captação",
                  color="Quantidade", color_continuous_scale="Oranges", text="Quantidade")
    fig8.update_traces(textposition="outside")
    fig8.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig8, use_container_width=True)

    # --- Tabela detalhada ---
    st.subheader("📋 Dados Detalhados")
    colunas_exibir = ["ESTADO", "CIDADE", "PRODUTO", "TOTAL_VISTA", "promotor", "CLOSER", "ponto_captacao"]
    colunas_ok     = [c for c in colunas_exibir if c in df_filtrado.columns]
    tabela = df_filtrado[colunas_ok].copy()
    tabela.columns = [
        c.replace("ESTADO","Estado").replace("CIDADE","Cidade").replace("PRODUTO","Produto")
         .replace("TOTAL_VISTA","Valor").replace("promotor","Promotor")
         .replace("CLOSER","Closer").replace("ponto_captacao","Ponto de Captação")
        for c in colunas_ok
    ]
    if "Valor" in tabela.columns:
        tabela = tabela.sort_values("Valor", ascending=False)
        st.dataframe(tabela.style.format({"Valor": "R$ {:,.2f}"}), use_container_width=True, height=400)
    else:
        st.dataframe(tabela, use_container_width=True, height=400)

    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#666;'>Dashboard de Clientes Ativos - Dados em tempo real</p>",
                unsafe_allow_html=True)

# ==================== MAIN ====================
def main():
    if "logado" not in st.session_state:
        st.session_state["logado"] = False
    if not st.session_state["logado"]:
        tela_login()
    else:
        dashboard_principal()

if __name__ == "__main__":
    main()
