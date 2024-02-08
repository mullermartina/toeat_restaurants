# ==================================================================
# Libraries
# ==================================================================
import pandas as pd
import inflection
from PIL import Image
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# ==================================================================
# Configurações da Página 
# ==================================================================
st.set_page_config(page_title = 'Main Page',
                   page_icon = '📌',
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

def restaurant_map( df1 ):
    fig = folium.Figure(width=1024, height=600)

# Cria o objeto map e adiciona ao painel
    mapa = folium.Map(max_bounds=True).add_to(fig)

    marker_cluster = MarkerCluster().add_to(mapa)

    icone= 'fa-cutlery'

    for index, location_info in df1.iterrows():
    	folium.Marker([location_info['latitude'],
                       location_info['longitude']],
                       icon=folium.Icon(color=location_info['rating_color_name'], icon=icone, prefix='fa'),
                       popup = folium.Popup(f"""<h6> <b> {location_info['restaurant_name']} </b> </h6> <br>
                       Cozinha: {location_info['cuisines']} <br>
                       Preço médio para dois: {location_info['average_cost_for_two'], location_info['currency']} <br>
                       Avaliação: {location_info['aggregate_rating']} / 5.0 <br>""",
                       max_width = len(f"{location_info['restaurant_name']}")*20)).add_to(marker_cluster)
    
    folium_static( mapa )
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
st.sidebar.markdown( """---""" ) #ssim eu crio uma linha
st.sidebar.markdown( '# Filtro' )

lista_paises = list(df1['country'].unique())
opcao_paises = st.sidebar.multiselect(
    'Escolha os paises que deseja visualizar',
    lista_paises,
    default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

linhas_selec = df1['country'].isin(opcao_paises)
df1 = df1.loc[linhas_selec, :]

st.sidebar.write("""---""")
st.sidebar.write('Desenvolvido por Martina Müller')

# ==================================================================
# Layout no Streamlit
# ==================================================================
st.header( 'ToEat Restaurants 🍎' )

with st.container():
    st.subheader( 'Métricas Gerais 🔎' )
    col1, col2, col3, col4, col5 = st.columns( 5,  gap='large' ) #esse gap é pra ter distancia

    with col1:
        country_unico = df1['country'].nunique()
        col1.markdown('Países')
        col1.subheader(country_unico)

    with col2:
        rest_unico = df1['restaurant_id'].nunique()
        col2.markdown('Restaurantes')
        col2.subheader(rest_unico)
            
    with col3:
        city_unico =  df1['city'].nunique()
        col3.markdown('Cidades')
        col3.subheader(city_unico)
            
    with col4:
        total_aval =  df1['votes'].sum()
        col4.markdown('Avaliações')
        col4.subheader(total_aval)

            
    with col5:
        cuisine_unico =  len(df1['cuisines'].unique())
        col5.markdown('Culinárias')
        col5.subheader(cuisine_unico)

with st.container():
    st.markdown( """---""" )
    st.subheader( 'Mapa 📌' )
    st.markdown( 'Dê zoom para visualizar os restaurantes de acordo com o endereço!' )
    restaurant_map( df1 )
        