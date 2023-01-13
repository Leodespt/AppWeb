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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
    Input('time-dropdown', 'value')
)
def update_output(value):
    global game_time
    game_time = int([int(integer)for integer in value.split() if integer.isdigit()][0])
    return f"\n\nUn Defi sera lancé toutes les {game_time} minutes\n"


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

rules = html.Div(
    [
        html.Div(id='output-dropdown'),
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
#Un Defi sera lancé toutes les  {} minutes,\n\n
        return f'Chaque joueur recevra un defi à réaliser pendant le temps imparti.\n\nLes joueurs sont :\n {str_joueurs}'


#%% Start Game

popup_bouton = html.Div(
    [
        dbc.Button("Start", id="open-game"),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

@app.callback(
    Output("popup", "is_open"),
    [Input("open-game", "n_clicks")],
    State("popup", "is_open"),
)
def toggle_modal(n, is_open=False): 
    if n:
        return not is_open
    else : 
        global start_time
        global game
        start_time = datetime.datetime.now()
        #game = Game(df,joueurs,start_time,0)
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
        is_open = False#True
        )
    ]
)

#timer
@app.callback(Output('timer', 'children'),
    [Input('interval', 'n_intervals')])
def update_interval(n):
    time_now = datetime.datetime.now()
    time_delta = datetime.timedelta(hours=0, minutes=game_time)
    final_time = start_time + time_delta
    countdown = final_time - time_now   
    h,rem = divmod(countdown.seconds, 3600)
    mins, secs = divmod(rem, 60)
    return '{:02d}:{:02d}'.format(mins, secs)


#%% Defi 

defi_bouton = html.Div([
    html.Div(id="defi-bouton",className="d-grid gap-2 col-4 mx-auto")
])

@app.callback(
    Output("defi-bouton", "children"),
    #[Input("open-game", "n_clicks")],
    Input("popup", "is_open")
)
def update_output(is_open):
    if is_open:
        boutons = []
        for i in range(len(joueurs)):
            bouton = html.Div([html.Button(f"Joueur  {i} : {joueurs[i].nom}",id = f"joueur-{i}")],className="d-grid gap-2 col-4 mx-auto")
            
            defi = df.sample(n=1).reset_index(drop = True)
            defi_text = f'Ton Defi : \n\n*{str(defi["defi"][0])}*\n\nLe defi vaut {str(defi["pts"][0])} points.\n\nBonne chance champion.'
            
            defi_popup = dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle(f"Joueur {i} : {joueurs[i].nom}")),
                            html.Div([dcc.Markdown(children=defi_text)],style={'width':'75%', 'margin':25, 'textAlign': 'center'})
                        ],
                        id=f"popup-{i}",
                        is_open = False,
                        className="d-grid gap-2 col-4 mx-auto")                 
                
            boutons.append(bouton)
            boutons.append(defi_popup)


            for j in range(len(joueurs)):
                @app.callback(
                    Output(f"popup-{j}", "is_open"),
                    [Input(f"joueur-{j}", "n_clicks")],
                    [State(f"popup-{j}", "is_open")],
                )
                def toggle_modal(n, is_open=False):
                    if n is not None:
                        return not is_open
                    else : return is_open

        return boutons

'''
html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Joueur 1: "+joueurs[i].nom)),
                #html.Div(id=,className="d-grid gap-2 col-2 mx-auto"),
                html.Div([dcc.Markdown(children=defi_text)],style={'width':'75%', 'margin':25, 'textAlign': 'center'})
            ],
            id=f"popup-{i}",
            is_open = False
        )],
    className="d-grid gap-2 col-4 mx-auto"),
'''



#%% Popup Layout
"""
@app.callback(
    Output('output-joueurs',"children"),
    [Input('open-game','n_clicks')], 
)
def update_output(clicks):
    if clicks is not None:
        str_joueurs = ''
        for j in joueurs:
            str_joueurs = str_joueurs +'\n\n - Joueur '+str(j.numero)+' : '+j.nom
        return str_joueurs
"""
popup = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Your Turn")),

                timer_popup_bouton,
                timer_popup,

                #ameliorer layout des joueurs
                #html.Div(id = 'output-joueurs',className="d-grid gap-2 col-4 mx-auto"),

                dcc.Markdown(children=space),
                dcc.Markdown(children=space),


                defi_bouton,

                #ameliorer boutons
                #dbc.Button('Joueur 1', id='btn-nclicks-1'),
                #html.Div([dbc.Button('Joueur 2', id='btn-nclicks-2')],style={ 'marginTop': 25, 'marginLeft': 485, 'width' : '15vh'}, className="d-grid"),

                #html.Div(id='joueur-choisi',className="d-grid gap-2 col-4 mx-auto"),
                #dcc.Markdown(children=space),
                #html.Div(id ='popup-defi', className="d-grid gap-2 col-4 mx-auto"),
                #dcc.Markdown(children=space),
            ],
            id="popup",
            fullscreen=True,
            is_open = False
        ),
    ]
)

#%% Defis
'''
@app.callback(
    Output('joueur-choisi', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
)
def displayClick(btn1, btn2):

    #choix du defi et selection du defi dans la BDD
    if "btn-nclicks-1" == ctx.triggered_id:
        defi = df.sample(n=1).reset_index(drop = True)
        defi_text = 'Ton Defi : \n'+'\n*'+str(defi['defi'][0])+'*\n\nLe defi vaut '+str(defi['pts'][0])+' points.\n\nBonne chance champion.'
        joueurs[1-1].defi_actuel = defi
        return html.Div(
                [
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Joueur 1: "+joueurs[1-1].nom)),
                            html.Div(id='joueur-choisi',className="d-grid gap-2 col-2 mx-auto"),
                            html.Div([dcc.Markdown(children=defi_text)],style={'width':'75%', 'margin':25, 'textAlign': 'center'})
                        ],
                        id="popup",
                        is_open = False
                    )],
                className="d-grid gap-2 col-4 mx-auto"),

    elif "btn-nclicks-2" == ctx.triggered_id:
        defi = df.sample(n=1)
        defi_text = 'Ton Defi : \n'+'\n'+str(defi['defi']).replace('Name: defi, dtype: object','')+'\n\nLe Defi vaut '+str(int(defi['pts']))+' points.\n\nBonne chance champion.'
        return html.Div(
                [   dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Defi : "+'joueur-choisi')),
                            html.Div(id='joueur-choisi',className="d-grid gap-2 col-2 mx-auto"),
                            html.Div([dcc.Markdown(children=defi_text)],style={'width':'75%', 'margin':25, 'textAlign': 'center'})
                        ],
                        id="popup",
                        is_open = False
                    )],
                className="d-grid gap-2 col-4 mx-auto"),
'''

#%% Layout

app.layout = dbc.Container([
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
        html.Div(id = 'btn-joueur'),
        popup,

        dash.page_container
        ], align='center',className="g-0",
    )
], fluid=True)


#%% Main

if __name__ == "__main__":
    app.run(debug=False)
