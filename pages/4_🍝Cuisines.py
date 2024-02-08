# ==================================================================
# Libraries
# ==================================================================
import pandas as pd
import plotly.express as px
import inflection
from PIL import Image
import streamlit as st

# ==================================================================
# Configurações da Página 
# ==================================================================
st.set_page_config(page_title = 'Cuisines MODULO',
                   page_icon = '🍝',
                  layout= 'centered')

# ==================================================================
# Funções 
# ==================================================================
# Função para renomear colunas
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# Função para converter código de país para nome de país
COUNTRIES = {
    1: 'India',
    14: 'Australia',
    30: 'Brazil',
    37: 'Canada',
    94: 'Indonesia',
    148: 'New Zeland',
    162: 'Philippines',
    166: 'Qatar',
    184: 'Singapure',
    189: 'South Africa',
    191: 'Sri Lanka',
    208: 'Turkey',
    214: 'United Arab Emirates',
    215: 'England',
    216:'United States of America'
    }

def country_name(country_id):
    return COUNTRIES[country_id]

# Função para criar categoria em relação ao preço da comida
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Função para transformar código de cor em nome de cor
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }

def color_name(color_code):
    return COLORS[color_code]

def clean_code( df1 ):
    """
    Esta função tem o objetivo de, junto às funções fornecidas no exercício, finalizar a limpeza do gráfico
    """
    # 1. Removendo linhas duplicadas
    df1.drop_duplicates(inplace=True)
    
    # 2. Verificando se há colunas inúteis, com só 1 valor por exemplo.
    df1 = df1.drop('switch_to_order_menu', axis=1)

    # 3. Pegando somente a primeira opção de Cuisines, usando estratégia do Pedro
    df1['cuisines'] = df1['cuisines'].astype(str)
    df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0])
    
    # 4. Convertendo tipo das colunas. Há cols com 0 e 1 então é bool e nao int
    df1['has_table_booking'] = df1['has_table_booking'].astype(bool)
    df1['has_online_delivery'] = df1['has_online_delivery'].astype(bool)
    df1['is_delivering_now'] = df1['is_delivering_now'].astype(bool)
    
    # 5. Retirando nan de df1['cuisines]
    linhas_selecionadas = (df1['cuisines'] != 'nan') & (df1['cuisines'] != 'Drinks Only') & (df1['cuisines'] != 'Mineira')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # 6. Retirando o outlier de average_cost_for_two
    #aust_max = df1.loc[df1['country'] == 'Australia', ['average_cost_for_two']].max()
    #aust_max = 25000017
    linhas_selec_aust = df1['average_cost_for_two'] != 25000017
    df1 = df1.loc[linhas_selec_aust, :].copy()

    return df1

def bar_graph_without_color_sequence(eixo_x, eixo_y, label_x, label_y, df_aux, title, title_size):
    """
    Esta função tem o objetivo de gerar um gráfico de barras sem legenda e sem diferenciação nas cores
    """
    fig = px.bar(df_aux,                                                            
                 x=eixo_x,
                 y=eixo_y,
                 labels={eixo_x:label_x, eixo_y:label_y})
    fig.update_layout(title_text=title, title_font_size=title_size, plot_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(marker=dict(color='indianred'))
    fig.update_yaxes( mirror=True, ticks='outside', showline=False, linecolor='black',gridcolor='darkgray')
    return fig

def best_cuisine(df1, cuisine, label): #return None?! df_aux, qual cuisine
    cols = ['cuisines', 'aggregate_rating', 'restaurant_name', 'restaurant_id', 'country', 'city', 'currency', 'average_cost_for_two']
    df_aux = ( df1.loc[df1['cuisines'] == cuisine, cols]
                        .groupby(['restaurant_id','restaurant_name', 'cuisines', 'country', 'city', 'currency', 'average_cost_for_two'])
                        .mean()
                        .sort_values(by='aggregate_rating', ascending=False).reset_index() )
    df_aux.loc[df_aux['aggregate_rating'] == df_aux['aggregate_rating'].max(), cols].groupby(['restaurant_name', 'cuisines']).min()
    st.metric(label=f'{label}: {df_aux.restaurant_name[0]}', 
                value=f'{df_aux.aggregate_rating[0]}/5.0',
                help=f"""
                País: {df_aux.country[0]} \n
                Cidade: {df_aux.city[0]} \n
                Preço para duas pessoas: {df_aux.currency[0]}{df_aux.average_cost_for_two[0]} 
                """
                )
    return None

# ==================================== Início da Estrutura Lógica ====================================
    
# ==================================================================
#Import dataset
# ==================================================================
df0 = pd.read_csv( 'dataset/zomato.csv' )

# ==================================================================
# Limpeza de Dados
# ==================================================================
df1 = rename_columns( df0 )
 
df1['country'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))

df1['category_price'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_tye(x))
   
df1['rating_color_name'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))
    
df1 = clean_code( df1 )

# ==================================================================
# Barra Lateral no Streamlit 
# ==================================================================
image_path = 'ftcfork4.png'
image = Image.open( image_path )
st.sidebar.image( image, width=250)

st.sidebar.markdown( '# ToEat Restaurants' ) 
st.sidebar.markdown( """---""" )
st.sidebar.markdown( '# Filtros' )

lista_paises = list(df1['country'].unique())
opcao_paises = st.sidebar.multiselect(
    'Escolha os paises que deseja visualizar:',
    lista_paises,
    default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

linhas_selec = df1['country'].isin(opcao_paises)
df1 = df1.loc[linhas_selec, :]
st.sidebar.markdown("""---""")

st.sidebar.markdown( '##### Selecione a quantidade que deseja visualizar:' )

value_slider = st.sidebar.slider(
    'Qual valor?',
    value=10,
    min_value=0,
    max_value=20)
st.sidebar.markdown("""---""")

lista_cozinhas = list(df1['cuisines'].unique())
opcao_cozinhas = st.sidebar.multiselect(
    'Escolha as culinárias que deseja visualizar:',
    lista_cozinhas,
    default = ['Italian', 'American', 'Arabian', 'Brazilian', 'Japanese', 'Cafe'])

linhas_selec2 = df1['cuisines'].isin(opcao_cozinhas)
df1 = df1.loc[linhas_selec2, :]

# ==================================================================
# Layout no Streamlit
# ==================================================================
st.header( 'ToEat Restaurants 🍎' )
st.subheader(' Visão Culinárias ')

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        italiana = best_cuisine(df1, 'Italian', 'Italiana')
        
    with col2:
        americana = best_cuisine(df1, 'American', 'Americana')

    with col3:
        arabe = best_cuisine(df1, 'Arabian', 'Árabe')

    with col4:
        japonesa = best_cuisine(df1, 'Japanese', 'Japonesa')

with st.container():
    st.markdown( """---""" )
    st.title( f'Top {value_slider} restaurantes' )
    cols = ['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'average_cost_for_two', 'currency', 'aggregate_rating', 'votes']
    df_aux = df1.loc[:, cols].sort_values(by='aggregate_rating', ascending=False).head(value_slider)
    df_aux2 = df_aux.sort_values(by='restaurant_id', ascending=True)
    st.dataframe( df_aux2 )
    st.markdown( """---""" )

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        cols = ['cuisines', 'aggregate_rating']          
        df_best_cuisine = df1.loc[:, cols].groupby('cuisines').mean().sort_values(by='aggregate_rating', ascending=False).reset_index().head(value_slider)
        fig = bar_graph_without_color_sequence('cuisines', 'aggregate_rating', 'Culinária', 'Nota Média', df_best_cuisine, 'Melhores tipos de culinária', 20)
        st.plotly_chart( fig, use_container_width=True )

    with col2:
        cols = ['cuisines', 'aggregate_rating']             
        df_worst_cuisine = df1.loc[:, cols].groupby('cuisines').mean().sort_values(by='aggregate_rating', ascending=True).reset_index().head(value_slider)
        fig = bar_graph_without_color_sequence('cuisines', 'aggregate_rating', 'Culinária', 'Nota Média', df_worst_cuisine, 'Piores tipos de culinária', 20)
        st.plotly_chart( fig, use_container_width=True )