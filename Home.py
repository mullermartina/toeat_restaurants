# ==================================================================
# Libraries
# ==================================================================
from PIL import Image
import streamlit as st

# ==================================================================
# Configurações
# ==================================================================
st.set_page_config(page_title = 'Home',
                   page_icon = '🍎',
                  layout= 'centered')

st.sidebar.image(Image.open('ftcfork4.png'), width=250)

# ==================================================================
# Barra Lateral
# ==================================================================

st.sidebar.markdown( '# ToEat Restaurants' ) 
st.sidebar.markdown( """---""" )

# ==================================================================
# Layout
# ==================================================================

st.header('ToEat Restaurants 🍎')

st.subheader('Um projeto de análise de dados', divider='gray')

st.markdown("""
           A partir do conhecimento obtido em curso realizado dentro da Comunidade DS, foi desenvolvida uma sequência de dashboards. Assim, aqui você encontrará uma análise realizada a partir de dados do marketplace Zomato, disponíveis no Kaggle.

           Na aba lateral das demais páginas você encontrará filtros. Selecione as opções desejadas e veja gráficos e métricas alterarem.
           
           Em Main Page você obterá alguns dados gerais bem como poderá navegar por um mapa interativo, que mostra a localização de cada restaurante, qual sua média de avaliação, o preço médio de um prato para duas pessoas e qual a moeda aceita.
           
           Nas demais páginas você obterá gráficos e números importantes acerca dos países, das cidades e das culinárias abrangidas.   
"""
)
st.markdown('')
st.markdown('')
st.markdown('✔ Dados disponíveis [aqui](https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv)')
st.markdown('''✔ Desenvolvido por Martina Müller. Contato [aqui](https://www.linkedin.com/in/martinaamuller/)''')