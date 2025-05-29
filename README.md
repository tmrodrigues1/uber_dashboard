# Painel de Desempenho
Este projeto tem como objetivo gerar um relatório interativo baseado nas corridas realizadas. Através de análises detalhadas, simulações e estimativas, o relatório oferece insights para apoiar na definição de estratégias.
<ul>
  <li>Análises mais detalhadas dos dados.</li>
  <li>Simulações e estimativas.</li>
  <li>Apoio na definição de estratégias.</li>
</ul>

## Utilização dos Scripts

#### 1) Bibliotecas necessárias
Certifique-se de ter o Python instalado e, em seguida, execute o seguinte comando no terminal para instalar as bibliotecas:
<pre><code>pip install streamlit matplotlib pandas numpy seaborn plotly openpyxl</code></pre>

#### 2) Faça download dos arquivos do projeto
<ul>
  <li>Baixe todos os arquivos disponíveis neste repositório.</li>
  <li>Respeite a hierarquia e estrutura das pastas conforme disponibilizado para garantir o correto funcionamento do script.</li>
</ul>

#### 3) Execute o script
No terminal ou prompt de comando, navegue até o diretório do projeto e execute:
<pre><code>python -m streamlit run Dashboard.py</code></pre>

Ao executar um prompt de comando será aberto, conforme abaixo:
![image](https://github.com/user-attachments/assets/b0f46b22-0ad5-4e04-acb4-ee39d9784a59)

Em seguida uma nova página do seu navegador será aberta com a seguinte URL: http://localhost:8501/ , conforme abaixo:
![image](https://github.com/user-attachments/assets/45d25fa8-5924-46d1-b257-1b7444d4b94f)

### Base de dados
Estão sendo utilizadas três bases de dados para a composição desse relatório
```
corridas_uber.xlsx = Estão relacionadas todas as suas corridas realizadas/efetivadas com KM, duração, valor, data/hora
gasolina.xlsx = Armazena o custo com manutenção ou combustível
ajustes_cancelamentos.xlsx = Relaciona as corridas que tiveram algum ajuste de valor ou foram canceladas

Obs.: Todos os dados são fícticios 
```
### Estrutura do Projeto</h2>
<pre>
<code>
├── Dashboard.py
├── pages/
│   └── Documentação
│   └── Glossário
</code>
</pre>

### Projeto hospedado no Streamlit
Confira clicando aqui o projeto em funcionamento real: xxxx
<br>
