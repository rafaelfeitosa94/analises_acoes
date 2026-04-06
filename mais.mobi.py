# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Apresentação das respostas para entrevista",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CARREGAMENTO DOS DADOS ==========
@st.cache_data
def load_data():
    data = {
        'user_id': [1, 2, 1, 3, 2, 4, 1, 5, 3, 3, 6, 2, 4, 4, 7, 5],
        'event_type': ['view', 'view', 'add_to_cart', 'view', 'purchase', 'view', 'purchase', 'view',
                       'add_to_cart', 'purchase', 'view', 'view', 'add_to_cart', 'purchase', 'view', 'view'],
        'category': ['Eletrônicos', 'Moda', 'Eletrônicos', 'Casa', 'Moda', 'Moda', 'Eletrônicos', 'Casa',
                     'Casa', 'Casa', 'Moda', 'Moda', 'Moda', 'Moda', 'Eletrônicos', 'Casa'],
        'event_timestamp': ['2023-10-01 10:00', '2023-10-01 10:05', '2023-10-01 10:10', '2023-10-01 10:15',
                            '2023-10-01 10:20', '2023-10-01 10:25', '2023-10-01 10:30', '2023-10-01 10:35',
                            '2023-10-01 10:40', '2023-10-01 10:45', '2023-10-01 10:50', '2023-10-01 10:55',
                            '2023-10-01 11:00', '2023-10-01 11:05', '2023-10-01 11:10', '2023-10-01 11:15'],
        'revenue': [0, 0, 0, 0, 150.00, 0, 300.00, 0, 0, 120.00, 0, 0, 0, 80.00, 0, 0]
    }
    df = pd.DataFrame(data)
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
    return df

df = load_data()

# ========== CÁLCULO DOS INDICADORES ==========
def calcular_metricas(df):
    # Exploração
    usuarios_unicos = df['user_id'].nunique()
    compras = df[df['event_type'] == 'purchase']
    media_receita_compra = compras['revenue'].mean()
    
    # Conversão
    usuarios_com_compra = df[df['event_type'] == 'purchase']['user_id'].nunique()
    taxa_conversao = (usuarios_com_compra / usuarios_unicos) * 100
    
    # Análise de Produto
    receita_categoria = df[df['event_type'] == 'purchase'].groupby('category')['revenue'].sum()
    categoria_top = receita_categoria.idxmax()
    receita_top = receita_categoria.max()
    
    # Tempo
    eventos_usuario = df.groupby('user_id').size()
    user_top_eventos = eventos_usuario.idxmax()
    num_eventos_top = eventos_usuario.max()
    
    df_user_top = df[df['user_id'] == user_top_eventos].sort_values('event_timestamp')
    tempo_total = (df_user_top['event_timestamp'].max() - df_user_top['event_timestamp'].min()).total_seconds() / 60
    
    # Eventos por tipo
    eventos_por_tipo = df['event_type'].value_counts()
    
    # Funil de conversão
    usuarios_view = df[df['event_type'] == 'view']['user_id'].nunique()
    usuarios_cart = df[df['event_type'] == 'add_to_cart']['user_id'].nunique()
    usuarios_purchase = usuarios_com_compra
    
    return {
        'usuarios_unicos': usuarios_unicos,
        'media_receita_compra': media_receita_compra,
        'taxa_conversao': taxa_conversao,
        'categoria_top': categoria_top,
        'receita_top': receita_top,
        'user_top_eventos': user_top_eventos,
        'num_eventos_top': num_eventos_top,
        'tempo_total': tempo_total,
        'eventos_por_tipo': eventos_por_tipo,
        'receita_categoria': receita_categoria,
        'funil': [usuarios_view, usuarios_cart, usuarios_purchase]
    }

metricas = calcular_metricas(df)

# ========== SIDEBAR ==========
with st.sidebar:
    st.image("https://www.mais.mobi/wp-content/uploads/2026/03/logo-mais-mobi.png", width=80)
    st.title("🎯 Navegação")
    
    st.markdown("---")
    
    # Filtros
    st.subheader("🔍 Filtros")
    
    # Filtro por categoria
    categorias = ['Todas'] + sorted(df['category'].unique())
    categoria_filtro = st.selectbox("Categoria", categorias)
    
    # Filtro por tipo de evento
    eventos = ['Todos'] + sorted(df['event_type'].unique())
    evento_filtro = st.selectbox("Tipo de Evento", eventos)
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if categoria_filtro != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['category'] == categoria_filtro]
    if evento_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['event_type'] == evento_filtro]
    
    st.markdown("---")
    st.caption(f"📅 Período: {df['event_timestamp'].min().strftime('%d/%m/%Y %H:%M')} - {df['event_timestamp'].max().strftime('%d/%m/%Y %H:%M')}")
    st.caption(f"📊 Dados atualizados em {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ========== MAIN CONTENT ==========
# Título Principal
st.title("📈 Dashboard de Análise de E-commerce")
st.markdown("---")

# ========== LINHA 1 - CARDS PRINCIPAIS ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Usuários Únicos",
        value=metricas['usuarios_unicos'],
        delta="Total na base"
    )

with col2:
    st.metric(
        label="💰 Ticket Médio",
        value=f"R$ {metricas['media_receita_compra']:.2f}",
        delta="Por compra"
    )

with col3:
    st.metric(
        label="🔄 Taxa de Conversão",
        value=f"{metricas['taxa_conversao']:.1f}%",
        delta=f"{metricas['taxa_conversao']-50:.1f}% vs meta",
        delta_color="normal" if metricas['taxa_conversao'] >= 50 else "inverse"
    )

with col4:
    st.metric(
        label="🏆 Categoria Top",
        value=metricas['categoria_top'],
        delta=f"R$ {metricas['receita_top']:.2f}",
        delta_color="off"
    )

st.markdown("---")

# ========== LINHA 2 - GRÁFICOS PRINCIPAIS ==========
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Receita por Categoria")
    fig_receita = px.bar(
        x=metricas['receita_categoria'].values,
        y=metricas['receita_categoria'].index,
        orientation='h',
        text=metricas['receita_categoria'].values,
        color=metricas['receita_categoria'].values,
        color_continuous_scale='Viridis',
        title="Receita Total por Categoria"
    )
    fig_receita.update_traces(texttemplate='R$ %{text:.2f}', textposition='outside')
    fig_receita.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_receita, use_container_width=True)

with col2:
    st.subheader("🔄 Funil de Conversão")
    funil_labels = ['Visualizações', 'Add ao Carrinho', 'Compras']
    fig_funil = go.Figure(go.Funnel(
        y=funil_labels,
        x=metricas['funil'],
        textposition="inside",
        textinfo="value+percent initial",
        marker={"color": ["#3498db", "#f39c12", "#2ecc71"]}
    ))
    fig_funil.update_layout(height=400, title="Jornada do Usuário")
    st.plotly_chart(fig_funil, use_container_width=True)

# ========== LINHA 3 - ANÁLISE COMPORTAMENTAL ==========
st.subheader("📈 Análise Comportamental")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Distribuição de Eventos
    fig_eventos = px.pie(
        values=metricas['eventos_por_tipo'].values,
        names=metricas['eventos_por_tipo'].index,
        title="Distribuição de Eventos",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.3
    )
    fig_eventos.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_eventos, use_container_width=True)

with col2:
    st.subheader("👑 Usuário Mais Ativo")
    st.info(f"""
    **Usuário ID:** {metricas['user_top_eventos']}
    
    **Total de Eventos:** {metricas['num_eventos_top']}
    
    **Tempo entre 1º e último evento:**
    {metricas['tempo_total']:.0f} minutos
    
    **Eventos do usuário:**
    """)
    eventos_user = df[df['user_id'] == metricas['user_top_eventos']]['event_type'].tolist()
    for evento in eventos_user:
        st.write(f"• {evento}")

with col3:
    st.subheader("📈 Estatísticas Rápidas")
    
    # Calcular algumas estatísticas adicionais
    tempo_medio_compra = df[df['event_type'] == 'purchase']['event_timestamp'].diff().mean()
    
    st.metric(
        label="Total de Compras",
        value=len(df[df['event_type'] == 'purchase'])
    )
    
    st.metric(
        label="Receita Total",
        value=f"R$ {df[df['event_type'] == 'purchase']['revenue'].sum():.2f}"
    )
    
    st.metric(
        label="Eventos por Usuário",
        value=f"{len(df)/metricas['usuarios_unicos']:.1f}"
    )

# ========== LINHA 4 - TABELA DE DADOS ==========
st.markdown("---")
st.subheader("📋 Dados Detalhados")

# Abas para diferentes visualizações
tab1, tab2, tab3 = st.tabs(["📊 Dados Filtrados", "👥 Análise por Usuário", "📈 Séries Temporais"])

with tab1:
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        height=400,
        column_config={
            "user_id": "Usuário",
            "event_type": "Tipo de Evento",
            "category": "Categoria",
            "event_timestamp": "Timestamp",
            "revenue": st.column_config.NumberColumn("Receita", format="R$ %.2f")
        }
    )

with tab2:
    # Análise por usuário
    analise_usuario = df.groupby('user_id').agg({
        'event_type': 'count',
        'revenue': 'sum'
    }).rename(columns={'event_type': 'total_eventos', 'revenue': 'receita_total'})
    
    # Adicionar se comprou ou não
    comprou = df[df['event_type'] == 'purchase']['user_id'].unique()
    analise_usuario['realizou_compra'] = analise_usuario.index.isin(comprou)
    
    st.dataframe(
        analise_usuario,
        use_container_width=True,
        height=400,
        column_config={
            "total_eventos": "Total de Eventos",
            "receita_total": st.column_config.NumberColumn("Receita Total", format="R$ %.2f"),
            "realizou_compra": "Realizou Compra"
        }
    )

with tab3:
    # Série temporal de eventos
    eventos_tempo = df.set_index('event_timestamp').groupby([pd.Grouper(freq='5min'), 'event_type']).size().unstack(fill_value=0)
    
    fig_tempo = px.line(
        eventos_tempo,
        title="Eventos ao Longo do Tempo",
        labels={"value": "Número de Eventos", "event_timestamp": "Tempo", "variable": "Tipo de Evento"}
    )
    fig_tempo.update_layout(height=400)
    st.plotly_chart(fig_tempo, use_container_width=True)

# ========== LINHA 5 - INSIGHTS ==========
st.markdown("---")
st.subheader("💡 Insights e Recomendações")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🎯 **Principais Insights**")
    st.write("""
    - **57.1%** dos usuários realizaram compras
    - Categoria **Eletrônicos** lidera em receita
    - Ticket médio de **R$ 162,50**
    """)

with col2:
    st.info("📌 **Oportunidades**")
    st.write("""
    - Aumentar conversão de add_to_cart para purchase
    - Incentivar compras na categoria Casa
    - Engajar usuários com apenas 1 evento
    """)

with col3:
    st.warning("⚠️ **Pontos de Atenção**")
    st.write("""
    - Usuário 1 concentra eventos em 30 min
    - Período de análise curto (75 min)
    - Apenas 4 usuários compraram
    """)

# ========== FOOTER ==========
st.markdown("---")
st.caption("🚀 Dashboard desenvolvido com Streamlit | Dados simulados para demonstração")