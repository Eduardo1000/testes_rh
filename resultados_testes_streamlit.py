import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go


def plot_cameron_quinn(fig1, r, theta, name, visible):
    try:
        fig1.add_trace(go.Scatterpolar(
            r=r,
            theta=theta,
            fill='tonext',
            name=name,
            visible=visible
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


def plot_ibaco(figure, x, y, text, name):
    try:
        figure.add_trace(go.Bar(
            x=x,
            y=y,
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
            showlegend=False,
            text=x.values,
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
    "VIDA EMOCIONAL": ['BIOFILIA', 'HUMOR', 'AUTOCONFIANÇA', 'AUS DEPRESSÃO', 'AUS ANSIEDADE'],
    "VÍNCULO": ['VINCULO FAMILIAR', 'SOCIOFILIA', 'SOLIDAR COMUN', 'SOLIDAR FRAGILI'],
    "CIVILIDADE": ['AMABILIDADE', 'COOPERAÇÃO', 'FRANQUEZA', 'HAB COMUNICAÇÃO'],
    'INTERAÇÃO<br>COM<br>AUTORIDADE': ['OBEDIÊNCIA', 'DEPENDE APROVAÇÃO', 'COAÇÃO'],
    'AFASTAMENTO': ['DESCONFIANÇA', 'IRRITABILIDADE', 'HOSTILIDADE', 'RIVALIDADE'],
    'COMPOSIÇÃO<br>DE IMAGEM': ['CUMPLICIDADE', 'DISSIMULAÇÃO', 'MANIPULAÇÃO', 'ESPERTEZA']
}


def main():
    st.set_page_config(page_title='Dados Liderança', layout='wide')
    st.header('Dados Liderança - Resultados dos Testes')

    # Abre a Planilha de dados
    df = pd.read_csv('resultados_testes_simplificado_lider.csv', sep=';')
    df['cla_atual'] = pd.to_numeric(df.cla_atual, errors='coerce')

    # Remove aqueles não fizeram nenhum dos 3 testes
    df = df.dropna(how='all', subset=egograma_vars + categorias_atual + categorias_ideal + mapeamento_vars)

    # Define o colaborador
    colaborador = st.selectbox('Colaborador:', df['colaborador'].dropna().to_list())

    # Define a area
    area = st.selectbox('Área:', df['area'].dropna().unique())

    # Define o contrato
    contrato = st.selectbox('Contrato:', df['contrato'].dropna().unique())

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

        df_area_selecionada_atual = df.groupby('area')[categorias_atual].mean()
        area_consulta_atual = df_area_selecionada_atual.loc[area].values.flatten()

        df_area_selecionada_ideal = df.groupby('area')[categorias_ideal].mean()
        area_consulta_ideal = df_area_selecionada_ideal.loc[area].values.flatten()

        df_contrato_selecionado_atual = df.groupby('contrato')[categorias_atual].mean()
        contrato_consulta_atual = df_contrato_selecionado_atual.loc[contrato].values.flatten()

        df_contrato_selecionado_ideal = df.groupby('contrato')[categorias_atual].mean()
        contrato_consulta_ideal = df_contrato_selecionado_ideal.loc[contrato].values.flatten()

        fig1 = go.Figure()

        plot_cameron_quinn(fig1, geral_atual, categorias, 'Spassu - Atual', visible=None)
        plot_cameron_quinn(fig1, geral_ideal, categorias, 'Spassu - Ideal', visible='legendonly')

        plot_cameron_quinn(fig1, colaborador_atual, categorias, 'Colaborador - Atual', visible=None)
        plot_cameron_quinn(fig1, colaborador_ideal, categorias, 'Colaborador - Ideal', visible='legendonly')

        plot_cameron_quinn(fig1, area_atual, categorias, f'Área {area_selecao} - Atual', visible=None)
        plot_cameron_quinn(fig1, area_ideal, categorias, f'Área {area_selecao} - Ideal', visible='legendonly')

        plot_cameron_quinn(fig1, contrato_atual, categorias, f'Contrato {contrato_selecao} - Atual', visible=None)
        plot_cameron_quinn(fig1, contrato_ideal, categorias, f'Contrato {contrato_selecao} - Ideal', visible='legendonly')

        if area != area_selecao:
            plot_cameron_quinn(fig1, area_consulta_atual, categorias, f'Área {area} - Atual', visible=None)
            plot_cameron_quinn(fig1, area_consulta_ideal, categorias, f'Área {area} - Ideal', visible='legendonly')

        if contrato != contrato_selecao:
            plot_cameron_quinn(fig1, contrato_consulta_atual, categorias, f'Contrato {contrato} - Atual', visible=None)
            plot_cameron_quinn(fig1, contrato_consulta_ideal, categorias, f'Contrato {contrato} - Atual', visible='legendonly')

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
            margin=dict(l=30, r=20, t=20, b=20),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.01
            )
        )
        st.plotly_chart(fig1, use_container_width=True)

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

    with col2:
        st.markdown("### IBACO")

        cols_ibaco = ['PC_ibaco', 'REHP', 'PCI', 'SBE', 'PIE', 'PRT', 'PRI']

        geral_ibaco = df[cols_ibaco].mean().values.flatten()
        colaborador_ibaco = df[(df['colaborador'] == colaborador)][cols_ibaco].values.flatten()
        df_contrato_ibaco = df.groupby('contrato')[cols_ibaco].mean()
        contrato_ibaco = df_contrato_ibaco.loc[contrato_selecao].values.flatten()
        df_area_ibaco = df.groupby('area')[cols_ibaco].mean()
        area_ibaco = df_area_ibaco.loc[area_selecao].values.flatten()

        df_contrato_selecionado_ibaco = df.groupby('contrato')[cols_ibaco].mean()
        contrato_selecionado_ibaco = df_contrato_selecionado_ibaco.loc[contrato].values.flatten()
        df_area_selecionada_ibaco = df.groupby('area')[cols_ibaco].mean()
        area_selecionada_ibaco = df_area_selecionada_ibaco.loc[area].values.flatten()

        fig_ibaco = go.Figure()

        dimensoes_ibaco = ['PC', 'REHP', 'PCI', 'SBE', 'PIE', 'PRT', 'PRI']
        plot_ibaco(fig_ibaco, dimensoes_ibaco, geral_ibaco, np.around(geral_ibaco, decimals=2), 'Spassu')
        plot_ibaco(fig_ibaco, dimensoes_ibaco, colaborador_ibaco, colaborador_ibaco, 'Colaborador')
        plot_ibaco(fig_ibaco, dimensoes_ibaco, area_ibaco, np.around(area_ibaco, decimals=2), f'Área {area_selecao}')
        plot_ibaco(fig_ibaco, dimensoes_ibaco, contrato_ibaco, np.around(contrato_ibaco, decimals=2),
                   f'Contrato {contrato_selecao}')

        if area != area_selecao:
            plot_ibaco(fig_ibaco, dimensoes_ibaco, area_selecionada_ibaco, np.around(area_selecionada_ibaco, decimals=2), f'Área {area}')

        if contrato != contrato_selecao:
            plot_ibaco(fig_ibaco, dimensoes_ibaco, contrato_selecionado_ibaco, np.around(contrato_selecionado_ibaco, decimals=2),
                   f'Contrato {contrato}')

        fig_ibaco.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig_ibaco, use_container_width=True)

        # Egograma
        st.markdown("### Egograma")
        fig2 = go.Figure()

        df_colaborador_egograma = df[(df['colaborador'] == colaborador)][egograma_vars].T
        df_colaborador_egograma.columns = ['valor']

        df_area_egograma = df.groupby('area')[egograma_vars].mean()
        area_egograma = df_area_egograma.loc[area_selecao].values.flatten()

        df_contrato_egograma = df.groupby('contrato')[egograma_vars].mean()
        contrato_egograma = df_contrato_egograma.loc[contrato_selecao].values.flatten()

        df_contrato_selecionado_egograma = df.groupby('contrato')[egograma_vars].mean()
        contrato_selecionado_egograma = df_contrato_selecionado_egograma.loc[contrato].values.flatten()

        df_area_selecionada_egograma = df.groupby('area')[egograma_vars].mean()
        area_selecionada_egograma = df_area_selecionada_egograma.loc[area].values.flatten()

        plot_egograma(fig2, df_colaborador_egograma.index, df[egograma_vars].mean(), 'Spassu')
        plot_egograma(fig2, df_colaborador_egograma.index, df_colaborador_egograma['valor'], 'Colaborador')
        plot_egograma(fig2, df_colaborador_egograma.index, area_egograma, f'Área {area_selecao}')
        plot_egograma(fig2, df_colaborador_egograma.index, contrato_egograma, f'Contrato {contrato_selecao}')

        if area != area_selecao:
            plot_egograma(fig2, df_colaborador_egograma.index, area_selecionada_egograma, f'Área {area}')

        if contrato != contrato_selecao:
            plot_egograma(fig2, df_colaborador_egograma.index, contrato_selecionado_egograma, f'Contrato {contrato}')

        fig2.update_traces(
            marker=dict(
                line=dict(
                    width=1,
                    color='DarkSlateGrey')),
            selector=dict(mode='markers'),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig2, use_container_width=True)

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
    fig3.update_xaxes(title_text='Zonas de Performance', tickangle=-60, side='top')
    fig3.update_yaxes(title_text='Área de Desempenho')
    fig3.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        yaxis_titlefont_size=16,
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Mapeamento Liderança Dimensões
    st.markdown("### Mapeamento Liderança")

    select_cols = ['LIDERANÇA', 'EQUIPE', 'RELAÇÃO HIERÁRQUICA', 'RESILIÊNCIA - R', 'FOCO EM RESULTADO', 'PROATIVIDADE',
                   'AÇÃO SOB PRESSÃO', 'NEGOCIAÇÃO', 'RESOLUÇÃO DE CONFLITO', 'INOVAÇÃO']
    df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
    if df_map_lider.isnull().values.all():
        st.write("Colaborador não tem dados de Mapeamento de Liderança!")
    else:
        # Define columns
        col_1, col_2 = st.columns([2,3])

        with col_1:
            # Mapeamento Liderança Indicadores
            st.markdown("### Indicadores")

            fig4 = go.Figure()

            select_cols = ['LIDERANÇA', 'EQUIPE', 'RELAÇÃO HIERÁRQUICA', 'RESILIÊNCIA - R', 'FOCO EM RESULTADO', 'PROATIVIDADE',
                           'AÇÃO SOB PRESSÃO', 'NEGOCIAÇÃO', 'RESOLUÇÃO DE CONFLITO', 'INOVAÇÃO']
            df_title = 'MACRO INDICADORES - DIREÇÃO POSITIVA'
            df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
            df_map_lider.columns = ['valor']

            plot_bar(fig4, df_map_lider['valor'], df_map_lider.index, 'Colaborador', 'lightgreen')

            fig4.update_layout(
                title=df_title,
                height=300,
                yaxis_tickfont_size=16,
                xaxis_tickfont_size=16,
                margin=dict(l=20, r=20, t=0, b=0),
            )
            st.plotly_chart(fig4, use_container_width=True)

            fig5 = go.Figure()

            select_cols = ['AUTONOMIA', 'ASSERTIVIDADE', 'FLEXIBILIDADE', 'COMUNICABILIDADE', 'EMPENHO', 'DISCIPLINA',
                           'SEGURANÇA',
                           'AUTENTICIDADE', 'TRANQUILIDADE - T', 'CUIDADO']
            df_title = 'MICRO INDICADORES - DIREÇÃO POSITIVA'
            df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
            df_map_lider.columns = ['valor']
            plot_bar(fig5, df_map_lider['valor'], df_map_lider.index, 'Colaborador', 'lightgreen')

            fig5.update_layout(
                title=df_title,
                height=300,
                yaxis_tickfont_size=16,
                xaxis_tickfont_size=16,
                margin=dict(l=20, r=20, t=0, b=0),
            )
            st.plotly_chart(fig5, use_container_width=True)

            fig6 = go.Figure()

            select_cols = ['PROTELAÇÃO', 'IMEDIATISMO', 'IMPULSIVIDADE - P', 'AGRESSIVIDADE', 'PASSIVIDADE', 'TORMENTO',
                           'DESÂNIMO']
            df_title = 'MICRO INDICADORES - DIREÇÃO NEGATIVA'
            df_map_lider = df[(df['colaborador'] == colaborador)][select_cols].T
            df_map_lider.columns = ['valor']
            plot_bar(fig6, df_map_lider['valor'], df_map_lider.index, 'Colaborador', 'purple')

            fig6.update_layout(
                title=df_title,
                height=250,
                yaxis_tickfont_size=16,
                xaxis_tickfont_size=16,
                margin=dict(l=20, r=20, t=0, b=0),
            )
            st.plotly_chart(fig6, use_container_width=True)

        with col_2:
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
            df_map_lider = df_map_lider.iloc[::-1]
            fig = go.Figure(data=[go.Bar(
                y=df_map_lider.reset_index()[['class', 'index']].T.values,
                x=df_map_lider.valor,
                marker_color=df_map_lider.color,  # marker color can be a single color value or an iterable
                orientation='h'
            )])
            fig.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=color_legend.index[::-1].values,
                    ticktext=color_legend.SIGNIFICADO[::-1].values,
                    type='category',
                    categoryorder='array',
                    categoryarray=color_legend.index[::-1].values,
                    # showgrid=True,
                    # ticks="outside",
                    # tickson="boundaries"
                    ticklen=8
                ),
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis_tickfont_size=16,
                yaxis_tickfont_size=16,
                height=1000
            )
            st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()