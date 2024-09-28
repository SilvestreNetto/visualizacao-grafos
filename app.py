import dash
from dash import dcc, html, Input, Output, State
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import networkx as nx
import base64
import os

# Configuração da aplicação
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

G = nx.Graph()
orientado = False
ponderado = False



# style = [
#     {
#         'selector': 'edge',
#         'style': {
#             'label': 'data(weight)',
#             'line-color': '#B10DC9',
#             'target-arrow-color': '#B10DC9',
#             'target-arrow-shape': 'vee',
#             'curve-style': 'bezier'
#         }
#     }
# ]



app.layout = dbc.Container([
    dbc.Row(
        dbc.Col([
            html.Header(
                children=[
                    html.Div(
                        children=[
                            html.Img(src='/assets/diagram-3-fill.svg', alt='Ícone de Grafo', style={'height': '60px', 'margin-right': '10px'}),
                            html.H1("REPRESENTAÇÃO DE GRAFOS", style={'margin': '0', 'font-size': '2rem'})
                        ],
                        style={
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center'
                        }
                    )
                ],
                style={
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'padding': '20px',
                    'background-color': '#f8f9fa'
                }
            )
        ])
    ),

    #botões centralizados com flexbox
    dbc.Row([
        dbc.Col([
            html.Div(
                dbc.ButtonGroup(
                    [

                        #dropdown para o botão "Grafo" com imagem
                        dbc.DropdownMenu(
                            label=[
                                html.Img(src='/assets/gear.svg', style={'height': '20px', 'margin-right': '5px'}),
                                "Grafo"
                            ],
                            children=[
                                dcc.Upload(
                                    id='upload-data',
                                    children=dbc.DropdownMenuItem([
                                        html.Img(src='/assets/upload.svg', style={'height': '20px', 'margin-right': '5px'}),
                                        "Carregar Grafo"
                                    ]),
                                    style={
                                        'width': '100%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                    },
                                    multiple=False,
                                ),

                                

                                html.Div(id='output-data-upload'),

                                dbc.DropdownMenuItem([
                                    html.Img(src='/assets/save.svg', style={'height': '20px', 'margin-right': '5px'}),
                                    "Baixar Grafo"
                                ], id="salvar-grafo",  n_clicks = 0)

                            ],
                            toggle_style={'margin': '0 10px', 'border-radius': '15px'},
                            style={'margin-right': '10px'}
                        ),
                        
                        # Outros botões
                        dbc.Button([html.Img(src='/assets/plus-lg.svg', style={'height': '20px', 'margin-right': '5px'}), "Adicionar Vértice"], color="success", style={'margin': '0 10px', 'border-radius': '15px'}, id='adicionar_vertice', n_clicks=0),
                        dbc.Input(id='entrada_vertice', type='value', placeholder='Nome do Vértice', style={'margin-right': '5px','width': '200px'}),
                        dbc.Button([html.Img(src='/assets/dash-lg.svg', style={'height': '20px', 'margin-right': '5px'}), "Remover Vértice"], color="danger", style={'margin': '0 10px', 'border-radius': '15px'}, id='remover_vertice', n_clicks=0),
                        dbc.Button([html.Img(src='/assets/arrows-vertical.svg', style={'height': '20px', 'margin-right': '5px'}), "Conectar Vértices"], color="success", style={'margin': '0 10px', 'border-radius': '15px'}, id='adicionar_aresta', n_clicks=0),

                        dbc.Button([html.Img(src='/assets/arrows-vertical.svg', style={'height': '20px', 'margin-right': '5px'}), "Remover Aresta"], color="danger", style={'margin': '0 10px', 'border-radius': '15px'}, id='remover_aresta', n_clicks=0),
                        
        
                    ],
                    style={'display': 'flex', 'justify-content': 'center'}  # Centraliza os botões
                ),
                style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
            )
            
        ]),

    ]),

    dbc.Row([
        dbc.Col([
            html.Div(
                dbc.ButtonGroup(
                    [
                        dbc.Button([html.Img(src='/assets/arrow-down-up.svg', style={'height': '20px', 'margin-right': '5px'}), "Orientado"], color="warning", style={'margin': '0 10px', 'border-radius': '15px'}, id='transformar_orientado', n_clicks=0),
                        dbc.Button([html.Img(src='/assets/arrows.svg', style={'height': '20px', 'margin-right': '5px'}), "Não Orientado"], color="warning", style={'margin': '0 10px', 'border-radius': '15px'}, id='transformar_nao_orientado', n_clicks=0),
                        dbc.Button([html.Img(src='/assets/1-circle-fill.svg', style={'height': '20px', 'margin-right': '5px'}), "Ponderado"], color="info", style={'margin': '0 10px', 'border-radius': '15px'}, id='transformar_ponderado', n_clicks=0),
                        dbc.Button([html.Img(src='/assets/0-circle-fill.svg', style={'height': '20px', 'margin-right': '5px'}), "Não Ponderado"], color="info", style={'margin': '0 10px', 'border-radius': '15px'}, id='transformar_nao_ponderado', n_clicks=0),
                        dbc.Button([html.Img(src='/assets/gear-wide-connected.svg', style={'height': '20px', 'margin-right': '5px'}), "BFS"], color="warning", style={'margin': '0 10px', 'border-radius': '15px'}, id='BFS', n_clicks=0),
                        dbc.Button([html.Img(src='/assets/gear-wide-connected.svg', style={'height': '20px', 'margin-right': '5px'}), "DFS"], color="warning", style={'margin': '0 10px', 'border-radius': '15px'}, id='DFS', n_clicks=0),
                        dbc.Button([html.Img(src='/assets/lightning-charge-fill.svg', style={'height': '20px', 'margin-right': '5px'}), "Atualizar"], color="success", style={'margin': '0 10px', 'border-radius': '15px'}, id='Atualizar', n_clicks=0),
                        dbc.Button([html.Img(src='/assets/lightning-charge-fill.svg', style={'height': '20px', 'margin-right': '5px'}), "Adicionar Peso"], color="success", style={'margin': '0 10px', 'border-radius': '15px'}, id='adicionar_peso', n_clicks=0),
                        dbc.Input(id='entrada_peso', type='value', placeholder='Peso da Aresta', style={'margin-right': '5px','width': '200px'}),
                    ],
                    style={'display': 'flex', 'justify-content': 'center'}
                ),
                style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
            )
        ]),
    ]),


    dbc.Row(
        dbc.Col([
            html.Div(id="grafo-info")
        ], width="auto"),  # Ajusta o tamanho da coluna automaticamente
        justify="left"
    ),

    # Quadro para representação do grafo
    dbc.Row(
        dbc.Col(
            cyto.Cytoscape(
                id='visualizacao_grafo',
                layout={'name': 'cose', 'animate': True},  # Usando o layout "cose" com animação
                style={
                    'width': '100%',
                    'height': '500px',
                    'border': '2px solid black',  # Adicionando a borda ao redor do gráfico
                    'margin-top': '30px'  # Adicionando uma distância entre os botões e a visualização
                },
                elements=[],
                stylesheet = [
                    {
                        'selector': 'node',
                        'style': {
                            'label': 'data(label)',
                            #'background-color': '#0074D9',
                            #'color': 'white',
                            'text-valign': 'center',
                            'text-halign': 'center',
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier'
                        }
                    }
                ],
                minZoom = 1.0,
                maxZoom = 4.0,
            ),
            width={"size": 10, "offset": 1}  # Centraliza o quadro
        )
    ),

], fluid= True)


# def gerar_elementos_cytoscape(G):

#     elements = []

#     # Adiciona nós
#     for node in G.nodes():
#         elements.append({
#             'data': {'id': node, 'label': node},
#             'style': {
#                 'background-color': '#AB9D9D',  # Cor de fundo dos nós
#                 'label': node
#             }
#         })

#     # Adiciona arestas
#     for edge in G.edges(data=True):
#         source, target, data = edge
#         label = data.get('weight', '')
#         edge_data = {
#             'style': {
#                 'label': 'data(weight)',
#                 'line-color': '#B10DC9',
#                 'target-arrow-color': '#B10DC9',
#                 'target-arrow-shape': 'vee',
#                 'line-color': '#252525'  # Cor das arestas
#             }
#         }
#         if 'weight' in data and data['weight'] is not None:
#             edge_data['data']['weight'] = data['weight']
#             edge_data['style']['width'] = 4 

#         elements.append(edge_data)

def salvar_grafo_txt(grafo, orientado=False):
    """Função para salvar o grafo no formato .txt"""
    linhas = []
    for u, v, data in grafo.edges(data=True):
        if orientado:
            linhas.append(f"{u}, {v}")
        else:
            if (v, u) not in grafo.edges():  # Evitar duplicatas em grafos não orientados
                linhas.append(f"{u}, {v}")
    
    conteudo = "\n".join(linhas)
    
    # Nome do arquivo
    nome_arquivo = "grafo.txt"
    
    # Criar um link para download
    return dcc.send_file(
        content=conteudo,
        filename=nome_arquivo,
        type="text/plain"
    )

def gerar_elementos_cytoscape(G):
    elements = []

    # Adicionar os nós
    for node in G.nodes():
        elements.append({
            'selector': f'node[id="{node}"]',
            'data': {'id': str(node), 'label': str(node)},
            'classes': 'node',
            'style': {
                #'background-color': '#0074D9',
                'border-width': '1.0px',
                'border-color': '#252525'
            }
        })

    # Adicionar as arestas
    for edge in G.edges(data=True):
        source, target, data = edge
        label = data.get('weight', '')

        elements.append({
            'selector': f'edge[source="{source}"][target="{target}"]',
            'data': {
                'source': str(source),
                'target': str(target),
                'label': str(label) if label else ''
            },
            'classes': 'edge',
            'style': {
                'width': '2.8px',
                'target-arrow-color': '#252525',
                #'line-color': '#252525',
                'target-arrow-shape': 'triangle' if nx.is_directed(G) else 'none',
                'arrow-scale': 1.3,
                'label': str(label) if label else '',
                'text-background-color': '#ffffff',
                'text-background-opacity': 0.5,
                'text-background-shape': 'round-rectangle',
            }
        })
    return elements


import networkx as nx

def carregar_grafo_txt(filename):

    G = nx.Graph()  # Inicializa um grafo não direcionado (default)
    ponderado = False
    orientado = False
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 2:
                u, v = parts
                G.add_edge(u.strip(), v.strip())
            elif len(parts) == 3:
                u, v, peso = parts
                G.add_edge(u.strip(), v.strip(), weight=float(peso.strip()))
                ponderado = True
    
    if any(G.has_edge(u, v) and G.has_edge(v, u) for u, v in G.edges()):
        G = nx.DiGraph(G)  
        orientado = True

    return G, ponderado, orientado



@app.callback(
    [Output('visualizacao_grafo', 'elements'),
     Output('grafo-info', 'children')],
    [Input('upload-data', 'contents'),
     Input('salvar-grafo', 'n_clicks'),
     Input('adicionar_vertice', 'n_clicks'),
     Input('adicionar_aresta', 'n_clicks'),
     Input('remover_vertice', 'n_clicks'),
     Input('remover_aresta', 'n_clicks'),
     Input('transformar_orientado', 'n_clicks'),
     Input('transformar_nao_orientado', 'n_clicks'),
     Input('adicionar_peso', 'n_clicks'),
     Input('transformar_ponderado', 'n_clicks'),
     Input('transformar_nao_ponderado', 'n_clicks'),
     Input('BFS', 'n_clicks'),
     Input('DFS', 'n_clicks'),
     Input('Atualizar', 'n_clicks'),
     Input('visualizacao_grafo', 'selectedNodeData'),
     Input('visualizacao_grafo', 'selectedEdgeData')],
    [State('upload-data', 'filename'),
     State('entrada_vertice', 'value'),
     State('entrada_peso', 'value'),
     State('visualizacao_grafo', 'elements')]
)


def update_graph(contents, salvar_grafo_clicks, add_node_clicks, add_edge_clicks, remove_node_clicks, remove_edge_clicks, refresh_button,
                to_directed_clicks, to_undirected_clicks, add_weight_clicks, bfs_clicks, btn_make_weighted_clicks, 
                btn_make_unweighted_clicks, dfs_clicks, selected_nodes, selected_edges, filename, add_node, add_edge_weight, elements):
    
    global G, ponderado, orientado
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return gerar_elementos_cytoscape(G), [html.P("Nenhum grafo carregado.")]
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    try:
        if button_id == 'upload-data' and contents is not None:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string).decode('utf-8')
            
            temp_filename = 'temp_graph.txt'
            with open(temp_filename, 'w') as temp_file:
                temp_file.write(decoded)
            
            G, ponderado, orientado = carregar_grafo_txt(temp_filename)
            os.remove(temp_filename)
            elements = gerar_elementos_cytoscape(G)

        elif button_id == 'salvar-grafo':
            # Transformar os elementos do grafo para o formato NetworkX
            G = nx.Graph()
            for edge in elements:
                if 'source' in edge['data'] and 'target' in edge['data']:
                    G.add_edge(edge['data']['source'], edge['data']['target'])

            # Verificar se o grafo é orientado ou não, e salvar como txt
            return elements, salvar_grafo_txt(G, G.is_directed())
        
        elif button_id == 'adicionar_vertice':
            # Verifica se o input não está vazio e se o vértice não existe
            if add_node and add_node not in G.nodes():
                G.add_node(add_node)
                elements = gerar_elementos_cytoscape(G)
            else:
                # Retorna uma mensagem de erro se o input estiver vazio ou o vértice já existir
                return elements, html.P(f"Erro: Vértice '{add_node}' já existe ou o campo está vazio.")
        
        elif button_id == 'remover_vertice':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")

            if selected_nodes:
                for node_data in selected_nodes:
                    remover_vertice(G, node_data['id'])
                elements = gerar_elementos_cytoscape(G)
            else:
                return elements, html.P("Nenhum vértice selecionado.")

        elif button_id == 'adicionar_aresta':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")
            
            if len(selected_nodes) == 1:
                # Caso o mesmo nó seja clicado duas vezes, force a criação do auto-loop
                source = selected_nodes[0]['id']
                target = source  # Auto-loop (source == target)
                
                if not G.has_edge(source, target):
                    G.add_edge(source, target)
                elements = gerar_elementos_cytoscape(G)

            elif len(selected_nodes) == 2:
                source = selected_nodes[0]['id']
                target = selected_nodes[1]['id']
                
                # Adiciona a aresta normalmente, seja entre dois nós diferentes ou iguais
                if not G.has_edge(source, target):
                    G.add_edge(source, target)
                elements = gerar_elementos_cytoscape(G)
            else:
                return elements, html.P("Selecione um (auto-loop) ou dois vértices para adicionar uma aresta.")

        elif button_id == 'remover_aresta':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")

            if selected_edges:
                for edge_data in selected_edges:
                    remover_aresta(G, edge_data['source'], edge_data['target'])
                elements = gerar_elementos_cytoscape(G)
            else:
                return elements, html.P("Nenhuma aresta selecionada.")

        elif button_id == 'adicionar_peso':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.") 

            if selected_edges and add_edge_weight is not None:
                weight = float(add_edge_weight)
                if not ponderado:
                    ponderado = True
                    for edge in G.edges():
                        G[edge[0]][edge[1]]['weight'] = 1.0
                for edge_data in selected_edges:
                    G[edge_data['source']][edge_data['target']]['weight'] = weight
                elements = gerar_elementos_cytoscape(G)
            else:
                return elements, html.P("Nenhuma aresta selecionada ou peso não fornecido.")

        elif button_id == 'BFS':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")

            if selected_nodes is None or len(selected_nodes) != 1:
                return elements, html.P("Selecione exatamente um nó para iniciar a busca BFS.")
            
            start_node = selected_nodes[0]['id']
            bfs_result = list(nx.bfs_edges(G, source=start_node))
            bfs_nodes = set([start_node] + [node for edge in bfs_result for node in edge])  # Coleta todos os nós visitados
            elements = gerar_elementos_cytoscape(G)
            
            # Reset color for all edges and nodes
            for element in elements:
                if 'data' in element:
                    if 'source' in element['data'] and 'target' in element['data']:
                        element['style'] = element.get('style', {})
                        element['style']['line-color'] = '#252525'  # Cor padrão
                    elif 'id' in element['data']:  # Assumindo que a identificação do nó está em 'id'
                        element['style'] = element.get('style', {})
                        element['style']['background-color'] = '#FFFFFF'  # Cor padrão para nós
            
            
            # Destaque o caminho percorrido e os nós visitados
            for u, v in bfs_result:
                for edge in elements:
                    if 'data' in edge and 'source' in edge['data'] and 'target' in edge['data']:
                        if edge['data']['source'] == u and edge['data']['target'] == v:
                            edge['style'] = edge.get('style', {})
                            edge['style']['line-color'] = 'red'  # Cor para destacar o caminho BFS
            
            adjacency_list = [
                html.P(
                    children=[
                        html.B(sorted(node)),  # Vértice em negrito
                        " -> ",
                        ', '.join(map(str, sorted(neighbors)))  # Ordena os vizinhos em ordem crescente
                    ],
                    style={'margin': '0', 'padding': '0'}  # Remove margens e espaçamentos
                ) for node, neighbors in nx.to_dict_of_lists(G).items()
            ]

            info = [
                html.P(f"Número de Vértices: ", style={'display': 'inline'}),
                html.B(f"{len(G.nodes)}", style={'display': 'inline'}),
                html.Br(),
                html.P(f"Número de Arestas: ", style={'display': 'inline'}),
                html.B(f"{len(G.edges)}", style={'display': 'inline'}),
                html.Br(),
                html.P(f"Ponderado: ", style={'display': 'inline'}),
                html.B(f"{'Sim' if ponderado else 'Não'}", style={'display': 'inline'}),
                html.Br(),
                html.P(f"Orientado: ", style={'display': 'inline'}),
                html.B(f"{'Sim' if orientado else 'Não'}", style={'display': 'inline'}),
                html.Br(),
                html.Br(),
                html.P(f"Lista de Adjacência: "),
                *adjacency_list,  # Exibindo a lista de adjacência formatada
                html.Br(),
                html.P(f"Resultado BFS a partir do nó: ", style={'display': 'inline'}),
                html.B(f"'{start_node}': {bfs_result}", style={'display': 'inline'}),
            ] 
            return elements, info

        elif button_id == 'DFS':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")

            if selected_nodes is None or len(selected_nodes) != 1:
                return elements, html.P("Selecione exatamente um nó para iniciar a busca DFS.")
            
            start_node = selected_nodes[0]['id']
            dfs_result = list(nx.dfs_edges(G, source=start_node))
            dfs_nodes = set([start_node] + [node for edge in dfs_result for node in edge])  # Coleta todos os nós visitados
            elements = gerar_elementos_cytoscape(G)
            
            # Reset color for all edges and nodes
            for element in elements:
                if 'data' in element:
                    if 'source' in element['data'] and 'target' in element['data']:
                        element['style'] = element.get('style', {})
                        element['style']['line-color'] = '#252525'  # Cor padrão
                    elif 'id' in element['data']:  # Assumindo que a identificação do nó está em 'id'
                        element['style'] = element.get('style', {})
                        element['style']['background-color'] = '#FFFFFF'  # Cor padrão para nós
            
            # Destaque o caminho percorrido e os nós visitados
            for u, v in dfs_result:
                for edge in elements:
                    if 'data' in edge and 'source' in edge['data'] and 'target' in edge['data']:
                        if edge['data']['source'] == u and edge['data']['target'] == v:
                            edge['style'] = edge.get('style', {})
                            edge['style']['line-color'] = 'blue'  # Cor para destacar o caminho DFS

            adjacency_list = [
                html.P(
                    children=[
                        html.B(sorted(node)),  # Vértice em negrito
                        " -> ",
                        ', '.join(map(str, sorted(neighbors)))  # Ordena os vizinhos em ordem crescente
                    ],
                    style={'margin': '0', 'padding': '0'}  # Remove margens e espaçamentos
                ) for node, neighbors in nx.to_dict_of_lists(G).items()
            ]

            info = dbc.Col([
                html.P(f"Número de Vértices: ", style={'display': 'inline'}),
                html.B(f"{len(G.nodes)}", style={'display': 'inline'}),
                html.Br(),
                html.P(f"Número de Arestas: ", style={'display': 'inline'}),
                html.B(f"{len(G.edges)}", style={'display': 'inline'}),
                html.Br(),
                html.P(f"Ponderado: ", style={'display': 'inline'}),
                html.B(f"{'Sim' if ponderado else 'Não'}", style={'display': 'inline'}),
                html.Br(),
                html.P(f"Orientado: ", style={'display': 'inline'}),
                html.B(f"{'Sim' if orientado else 'Não'}", style={'display': 'inline'}),
                html.Br(),
                html.Br(),
                html.P(f"Lista de Adjacência: "),
                *adjacency_list,  # Exibindo a lista de adjacência formatada
                html.Br(),
                html.P(f"Resultado DFS a partir do nó: ", style={'display': 'inline'}),
                html.B(f"'{start_node}': {dfs_result}", style={'display': 'inline'}),
            ], style={'text-align': 'left'})  # Alinha o texto à esquerda 
            
            return elements, info

        elif button_id == 'transformar_orientado':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")

            if len(G.edges) <= 0:
                return elements, html.P("Número de arestas insuficiente para converter.")

            if G.is_directed():
                return elements, html.P("O grafo já é orientado.")
            
            G_dir = nx.DiGraph()
            for u, v, data in G.edges(data=True):
                G_dir.add_edge(u, v, **data)  # Mantém a direção das arestas conforme a entrada original
            
            G = G_dir
            orientado = True
            elements = gerar_elementos_cytoscape(G)

        elif button_id == 'transformar_nao_orientado':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")

            if G.is_directed():
                G = nx.Graph(G)  
                orientado = False
                elements = gerar_elementos_cytoscape(G)
            else:
                return elements, html.P("O grafo já é não-orientado.")

        elif button_id == 'transformar_ponderado':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")

            if ponderado == True:
                return elements, html.P("O grafo já é ponderado.")

            for u, v in G.edges():
                G[u][v]['weight'] = G[u][v].get('weight', 1.0)
            ponderado = True
            elements = gerar_elementos_cytoscape(G)

        elif button_id == 'transformar_nao_ponderado':

            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")

            if ponderado == False:
                return elements, html.P("O grafo já é não-ponderado.")

            for u, v in G.edges():
                G[u][v].pop('weight', None)  # Remove o atributo 'weight' se existir
            ponderado = False
            elements = gerar_elementos_cytoscape(G)

        elif button_id == 'Atualizar':
            if G.number_of_nodes() == 0:
                return elements, html.P("Nenhum grafo carregado.")
    
            elements = gerar_elementos_cytoscape(G)

        adjacency_list = [
            html.P(
                children=[
                    html.B(sorted(node)),  # Vértice em negrito
                    " -> ",
                    ', '.join(map(str, sorted(neighbors)))  # Ordena os vizinhos em ordem crescente
                ],
                style={'margin': '0', 'padding': '0'}  # Remove margens e espaçamentos
            ) for node, neighbors in nx.to_dict_of_lists(G).items()
        ]

        info = [
            html.P(f"Número de Vértices: ", style={'display': 'inline'}),
            html.B(f"{len(G.nodes)}", style={'display': 'inline'}),
            html.Br(),
            html.P(f"Número de Arestas: ", style={'display': 'inline'}),
            html.B(f"{len(G.edges)}", style={'display': 'inline'}),
            html.Br(),
            html.P(f"Ponderado: ", style={'display': 'inline'}),
            html.B(f"{'Sim' if ponderado else 'Não'}", style={'display': 'inline'}),
            html.Br(),
            html.P(f"Orientado: ", style={'display': 'inline'}),
            html.B(f"{'Sim' if orientado else 'Não'}", style={'display': 'inline'}),
            html.Br(),
            html.Br(),
            html.P(f"Lista de Adjacência: "),
            *adjacency_list,  # Exibindo a lista de adjacência formatada
        ]
        
        return elements, info
    
    except Exception as e:
        return elements, html.P(f"Erro: {str(e)}")




if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
