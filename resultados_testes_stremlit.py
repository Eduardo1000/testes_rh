import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title='Dados Liderança')
st.header('Dados Liderança - Resultados dos Testes')
# st.subheader('Resultados dos Testes')

df = pd.read_csv('resultados_testes_simplificado_lider.csv', sep=';', encoding='latin-1')

df['cla_atual'] = pd.to_numeric(df.cla_atual, errors='coerce')

categorias = ['Inovativa', 'Mercado', 'Hierarquia', 'Clã']
categorias_atual = ['inovativa_atual', 'mercado_atual', 'hierarquia_atual', 'cla_atual']
categorias_ideal = ['inovativa_ideal', 'mercado_ideal', 'hierarquia_ideal', 'cla_ideal']

egograma_vars = ['PC', 'PP', 'A', 'CL', 'CA']

mapeamento_vars = [f"Escala{number:02d}" for number in range(1, 21)]

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

# Remove quem não fez nenhum dos 3 testes
df = df.dropna(how='all', subset=egograma_vars+categorias_atual+categorias_ideal+mapeamento_vars)

# Define o colaborador
colaborador = st.selectbox('Colaborador:', df['colaborador'].dropna().to_list())


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


def plot_bar(figure, x, y, name, color):
    try:
        figure.add_trace(go.Bar(
            x=x,
            y=y,
            name=name,
            orientation='h',
            marker=dict(
                color=color,
                # line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
            )
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
            range=[0, 30]
        ),
        angularaxis=dict(
                tickfont_size=18,
                rotation=45,
                direction="clockwise"
              )
    ),
    showlegend=True,
)
fig1.update_layout(polar={"radialaxis":{
    "tickmode":"array",
    "tickvals":[i for i in range(0, 31, 10)],
    "ticktext":[i for i in range(0, 31, 10)]}})
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

# Johari
st.markdown("### Johari")
select_cols = ['johari_A', 'johari_C', 'johari_O', 'johari_D']

df_johari = df[(df['colaborador'] == colaborador)][select_cols].values[0]
fig = go.Figure(data=[go.Table(
  cells=dict(
    values=[['<br><br>A (Aberta ou Arena)', '<br><br>O (Oculta ou Fechada)'],
            ['<br><br>C (Cega)', '<br><br>D (Desconhecida)']],
    line_color=['black'],
    fill_color=np.where(np.resize(df_johari, (2, 2)), 'rgb(242, 140, 40)', 'rgb(249, 249, 249)'),
    align='center', font=dict(color='black', size=12),
    font_size=24,
    height=100
  ))
])
fig.layout['template']['data']['table'][0]['header']['fill']['color'] = 'rgba(0,0,0,0)'
st.plotly_chart(fig)


# Mapeamento
st.markdown("### Mapeamento")
fig3 = go.Figure()

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

# Mapeamento Liderança Dimensões
st.markdown("### Mapeamento Liderança Dimensões")

legend = [
    ['color',	'ABREVIAÇÃO',	'SIGNIFICADO'],
    ['blue',	'DST',	'Destaque'],
    ['green',	'SAT',	'Satisfatório'],
    ['gray',	'ADQ',	'Adequado'],
    ['yellow',	'DES',	'Desenvolver'],
    ['orange',	'MAA',	'Merece Atenção Alto'],
    ['orange',	'MAB',	'Merece Atenção Baixo'],
    ['red',	'CRA',	'Crítico Alto'],
    ['red',	'CRB',	'Crítico Baixo']
]

# Mapeamento Liderança Dimensões - Positivas
st.write("Escalas Positivas")

fig = go.Figure()

select_cols = ['BUSCA INFORMAÇÃO', 'COMPETIÇÃO', 'DECISÃO',	'COMANDO', 'EXIGÊNCIA']
df_title = 'EMPREENDER'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


fig = go.Figure()

select_cols = ['PERSISTÊNCIA',	'ATENÇÃO',	'RESISTE DISTRAÇÃO']
df_title = 'FOCO'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


fig = go.Figure()

select_cols = ['PLANEJAMENTO',	'ORGANIZAÇÃO',	'ROTINA']
df_title = 'ORDEM'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


fig = go.Figure()

select_cols = ['ADAPTABILIDADE',	'AGILIDADE',	'DILIGÊNCIA']
df_title = 'DINAMISMO'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


fig = go.Figure()

select_cols = ['BIOFILIA',	'HUMOR',	'AUTOCONFIANÇA',	'AUS DEPRESSÃO',	'AUS ANSIEDADE']
df_title = 'VITA EMOCIONAL'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


fig = go.Figure()

select_cols = ['VINCULO FAMILIAR',	'SOCIOFILIA',	'SOLIDAR COMUN','SOLIDAR FRAGILI']
df_title = 'VÍNCULO'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


fig = go.Figure()

select_cols = ['AMABILIDADE',	'COOPERAÇÃO',	'FRANQUEZA',	'HAB COMUNICAÇÃO']
df_title = 'CIVILIDADE'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


# Mapeamento Liderança Dimensões - Negativas
st.write("Escalas Negativas")


fig = go.Figure()

select_cols = ['OBEDIÊNCIA',	'DEPENDE APROVAÇÃO',	'COAÇÃO']
df_title = 'INTERAÇÃO COM AUTORIDADE'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


fig = go.Figure()

select_cols = ['DESCONFIANÇA',	'IRRITABILIDADE',	'HOSTILIDADE',	'RIVALIDADE']
df_title = 'AFASTAMENTO'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


fig = go.Figure()

select_cols = ['CUMPLICIDADE',	'DISSIMULAÇÃO',	'MANIPULAÇÃO',	'ESPERTEZA']
df_title = 'COMPOSIÇÃO DE IMAGEM'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_egograma(fig, df_map_lider.index, df_map_lider['valor'], 'Colaborador')

fig.update_layout(
    title=df_title
)
st.plotly_chart(fig)


# Mapeamento Liderança Indicadores
st.markdown("### Mapeamento Liderança Indicadores")
fig4 = go.Figure()

select_cols = ['LIDERANÇA', 'EQUIPE', 'RELAÇÃO HIERÁRQUICA', 'RESILIÊNCIA - R', 'FOCO EM RESULTADO', 'PROATIVIDADE',
               'AÇÃO SOB PRESSÃO', 'NEGOCIAÇÃO', 'RESOLUÇÃO DE CONFLITO', 'INOVAÇÃO']
df_title = 'MACRO INDICADORES - DIREÇÃO POSITIVA'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_bar(fig4, df_map_lider['valor'], df_map_lider.index, 'Colaborador', 'lightgreen')

fig4.update_layout(
    title=df_title
)
st.plotly_chart(fig4)


fig5 = go.Figure()

select_cols = ['AUTONOMIA', 'ASSERTIVIDADE', 'FLEXIBILIDADE', 'COMUNICABILIDADE', 'EMPENHO', 'DISCIPLINA', 'SEGURANÇA',
               'AUTENTICIDADE', 'TRANQUILIDADE - T', 'CUIDADO']
df_title = 'MICRO INDICADORES - DIREÇÃO POSITIVA'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_bar(fig5, df_map_lider['valor'], df_map_lider.index, 'Colaborador', 'lightgreen')

fig5.update_layout(
    title=df_title
)
st.plotly_chart(fig5)


fig6 = go.Figure()

select_cols = ['PROTELAÇÃO', 'IMEDIATISMO', 'IMPULSIVIDADE - P', 'AGRESSIVIDADE', 'PASSIVIDADE', 'TORMENTO', 'DESÂNIMO']
df_title = 'MICRO INDICADORES - DIREÇÃO NEGATIVA'
df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
df_map_lider.columns = ['valor']
plot_bar(fig6, df_map_lider['valor'], df_map_lider.index, 'Colaborador', 'purple')

fig6.update_layout(
    title=df_title
)
st.plotly_chart(fig6)

