import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global AI Index — Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── ESTILOS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fundo e tipografia geral */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    section[data-testid="stSidebar"] { background-color: #161b22; }
    h1, h2, h3, h4 { color: #58a6ff !important; }

    /* Cards de métricas */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 18px 22px;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #58a6ff; }
    .metric-label { font-size: 0.82rem; color: #8b949e; margin-top: 4px; }
    .metric-sub   { font-size: 0.78rem; color: #3fb950; margin-top: 2px; }

    /* Box de insight */
    .insight-box {
        background: #1c2128;
        border-left: 4px solid #58a6ff;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 8px 0 16px 0;
        font-size: 0.93rem;
        color: #c9d1d9;
    }

    /* Rodapé de seção */
    .section-divider {
        border: none;
        border-top: 1px solid #30363d;
        margin: 32px 0;
    }

    /* Tags de cluster */
    .tag {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 2px;
    }
    .tag-power   { background:#1f3a5f; color:#58a6ff; }
    .tag-trad    { background:#1a3a2a; color:#3fb950; }
    .tag-rising  { background:#3a2a0f; color:#d29922; }
    .tag-waking  { background:#2a1f3a; color:#a371f7; }
    .tag-nascent { background:#3a1a1a; color:#f78166; }

    /* Página de capa */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #58a6ff;
        line-height: 1.2;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #8b949e;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── DADOS ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("AI_index_db.csv")
    df.columns = df.columns.str.strip()
    df["Country_short"] = df["Country"].replace({
        "United States of America": "EUA",
        "United Kingdom": "Reino Unido",
        "South Korea": "Coreia do Sul",
        "The Netherlands": "Holanda",
        "New Zealand": "Nova Zelândia",
        "Saudi Arabia": "Arábia Saudita",
        "United Arab Emirates": "Emirados Árabes",
        "South Africa": "África do Sul",
    })
    return df

df = load_data()

PILARES = ["Talent", "Infrastructure", "Operating Environment",
           "Research", "Development", "Government Strategy", "Commercial"]
PILARES_PT = {
    "Talent": "Talento",
    "Infrastructure": "Infraestrutura",
    "Operating Environment": "Ambiente Regulatório",
    "Research": "Pesquisa",
    "Development": "Desenvolvimento",
    "Government Strategy": "Estratégia Gov.",
    "Commercial": "Comercial",
}
CLUSTER_ORDER = ["Power players", "Traditional champions", "Rising stars", "Waking up", "Nascent"]
CLUSTER_COLORS = {
    "Power players":        "#58a6ff",
    "Traditional champions":"#3fb950",
    "Rising stars":         "#d29922",
    "Waking up":            "#a371f7",
    "Nascent":              "#f78166",
}
REGIME_COLORS = {
    "Liberal democracy":    "#3fb950",
    "Electoral democracy":  "#58a6ff",
    "Electoral autocracy":  "#d29922",
    "Closed autocracy":     "#f78166",
}

plotly_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c9d1d9", family="Inter, sans-serif"),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
    margin=dict(l=30, r=30, t=50, b=30),
)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Global AI Index")
    st.markdown("**5ª edição — Set/2024**")
    st.markdown("*Tortoise Media · 62 países · 7 pilares*")
    st.markdown("---")

    pagina = st.radio(
        "Navegar para",
        ["🏠 Introdução",
         "🌍 Panorama Global",
         "📊 Análise Estatística",
         "🔗 Correlações",
         "🏛️ Regimes & Renda",
         "🇧🇷 Brasil no Mundo",
         "💡 Conclusões"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.78rem;color:#8b949e;'>Fonte: "
        "<a href='https://www.tortoisemedia.com/data/global-ai' "
        "style='color:#58a6ff'>Tortoise Media</a></div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 — INTRODUÇÃO
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "🏠 Introdução":
    st.markdown("""
    <div class='hero-title'>A Corrida Global pela<br>Inteligência Artificial</div>
    <div class='hero-sub'>Quem lidera, quem está acordando — e onde o Brasil se encaixa?</div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("62", "Países avaliados", "em 6 regiões do mundo"),
        ("7", "Pilares de análise", "Talento · Infra · Pesquisa · ..."),
        ("122", "Indicadores", "de 24 fontes globais"),
        ("5ª", "Edição do índice", "publicada em setembro/2024"),
    ]
    for col, (val, lbl, sub) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
              <div class='metric-value'>{val}</div>
              <div class='metric-label'>{lbl}</div>
              <div class='metric-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("### O que é o Global AI Index?")
        st.markdown("""
O **Global AI Index**, produzido pela **Tortoise Media** (Londres), é a principal 
referência global para comparar países em capacidade de Inteligência Artificial.

Avalia governos em **três grandes pilares**:

| Dimensão | O que mede |
|---|---|
| 🎯 **Implementação** | Talento, Infraestrutura, Ambiente Regulatório |
| 🔬 **Inovação** | Pesquisa acadêmica, Desenvolvimento de plataformas |
| 💰 **Investimento** | Estratégia governamental, Atividade comercial |

> Cada pilar recebe uma pontuação de **0 a 100**, e o **Total Score** consolida 
todos em um único índice de competitividade em IA.
        """)

    with col_b:
        st.markdown("### Como os países são classificados?")

        clusters_info = {
            "Power players":        ("🔵", "Dominam globalmente. EUA e China.", "#58a6ff"),
            "Traditional champions":("🟢", "Sólidos em tradição científica.", "#3fb950"),
            "Rising stars":         ("🟡", "Crescimento acelerado e consistente.", "#d29922"),
            "Waking up":            ("🟣", "Potencial real, mas ainda emergindo.", "#a371f7"),
            "Nascent":              ("🔴", "Primeiros passos em IA.", "#f78166"),
        }
        for cluster, (emoji, desc, cor) in clusters_info.items():
            n = len(df[df["Cluster"] == cluster])
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:12px;
                        background:#161b22;border-radius:8px;
                        padding:10px 14px;margin:6px 0;
                        border-left:3px solid {cor}'>
              <span style='font-size:1.2rem'>{emoji}</span>
              <div>
                <strong style='color:{cor}'>{cluster}</strong>
                <span style='color:#8b949e;font-size:0.82rem;margin-left:8px'>({n} países)</span><br>
                <span style='color:#c9d1d9;font-size:0.83rem'>{desc}</span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("### 🗺️ Nossa história em dados")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class='insight-box'>
        <strong>Pergunta 1</strong><br>
        Quais países realmente lideram a corrida pela IA e em que dimensões?
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='insight-box'>
        <strong>Pergunta 2</strong><br>
        Regime político e nível de renda influenciam o desempenho em IA?
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='insight-box'>
        <strong>Pergunta 3</strong><br>
        O que os dados revelam sobre a posição do Brasil e seus gargalos?
        </div>""", unsafe_allow_html=True)

    st.info("👈 Use o menu lateral para navegar pelas seções do dashboard.")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 — PANORAMA GLOBAL
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🌍 Panorama Global":
    st.title("🌍 Panorama Global da IA")
    st.markdown("Uma visão do estado atual da IA no mundo — rankings, líderes e a distribuição entre clusters.")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Top 10
    st.markdown("### 🏆 Top 10 países — Pontuação Total")
    top10 = df.nlargest(10, "Total score")[["Country_short", "Total score", "Cluster", "Region"]].reset_index(drop=True)
    top10.index += 1

    fig_top10 = px.bar(
        top10, x="Total score", y="Country_short",
        orientation="h",
        color="Cluster",
        color_discrete_map=CLUSTER_COLORS,
        text="Total score",
        hover_data={"Region": True, "Cluster": True},
    )
    fig_top10.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_top10.update_yaxes(categoryorder="total ascending")
    fig_top10.update_layout(**plotly_layout,
        title="Pontuação total consolidada (escala 0-100)",
        height=400,
        showlegend=True,
    )
    st.plotly_chart(fig_top10, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>Destaque:</strong> Os <strong>EUA lideram com pontuação máxima (100)</strong> em 4 dos 7 pilares 
    (Talento, Pesquisa, Desenvolvimento e Comercial). A <strong>China</strong>, em 2º, domina Infraestrutura (100) 
    e Estratégia de Governo (94,87) — mas fica bem abaixo em Talento (16,51), revelando uma estratégia 
    top-down fortemente estatal.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### 🌐 Distribuição por Região")
        avg_region = df.groupby("Region")["Total score"].mean().reset_index().sort_values("Total score", ascending=False)
        fig_reg = px.bar(
            avg_region, x="Region", y="Total score",
            color="Region",
            color_discrete_sequence=px.colors.qualitative.Bold,
            text="Total score",
        )
        fig_reg.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_reg.update_layout(**plotly_layout,
            title="Score médio por região geográfica",
            showlegend=False,
            height=360,
            yaxis_range=[0, 60],
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with col2:
        st.markdown("### 🗂️ Países por Cluster")
        cluster_counts = df["Cluster"].value_counts().reindex(CLUSTER_ORDER).reset_index()
        cluster_counts.columns = ["Cluster", "count"]
        fig_pie = px.pie(
            cluster_counts, values="count", names="Cluster",
            color="Cluster",
            color_discrete_map=CLUSTER_COLORS,
            hole=0.45,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(**plotly_layout,
            title="Distribuição de países por maturidade em IA",
            height=360,
            showlegend=False,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>Insight regional:</strong> As <strong>Américas e Ásia-Pacífico</strong> puxam as maiores médias graças 
    a EUA, China e Singapura. A <strong>África</strong> concentra os países do cluster "Nascent", 
    com média abaixo de 6 pontos — menos de 1/10 da pontuação americana.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 🎯 Score por pilar — Top 15 países")
    top15 = df.nlargest(15, "Total score")
    pilares_pt_list = [PILARES_PT[p] for p in PILARES]

    fig_heat = go.Figure(data=go.Heatmap(
        z=top15[PILARES].values,
        x=pilares_pt_list,
        y=top15["Country_short"].tolist(),
        colorscale="Blues",
        text=np.round(top15[PILARES].values, 1),
        texttemplate="%{text}",
        hovertemplate="País: %{y}<br>Pilar: %{x}<br>Score: %{z:.1f}<extra></extra>",
        colorbar=dict(title="Score"),
    ))
    fig_heat.update_layout(**plotly_layout,
        title="Heatmap de scores por pilar (top 15 países)",
        height=500,
        yaxis=dict(autorange="reversed", gridcolor="#21262d"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>Padrão visível:</strong> Não existe um líder perfeito em todos os pilares. Os EUA se destacam 
    em 4 colunas, mas a China domina Infraestrutura e Estratégia de Governo. 
    O Reino Unido e Canadá têm scores equilibrados — sem pontas, mas também sem gargalos extremos.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 — ANÁLISE ESTATÍSTICA
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📊 Análise Estatística":
    st.title("📊 Análise Estatística")
    st.markdown("Medidas de posição, dispersão e distribuição dos dados — a base quantitativa da análise.")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Seletor de pilar
    pilar_sel_pt = st.selectbox(
        "Selecionar pilar para análise detalhada:",
        options=["Total score"] + list(PILARES_PT.values()),
    )
    pilar_mapa = {"Total score": "Total score"}
    pilar_mapa.update({v: k for k, v in PILARES_PT.items()})
    pilar_sel = pilar_mapa[pilar_sel_pt]

    col1, col2, col3, col4, col5 = st.columns(5)
    dados = df[pilar_sel]
    stats = {
        "Média":     dados.mean(),
        "Mediana":   dados.median(),
        "Desvio Padrão": dados.std(),
        "Mínimo":    dados.min(),
        "Máximo":    dados.max(),
    }
    icones = ["📐", "📏", "〰️", "⬇️", "⬆️"]
    for col, (label, val), icone in zip([col1,col2,col3,col4,col5], stats.items(), icones):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
              <div style='font-size:1.5rem'>{icone}</div>
              <div class='metric-value'>{val:.2f}</div>
              <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        st.markdown(f"### 📈 Distribuição — {pilar_sel_pt}")
        fig_hist = px.histogram(
            df, x=pilar_sel, nbins=15,
            color_discrete_sequence=["#58a6ff"],
        )
        fig_hist.add_vline(x=dados.mean(),   line_dash="solid", line_color="#3fb950",
                           annotation_text=f"Média: {dados.mean():.1f}",
                           annotation_position="top right")
        fig_hist.add_vline(x=dados.median(), line_dash="dash", line_color="#d29922",
                           annotation_text=f"Mediana: {dados.median():.1f}",
                           annotation_position="top left")
        fig_hist.update_layout(**plotly_layout, height=360,
            title=f"Histograma de {pilar_sel_pt} — {len(df)} países",
            bargap=0.08)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        st.markdown("### 📦 Dispersão por Cluster")
        fig_box = px.box(
            df, x="Cluster", y=pilar_sel,
            category_orders={"Cluster": CLUSTER_ORDER},
            color="Cluster",
            color_discrete_map=CLUSTER_COLORS,
            points="all",
            hover_data=["Country_short"],
        )
        fig_box.update_layout(**plotly_layout, height=360,
            title=f"Boxplot de {pilar_sel_pt} por cluster",
            showlegend=False,
            xaxis_tickangle=-20)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 📐 Medidas de dispersão — todos os pilares")
    dispersao = df[PILARES + ["Total score"]].describe().T[["mean", "std", "min", "50%", "max"]]
    dispersao.columns = ["Média", "Desvio Padrão", "Mínimo", "Mediana", "Máximo"]
    dispersao.index = [PILARES_PT.get(i, i) for i in dispersao.index]
    dispersao = dispersao.round(2)

    st.dataframe(
        dispersao.style
            .background_gradient(subset=["Desvio Padrão"], cmap="Blues")
            .background_gradient(subset=["Média"], cmap="Greens")
            .format("{:.2f}"),
        use_container_width=True,
    )

    st.markdown("""<div class='insight-box'>
    📌 <strong>Interpretação:</strong> O pilar <strong>Comercial</strong> apresenta o maior desvio padrão — 
    indicando alta concentração de valor nos EUA (100) e extrema escassez nos demais países. 
    Já o pilar <strong>Ambiente Regulatório</strong> tem média elevada mas desvio menor, 
    sugerindo que mesmo países emergentes estão investindo em marcos regulatórios de IA.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 🎻 Violinplot — Distribuição por pilar")
    df_melt = df.melt(id_vars=["Country_short", "Cluster"],
                      value_vars=PILARES, var_name="Pilar", value_name="Score")
    df_melt["Pilar_PT"] = df_melt["Pilar"].map(PILARES_PT)

    fig_violin = px.violin(
        df_melt, x="Pilar_PT", y="Score",
        color="Pilar_PT",
        box=True, points="outliers",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig_violin.update_layout(**plotly_layout, height=420,
        title="Distribuição de scores em cada pilar (62 países)",
        showlegend=False, xaxis_tickangle=-25)
    st.plotly_chart(fig_violin, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>Assimetria visível:</strong> A maioria dos pilares apresenta distribuição fortemente 
    assimétrica à direita (média &gt; mediana) — poucos países com scores altíssimos 
    "puxam" a média para cima. Isso confirma uma concentração de poder em IA em um 
    grupo pequeno e seleto de nações.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 4 — CORRELAÇÕES
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🔗 Correlações":
    st.title("🔗 Correlações entre Pilares")
    st.markdown("O que mais impacta a pontuação total? Quais pilares andam juntos?")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 🔥 Mapa de correlação — todos os pilares")
    corr = df[PILARES + ["Total score"]].corr()
    labels = [PILARES_PT.get(c, c) for c in corr.columns]

    fig_corr = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=labels, y=labels,
        colorscale="RdBu",
        zmid=0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>",
        colorbar=dict(title="r de Pearson"),
    ))
    fig_corr.update_layout(**plotly_layout, height=500,
        title="Matriz de correlação de Pearson (r)")
    st.plotly_chart(fig_corr, use_container_width=True)

    # Ranking de correlação com Total score
    cor_total = corr["Total score"].drop("Total score").sort_values(ascending=False)

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("### 🏅 Correlação de cada pilar com o Total Score")
        fig_bar_cor = px.bar(
            x=cor_total.values,
            y=[PILARES_PT[p] for p in cor_total.index],
            orientation="h",
            color=cor_total.values,
            color_continuous_scale="Blues",
            text=np.round(cor_total.values, 3),
        )
        fig_bar_cor.update_traces(textposition="outside")
        fig_bar_cor.update_yaxes(categoryorder="total ascending")
        fig_bar_cor.update_layout(**plotly_layout, height=360,
            title="r de Pearson vs. Total Score",
            showlegend=False, coloraxis_showscale=False,
            xaxis_range=[0, 1.05])
        st.plotly_chart(fig_bar_cor, use_container_width=True)

    with col2:
        st.markdown("### 🔍 Scatter interativo — pilar vs. Total Score")
        pilar_x = st.selectbox("Pilar no eixo X:", options=list(PILARES_PT.values()), index=0)
        pilar_x_en = {v: k for k, v in PILARES_PT.items()}[pilar_x]

        fig_scat = px.scatter(
            df, x=pilar_x_en, y="Total score",
            color="Cluster",
            color_discrete_map=CLUSTER_COLORS,
            hover_name="Country_short",
            size="Total score",
            trendline="ols",
            category_orders={"Cluster": CLUSTER_ORDER},
        )
        fig_scat.update_layout(**plotly_layout, height=360,
            title=f"{pilar_x} vs. Pontuação Total")
        st.plotly_chart(fig_scat, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>Pilares mais decisivos:</strong> <strong>Talento</strong> (r ≈ 0.93) e 
    <strong>Comercial</strong> (r ≈ 0.92) são os pilares com maior correlação com a pontuação total — 
    países que atraem e retêm profissionais qualificados e têm ecossistema de startups 
    tendem a liderar globalmente. 
    <strong>Estratégia de Governo</strong> tem correlação moderada, sugerindo que a política pública 
    sozinha não garante liderança — é preciso que o setor privado também se mova.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 🕸️ Radar — Perfil médio por cluster")
    radar_data = df.groupby("Cluster")[PILARES].mean()

    fig_radar = go.Figure()
    for cluster in CLUSTER_ORDER:
        if cluster in radar_data.index:
            vals = radar_data.loc[cluster].tolist()
            vals_closed = vals + [vals[0]]
            theta_closed = [PILARES_PT[p] for p in PILARES] + [PILARES_PT[PILARES[0]]]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals_closed,
                theta=theta_closed,
                name=cluster,
                line=dict(color=CLUSTER_COLORS[cluster], width=2),
                fill="toself",
                fillcolor=CLUSTER_COLORS[cluster].replace(")", ",0.08)").replace("rgb", "rgba")
                    if "rgb" in CLUSTER_COLORS[cluster]
                    else CLUSTER_COLORS[cluster] + "15",
                opacity=0.85,
            ))
    fig_radar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9"),
        polar=dict(
            bgcolor="rgba(22,27,34,0.6)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#30363d"),
            angularaxis=dict(gridcolor="#30363d"),
        ),
        title="Perfil médio de cada cluster por pilar",
        height=500,
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>Perfis opostos:</strong> Os <em>Power players</em> têm área de radar massiva e uniforme. 
    Os <em>Waking up</em> mostram picos pontuais — muitos têm boa regulação, mas carecem de 
    ecossistema comercial e pesquisa. Os <em>Nascent</em> têm o menor espaço, mas os dados 
    revelam que a limitação não é somente vontade política: infraestrutura e talento 
    são os maiores gargalos.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 5 — REGIMES & RENDA
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🏛️ Regimes & Renda":
    st.title("🏛️ Regimes Políticos & Nível de Renda")
    st.markdown("Democracias investem mais em IA? Países ricos dominam o ranking?")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🗳️ Score médio por regime político")
        avg_regime = df.groupby("Political regime")["Total score"].agg(["mean", "count"]).reset_index()
        avg_regime.columns = ["Regime", "Média", "n"]
        avg_regime = avg_regime.sort_values("Média", ascending=False)

        fig_reg = px.bar(
            avg_regime, x="Regime", y="Média",
            color="Regime",
            color_discrete_map=REGIME_COLORS,
            text="Média",
            hover_data={"n": True},
        )
        fig_reg.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_reg.update_layout(**plotly_layout, height=380,
            title="Pontuação média em IA por regime político",
            showlegend=False, xaxis_tickangle=-20,
            yaxis_range=[0, 50])
        st.plotly_chart(fig_reg, use_container_width=True)

    with col2:
        st.markdown("### 💰 Score médio por grupo de renda")
        avg_income = df.groupby("Income group")["Total score"].agg(["mean", "count"]).reset_index()
        avg_income.columns = ["Renda", "Média", "n"]
        income_order = ["High", "Upper middle", "Lower middle"]
        avg_income["Renda"] = pd.Categorical(avg_income["Renda"], categories=income_order, ordered=True)
        avg_income = avg_income.sort_values("Renda")

        fig_inc = px.bar(
            avg_income, x="Renda", y="Média",
            color="Renda",
            color_discrete_sequence=["#58a6ff", "#a371f7", "#f78166"],
            text="Média",
        )
        fig_inc.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_inc.update_layout(**plotly_layout, height=380,
            title="Pontuação média em IA por nível de renda",
            showlegend=False, yaxis_range=[0, 45])
        st.plotly_chart(fig_inc, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>Democracias lideram, mas há exceções notáveis:</strong> As <em>Liberal democracies</em> têm 
    a maior média — beneficiadas por liberdade acadêmica, ecossistema privado e talento global. 
    Porém, a <strong>China</strong> (Closed autocracy) prova que uma estratégia de Estado centralizada 
    e bem-financiada pode alcançar o 2º lugar mundial. Já a correlação com renda é 
    praticamente linear: países de <em>renda alta</em> têm média 3× superior aos de <em>renda média-baixa</em>.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 🔎 Distribuição detalhada — Regime × Cluster")
    cross = pd.crosstab(df["Political regime"], df["Cluster"])[
        [c for c in CLUSTER_ORDER if c in df["Cluster"].unique()]
    ]

    fig_cross = px.imshow(
        cross,
        color_continuous_scale="Blues",
        text_auto=True,
        aspect="auto",
    )
    fig_cross.update_layout(**plotly_layout, height=340,
        title="Quantidade de países por regime político × cluster de maturidade em IA",
        coloraxis_showscale=False)
    st.plotly_chart(fig_cross, use_container_width=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 📊 Pilares por regime — Estratégia de Governo vs. Comercial")
    gov_com = df.groupby("Political regime")[["Government Strategy", "Commercial"]].mean().reset_index()

    fig_gc = px.scatter(
        gov_com,
        x="Government Strategy", y="Commercial",
        color="Political regime",
        color_discrete_map=REGIME_COLORS,
        size="Commercial",
        text="Political regime",
        size_max=40,
    )
    fig_gc.update_traces(textposition="top center")
    fig_gc.update_layout(**plotly_layout, height=400,
        title="Média de Estratégia Governamental vs. Atividade Comercial em IA por regime",
        showlegend=False,
        xaxis_title="Estratégia de Governo (média)",
        yaxis_title="Comercial / Startups (média)",
    )
    st.plotly_chart(fig_gc, use_container_width=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>A grande contradição:</strong> <em>Closed autocracies</em> têm a maior média em 
    <strong>Estratégia de Governo</strong> — o Estado financia e planeja IA de forma robusta. 
    Mas suas empresas privadas e startups (<strong>Comercial</strong>) ficam muito atrás das 
    democracias liberais. Isso revela dois modelos opostos de corrida pela IA: 
    um <em>state-led</em> e outro <em>market-led</em>.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 6 — BRASIL NO MUNDO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🇧🇷 Brasil no Mundo":
    st.title("🇧🇷 O Brasil no Cenário Global de IA")
    st.markdown("Onde o Brasil está, em que se destaca e quais são seus maiores gargalos.")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    brasil = df[df["Country"] == "Brazil"].iloc[0]
    rank_total = df["Total score"].rank(ascending=False).loc[df["Country"] == "Brazil"].values[0]

    col1, col2, col3, col4 = st.columns(4)
    metricas_br = [
        ("🏅", f"#{int(rank_total)}º", "Ranking Global", "entre 62 países"),
        ("📊", f"{brasil['Total score']:.1f}", "Total Score", "Cluster: Waking up"),
        ("🎓", f"{brasil['Talent']:.1f}", "Talento", f"#{int(df['Talent'].rank(ascending=False).loc[df['Country']=='Brazil'].values[0])}º mundial"),
        ("🏛️", f"{brasil['Government Strategy']:.1f}", "Estratégia Gov.", "Ponto forte relativo"),
    ]
    for col, (icone, val, lbl, sub) in zip([col1,col2,col3,col4], metricas_br):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
              <div style='font-size:1.4rem'>{icone}</div>
              <div class='metric-value'>{val}</div>
              <div class='metric-label'>{lbl}</div>
              <div class='metric-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("### 🕸️ Perfil do Brasil vs. BRICS vs. Top 3")
        paises_comp = ["Brazil", "China", "India", "United States of America", "Russian Federation"]
        paises_comp_reais = [p for p in paises_comp if p in df["Country"].values]
        # Adicionar Russia se existir com outro nome
        if "Russia" in df["Country"].values:
            paises_comp_reais.append("Russia")

        df_comp = df[df["Country"].isin(paises_comp_reais)].copy()
        df_comp["Label"] = df_comp["Country"].replace({
            "United States of America": "EUA",
            "Brazil": "Brasil 🇧🇷",
        })

        fig_radar_br = go.Figure()
        cores_comp = {"Brasil 🇧🇷": "#f78166", "EUA": "#58a6ff", "China": "#d29922", "India": "#3fb950"}
        for _, row in df_comp.iterrows():
            label = row["Label"]
            vals = [row[p] for p in PILARES]
            vals_c = vals + [vals[0]]
            theta_c = [PILARES_PT[p] for p in PILARES] + [PILARES_PT[PILARES[0]]]
            fig_radar_br.add_trace(go.Scatterpolar(
                r=vals_c, theta=theta_c, name=label,
                line=dict(color=cores_comp.get(label, "#8b949e"), width=2.5),
                fill="toself",
                opacity=0.7,
            ))
        fig_radar_br.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c9d1d9"),
            polar=dict(
                bgcolor="rgba(22,27,34,0.6)",
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#30363d"),
                angularaxis=dict(gridcolor="#30363d"),
            ),
            height=420, showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            title="Brasil vs. principais economias por pilar",
        )
        st.plotly_chart(fig_radar_br, use_container_width=True)

    with col_b:
        st.markdown("### 📍 Brasil vs. Vizinhos Latino-americanos")
        latam = df[df["Region"] == "Americas"].copy()
        latam["Label"] = latam["Country"].replace({"United States of America": "EUA"})
        latam = latam.sort_values("Total score", ascending=False)

        colors_latam = ["#f78166" if c == "Brazil" else "#30363d" for c in latam["Country"]]
        fig_latam = px.bar(
            latam, x="Total score", y="Label",
            orientation="h",
            text="Total score",
            color="Country",
            color_discrete_sequence=colors_latam,
        )
        fig_latam.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_latam.update_yaxes(categoryorder="total ascending")
        fig_latam.update_layout(**plotly_layout, height=420,
            title="Ranking nas Américas — Total Score",
            showlegend=False, xaxis_range=[0, 115])
        st.plotly_chart(fig_latam, use_container_width=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 📊 Desempenho do Brasil em cada pilar — ranking e score")
    br_pilares = []
    for pilar in PILARES:
        score = brasil[pilar]
        rank = int(df[pilar].rank(ascending=False).loc[df["Country"] == "Brazil"].values[0])
        media_global = df[pilar].mean()
        br_pilares.append({
            "Pilar": PILARES_PT[pilar],
            "Score Brasil": round(score, 2),
            "Média Global": round(media_global, 2),
            "Ranking": f"#{rank}º",
            "vs. Média": "✅ Acima" if score > media_global else "❌ Abaixo",
        })

    df_br_pl = pd.DataFrame(br_pilares)

    fig_br_comp = go.Figure()
    fig_br_comp.add_trace(go.Bar(
        name="Brasil",
        x=df_br_pl["Pilar"], y=df_br_pl["Score Brasil"],
        marker_color="#f78166",
        text=df_br_pl["Score Brasil"],
        texttemplate="%{text:.1f}",
        textposition="outside",
    ))
    fig_br_comp.add_trace(go.Bar(
        name="Média Global",
        x=df_br_pl["Pilar"], y=df_br_pl["Média Global"],
        marker_color="#30363d",
        text=df_br_pl["Média Global"],
        texttemplate="%{text:.1f}",
        textposition="outside",
    ))
    fig_br_comp.update_layout(**plotly_layout, height=400,
        title="Brasil vs. Média global por pilar",
        barmode="group", yaxis_range=[0, 95])
    st.plotly_chart(fig_br_comp, use_container_width=True)

    st.dataframe(df_br_pl, use_container_width=True, hide_index=True)

    st.markdown("""<div class='insight-box'>
    📌 <strong>O que os dados dizem sobre o Brasil:</strong><br>
    ✅ <strong>Pontos fortes:</strong> <em>Talento</em> (13,46 — acima da média de países da mesma faixa de renda) 
    e <em>Estratégia de Governo</em> (67,72 — demonstra compromisso político com IA).<br>
    ❌ <strong>Gargalos críticos:</strong> <em>Pesquisa</em> (4,83), <em>Comercial</em> (1,36) e 
    <em>Desenvolvimento</em> (5,07) são alarmantemente baixos — o ecossistema de 
    inovação e startups de IA no Brasil ainda é incipiente.<br>
    🔑 <strong>Conclusão:</strong> O Brasil tem agenda governamental, mas carece de transformar isso 
    em pesquisa aplicada, produtos e empresas de IA competitivas globalmente.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 7 — CONCLUSÕES
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "💡 Conclusões":
    st.title("💡 Conclusões & Insights")
    st.markdown("O que os dados nos contam sobre a corrida global pela Inteligência Artificial.")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 📖 A história que os dados contam")

    insights = [
        ("🥇", "#58a6ff",
         "A hegemonia americana é real — mas frágil em infraestrutura",
         "Os EUA lideram com 100 pontos no total e dominam 4 dos 7 pilares. "
         "No entanto, sua infraestrutura (94,02) fica atrás de China (100) e Hong Kong (96,11). "
         "A liderança americana é construída sobre talento, pesquisa e capital privado — "
         "não sobre infraestrutura pública."),

        ("🇨🇳", "#d29922",
         "China: o modelo state-led de IA funciona — até certo ponto",
         "A China domina infraestrutura e estratégia governamental, mas fica em 16º em Talento. "
         "Isso revela um modelo de IA centralizado: o Estado financia e direciona, "
         "mas o ecossistema de inovação orgânica das democracias liberais ainda gera mais valor "
         "em termos comerciais e científicos."),

        ("🔗", "#3fb950",
         "Talento é o principal predictor de liderança em IA (r = 0,93)",
         "De todos os pilares, Talento tem a maior correlação com a pontuação total. "
         "Países que atraem, formam e retêm profissionais qualificados em IA constroem "
         "vantagens duradouras. Isso coloca a educação e a política de imigração de talentos "
         "como alavancas estratégicas centrais."),

        ("🏛️", "#a371f7",
         "Política pública é necessária, mas insuficiente",
         "Países como Arábia Saudita, França e Colômbia têm altos scores em Estratégia de Governo, "
         "mas ficam longe do topo. A correlação de Governo com o Total Score (r ≈ 0,69) é a menor "
         "entre os pilares — confirmar que política sem ecossistema privado e pesquisa "
         "não transforma intenção em liderança real."),

        ("🌍", "#f78166",
         "A desigualdade global em IA é estrutural",
         "Os países da África (Quênia, Nigéria, Tunísia) têm scores abaixo de 10 — "
         "menos de 1/10 da média dos países de renda alta. O problema não é estratégia: "
         "é falta de infraestrutura básica (energia, conectividade) e talento. "
         "A corrida pela IA está sendo disputada por um grupo muito pequeno de nações."),

        ("🇧🇷", "#ff8c42",
         "O Brasil tem agenda, mas precisa de ação no ecossistema",
         "Com 18,89 pontos e ranking 39º, o Brasil está no cluster 'Waking up'. "
         "Seu maior trunfo é a Estratégia de Governo (67,72) — mas Pesquisa (4,83) e "
         "Comercial (1,36) revelam que ainda falta conectar política pública "
         "a resultados científicos e empresariais concretos."),
    ]

    for i, (emoji, cor, titulo, texto) in enumerate(insights, 1):
        st.markdown(f"""
        <div style='background:#161b22;border-radius:12px;padding:20px 24px;
                    margin:12px 0;border-left:4px solid {cor}'>
          <div style='display:flex;align-items:center;gap:12px;margin-bottom:8px'>
            <span style='font-size:1.6rem'>{emoji}</span>
            <strong style='font-size:1.05rem;color:{cor}'>{i}. {titulo}</strong>
          </div>
          <p style='color:#c9d1d9;font-size:0.92rem;margin:0;line-height:1.6'>{texto}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("### 🏁 Síntese visual final")

    df_final = df.copy()
    df_final["Destaque"] = df_final["Country"].apply(
        lambda x: "Brasil" if x == "Brazil"
        else ("EUA" if x == "United States of America"
              else ("China" if x == "China" else "Outros"))
    )
    cores_final = {"EUA": "#58a6ff", "China": "#d29922", "Brasil": "#f78166", "Outros": "#30363d"}

    fig_final = px.scatter(
        df_final, x="Talent", y="Commercial",
        size="Total score",
        color="Destaque",
        color_discrete_map=cores_final,
        hover_name="Country_short",
        hover_data={"Total score": True, "Cluster": True},
        size_max=55,
        opacity=0.85,
    )
    fig_final.add_annotation(
        x=df_final[df_final["Country"]=="United States of America"]["Talent"].values[0],
        y=df_final[df_final["Country"]=="United States of America"]["Commercial"].values[0],
        text="🇺🇸 EUA", showarrow=False, yshift=15, font=dict(color="#58a6ff", size=12),
    )
    fig_final.add_annotation(
        x=df_final[df_final["Country"]=="China"]["Talent"].values[0],
        y=df_final[df_final["Country"]=="China"]["Commercial"].values[0],
        text="🇨🇳 China", showarrow=False, yshift=15, font=dict(color="#d29922", size=12),
    )
    fig_final.add_annotation(
        x=df_final[df_final["Country"]=="Brazil"]["Talent"].values[0],
        y=df_final[df_final["Country"]=="Brazil"]["Commercial"].values[0],
        text="🇧🇷 Brasil", showarrow=False, yshift=15, font=dict(color="#f78166", size=12),
    )
    fig_final.update_layout(**plotly_layout, height=480,
        title="Talento × Atividade Comercial — o eixo central da liderança em IA",
        xaxis_title="Talento (score 0-100)",
        yaxis_title="Comercial / Startups (score 0-100)",
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_final, use_container_width=True)

    st.markdown("""<div class='insight-box' style='border-left-color:#58a6ff'>
    🎯 <strong>Mensagem final:</strong> A corrida pela IA não é vencida só com investimento público. 
    É vencida por países que conseguem combinar <strong>talento de classe mundial</strong>, 
    <strong>ecossistema privado dinâmico</strong> e <strong>pesquisa aplicada robusta</strong>. 
    O Brasil tem o primeiro ingrediente em formação e o terceiro como prioridade declarada — 
    mas precisa urgentemente desenvolver o segundo para não ficar para trás na década da IA.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center;color:#8b949e;font-size:0.85rem;padding:12px'>
      Dashboard desenvolvido com Python · Streamlit · Plotly<br>
      Dados: <strong>Global AI Index 5ª edição</strong> — Tortoise Media (Set/2024)<br>
      FIAP 2025 · Análise de Dados · CP2
    </div>
    """, unsafe_allow_html=True)