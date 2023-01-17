import dash
from dash import html,Output,Input,State,dcc,ctx
import dash_bootstrap_components as dbc
import pandas as pd
import time
import datetime

from Joueur import Joueur
from Game import Game

external_stylesheets=[dbc.themes.SPACELAB]

df = pd.read_csv('Defis.csv',sep=';')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
#%% WPA
app.index_string = '''<!DOCTYPE html>
<html>
<head>
<title>My Game</title>
<link rel="manifest" href="/.../assets/manifest.json" />
{%metas%}
{%favicon%}
{%css%}
</head>
<script type="module">
   import 'https://cdn.jsdelivr.net/npm/@pwabuilder/pwaupdate';
   const el = document.createElement('pwa-update');
   document.body.appendChild(el);
</script>
<body>
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', ()=> {
      navigator
      .serviceWorker
      .register('/.../assets/sw01.js')
      .then(()=>console.log("Ready."))
      .catch(()=>console.log("Err..."));
    });
  }
</script>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''

server = app.server

@app.callback(
    Output('output', 'children'),
    [Input('reset-button', 'n_clicks')],
    [State('output', 'children')]
)
def reset_output(n_clicks, children):
    if dash.callback_context.triggered[0]['prop_id'] == 'reset-button.n_clicks':
        # Reset all necessary variables here
        global joueurs
        joueurs = []
        global variable2
        variable2 = []
        # Reset all necessary callbacks here
        dash.callback_context.reset()
        return 'Reset successful'
    return children

#%% Header

Menu = html.Div(
    [
        html.H3('My Game',style={'textAlign': 'center'})
        ],    
    className="my-3",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            Menu,
        ]
    ),
    color='#111111',#"dark",
    dark=True,
)

space = '''
###

'''

#%% Choix du temps d'un tour

time_txt = html.Div(
    [
        dcc.Markdown(children="Temps d'un tour (en minutes)\n\n"),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

time_dropdown = html.Div([
    html.Div([dcc.Dropdown(['60', '45', '30'], '60', id='time-dropdown')],className="d-grid gap-2 col-4 mx-auto"),
])

@app.callback(
    Output('output-dropdown', 'children'),
    [Input('time-dropdown','value')], 
)
def update_output(value):
    str = f"\n\nUn Defi sera lancé toutes les {value} minutes.\n"
    return str,


#%% Choix du nombre de joueurs

n_joueurs_txt = html.Div(
    [
        dcc.Markdown(children="Choix du nombre de joueurs\n\n"),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

n_joueurs_dropdown = html.Div([
    html.Div([dcc.Dropdown([i for i in range(20)], 3, id='nj-dropdown')],className="d-grid gap-2 col-4 mx-auto"),
])

@app.callback(
    Output('output-njdropdown','children'),
    [Input('game-rules','n_clicks')], 
    [State('nj-dropdown', 'value')]

)
def update_output(n_clicks,value):
    if n_clicks is not None:
        #global nb_joueurs
        nb_joueurs = value
        return f"\n\nLa partie comprend {nb_joueurs} joueurs.\n"


#%% Initialisation des joueurs

joueur_txt = html.Div(
    [
        dcc.Markdown(children='\n\nEntrez le nom des Joueurs :'),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

global joueurs 
joueurs = []
    
# Show the list of the players
list_joueurs = html.Div(
    [
        dcc.Markdown(id = 'output-joueur'),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

# Add player
button_add = html.Div(
    [
        dbc.Button("Add",id = 'add',type = 'submit',color="success"),
    ],
    style={ 'marginTop': 25, 'marginLeft': 485, 'width' : '15vh'},
    className="d-grid",
)

# Remove player 
button_drop = html.Div(
    [
        dbc.Button("Drop",id = 'drop',type = 'submit',color="danger"),
    ],
    style={ 'marginTop': 25, 'marginLeft': 235, 'width' : '15vh'},
    className="d-grid",
)

joueur_input = html.Div(
    [
        dcc.Input(id="joueur-input", type="text", value = '',placeholder=""),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

#Fonction qui permet de supprimer et ajouter des joueurs
@app.callback(
    Output('output-joueur',"children"),
    [Input('drop','n_clicks'),Input('add','n_clicks')],
    [State("joueur-input", "value"),
    State('nj-dropdown', 'value')]
)
def update_output2(click_drop,click_add,nom,nj):
    if click_add is not None:
        if len(joueurs) < nj:
            joueurs.append(Joueur(nom,0,0,any,any))
    
    #Problem dans remove
    elif click_drop is not None:
        for j in joueurs:
            if j.nom == nom:
                joueurs.remove(j)

    #Show the players and their number
    str_joueurs = ''
    numero = 1
    for j in joueurs:
        j.numero = numero
        str_joueurs = str_joueurs +'\n - Joueur '+str(numero)+' : '+j.nom
        numero+=1

    return str_joueurs

#%% Regles

rules_button = html.Div(
    [
        dbc.Button("Show Final Rules",id = 'game-rules',type = 'submit',color="primary"),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

rules = html.Div(
    [
        dcc.Markdown(id='output-dropdown'),
        dcc.Markdown(id='output-njdropdown'),
        dcc.Markdown(id='output-regles'),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

#Fonction qui affiche les regles
@app.callback(
    Output('output-regles',"children"),
    [Input('game-rules','n_clicks')], 
)
def update_output(clicks):
    if clicks is not None:
        str_joueurs = ''
        for j in joueurs:
            str_joueurs = str_joueurs +'\n - Joueur '+str(j.numero)+' : '+j.nom
        return f'Chaque joueur recevra un defi à réaliser pendant le temps imparti.\n\nLes joueurs sont :\n {str_joueurs}'


#%% Start Game

popup_bouton = html.Div(
    [
        dbc.Button("Start", id="open-game"),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

global nb_joueurs
nb_joueurs = 3

@app.callback(
    Output("popup", "is_open"),
    [Input("open-game", "n_clicks")],
    State("popup", "is_open"),
)
def toggle_modal(n, is_open): 
    if n:
        return not is_open
    else : 
        global start_time
        start_time = datetime.datetime.now()
        nb_joueurs = len(joueurs)
        #game.append(Game(df,joueurs,len(joueurs),start_time,0))

        #game.defi_list = df
        #game.joueur_list = joueurs
        #game.n_joueurs = len(joueurs)
        #game.start_time = start_time

        return is_open


#%% Timer 

#timer popup bouton
timer_popup_bouton = html.Div(
    [
        dbc.Button("See Timer", id="open-timer"),
    ],
    style={ 'marginTop': 15, 'marginLeft': 1300},
)

@app.callback(
    Output("time-popup", "is_open"),
    [Input("open-timer", "n_clicks")],
    State("time-popup", "is_open"),
)
def toggle_modal(n, is_open=False): 
    if n:
        return not is_open
    else : return is_open

#timer popup
timer_popup = html.Div(
    [   
        dbc.Modal(
        [
            html.Div(dbc.ModalHeader(dbc.ModalTitle("Timer")),style={'width':'75%', 'margin':25, 'textAlign': 'center'}),
            dcc.Interval(id='interval', interval= 1000, n_intervals=0),
            html.Div([html.H1(id='timer', children='')],style={'width':'75%', 'margin':25, 'textAlign': 'center'}),
        ],
        id="time-popup",
        size="sm",
        style={'top': 0,'left': 550},
        is_open = True
        )
    ]
)

#timer
@app.callback(Output('timer', 'children'),
    Input('interval', 'n_intervals'),
    State('time-dropdown','value')
)
def update_interval(n,game_time):
    game_time = int(game_time)
    time_now = datetime.datetime.now()
    hours = 0
    while game_time >= 60 :
        game_time = game_time - 60
        hours+=1
    time_delta = datetime.timedelta(hours=hours, minutes=game_time)
    final_time = start_time + time_delta
    countdown = final_time - time_now   
    h,rem = divmod(countdown.seconds, 3600)
    mins, secs = divmod(rem, 60)
    return '{:02d}:{:02d}'.format(mins, secs)

#%% Defis


defi_bouton = html.Div([
    html.Div([
        *[dbc.Button(f"Joueur  {i} : ", id=f"button_{i}") for i in range(1,nb_joueurs+1)],
        *[dbc.Modal(id=f"modal_{i}", children=[
            html.H2(f"Joueur  {i} : ",className="d-grid gap-2 col-4 mx-auto"),
            html.Div(id=f"output_{i}",className="d-grid gap-2 col-8 mx-auto")],
            size="lg", backdrop= True,is_open=False,className="d-grid gap-2 col-3 mx-auto",
            centered=True,style={'white-space': 'pre','text-align':'center','font-weight': 'bold'}) for i in range(1,nb_joueurs+1)],
    ],className="d-grid gap-2 col-3 mx-auto")
])

@app.callback(
    [Output(f"output_{i}", "children") for i in range(1,nb_joueurs+1)],
    [Input(f"button_{i}", "n_clicks") for i in range(1,nb_joueurs+1)],
)
def update_output(*args):
    outputs = []
    for i, clicks in enumerate(args):
        if clicks:
            defi = df.sample(n=1).reset_index(drop = True)
            defi_text = f"\nTon Defi :\n\n {str(defi['defi'][0])}\n\nLe defi vaut {str(defi['pts'][0])} points.\n\nBonne chance champion.\n\n"

            outputs.append(defi_text)
        else:
            outputs.append(f"Bouton non cliqué")
    return outputs

for i in range(1, 11):
    @app.callback(
        Output(f"modal_{i}", "is_open"),
        [Input(f"button_{i}", "n_clicks")],
        [State(f"modal_{i}", "is_open")],
    )
    def toggle_modal(n, is_open):
        if n:
            return not is_open
        else:
            return is_open


#%% Popup Layout

@app.callback(
    Output('output-njoueurs',"children"),
    [Input('popup','is_open')], 
)
def update_output(is_open):
    if is_open:
        str_joueurs = 'Chaque joueur doit accomplir le defi lui etant associé.\nVous decouvrirez votre défi en cliquant sur le bouton associé à votre numéro de joueur.\n'
        for j in joueurs:
            str_joueurs = str_joueurs +'\n - Joueur '+str(j.numero)+' : '+j.nom
        return str_joueurs


popup = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Your Turn")),
                timer_popup_bouton,
                timer_popup,

                #ameliorer layout des joueurs
                html.Div(id = 'output-njoueurs',style={'white-space': 'pre','text-align':'center','font-weight': 'bold'},
                className="d-grid gap-2 col-6 mx-auto"),

                dcc.Markdown(children=space),
                dcc.Markdown(children=space),
                defi_bouton,
            ],
            id="popup",
            fullscreen= True,
            is_open = False,
        ),
    ]
)


"""
#%% Layout

app.layout =  dbc.Container([
    dbc.Row(
    html.Div([
    html.Button('Parametre de jeu', id='bouton1'),
    html.Button('Commencer la partie', id='bouton2'),
    html.Div(id='layout',className="d-grid gap-2 col-4 mx-auto"),
],className="d-grid gap-2 col-4 mx-auto"))], fluid=True)


@app.callback(
    Output('layout','children'),
    [Input('bouton1','n_clicks'),
    Input('bouton2','n_clicks')]
)
def layout_creation(n1,n2):

    #%% Header

    Menu = html.Div(
        [
            html.H3('My Game',style={'textAlign': 'center'})
            ],    
        className="my-3",
    )

    navbar = dbc.Navbar(
        dbc.Container(
            [
                Menu,
            ]
        ),
        color='#111111',#"dark",
        dark=True,
    )

    space = '''
    ###

    '''

    #%% Choix du temps d'un tour
    time_txt = html.Div(
            [
                dcc.Markdown(children="Temps d'un tour\n\n"),
            ],
            className="d-grid gap-2 col-4 mx-auto",
        )

    time_dropdown = html.Div([
        html.Div([dcc.Dropdown(['60 min', '45 min', '30 min'], '60 min', id='time-dropdown')],className="d-grid gap-2 col-4 mx-auto"),
    ])

    @app.callback(
        Output('output-dropdown', 'children'),
        [Input('game-rules','n_clicks')], 
        State('time-dropdown', 'value')
    )
    def update_output(n_clicks,value):
        if n_clicks is not None:
            global game_time
            game_time = int([int(integer)for integer in value.split() if integer.isdigit()][0])
            return f"\n\nUn Defi sera lancé toutes les {game_time} minutes.\n"
    #%% Initialisation des joueurs

    joueur_txt = html.Div(
        [
            dcc.Markdown(children='\n\nEntrez le nom des Joueurs :'),
        ],
        className="d-grid gap-2 col-4 mx-auto",
    )

    global joueurs 
    joueurs = []
        
    # Show the list of the players
    list_joueurs = html.Div(
        [
            dcc.Markdown(id = 'output-joueur'),
        ],
        className="d-grid gap-2 col-4 mx-auto",
    )

    # Add player
    button_add = html.Div(
        [
            dbc.Button("Add",id = 'add',type = 'submit',color="success"),
        ],
        style={ 'marginTop': 25, 'marginLeft': 485, 'width' : '15vh'},
        className="d-grid",
    )

    # Remove player 
    button_drop = html.Div(
        [
            dbc.Button("Drop",id = 'drop',type = 'submit',color="danger"),
        ],
        style={ 'marginTop': 25, 'marginLeft': 235, 'width' : '15vh'},
        className="d-grid",
    )

    joueur_input = html.Div(
        [
            dcc.Input(id="joueur-input", type="text", value = '',placeholder=""),
        ],
        className="d-grid gap-2 col-4 mx-auto",
    )

    #Fonction qui permet de supprimer et ajouter des joueurs
    @app.callback(
        Output('output-joueur',"children"),
        [Input('drop','n_clicks'),Input('add','n_clicks')],
        [State("joueur-input", "value")]
    )
    def update_output2(click_drop,click_add,nom):
        if click_add is not None:
            joueurs.append(Joueur(nom,0,0,any,any))
        
        #Problem dans remove
        elif click_drop is not None:
            for j in joueurs:
                if j.nom == nom:
                    joueurs.remove(j)

        #Show the players and their number
        str_joueurs = ''
        numero = 1
        for j in joueurs:
            j.numero = numero
            str_joueurs = str_joueurs +'\n - Joueur '+str(numero)+' : '+j.nom
            numero+=1

        return str_joueurs

    #%% Regles

    rules_button = html.Div(
        [
            dbc.Button("Show Final Rules",id = 'game-rules',type = 'submit',color="primary"),
        ],
        className="d-grid gap-2 col-4 mx-auto",
    )
    
    nb_joueurs = len(joueurs)

    rules = html.Div(
        [
            dcc.Markdown(id='output-dropdown'),
            #dcc.Markdown(id='output-njdropdown'),
            dcc.Markdown(id='output-regles'),
            #html.Div(id='output-dropdown')
        ],
        className="d-grid gap-2 col-4 mx-auto",
    )

    #Fonction qui affiche les regles
    @app.callback(
        Output('output-regles',"children"),
        [Input('game-rules','n_clicks')], 
    )
    def update_output(clicks):
        if clicks is not None:
            str_joueurs = ''
            for j in joueurs:
                str_joueurs = str_joueurs +'\n - Joueur '+str(j.numero)+' : '+j.nom
            return f'Chaque joueur recevra un defi à réaliser pendant le temps imparti.\n\nLes joueurs sont :\n {str_joueurs}'


    #%% Bouton 1
    if n1 : 
        #%% Parameter Layout

        layout= dbc.Container([
            dbc.Row( 
                [
                # Header
                navbar,
                dcc.Markdown(children=space),

                # Choix du temps d'un tour
                time_txt,
                time_dropdown,
                dcc.Markdown(children=space),
                dcc.Markdown(children=space),

                # Choix du nombre de joueurs
                #n_joueurs_txt,
                #n_joueurs_dropdown,
                dcc.Markdown(children=space),
                dcc.Markdown(children=space),

                # Initialisation des joueurs
                joueur_txt,
                dcc.Markdown(children=space),
                joueur_input,
                dcc.Markdown(children=space),
                button_add,
                button_drop,
                dcc.Markdown(children=space),
                dcc.Markdown(children=space),
                list_joueurs,
                dcc.Markdown(children=space),
                dcc.Markdown(children=space),

                # Regles
                rules_button,
                dcc.Markdown(children=space),
                rules,
                dcc.Markdown(children=space),

                ],
            )], fluid=True)

        return layout
    #%% Bouton 2
    if n2 :
        @app.callback(
            Output("time", "value"),
            [Input("open-game", "n_clicks")],
        )
        def toggle_modal(n): 
            if not n:
                global start_time
                start_time = datetime.datetime.now()

                return start_time
        #%% Timer 

        #timer popup bouton
        timer_popup_bouton = html.Div(
            [
                dbc.Button("See Timer", id="open-timer"),
            ],
            style={ 'marginTop': 15, 'marginLeft': 1300},
        )

        @app.callback(
            Output("time-popup", "is_open"),
            [Input("open-timer", "n_clicks")],
            State("time-popup", "is_open"),
        )
        def toggle_modal(n, is_open=False): 
            if n:
                return not is_open
            else : return is_open

        #timer popup
        timer_popup = html.Div(
            [   
                dbc.Modal(
                [
                    html.Div(dbc.ModalHeader(dbc.ModalTitle("Timer")),style={'width':'75%', 'margin':25, 'textAlign': 'center'}),
                    dcc.Interval(id='interval', interval= 1000, n_intervals=0),
                    html.Div([html.H1(id='timer', children='')],style={'width':'75%', 'margin':25, 'textAlign': 'center'}),
                ],
                id="time-popup",
                size="sm",
                style={'top': 0,'left': 550},
                is_open = True
                )
            ]
        )

        #timer
        @app.callback(Output('timer', 'children'),
            [Input('interval', 'n_intervals')]
        )
        def update_interval(n):
            time_now = datetime.datetime.now()
            time_delta = datetime.timedelta(hours=0, minutes=game_time)
            final_time = start_time + time_delta
            countdown = final_time - time_now   
            h,rem = divmod(countdown.seconds, 3600)
            mins, secs = divmod(rem, 60)
            return '{:02d}:{:02d}'.format(mins, secs)

        #%% Defis


        defi_bouton = html.Div([
            html.Div([
                *[dbc.Button(f"Joueur  {i} : ", id=f"button_{i}") for i in range(nb_joueurs)],
                *[dbc.Modal(id=f"modal_{i}", children=[
                    html.H2(f"Joueur  {i} : ",className="d-grid gap-2 col-4 mx-auto"),
                    html.Div(id=f"output_{i}",className="d-grid gap-2 col-8 mx-auto")],
                    size="lg", backdrop= True,is_open=False,className="d-grid gap-2 col-3 mx-auto",
                    centered=True,style={'white-space': 'pre','text-align':'center','font-weight': 'bold'}) for i in range(nb_joueurs)],
            ],className="d-grid gap-2 col-3 mx-auto")
        ])

        @app.callback(
            [Output(f"output_{i}", "children") for i in range(nb_joueurs)],
            [Input(f"button_{i}", "n_clicks") for i in range(nb_joueurs)],
        )
        def update_output(*args,nb_joueurs):
            outputs = []
            for i, clicks in enumerate(args):
                if clicks:
                    defi = df.sample(n=1).reset_index(drop = True)
                    defi_text = f"\nTon Defi :\n\n {str(defi['defi'][0])}\n\nLe defi vaut {str(defi['pts'][0])} points.\n\nBonne chance champion.\n\n"

                    outputs.append(defi_text)
                else:
                    outputs.append(f"Bouton non cliqué")
            return outputs

        for i in range(1, 11):
            @app.callback(
                Output(f"modal_{i}", "is_open"),
                [Input(f"button_{i}", "n_clicks")],
                [State(f"modal_{i}", "is_open")],
            )
            def toggle_modal(n, is_open):
                if n:
                    return not is_open
                else:
                    return is_open


        #%% Game Layout

        @app.callback(
            Output('output-njoueurs',"children"),
            [Input('popup','is_open')], 
        )
        def update_output(is_open):
            if is_open:
                str_joueurs = 'Chaque joueur doit accomplir le defi lui etant associé.\nVous decouvrirez votre défi en cliquant sur le bouton associé à votre numéro de joueur.\n'
                for j in joueurs:
                    str_joueurs = str_joueurs +'\n - Joueur '+str(j.numero)+' : '+j.nom
                return str_joueurs


        popup = html.Div(
            [
 
                        html.Header(html.Title("Your Turn")),
                        timer_popup_bouton,
                        timer_popup,

                        #ameliorer layout des joueurs
                        html.Div(id = 'output-njoueurs',style={'white-space': 'pre','text-align':'center','font-weight': 'bold'},
                        className="d-grid gap-2 col-6 mx-auto"),

                        dcc.Markdown(children=space),
                        dcc.Markdown(children=space),
                        defi_bouton,
            ]
        )

        return popup
        #%% Else
    else :
        return html.Div(["Clicker sur 'Parametre de jeu' pour commencer à parametrer la partie."])
"""

#%% Main & Layout

app.layout= dbc.Container([
            dbc.Row( 
                [
                # Header
                navbar,
                dcc.Markdown(children=space),

                html.Div([
    html.Button('Reset', id='reset-button'),
    html.Div(id='output'),
]),

                # Choix du temps d'un tour
                time_txt,
                #dcc.Input(id='output-time', type='hidden'),
                time_dropdown,
                dcc.Markdown(children=space),
                dcc.Markdown(children=space),

                # Choix du nombre de joueurs
                n_joueurs_txt,
                n_joueurs_dropdown,
                dcc.Markdown(children=space),
                dcc.Markdown(children=space),

                # Initialisation des joueurs
                joueur_txt,
                dcc.Markdown(children=space),
                joueur_input,
                dcc.Markdown(children=space),
                button_add,
                button_drop,
                dcc.Markdown(children=space),
                dcc.Markdown(children=space),
                list_joueurs,
                dcc.Markdown(children=space),
                dcc.Markdown(children=space),

                # Regles
                rules_button,
                dcc.Markdown(children=space),
                rules,
                dcc.Markdown(children=space),

                # Debut du jeu
                popup_bouton,
                popup,

                ],
            )], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True)

