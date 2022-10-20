import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Dados Liderança')
st.header('Dados Liderança - Resultados dos Testes')
# st.subheader('Resultados dos Testes')

df = pd.read_csv('resultados_testes_simplificado.csv', sep=';')

df['cla_atual'] = pd.to_numeric(df.cla_atual, errors='coerce')

colaboradores = df['colaborador'].dropna().to_list()

categorias = ['Clã', 'Hierarquia', 'Inovativa', 'Mercado']
categorias_atual = ['cla_atual', 'hierarquia_atual', 'inovativa_atual', 'mercado_atual']
categorias_ideal = ['cla_ideal', 'hierarquia_ideal', 'inovativa_ideal', 'mercado_ideal']

egograma_vars = ['PC', 'PP', 'A', 'CL', 'CA']

mapeamento_escalas = [
    'Pressões da Vida que vivencia com dificuldade',
    'Satisfações da Vida vivenciadas com prazer',
    'Consciência Emocional',
    'Expressão Emocional',
    'Consciência Emocional dos Outros(rapport)',
    'Intencionalidade(Foco)',
    'Criatividade',
    'Elasticidade(Flexibilidade)',
    'Conexões Interpessoais autênticas',
    'Insatisfação Construtiva(Consenso)',
    'Perspectiva otimista(Euforia)',
    'Compaixão Empática',
    'Intuição Acatada',
    'Raio de Confiança(Lógica)',
    'Poder Pessoal(Carisma)',
    'Integridade',
    'Saúde Geral',
    'Qualidade de Vida',
    'Quociente de Relacionamento',
    'Desempenho Ótimo'
]
mapeamento_desempenho = {1: 'Atenção', 2: 'Vulnerável', 3: 'Proficiente', 4: 'Ótimo'}

colaborador = st.selectbox('Colaborador:',
                           colaboradores)


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


def plot_egograma(figure, x, y, name):
    try:
        figure.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name=name
        ))
    except:
        pass


# Cameron e Quinn
st.markdown("### Cameron e Quinn")

geral_ideal = df[categorias_ideal].mean().values.flatten()
geral_atual = df[categorias_atual].mean().values.flatten()

colaborador_atual = df[(df['colaborador'] == colaborador)][categorias_atual].values.flatten()
colaborador_ideal = df[(df['colaborador'] == colaborador)][categorias_ideal].values.flatten()

contrato_selecao = df[(df['colaborador'] == colaborador)]['contrato'].item()

df_contrato_atual = df.groupby('contrato')[categorias_atual].mean()
contrato_atual = df_contrato_atual.loc[contrato_selecao].values.flatten()

df_contrato_ideal = df.groupby('contrato')[categorias_ideal].mean()
contrato_ideal = df_contrato_ideal.loc[contrato_selecao].values.flatten()

area_selecao = df[(df['colaborador'] == colaborador)]['area'].item()

df_area_atual = df.groupby('area')[categorias_atual].mean()
area_atual = df_area_atual.loc[area_selecao].values.flatten()

df_area_ideal = df.groupby('area')[categorias_ideal].mean()
area_ideal = df_area_ideal.loc[area_selecao].values.flatten()

fig1 = go.Figure()

plot_cameron_quinn(fig1, geral_atual, categorias, 'Spassu - Atual')
plot_cameron_quinn(fig1, geral_ideal, categorias, 'Spassu - Ideal')

plot_cameron_quinn(fig1, colaborador_atual, categorias, 'Colaborador - Atual')
plot_cameron_quinn(fig1, colaborador_ideal, categorias, 'Colaborador - Ideal')

plot_cameron_quinn(fig1, contrato_atual, categorias, f'Contrato ({contrato_selecao}) - Atual')
plot_cameron_quinn(fig1, contrato_ideal, categorias, f'Contrato ({contrato_selecao}) - Ideal')

plot_cameron_quinn(fig1, area_atual, categorias, f'Área ({area_selecao}) - Atual')
plot_cameron_quinn(fig1, area_ideal, categorias, f'Área ({area_selecao}) - Ideal')

fig1.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 50]
        )),
    showlegend=True
)

st.plotly_chart(fig1)

# Egograma
st.markdown("### Egograma")
fig2 = go.Figure()

df_colaborador_egograma = df[(df['colaborador'] == colaborador)][egograma_vars].T
df_colaborador_egograma.columns = ['valor']

df_contrato_egograma = df.groupby('contrato')[egograma_vars].mean()
contrato_egograma = df_contrato_egograma.loc[contrato_selecao].values.flatten()

df_area_egograma = df.groupby('area')[egograma_vars].mean()
area_egograma = df_area_egograma.loc[area_selecao].values.flatten()

plot_egograma(fig2, df_colaborador_egograma.index, df[egograma_vars].mean(), 'Spassu')
plot_egograma(fig2, df_colaborador_egograma.index, df_colaborador_egograma['valor'], 'Colaborador')
plot_egograma(fig2, df_colaborador_egograma.index, contrato_egograma, f'Contrato ({contrato_selecao})')
plot_egograma(fig2, df_colaborador_egograma.index, area_egograma, f'Área ({area_selecao})')

fig2.update_traces(marker=dict(line=dict(width=1,
                                         color='DarkSlateGrey')),
                   selector=dict(mode='markers'))

st.plotly_chart(fig2)

# Mapeamento
st.markdown("### Mapeamento")
fig3 = go.Figure()

mapeamento_vars = [f"Escala{number:02d}" for number in range(1, 21)]
df_mapeamento = df[(df['colaborador'] == colaborador)][mapeamento_vars].T
df_mapeamento.columns = ['valor']
df_mapeamento.index = mapeamento_escalas
df_mapeamento = df_mapeamento.replace(mapeamento_desempenho)

plot_egograma(fig3, df_mapeamento.index, df_mapeamento['valor'], 'Colaborador')

fig3.update_traces(marker=dict(line=dict(width=1,
                                         color='DarkSlateGrey')),
                   selector=dict(mode='markers'),
                   )
fig3.update_xaxes(title_text='Zonas de Performance', tickangle=-45, side='top')
fig3.update_yaxes(title_text='Área de Desempenho')

st.plotly_chart(fig3)
