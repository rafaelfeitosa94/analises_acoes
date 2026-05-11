import streamlit as st
import pandas as pd

# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================
st.set_page_config(
    page_title="BI Estratégico - Carteira Alta Renda",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# LOGO CENTRALIZADA
# ======================================================
logo_url = "https://vectorseek.com/wp-content/uploads/2023/09/Sicoob-Novo-Logo-Vector.svg-.png"

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(logo_url, width=280)

# ======================================================
# CSS PERSONALIZADO
# ======================================================
st.markdown("""
<style>

.main {
    background-color: #f1f5f9;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    text-align: center;
}

.titulo {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: #0f172a;
}

.subtitulo {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 30px;
}

.metric-label {
    font-size: 16px;
    color: #64748b;
}

.metric-value {
    font-size: 36px;
    font-weight: bold;
    color: #0f172a;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# TÍTULO
# ======================================================
st.markdown("""
<div class="titulo">
BI Estratégico - Carteira Alta Renda
</div>

<div class="subtitulo">
Análise comercial da carteira PF Alto Relacionamento
</div>
""", unsafe_allow_html=True)

# ======================================================
# DADOS
# ======================================================
cooperados = [
    {
        'nome': 'ELIZABETE DE SA CARVALHO PINTO TRINDADE',
        'quadrante': 'Q4',
        'diagnostico': 'Perfil conservador e pouco engajado',
        'risco': 'Baixo',
        'foco': 'Investimentos e seguros',
        'saldo': 720,
    },
    {
        'nome': 'JAYME DOS SANTOS CASTRO',
        'quadrante': 'Q2',
        'diagnostico': 'Cooperado premium e rentável',
        'risco': 'Moderado',
        'foco': 'Reorganização financeira',
        'saldo': -2200,
    },
    {
        'nome': 'FABIO PEREIRA DA CRUZ',
        'quadrante': 'Q1',
        'diagnostico': 'Perfil de atenção financeira',
        'risco': 'Alto',
        'foco': 'Renegociação financeira',
        'saldo': -3006,
    },
    {
        'nome': 'DAMIAO PEREIRA DA SILVA',
        'quadrante': 'Q1',
        'diagnostico': 'Perfil saudável',
        'risco': 'Baixo',
        'foco': 'Expansão de produtos',
        'saldo': 0.46,
    },
    {
        'nome': 'MARIA MOREIRA DA SILVA',
        'quadrante': 'Q1',
        'diagnostico': 'Relacionamento sólido',
        'risco': 'Baixo',
        'foco': 'Investimentos e previdência',
        'saldo': 9159,
    },
    {
        'nome': 'MAIRA MARQUES DE ALMEIDA',
        'quadrante': 'Q4',
        'diagnostico': 'Alta renda pouco ativa',
        'risco': 'Baixo',
        'foco': 'Ativação comercial',
        'saldo': 24,
    },
    {
        'nome': 'UILLIAN PETRONIO DOS SANTOS MONTEIRO',
        'quadrante': 'Q1',
        'diagnostico': 'Muito ativo e pressionado',
        'risco': 'Moderado',
        'foco': 'Controle de endividamento',
        'saldo': -2597,
    },
    {
        'nome': 'EDINALDO FERREIRA DA SILVA',
        'quadrante': 'Q2',
        'diagnostico': 'Rentável com dependência do rotativo',
        'risco': 'Moderado',
        'foco': 'Transformar cheque especial em crédito',
        'saldo': -4932,
    },
]

df = pd.DataFrame(cooperados)

# ======================================================
# MÉTRICAS
# ======================================================
total_cooperados = len(df)
total_q1 = len(df[df["quadrante"] == "Q1"])
total_q2 = len(df[df["quadrante"] == "Q2"])
total_q4 = len(df[df["quadrante"] == "Q4"])

# ======================================================
# CARDS
# ======================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Total Cooperados</div>
        <div class="metric-value">{total_cooperados}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Quadrante Q1</div>
        <div class="metric-value">{total_q1}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Quadrante Q2</div>
        <div class="metric-value">{total_q2}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Quadrante Q4</div>
        <div class="metric-value">{total_q4}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("##")

# ======================================================
# TABELA
# ======================================================
st.subheader("📋 Visão Estratégica da Carteira")

df_exibicao = df.copy()

df_exibicao["saldo"] = df_exibicao["saldo"].apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

df_exibicao.columns = [
    "Cooperado",
    "Quadrante",
    "Diagnóstico",
    "Risco",
    "Foco Comercial",
    "Saldo Conta"
]

st.dataframe(
    df_exibicao,
    use_container_width=True,
    height=450
)

# ======================================================
# GRÁFICOS
# ======================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribuição por Quadrante")
    st.bar_chart(df["quadrante"].value_counts())

with col2:
    st.subheader("⚠️ Distribuição por Risco")
    st.bar_chart(df["risco"].value_counts())

# ======================================================
# OPORTUNIDADES E ALERTAS
# ======================================================
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Principais Oportunidades")

    st.success("Reorganização financeira preventiva")
    st.success("Open Finance para centralização")
    st.success("Previdência privada")
    st.success("Seguro residencial e vida")
    st.success("Expansão de investimentos")

with col2:
    st.subheader("🚨 Alertas da Carteira")

    st.warning("Uso elevado de cheque especial")
    st.warning("Dependência de rotativo em alguns perfis")
    st.warning("Cooperados Q4 pouco engajados")
    st.warning("Falta de investimentos em parte da carteira")
    st.warning("Oportunidade de retenção premium")

# ======================================================
# MAPA ESTRATÉGICO
# ======================================================
st.markdown("---")

st.subheader("📌 Resumo Executivo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("👑 Perfis Premium: 3")

with col2:
    st.warning("⚠️ Perfis em Atenção: 3")

with col3:
    st.success("💰 Potencial Investimentos: 5")

with col4:
    st.success("🔗 Potencial Open Finance: 8")

# ======================================================
# RODAPÉ
# ======================================================
st.markdown("---")

st.markdown("""
<div style='text-align:center; color:gray;'>
Dashboard Estratégico de Alta Renda • Desenvolvido em Streamlit
</div>
""", unsafe_allow_html=True)