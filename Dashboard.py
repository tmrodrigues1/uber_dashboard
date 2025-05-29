import streamlit as st
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Painel Uber", layout="wide")

# =========================
# Helpers e Funções Utilitárias
# =========================

@st.cache_data
def carregar_dados():
    df_corridas = pd.read_excel('basedados/corridas_uber.xlsx', dtype={
        'Tipo': 'string',
        'KM': 'float64',
        'Duracao': 'int64',
        'Valor': 'float64',
        'Link': 'string'
    })
    df_corridas['Data'] = pd.to_datetime(df_corridas['Data'], dayfirst=True)
    df_corridas['Hora'] = pd.to_datetime(df_corridas['Hora'], format='%H:%M:%S', errors='coerce').dt.time

    df_custos = pd.read_excel('basedados/gasolina.xlsx')
    df_custos['Data'] = pd.to_datetime(df_custos['Data'], dayfirst=True)

    return df_corridas, df_custos

def classificar_periodo(hora):
    if 5 <= hora < 12:
        return 'Manhã'
    elif 12 <= hora < 18:
        return 'Tarde'
    else:
        return 'Noite'

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')

def formatar_percentual(valor):
    return f"{valor:.1f}%"

def highlight_arrow(val):
    if val == "-" or pd.isnull(val):
        return ""
    try:
        val_float = float(val)
        if val_float > 0:
            return "color: #54DD5B;"
        elif val_float < 0:
            return "color: #EE595D;"
        else:
            return ""
    except Exception:
        return ""

def format_arrow(val):
    if val == "-" or pd.isnull(val):
        return "-"
    try:
        val_float = float(val)
        if val_float > 0:
            return f"↑ {val_float:.1f}%"
        elif val_float < 0:
            return f"↓ {abs(val_float):.1f}%"
        else:
            return f"{val_float:.1f}%"
    except Exception:
        return "-"

def gerar_tabela_momwow(df, periodo_col, col_metrica, nome_coluna, periodo_fmt, anterior_label):
    df = df.assign(
        Faturamento_por_Dia=df.groupby([periodo_col, 'Data'])['Valor'].transform('sum'),
        Faturamento_por_Corrida=df.groupby([periodo_col, 'Data'])['Valor'].transform('sum') / df.groupby([periodo_col, 'Data'])['Valor'].transform('count')
    )
    agrupado = df.groupby(periodo_col).agg(
        Valor=('Valor', 'sum'),
        Faturamento_por_Dia=('Faturamento_por_Dia', 'mean'),
        Faturamento_por_Corrida=('Faturamento_por_Corrida', 'mean')
    ).reset_index()
    agrupado[f'Valor {anterior_label} anterior'] = agrupado[col_metrica].shift(1)
    agrupado['Diferença (%)'] = ((agrupado[col_metrica] - agrupado[f'Valor {anterior_label} anterior']) / agrupado[f'Valor {anterior_label} anterior']) * 100
    agrupado['Período'] = agrupado[periodo_col].dt.strftime(periodo_fmt)
    tabela = agrupado[['Período', col_metrica, f'Valor {anterior_label} anterior', 'Diferença (%)']].copy()
    tabela.rename(columns={
        col_metrica: nome_coluna,
        f'Valor {anterior_label} anterior': f"{nome_coluna} {anterior_label} anterior",
        'Diferença (%)': 'Variação'
    }, inplace=True)
    tabela[nome_coluna] = tabela[nome_coluna].apply(formatar_moeda)
    tabela[f"{nome_coluna} {anterior_label} anterior"] = tabela[f"{nome_coluna} {anterior_label} anterior"].apply(
        lambda x: formatar_moeda(x) if pd.notnull(x) else "-"
    )
    return tabela


# Dicionário para garantir nomes dos dias em português
dias_semana = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

# =========================
# Carregamento e Preprocessamento
# =========================

df_corridas, df_custos = carregar_dados()

# Preprocessamento
df_corridas = df_corridas.assign(
    Hora_decimal=lambda df: df['Hora'].apply(lambda t: t.hour + t.minute / 60),
    Hora_int=lambda df: df['Hora'].apply(lambda t: t.hour),
    DiaSemana=lambda df: df['Data'].dt.day_name().map(dias_semana),
    Periodo=lambda df: df['Hora'].apply(lambda t: classificar_periodo(t.hour))
)

# =========================
# Filtros
# =========================

st.sidebar.title("🎯 Filtros")
opcao_filtro = st.sidebar.selectbox("Selecione uma data", ["Toda a base", "Período específico", "Últimos X dias"])

if opcao_filtro == "Toda a base":
    data_inicio = df_corridas['Data'].min()
    data_fim = df_corridas['Data'].max()
elif opcao_filtro == "Período específico":
    data_min = df_corridas['Data'].min()
    data_max = df_corridas['Data'].max()
    data_inicio = st.sidebar.date_input("Data Inicial", value=data_min, min_value=data_min, max_value=data_max)
    data_fim    = st.sidebar.date_input("Data Final", value=data_max, min_value=data_min, max_value=data_max)
else:  # Últimos X dias
    dias = st.sidebar.slider("Quantidade de dias:", 1, 90, 30)
    data_fim = df_corridas['Data'].max()
    data_inicio = data_fim - timedelta(days=dias)

filtro_corridas = df_corridas[(df_corridas['Data'] >= pd.to_datetime(data_inicio)) & (df_corridas['Data'] <= pd.to_datetime(data_fim))]
filtro_custos   = df_custos[(df_custos['Data'] >= pd.to_datetime(data_inicio)) & (df_custos['Data'] <= pd.to_datetime(data_fim))]

# Adicione as colunas 'Mes' e 'Semana' para análises MoM e WoW
filtro_corridas = filtro_corridas.copy()
filtro_corridas['Mes'] = filtro_corridas['Data'].dt.to_period('M').dt.to_timestamp()
filtro_corridas['Semana'] = filtro_corridas['Data'].dt.to_period('W').apply(lambda r: r.start_time)


# =========================
# Visão Geral
# =========================

st.title("🚗 Painel de Desempenho: Uber")
st.markdown(
    "Esse relatório se baseia apenas nas corridas **realizadas** e tem como objetivo "
    "trazer análises mais detalhadas e algumas simulações/estimativas para apoiar na estratégia", unsafe_allow_html=True)
st.markdown(f"##### Período analisado: `{data_inicio.strftime('%d/%m/%Y')}` a `{data_fim.strftime('%d/%m/%Y')}`")

st.markdown("---")
st.subheader("💸 Visão Geral")

receita_total = filtro_corridas['Valor'].sum()
duracao = filtro_corridas['Duracao'].sum()
duracao_hora = duracao // 60
qtd_corridas = len(filtro_corridas)
km_total = filtro_corridas['KM'].sum()
valor_total_custos = filtro_custos['Valor'].sum()
lucro_liquido = receita_total - valor_total_custos
mediana_valor = filtro_corridas['Valor'].median()
corridas_por_dia = filtro_corridas.groupby('Data').size()
valor_por_dia = filtro_corridas.groupby('Data')['Valor'].sum()
mediana_corridas_dia = corridas_por_dia.median()
mediana_valor_dia = valor_por_dia.median()
mediana_km_corrida = filtro_corridas['KM'].median() if not filtro_corridas.empty else 0
dias_corridos = corridas_por_dia.size

col1, col2, col3, col4 = st.columns(4)
col1.metric("Corridas", qtd_corridas)
col2.metric("Corridas por Dia (Mediana)", f"{mediana_corridas_dia:.1f}")
col3.metric("KM Rodados", f"{km_total:.2f} km")
col4.metric("KM por Corrida (Mediana)", f"{mediana_km_corrida:.2f} km")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Faturamento Bruto", formatar_moeda(receita_total))
col6.metric("Faturamento por Dia (Mediana)", formatar_moeda(mediana_valor_dia))
col7.metric("Faturamento por Corrida (Mediana)", formatar_moeda(mediana_valor))
col8.metric("Duração", f"{duracao:.0f} min /  {duracao_hora}h")

col9, col10, col11, col12 = st.columns(4)
col9.metric("Custos Operacionais", formatar_moeda(valor_total_custos))
col10.metric("Lucro Líquido", formatar_moeda(lucro_liquido))
col11.metric("Dias Corridos", f"{dias_corridos}")

# =========================
# Gráficos Gerais
# =========================

st.markdown("---")
st.subheader("📈 Gráficos Gerais")

opcoes_metricas = {
    "Faturamento Bruto": ("Valor", "Faturamento"),
    "Faturamento por Dia": ("Faturamento_por_Dia", "Faturamento por Dia"),
    "Faturamento por Corrida": ("Faturamento_por_Corrida", "Faturamento por Corrida")
}

col_sel, _ = st.columns([0.25, 0.75])  # Ajuste o valor para o tamanho desejado
with col_sel:
    metrica_selecionada = st.selectbox(
        "Métrica para análise comparativa:",
        list(opcoes_metricas.keys()),
        index=0,
        key="metrica_momwow"
    )
st.markdown("")
col_metrica, nome_coluna = opcoes_metricas[metrica_selecionada]

col_tab_mom, col_tab_wow = st.columns(2)

with col_tab_mom:
    st.markdown(f"###### Comparativo por Mês (MoM) - {nome_coluna}")
    tabela_mom = gerar_tabela_momwow(
        filtro_corridas, 'Mes', col_metrica, nome_coluna, '%b/%y', 'mês'
    )
    st.dataframe(
        tabela_mom.style
            .map(highlight_arrow, subset=['Variação'])
            .format({'Variação': format_arrow}, na_rep="-")
            .hide(axis="index"),
        use_container_width=True,
        height=180
    )

with col_tab_wow:
    st.markdown(f"###### Comparativo por Semana (WoW) - {nome_coluna}")
    tabela_wow = gerar_tabela_momwow(
        filtro_corridas, 'Semana', col_metrica, nome_coluna, '%d/%m/%y', 'semana'
    )
    st.dataframe(
        tabela_wow.style
            .map(highlight_arrow, subset=['Variação'])
            .format({'Variação': format_arrow}, na_rep="-")
            .hide(axis="index"),
        use_container_width=True,
        height=180
    )

# =========================
# Gráficos Visuais
# =========================

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown("ㅤㅤ")
    st.markdown("###### Faturamento por Mês")
    df_mes = filtro_corridas.copy()
    df_mes['Periodo'] = df_mes['Data'].dt.to_period('D').dt.to_timestamp()
    faturamento_mes = df_mes.groupby('Periodo')['Valor'].sum().reset_index()
    st.bar_chart(data=faturamento_mes, x='Periodo', y='Valor', use_container_width=True)

with col_graf2:
    st.markdown("ㅤㅤ")
    st.markdown("###### Mapa de Calor - Faturamento por Hora x Dia")
    df_heatmap = filtro_corridas.copy()
    df_heatmap['Hora_int'] = df_heatmap['Hora'].apply(lambda x: x.hour if pd.notnull(x) else None)
    dias_semana_abrev = {
        'Monday': 'Seg', 'Tuesday': 'Ter', 'Wednesday': 'Qua', 'Thursday': 'Qui',
        'Friday': 'Sex', 'Saturday': 'Sáb', 'Sunday': 'Dom'
    }
    df_heatmap['Dia_semana'] = df_heatmap['Data'].dt.day_name().map(dias_semana_abrev)
    pivot_heatmap = df_heatmap.pivot_table(
        index='Hora_int',
        columns='Dia_semana',
        values='Valor',
        aggfunc='sum',
        fill_value=0
    )
    dias_ordenados = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    pivot_heatmap = pivot_heatmap.reindex(columns=dias_ordenados)
    sns.set_style("white")
    fundo_cor = "#0E1117"
    fig, ax = plt.subplots(figsize=(3, 2), facecolor=fundo_cor)
    heatmap = sns.heatmap(
        pivot_heatmap,
        cmap="Blues",
        linewidths=0.5,
        annot=False,
        fmt=".0f",
        ax=ax,
        cbar_kws={
            'label': 'Faturamento (R$)',
            'shrink': 1
        }
    )
    ax.set_facecolor(fundo_cor)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(axis='both', labelsize=4, colors='white')
    cbar = heatmap.collections[0].colorbar
    cbar.ax.yaxis.label.set_size(5)
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(colors='white', labelsize=5)
    st.pyplot(fig)

# =========================
# Análises Estatísticas
# =========================

st.markdown("---")
st.subheader("📊 Análises Estatísticas")

df_rent = filtro_corridas[(filtro_corridas['KM'] > 0) & (filtro_corridas['Duracao'] > 0)].copy()
df_rent['Rentabilidade_KM'] = df_rent['Valor'] / df_rent['KM']
df_rent['Rentabilidade_Tempo'] = df_rent['Valor'] / df_rent['Duracao']

col_rent1, col_rent2 = st.columns(2)

with col_rent1:
    st.markdown("##### Rentabilidade por KM (Histograma)")
    st.markdown(
        "O histograma mostra a frequência de corridas em cada faixa de rentabilidade por quilômetro. "
        "Assim, é possível identificar se a maioria das corridas está concentrada em uma faixa específica ou se há muita variação."
    )
    fig_hist = px.histogram(
        df_rent,
        x="Rentabilidade_KM",
        nbins=30,
        title="Distribuição da Rentabilidade por KM",
        labels={"Rentabilidade_KM": "R$/KM"},
        color_discrete_sequence=["#1f77b4"]
    )
    fig_hist.update_layout(bargap=0.1, xaxis_title="R$/KM", yaxis_title="Quantidade de Corridas")
    st.plotly_chart(fig_hist, use_container_width=True)

with col_rent2:
    st.markdown("##### Análise de Outliers (Boxplot)")
    st.markdown(
        "O boxplot destaca a mediana, os limites normais e os valores extremos (outliers) da rentabilidade por KM. "
        "Ele facilita a identificação de corridas fora do padrão, seja por promoções, tarifas dinâmicas ou situações atípicas."
    )
    fig_box = px.box(
        df_rent,
        y="Rentabilidade_KM",
        points="outliers",
        title="Boxplot da Rentabilidade por KM",
        labels={"Rentabilidade_KM": "R$/KM"},
        color_discrete_sequence=["#ff7f0e"]
    )
    fig_box.update_layout(yaxis_title="R$/KM")
    st.plotly_chart(fig_box, use_container_width=True)

col_disp, col_pareto = st.columns(2)

with col_disp:
    st.markdown("##### Dispersão: Rentabilidade por KM x Rentabilidade por Tempo")
    st.markdown(
        "Cada ponto representa uma corrida. O gráfico mostra se existe relação entre ganhar mais por quilômetro e por tempo. "
        "Corridas no canto superior direito são as mais rentáveis em ambos os aspectos."
    )
    fig_scatter = px.scatter(
        df_rent,
        x="Rentabilidade_KM",
        y="Rentabilidade_Tempo",
        hover_data=["Data", "Valor", "KM", "Duracao"],
        title="Rentabilidade por KM vs. Rentabilidade por Tempo",
        labels={"Rentabilidade_KM": "R$/KM", "Rentabilidade_Tempo": "R$/min"},
        color_discrete_sequence=["#2ca02c"]
    )
    fig_scatter.update_traces(marker=dict(size=8, opacity=0.7))
    fig_scatter.update_layout(xaxis_title="Rentabilidade por KM (R$/KM)", yaxis_title="Rentabilidade por Tempo (R$/min)")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_pareto:
    st.markdown("##### Curva de Pareto 80/20")
    st.markdown(
        "A curva de Pareto mostra como o faturamento se acumula conforme as corridas são somadas do maior para o menor valor. "
        "O objetivo é identificar se uma pequena parcela das corridas é responsável pela maior parte do faturamento. "
        "A linha vermelha indica o ponto onde 80% do faturamento é atingido."
    )
    df_pareto = filtro_corridas.sort_values(by='Valor', ascending=False).copy()
    df_pareto['cumulativo'] = df_pareto['Valor'].cumsum()
    df_pareto['percentual'] = 100 * df_pareto['cumulativo'] / receita_total
    df_pareto['corrida_num'] = range(1, len(df_pareto)+1)
    pareto_cutoff = df_pareto[df_pareto['percentual'] <= 80]
    percent_corridas = 100 * len(pareto_cutoff) / len(df_pareto)
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Scatter(
        x=df_pareto['corrida_num'],
        y=df_pareto['percentual'],
        mode='lines+markers',
        name='Acumulado (%)'
    ))
    fig_pareto.add_shape(
        type="line", x0=0, x1=len(df_pareto), y0=80, y1=80,
        line=dict(color="red", width=1, dash="dash")
    )
    fig_pareto.update_layout(
        title="Curva de Pareto: Acumulado do Faturamento por Corrida",
        xaxis_title="Corridas (ordenadas do maior para o menor valor)",
        yaxis_title="Faturamento Acumulado (%)",
        showlegend=False
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

# =========================
# Melhor e Pior Dia
# =========================

agrupado_dia = filtro_corridas.groupby('DiaSemana').agg(
    median_valor=('Valor', 'median'),
    mean_valor=('Valor', 'mean'),
    std_valor=('Valor', 'std'),
    count=('Valor', 'count')
).reset_index()
agrupado_dia = agrupado_dia[agrupado_dia['count'] >= 3]
agrupado_dia['cv'] = (agrupado_dia['std_valor'] / agrupado_dia['mean_valor']) * 100

dias_ordenados = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
agrupado_dia = agrupado_dia.set_index('DiaSemana').reindex(dias_ordenados).reset_index()
fig_dias = px.bar(
    agrupado_dia,
    x='DiaSemana',
    y='median_valor',
    error_y='std_valor',
    labels={'DiaSemana': 'Dia da Semana', 'median_valor': 'Mediana do Valor'},
    title='Mediana do Valor por Dia da Semana (com desvio padrão)'
)
st.plotly_chart(fig_dias, use_container_width=True)
if not agrupado_dia.empty:
    melhor_dia = agrupado_dia.loc[agrupado_dia['median_valor'].idxmax()]
    pior_dia = agrupado_dia.loc[agrupado_dia['median_valor'].idxmin()]

    col_melhor, col_pior = st.columns(2)
    with col_melhor:
        st.markdown(
            f"👍 **Melhor dia**: {melhor_dia['DiaSemana']} com mediana de {formatar_moeda(melhor_dia['median_valor'])} "
            f"em {int(melhor_dia['count'])} corridas (CV = {melhor_dia['cv']:.0f}%)",
            unsafe_allow_html=True
        )
    with col_pior:
        st.markdown(
            f"👎 **Pior dia**: {pior_dia['DiaSemana']} com mediana de {formatar_moeda(pior_dia['median_valor'])} "
            f"em {int(pior_dia['count'])} corridas (CV = {pior_dia['cv']:.0f}%)",
            unsafe_allow_html=True
        )

# =========================
# Revisão Semanal
# =========================

st.markdown("---")
st.subheader("📆 Revisão Semanal")

agrupado_dia = filtro_corridas.groupby('DiaSemana').agg(
    Faturamento=('Valor', 'sum'),
    Média_por_Corrida=('Valor', 'mean'),
    Mediana_por_Corrida=('Valor', 'median'),
    Desvio_Padrao=('Valor', 'std'),
    Corridas=('Valor', 'count')
).reset_index()
agrupado_dia = agrupado_dia[agrupado_dia['Corridas'] >= 3].copy()
agrupado_dia['CV'] = (agrupado_dia['Desvio_Padrao'] / agrupado_dia['Média_por_Corrida']) * 100
agrupado_dia.drop(columns=['Desvio_Padrao'], inplace=True)
agrupado_dia['Dia'] = agrupado_dia['DiaSemana'].str[:3].str.capitalize()
agrupado_dia.drop(columns=['DiaSemana'], inplace=True)
agrupado_dia = agrupado_dia[['Dia', 'Faturamento', 'Corridas', 'Média_por_Corrida', 'Mediana_por_Corrida', 'CV']]
agrupado_dia['Faturamento'] = agrupado_dia['Faturamento'].apply(formatar_moeda)
agrupado_dia['Média_por_Corrida'] = agrupado_dia['Média_por_Corrida'].apply(formatar_moeda)
agrupado_dia['Mediana_por_Corrida'] = agrupado_dia['Mediana_por_Corrida'].apply(formatar_moeda)
agrupado_dia['CV'] = agrupado_dia['CV'].apply(formatar_percentual)
st.dataframe(agrupado_dia.reset_index(drop=True), use_container_width=True)

# =========================
# Calculadora de Metas
# =========================

st.markdown("---")
st.subheader("🎯 Calculadora de Metas")
st.markdown("Use esta calculadora para definir sua meta de faturamento bruto, visualizar a quantidade de corridas "
"necessárias por dia e ajustar sua estratégia com base no seu desempenho atual.", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    meta_valor = st.number_input("Qual sua meta de faturamento bruto (R$)?", min_value=0.0, step=100.0, value=0.0)
with col2:
    dias_para_meta = st.number_input("Em quantos dias deseja alcançar a meta?", min_value=1, step=1, value=30)

# Só mostra os resultados se ambos os campos forem preenchidos (>0)
if meta_valor > 0 and dias_para_meta > 0:
    meta_dia = meta_valor / dias_para_meta
    media_corrida = filtro_corridas['Valor'].mean() if not filtro_corridas.empty else 0
    corridas_necessarias_dia = meta_dia / media_corrida if media_corrida > 0 else 0

    # Valores reais do período filtrado
    faturamento_por_dia = filtro_corridas.groupby('Data')['Valor'].sum()
    faturamento_medio_atual = faturamento_por_dia.mean() if not faturamento_por_dia.empty else 0
    corridas_por_dia_real = filtro_corridas.groupby('Data').size().mean() if not filtro_corridas.empty else 0
    dias_atingir_meta = meta_valor / faturamento_medio_atual if faturamento_medio_atual > 0 else 0
    mediana_valor_corrida_real = filtro_corridas['Valor'].median() if not filtro_corridas.empty else 0

    col_sim, col_dist = st.columns(2)

    with col_sim:
        st.markdown("### 📌 Resultado da Simulação")
        st.markdown(f"- **Meta diária sugerida:** R$ {meta_dia:.2f}  *<span style='color:gray'>(No momento você faz: RS {faturamento_medio_atual:.2f})*</span>", unsafe_allow_html=True)
        st.markdown(f"- **Meta por Corrida sugerida:** R$ {media_corrida:.2f} *<span style='color:gray'>(No momento você faz: RS {mediana_valor_corrida_real:.1f})*</span>", unsafe_allow_html=True) 
        st.markdown(f"- **Corridas necessárias:** {corridas_necessarias_dia:.1f} *<span style='color:gray'>(No momento você faz: {corridas_por_dia_real:.1f} corridas/dia)*</span>", unsafe_allow_html=True)
        st.markdown(f"-  No ritmo atual, você atingiria a meta em aproximadamente: {dias_atingir_meta:.0f} dias", unsafe_allow_html=True)

    with col_dist:
        st.markdown("### ⏰ Sugestão por Turno")
        distrib_turno = filtro_corridas['Periodo'].value_counts(normalize=True) * 100
        corridas_turno_real = filtro_corridas.groupby('Periodo').size() / dias_para_meta if dias_para_meta > 0 else 0
        faturamento_turno_real = filtro_corridas.groupby('Periodo')['Valor'].sum() / dias_para_meta if dias_para_meta > 0 else 0
        for turno in ['Manhã', 'Tarde', 'Noite']:
            perc = distrib_turno.get(turno, 0)
            qtd_turno = (corridas_necessarias_dia * perc / 100)
            real_corridas = corridas_turno_real.get(turno, 0)
            real_fat = faturamento_turno_real.get(turno, 0)
            st.markdown(
                f"- **{turno}:** ~{qtd_turno:.1f} corridas/dia ({perc:.0f}%) "
                f"<span style='color:gray; font-style:italic;'>(No momento você faz: {real_corridas:.1f} corridas/dia, {formatar_moeda(real_fat)}/dia)</span>",
                unsafe_allow_html=True
            )

    delta_meta = faturamento_medio_atual - meta_dia
    atingivel = delta_meta >= 0
    if atingivel:
        st.success("✅ Sua meta é possível com base no seu desempenho atual! Continue assim! 💪")
    else:
        st.error("❌ Sua meta é desafiadora no ritmo atual. Considere ajustar os dias ou melhorar o faturamento médio.")

# =========================
# Desenvolvido por TR1
# =========================

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center;'>
    <div style='display: inline-block; padding: 6px 20px; background-color: #1f77b4;
                color: white; border-radius: 10px; font-size: 0.88em;'>
        <a href='https://thiagorodrigues1.com.br' target='_blank' style='text-decoration: none; color: white;'>
            Desenvolvido por <b>TR1</b>
        </a>
    </div>
</div>""", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; font-size: 0.85em;'><br>Versão 1.1</div>", unsafe_allow_html=True)
