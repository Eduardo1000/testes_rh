import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go


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
categorias = ['Inovativa', 'Mercado', 'Hierarquia', 'Clã']
categorias_atual = ['inovativa_atual', 'mercado_atual', 'hierarquia_atual', 'cla_atual']
categorias_ideal = ['inovativa_ideal', 'mercado_ideal', 'hierarquia_ideal', 'cla_ideal']
egograma_vars = ['PC', 'PP', 'A', 'CL', 'CA']
mapeamento_vars = [f"Escala{number:02d}" for number in range(1, 21)]
mapeamento_desempenho = {1: 'Atenção', 2: 'Vulnerável', 3: 'Proficiente', 4: 'Ótimo'}
legend = [
    ['color', 'ABREVIAÇÃO', 'SIGNIFICADO'],
    ['blue', 'DST', 'Destaque'],
    ['green', 'SAT', 'Satisfatório'],
    ['gray', 'ADQ', 'Adequado'],
    ['yellow', 'DES', 'Desenvolver'],
    ['orange', 'MAA', 'Merece Atenção Alto'],
    ['orange', 'MAB', 'Merece Atenção Baixo'],
    ['red', 'CRA', 'Crítico Alto'],
    ['red', 'CRB', 'Crítico Baixo'],
    ['white', '', '']
]
map_lid_dim = {
    "EMPREENDER": ['BUSCA INFORMAÇÃO', 'COMPETIÇÃO', 'DECISÃO', 'COMANDO', 'EXIGÊNCIA'],
    "FOCO": ['PERSISTÊNCIA', 'ATENÇÃO', 'RESISTE DISTRAÇÃO'],
    "ORDEM": ['PLANEJAMENTO', 'ORGANIZAÇÃO', 'ROTINA'],
    "DINAMISMO": ['ADAPTABILIDADE', 'AGILIDADE', 'DILIGÊNCIA'],
    "VITA EMOCIONAL": ['BIOFILIA', 'HUMOR', 'AUTOCONFIANÇA', 'AUS DEPRESSÃO', 'AUS ANSIEDADE'],
    "VÍNCULO": ['VINCULO FAMILIAR', 'SOCIOFILIA', 'SOLIDAR COMUN', 'SOLIDAR FRAGILI'],
    "CIVILIDADE": ['AMABILIDADE', 'COOPERAÇÃO', 'FRANQUEZA', 'HAB COMUNICAÇÃO'],
    'INTERAÇÃO <br>COM AUTORIDADE': ['OBEDIÊNCIA', 'DEPENDE APROVAÇÃO', 'COAÇÃO'],
    'AFASTAMENTO': ['DESCONFIANÇA', 'IRRITABILIDADE', 'HOSTILIDADE', 'RIVALIDADE'],
    'COMPOSIÇÃO DE IMAGEM': ['CUMPLICIDADE', 'DISSIMULAÇÃO', 'MANIPULAÇÃO', 'ESPERTEZA']
}


def main():
    st.set_page_config(page_title='Dados Liderança', layout='wide')
    st.header('Dados Liderança - Resultados dos Testes')

    # Abre a Planilha de dados
    df = pd.read_csv('resultados_testes_simplificado_lider.csv', sep=';', encoding='latin-1')
    df['cla_atual'] = pd.to_numeric(df.cla_atual, errors='coerce')

    # Remove aqueles não fizeram nenhum dos 3 testes
    df = df.dropna(how='all', subset=egograma_vars + categorias_atual + categorias_ideal + mapeamento_vars)

    # Define o colaborador
    colaborador = st.selectbox('Colaborador:', df['colaborador'].dropna().to_list())

    # Define colunas
    col1, col2 = st.columns(2)

    with col1:
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
            "tickvals":[i for i in range(0, 51, 10)],
            "ticktext":[i for i in range(0, 51, 10)]}})
        st.plotly_chart(fig1)

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

    with col2:
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

        # IBACO
        st.markdown("### IBACO")
        df_ibaco = pd.read_csv('resultados_testes_ibaco.csv', sep=',')

        ibaco = ['PC', 'REHP', 'PCI', 'SBE', 'PIE', 'PRT', 'PRI']

        colaborador_ibaco = df_ibaco[(df_ibaco['colaborador'] == colaborador)][ibaco].values.flatten()

        df_contrato_ibaco = df_ibaco.groupby('contrato')[ibaco].mean()
        contrato_ibaco = df_contrato_ibaco.loc[contrato_selecao].values.flatten()

        df_area_ibaco = df_ibaco.groupby('area')[ibaco].mean()
        area_ibaco = df_area_ibaco.loc[area_selecao].values.flatten()

        fig7 = go.Figure(data=[
            go.Bar(name='Colaborador', x=ibaco, y=colaborador_ibaco),
            go.Bar(name=f'{contrato_selecao}', x=ibaco, y=contrato_ibaco),
            go.Bar(name=f'{area_selecao}', x=ibaco, y=area_ibaco)
        ])

        fig7.update_layout(barmode='stack')

        st.plotly_chart(fig7)

    # Mapeamento Liderança Dimensões
    st.markdown("### Mapeamento Liderança")

    # Mapeamento Liderança Indicadores
    st.markdown("### Indicadores")

    # Define columns
    col_1, col_2, col_3 = st.columns(3)

    with col_1:
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

    with col_2:
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

    with col_3:
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

    # Mapeamento Liderança Indicadores
    st.markdown("### Dimensões")

    select_cols = [value for values in map_lid_dim.values() for value in values]
    df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
    df_map_lider.columns = ['valor']

    color_legend = pd.DataFrame(legend)
    new_header = color_legend.iloc[0]  # grab the first row for the header
    color_legend = color_legend[1:]  # take the data less the header row
    color_legend.columns = new_header  # set the header row as the df header
    color_legend = color_legend.set_index('ABREVIAÇÃO')

    df_map_lider['class'] = [key for key, values in map_lid_dim.items() for value in values]
    df_map_lider['color'] = color_legend.loc[df_map_lider['valor'].values]['color'].values
    fig = go.Figure(data=[go.Bar(
        x=df_map_lider.reset_index()[['class', 'index']].T.values,
        y=df_map_lider.valor,
        marker_color=df_map_lider.color  # marker color can be a single color value or an iterable
    )])
    fig.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=color_legend.index.values,
            ticktext=color_legend.SIGNIFICADO.values,
            type='category',
            categoryorder='array',
            # range=[0, len(color_legend)],
            categoryarray=color_legend.index[::-1].values,
        ),
        width=1800
    )
    # fig.update_xaxes(tickangle=15)
    st.plotly_chart(fig)


if __name__ == '__main__':
    main()