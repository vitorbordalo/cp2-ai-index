# 🤖 Global AI Index Dashboard — CP2

Dashboard interativo construído com **Streamlit + Plotly** para análise do Global AI Index (Tortoise Media, 5ª edição, Set/2024).

## Deploy no Streamlit Cloud

1. Faça upload deste repositório no GitHub (público)
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório
4. Main file: `app.py`
5. Clique em Deploy

## Estrutura

```
├── app.py              # Dashboard principal
├── AI_index_db.csv     # Dataset (62 países, 13 colunas)
├── requirements.txt    # Dependências Python
└── README.md
```

## Seções do Dashboard

| # | Seção | Conteúdo |
|---|-------|----------|
| 1 | 🏠 Introdução | Contexto, índice, clusters |
| 2 | 🌍 Panorama Global | Top 10, regiões, heatmap |
| 3 | 📊 Análise Estatística | Média, mediana, desvio, boxplot, violinplot |
| 4 | 🔗 Correlações | Heatmap Pearson, scatter, radar |
| 5 | 🏛️ Regimes & Renda | Democracia vs. autocracia, renda |
| 6 | 🇧🇷 Brasil no Mundo | Ranking, gargalos, vs. BRICS |
| 7 | 💡 Conclusões | Insights narrativos, síntese visual |
