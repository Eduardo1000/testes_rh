import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Resultados dos Testes')
st.header('Resultados dos Testes')
# st.subheader('XXXXXXXXXX')

df = pd.read_csv('resultados_testes_simplificado.csv')

df['cla_atual'] = pd.to_numeric(df.cla_atual, errors='coerce')

clientes = df['cliente'].dropna().to_list()

categorias = ['Clã', 'Hierarquia', 'Inovativa', 'Mercado']
categorias_atual = ['cla_atual', 'hierarquia_atual', 'inovativa_atual', 'mercado_atual']
categorias_ideal = ['cla_ideal', 'hierarquia_ideal', 'inovativa_ideal', 'mercado_ideal']

egograma_vars = ['PC', 'PP', 'A', 'CL', 'CA']

cliente = st.selectbox('Cliente:',
                               clientes)

def plot_cameron_quinn(fig1, r, theta, name):
    try:
        fig1.add_trace(go.Scatterpolar(
              r=r,
              theta=theta,
              fill='tonext',
              name=name
        ))
    except:
        pass

def plot_egograma(fig2, x, y, name):
    try:
        fig2.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name=name
        ))
    except:
        pass   

        
# Cameron e Quinn
geral_ideal = df[categorias_ideal].mean().values.flatten()
geral_atual = df[categorias_atual].mean().values.flatten()

cliente_atual = df[(df['cliente'] == cliente)][categorias_atual].values.flatten()
cliente_ideal = df[(df['cliente'] == cliente)][categorias_ideal].values.flatten()

contrato_selecao = df[(df['cliente'] == cliente)]['contrato']

df_contrato_atual = df.groupby('contrato')[categorias_atual].mean()
contrato_atual = df_contrato_atual.loc[contrato_selecao].values.flatten()

df_contrato_ideal = df.groupby('contrato')[categorias_ideal].mean()
contrato_ideal = df_contrato_ideal.loc[contrato_selecao].values.flatten()

area_selecao = df[(df['cliente'] == cliente)]['area']

df_area_atual = df.groupby('area')[categorias_atual].mean()
area_atual = df_area_atual.loc[area_selecao].values.flatten()

df_area_ideal = df.groupby('area')[categorias_ideal].mean()
area_ideal = df_area_ideal.loc[area_selecao].values.flatten()

# print(cliente)
# print(contrato_selecao)
# print(area_selecao)

fig1 = go.Figure()

plot_cameron_quinn(fig1, geral_atual, categorias, 'Geral Atual')
plot_cameron_quinn(fig1, geral_ideal, categorias, 'Geral Ideal')

plot_cameron_quinn(fig1, cliente_atual, categorias, 'Cliente Atual')
plot_cameron_quinn(fig1, cliente_ideal, categorias, 'Cliente Ideal')

plot_cameron_quinn(fig1, contrato_atual, categorias, 'Contrato Atual')
plot_cameron_quinn(fig1, contrato_ideal, categorias, 'Contrato Ideal')

plot_cameron_quinn(fig1, area_atual, categorias, 'Area Atual')
plot_cameron_quinn(fig1, area_ideal, categorias, 'Area Ideal')

fig1.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 40]
    )),
  showlegend=True
)

# fig1.show()
st.plotly_chart(fig1)

# Egograma
fig2 = go.Figure()

df_cliente_egograma = df[(df['cliente'] == cliente)][egograma_vars].T
df_cliente_egograma.columns = ['valor']

df_contrato_egograma = df.groupby('contrato')[egograma_vars].mean()
contrato_egograma = df_contrato_egograma.loc[contrato_selecao].values.flatten()

df_area_egograma = df.groupby('area')[egograma_vars].mean()
area_egograma = df_area_egograma.loc[area_selecao].values.flatten()

plot_egograma(fig2, df_cliente_egograma.index, df[egograma_vars].mean(), 'Geral')
plot_egograma(fig2, df_cliente_egograma.index, df_cliente_egograma['valor'], 'Cliente')
plot_egograma(fig2, df_cliente_egograma.index, contrato_egograma, 'Contrato')
plot_egograma(fig2, df_cliente_egograma.index, area_egograma, 'Área')

fig2.update_traces(marker=dict(line=dict(width=1,
                                color='DarkSlateGrey')),
          selector=dict(mode='markers'))

# fig2.show()
st.plotly_chart(fig2)
