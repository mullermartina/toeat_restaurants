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
st.set_page_config(page_title = 'Countries',
                   page_icon = '🌎',
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

def bar_graph_with_colors(eixo_x, eixo_y, legenda, label_x, label_y, label_legenda, df_aux, title, title_size):
    fig = px.bar(df_aux,
                 x= eixo_x,
                 y=eixo_y,
                 color=legenda,
                 labels={eixo_x: label_x, eixo_y: label_y, legenda: label_legenda},
                 color_discrete_sequence=['mediumpurple', 'indianred', 'mediumseagreen', 'lightskyblue', 'pink', 'oldlace', 'greenyellow', 'orange', 'darksalmon', 'mediumaquamarine', 'lavenderblush', 'powderblue', 'khaki', 'deeppink', 'royalblue']
                )
    fig.update_layout(title_text=title, title_font_size= title_size, plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes( mirror=True, ticks='outside', showline=False, linecolor='black',gridcolor='darkgray')
    return fig

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
st.sidebar.markdown( '# Filtro' )

lista_paises = list(df1['country'].unique())
opcao_paises = st.sidebar.multiselect(
    'Escolha os paises que deseja visualizar',
    lista_paises,
    default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

linhas_selec = df1['country'].isin(opcao_paises)
df1 = df1.loc[linhas_selec, :]

# ==================================================================
# Layout no Streamlit
# ==================================================================
st.header( 'ToEat Restaurants 🍎' )
st.subheader(' Visão Países ')

with st.container():
    st.markdown( """---""" )
    df_restaurants_per_country = df1.loc[:, ['country', 'restaurant_name']].groupby('country').count().sort_values( by='restaurant_name', ascending=False ).reset_index()
    fig = bar_graph_without_color_sequence('country', 'restaurant_name', 'País', 'Nome dos Restaurante', df_restaurants_per_country, 'Quantidade de Restaurantes Registrados por País', 26)
    st.plotly_chart( fig )

with st.container():
    st.markdown( """---""" ) # antes havia escrito df1.loc[:, 'country', 'city'], sem [] nas colunas e deu erro 'too many indexers'
    df_cities_per_country = df1.loc[:, ['country', 'city']].groupby('country').nunique().sort_values(by='city', ascending=False).reset_index()
    fig = bar_graph_without_color_sequence('country', 'city', 'País', 'Cidade', df_cities_per_country, 'Quantidade de Cidades Registradas por País', 26)
    st.plotly_chart( fig )
    
with st.container():
    st.markdown( """---""" )
    df_votes_per_country = df1.loc[:, ['country', 'votes']].groupby('country').mean().reset_index()
    fig = bar_graph_without_color_sequence('country', 'votes', 'País', 'Avaliações', df_votes_per_country, 'Média de Avaliações por País', 26)
    st.plotly_chart( fig, use_container_width=True )



with st.container():
    st.markdown( """---""" )
    df_cost_per_country_and_currency = round(df1.loc[:, ['country', 'average_cost_for_two', 'currency']].groupby(['country', 'currency']).mean(), 2).reset_index()
    fig = bar_graph_with_colors('country', 'average_cost_for_two', 'currency', 'País', 'Preço Médio para 2 pessoas', 'Moeda', df_cost_per_country_and_currency, 'Preço médio para 2 pessoas segundo cada país', 26)
    st.plotly_chart( fig )        
        
        
    