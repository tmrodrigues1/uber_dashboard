import streamlit as st

st.set_page_config(page_title="Glossário", layout="wide")

# =========================
# Sidebar com busca
busca = st.sidebar.text_input("🔎 Pesquisar termo")
st.sidebar.markdown("""
## Como usar este glossário?

Sempre que estiver analisando seus relatórios de corridas, consulte estes conceitos para:  
- Interpretar melhor os números
- Ajustar suas metas
- Otimizar sua rotina e ganhos
""")

st.sidebar.markdown("""
                    ---
<div style='text-align: center;'>
    <div style='display: inline-block; padding: 6px 20px; background-color: #1f77b4;
                color: white; border-radius: 10px; font-size: 0.88em;'>
        <a href='https://thiagorodrigues1.com.br' target='_blank' style='text-decoration: none; color: white;'>
            Desenvolvido por <b>TR1</b>
        </a>
    </div>
</div>""", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; font-size: 0.85em;'><br>Versão 1.1</div>", unsafe_allow_html=True)

# =========================
# Glossário em página única
# =========================

st.title("Glossário de Termos e Conceitos")
st.markdown(""" ###### Este glossário é uma ferramenta essencial para entender melhor os termos e conceitos usados na análise de suas corridas.
---""")

# Conteúdo do glossário (cada item é um dicionário com 'titulo', 'explicacao', 'exemplo')
glossario = [
    {
        "titulo": "📊 Desvio Padrão",
        "explicacao": """
**Definição**:  
O Desvio Padrão mede o quanto os seus ganhos variam em relação à média. Quanto maior o desvio, mais imprevisíveis são os seus ganhos.

**Por que é importante?**  
Ajuda a entender se você pode contar com uma previsibilidade de ganhos diária.
""",
        "exemplo": """
**Exemplo real:**  
- Corridas com valores variando de RS 7,89 a RS 35,91 em um mesmo dia.
- Esse intervalo expressivo resulta em um desvio padrão considerável.
"""
    },
    {
        "titulo": "📏 Coeficiente de Variação (CV)",
        "explicacao": """
**Definição**:  
É a razão entre o desvio padrão e a média dos ganhos.  

- **CV baixo** → ganhos mais estáveis e previsíveis.  
- **CV alto** → ganhos mais instáveis e imprevisíveis.

**Dica**:  
Use o CV para definir metas e ajustar suas estratégias de horário e local de atuação.
""",
        "exemplo": """
**Exemplo real:**  
- Em um dia, a média das corridas foi de **RS 14,00**, mas com corridas que oscilaram entre **RS 7,89** e **RS 35,91**.
- Isso indica um CV relativamente alto, apontando para imprevisibilidade.
"""
    },
    {
        "titulo": "🔧 Custos Operacionais",
        "explicacao": """
**Definição**:  
São todos os gastos necessários para realizar as corridas, como combustível, manutenção do veículo, pedágios e limpeza.

**Importante:**  
Incluir custos operacionais na sua análise financeira é fundamental para saber o lucro real.
""",
        "exemplo": """
**Exemplo real:**  
- Para uma corrida de **4,99 km** com ganho de **RS 19,82**, se o custo médio de combustível for **RS 0,50/km**, o custo operacional seria de aproximadamente **R$ 2,50**.
- Logo, o lucro líquido dessa corrida seria:  
  **RS 19,82 - RS 2,50 = RS 17,32**
"""
    },
    {
        "titulo": "💰 Lucro Líquido",
        "explicacao": """
**Definição**:  
É o valor que sobra após subtrair os custos operacionais do faturamento bruto.

**Fórmula:**  
`Lucro Líquido = Faturamento Bruto - Custos Operacionais`

**Dica**:  
Analisar o lucro líquido, e não apenas o faturamento, evita uma falsa percepção de lucratividade.
""",
        "exemplo": """
**Exemplo real:**  
- Faturamento Bruto: **R$ 12,69** (corrida de 3 km)  
- Custo Operacional: **R$ 1,50**  
- **Lucro Líquido**: **R$ 11,19**
"""
    },
    {
        "titulo": "🔄 MoM e WoW",
        "explicacao": """
**Definição**:  
- **MoM (Month over Month)** → comparação dos resultados de um mês com o mês anterior.  
- **WoW (Week over Week)** → comparação dos resultados de uma semana com a semana anterior.

**Por que é útil?**  
Ajuda a entender a evolução das suas corridas e ajustar sua disponibilidade.
""",
        "exemplo": """
**Exemplo real:**  
- Na semana de **30/03/2025**, você realizou 10 corridas, totalizando cerca de **R$ 120,00**.  
- Comparando com a semana anterior (por exemplo, **R$ 95,00**), houve um crescimento de aproximadamente **26%**.
"""
    },
    {
        "titulo": "📦 Boxplot",
        "explicacao": """
**Definição**:  
O boxplot é um gráfico estatístico que mostra a distribuição dos valores de uma variável, destacando a mediana, os quartis e os outliers.

**Como ler:**  
- A linha central do box representa a mediana.
- As bordas do box mostram o intervalo onde está metade dos valores (do 1º ao 3º quartil).
- Pontos fora das "linhas" (bigodes) são outliers (corridas muito fora do padrão).

**Para que serve?**  
Permite identificar rapidamente se a maioria das corridas está concentrada em uma faixa de valor, se há muita variação e se existem valores extremos.
""",
        "exemplo": """
**Exemplo prático:**  
- Se o boxplot das corridas mostra a mediana em RS 12,00, com a maioria das corridas entre RS 10,00 e RS 16,00, e alguns pontos acima de R$ 30,00, isso indica que a maior parte dos seus ganhos está em corridas médias, mas há algumas corridas excepcionais.
"""
    },
    {
        "titulo": "📈 Curva de Pareto (80/20)",
        "explicacao": """
**Definição**:  
O gráfico de Pareto mostra como o faturamento se acumula conforme as corridas são somadas do maior para o menor valor.

**Como ler:**  
- O eixo X mostra as corridas ordenadas do maior para o menor valor.
- O eixo Y mostra o percentual acumulado do faturamento.
- Uma linha horizontal marca o ponto de 80%.

**Para que serve?**  
Ajuda a identificar se uma pequena parcela das corridas é responsável pela maior parte do faturamento (princípio 80/20).
""",
        "exemplo": """
**Exemplo prático:**  
- Se 20% das suas corridas representam 80% do seu faturamento, foque em estratégias para aumentar esse tipo de corrida.
- No seu dado real, as corridas acima de R$ 19,00 podem ser as que mais contribuem para o faturamento total.
"""
    },
    {
        "titulo": "🚗 Rentabilidade por KM e por Minuto",
        "explicacao": """
**Definição**:  
- **Rentabilidade por KM**: quanto você ganha, em média, por quilômetro rodado.
- **Rentabilidade por Minuto**: quanto você ganha, em média, por minuto de corrida.

**Como ler o histograma:**  
- O eixo X mostra faixas de rentabilidade (ex: R$ 1,00/km, R$ 2,00/km).
- O eixo Y mostra quantas corridas estão em cada faixa.

**Para que serve?**  
Ajuda a identificar se suas corridas estão concentradas em faixas mais rentáveis e se vale a pena buscar corridas mais longas ou rápidas.
""",
        "exemplo": """
**Exemplo prático:**  
- Se a maioria das corridas está entre RS 1,50/km e RS 2,00/km, você pode usar esse valor como referência para aceitar ou recusar corridas.
- No seu dado real, uma corrida de 13,42 km por RS 26,44 resulta em cerca de RS 1,97/km.
"""
    },
    {
        "titulo": "🔬 Dispersão (Scatter Plot)",
        "explicacao": """
**Definição**:  
O gráfico de dispersão mostra a relação entre duas variáveis, por exemplo, rentabilidade por km e por minuto.

**Como ler:**  
- Cada ponto representa uma corrida.
- O eixo X pode ser a rentabilidade por km, o eixo Y a rentabilidade por minuto.
- Pontos no canto superior direito são as corridas mais rentáveis em ambos os aspectos.

**Para que serve?**  
Permite identificar padrões, como corridas que são boas tanto por km quanto por tempo, e possíveis oportunidades de otimização.
""",
        "exemplo": """
**Exemplo prático:**  
- Se a maioria dos pontos está agrupada entre RS 1,50/km e RS 2,00/km e entre RS 1,00/min e R 2,00/min, você está conseguindo boas corridas em ambos os critérios.
- Corridas isoladas no gráfico podem indicar oportunidades ou exceções (ex: uma corrida curta, mas muito rentável por tempo).
"""
    },
]

# Filtrar glossário se houver busca
if busca:
    glossario_filtrado = [item for item in glossario if busca.lower() in item["titulo"].lower() or busca.lower() in item["explicacao"].lower() or busca.lower() in item["exemplo"].lower()]
else:
    glossario_filtrado = glossario

# Exibir todos os itens em página única
for item in glossario_filtrado:
    st.markdown(f"### {item['titulo']}")
    st.markdown(item['explicacao'])
    st.markdown(item['exemplo'])
    st.markdown("---")

