import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import csv
import plotly.express as px
import seaborn as sns
from st_aggrid import AgGrid, GridOptionsBuilder

# 1 - Explicação do Objetivo e Motivação:
#Explique o objetivo do dashboard que você está desenvolvendo e a motivação por trás da escolha dos dados e funcionalidades que serão implementados.
#R.
# O dashboard se trata de uma análise de dados de turismo sobre o Parque Nacional da Tijuca, o usuário pode visualizar, filtrar, e obter insights sobre esses dados.
# Escolhi esse dataset pois eu mesmo já fui e fiquei encantado com a natureza e a paisagem que temos dos pontos altos.


# 2 - Realizar Upload de Arquivo CSV:
# Crie uma interface em Streamlit que permita ao usuário fazer o upload de um arquivo CSV contendo dados de turismo do portal Data.Rio.

st.set_page_config(page_title='Análise de Dados de Turismo - Parque Nacional da Tijuca')
st.title('Análise de Dados de Turismo - Parque Nacional da Tijuca')


# Upload de CSV
uploaded_file = st.file_uploader('Faça o upload do arquivo CSV', type=['csv'])
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, sep=';')
    return df
if uploaded_file:
    df = load_data(uploaded_file)       
    st.write('Dados carregados com sucesso!')
    st.dataframe(df)
else:
    st.write('Nenhum arquivo foi carregado.')



# 3 - Filtro de Dados e Seleção:
# Implemente seletores (radio, checkbox, dropdowns) na interface que permitam ao usuário filtrar os dados carregados e selecionar as colunas ou linhas que deseja visualizar.

# Filtrando os dados
if uploaded_file:
    selected_columns = st.multiselect("Selecione as colunas", df.columns.tolist(), default=df.columns.tolist())
    selected_setores = st.multiselect("Selecione os setores", df['Setor'].unique(), default=df['Setor'].unique())
    selected_segmentos = st.multiselect("Selecione os segmentos", df['Segmento'].unique(), default=df['Segmento'].unique())
    selected_categorias = st.multiselect("Selecione as categorias", df['Categorias'].unique(), default=df['Categorias'].unique())
    df_filtrado = df[(df['Setor'].isin(selected_setores)) & 
                    (df['Segmento'].isin(selected_segmentos)) & 
                    (df['Categorias'].isin(selected_categorias))]
    st.write('Dados filtrados:')
    st.dataframe(df_filtrado[selected_columns])
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_filtrado)
    


# 4 - Desenvolver Serviço de Download de Arquivos:
# Implemente um serviço que permita ao usuário fazer o download dos dados filtrados em formato CSV diretamente pela interface da aplicação.

if uploaded_file:
    # Baixar csv
    st.download_button(
        label='Baixar dados filtrados',
        data=csv,
        file_name='dados_filtrados.csv',
        mime='text/csv',
    )

# 5 - Utilizar Barra de Progresso e Spinners:
# Adicione uma barra de progresso e um spinner para indicar o carregamento dos dados enquanto o arquivo CSV é processado e exibido na interface.


# Simulação do carregamento de dados
if uploaded_file:
    with st.spinner('Processando os dados...'):
        progress_bar = st.progress(0)  
        for perc_complete in range(100):
            time.sleep(0.05)  
            progress_bar.progress(perc_complete + 1) 
        st.success('Dados carregados com sucesso!')




# 6 - Utilizar Color Picker:
# Adicione um color picker à interface que permita ao usuário personalizar a cor de fundo do painel e das fontes exibidas na aplicação.

if uploaded_file:
    # Cor de fundo
    bg_color = st.color_picker('Escolha a cor de fundo', '#3C3756')
    st.markdown(f'''<style>.stApp {{background-color: {bg_color};}}</style>''', unsafe_allow_html=True)




# 7 - Utilizar Funcionalidade de Cache:
# Utilize a funcionalidade de cache do Streamlit para armazenar os dados carregados de grandes arquivos CSV, evitando a necessidade de recarregá-los a cada nova interação.
# Função para carregar o arquivo CSV

# Armazenar os dados em cache e verificação do arquivo

# Função para carregar dados do CSV
@st.cache_data
def load_data(file):
    return pd.read_csv(file, sep=';')



# Carregamento de arquivo
upload_file = st.file_uploader('Faça o upload do arquivo', type=['csv'])



# 8 - Persistir Dados Usando Session State:
# Implemente a persistência de dados na aplicação utilizando Session State para manter as preferências do usuário (como filtros e seleções) durante a navegação.

# Verifica se o arquivo já foi carregado anteriormente
if 'Parque_Nacional_Tijuca.csv' not in st.session_state:
    st.session_state.csv_data = None

if upload_file is not None:
    # Carrega o arquivo e armazena no session state
    st.session_state.csv_data = load_data(upload_file)
    st.session_state.upload_filename = upload_file.name
    st.success(f'Arquivo {upload_file.name} carregado com sucesso!')

# Verifica se há dados no session state e exibe
if st.session_state.csv_data is not None:
    st.write(f"Arquivo carregado: {st.session_state.upload_filename}")
    st.write(st.session_state.csv_data)
else:
    st.write("Nenhum arquivo carregado ainda.")

# 9 - Criar Visualizações de Dados - Tabelas:
# Crie uma tabela interativa que exiba os dados carregados e permita ao usuário ordenar e filtrar as colunas diretamente pela interface.

if uploaded_file:

    # Criar opções da tabela com filtros e ordenação
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)  
    gb.configure_default_column(editable=True, groupable=True, sortable=True, filter=True) 
    gridOptions = gb.build()

    # Exibir tabela interativa 
    st.subheader("Tabela Interativa")
    grid_response = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, update_mode='SELECTION_CHANGED')




# 10 - Criar Visualizações de Dados - Gráficos Simples:
# Desenvolva gráficos simples (como barras, linhas, e pie charts) para visualização dos dados carregados, utilizando o Streamlit.

if uploaded_file:
    
    # Seletor de colunas
    colunas = df.columns.tolist()

    # Gráfico de barras
    st.subheader('Gráfico de Barras')
    x_col_barra = st.selectbox('Selecione a coluna para o eixo X (Indico selecionar uma coluna categórica)', colunas, key='x_barra')
    y_col_barra = st.selectbox('Selecione a coluna para o eixo Y(Indico selecionar uma coluna numérica) ', colunas, key='y_barra')
    
    if x_col_barra and y_col_barra:
        grafico_barra = px.bar(df, x=x_col_barra, y=y_col_barra, title=f'Gráfico de Barras: {x_col_barra} vs {y_col_barra}')
        st.plotly_chart(grafico_barra)

    # Gráfico de linhas
    st.subheader('Gráfico de Linhas')
    x_col_linhas = st.selectbox('Selecione a coluna para o eixo X (Indico selecionar uma coluna numérica)', colunas, key='x_linha')
    y_col_linhas = st.selectbox('Selecione a coluna para o eixo Y (Indico selecionar uma coluna numérica)', colunas, key='y_linha')
    
    if x_col_linhas and y_col_linhas:
        grafico_linhas = px.line(df, x=x_col_linhas, y=y_col_linhas, title=f'Gráfico de Linhas: {x_col_linhas} vs {y_col_linhas}')
        st.plotly_chart(grafico_linhas)

    # Gráfico de pizza 
    st.subheader('Gráfico de Pizza')
    pie_col = st.selectbox('Selecione a coluna para os valores (Indico selecionar uma coluna numérica)', colunas, key='pie')
    pie_col_names = st.selectbox('Selecione a coluna para os nomes ', colunas, key='pie_names')
    
    if pie_col and pie_col_names:
        grafico_pizza = px.pie(df, values=pie_col, names=pie_col_names, title=f'Gráfico de Pizza: {pie_col_names} - {pie_col}')
        st.plotly_chart(grafico_pizza)



# 11 - Criar Visualizações de Dados - Gráficos Avançados:
# Adicione gráficos mais avançados (como histograma ou scatter plot) para fornecer insights mais profundos sobre os dados.

if uploaded_file:
    # Histograma
    st.subheader('Histograma')
    x_col_histo = st.selectbox('Selecione o eixo x (Indico selecionar uma coluna categórica)', colunas, key='x_histo')
    y_col_histo = st.selectbox('Selecione o eixo Y (Indico selecionar "Ano")', colunas, key='y_histo')
    grafico_histograma = px.histogram(df, x=x_col_histo, y=y_col_histo, nbins=200, )
    st.plotly_chart(grafico_histograma)

    # Scatter plot
    st.subheader('Scatter Plot')
    x_col_scatter = st.selectbox('Selecione o eixo x', colunas, key='x_scatter')
    y_col_scatter = st.selectbox('Selecione o eixo Y ', colunas, key='y_scatter')
    grafico_scatter = px.scatter(df, x=x_col_scatter, y=y_col_scatter)
    st.plotly_chart(grafico_scatter)


# 12 - Exibir Métricas Básicas:
# Implemente a exibição de métricas básicas (como contagem de registros, médias, somas) diretamente na interface para fornecer um resumo rápido dos dados carregados.

if uploaded_file:
# Limpar colunas numéricas removendo espaços e convertendo para números
    for coluna in df.columns:
        if df[coluna].dtype == 'object':
            df[coluna] = df[coluna].str.replace(r'[^\d]', '', regex=True) 
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')  

if uploaded_file:

    st.subheader("Métricas Básicas")
    
    # Contagem de registros
    total_registros = len(df)
    st.metric(label="Total de Registros", value=total_registros)
    
    # Soma de uma coluna numérica 
    sum_total = st.selectbox('Selecione uma coluna numérica para somar seus valores)', colunas, key='sum')
    total_Total = df[sum_total].sum()
    st.metric(label="Total ", value=total_Total)

    # Cálculo da média de outra coluna numérica
    mean_total = st.selectbox('Selecione uma coluna numérica para obter sua média)', colunas, key='mean')
    media_Total = df[mean_total].mean()
    st.metric(label="Média ", value=round(media_Total, 2))

    # Outras estatísticas descritivas
    st.write("Estatísticas descritivas gerais")
    st.write(df.describe())  

