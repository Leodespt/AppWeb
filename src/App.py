import dash
from dash import html,Output,Input,State,dcc,ctx
import dash_bootstrap_components as dbc

#external_stylesheets = ["/workspaces/MyPortfolioTracker/project/pages/style.css"]


from Joueur import Joueur

external_stylesheets=[dbc.themes.SPACELAB]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.index_string = '''<!DOCTYPE html>
<html>
<head>
<title>My Game</title>
<link rel="manifest" href="./assets/manifest.json" />
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
      .register('./assets/sw01.js')
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


button = html.Div(
    [
        dbc.Button("Show Final Rules",id = 'start-game',type = 'submit',color="primary"),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

frequence_input = html.Div(
    [
        dcc.Input(id="frequence-input", type="text",value = '', placeholder=""),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

unite_input = html.Div(
    [
        dcc.Input(id="unite-input", type="text", value = '',placeholder=""),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

frequence_txt = html.Div(
    [
        dcc.Markdown(children='Frequence de la notification (1,2,40)'),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

unite_txt = html.Div(
    [
        dcc.Markdown(children='unité de la frequence (min/h)'),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

joueur_txt = html.Div(
    [
        dcc.Markdown(children='Joueurs :'),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

space = '''
###

'''

regles = html.Div(
    [
        dcc.Markdown(id='output-regles'),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)


global joueurs 
joueurs = []
    

list_joueurs = html.Div(
    [
        dcc.Markdown(id = 'output-joueur'),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

button_add = html.Div(
    [
        dbc.Button("Add",id = 'add',type = 'submit',color="success"),
    ],
    className="d-grid gap-1 col-2 mx-auto",
)

button_drop = html.Div(
    [
        dbc.Button("Drop",id = 'drop',type = 'submit',color="danger"),
    ],
    className="d-grid gap-1 col-2 mx-auto",
)

joueur_input = html.Div(
    [
        dcc.Input(id="joueur-input", type="text", value = '',placeholder=""),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

popup_bouton = html.Div(
    [
        dbc.Button("Start", id="open-game"),
    ],
    className="d-grid gap-2 col-4 mx-auto",
)

###########
from random import shuffle,random
from random import seed
seed(1)
r = random()
#joueurs = random.shuffle(joueurs, lambda: r)
############


popup = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Your Turn")),
                list_joueurs,
                html.Div([
                dbc.Button('Joueur 1', id='btn-nclicks-1'),
                dbc.Button('Joueur 2', id='btn-nclicks-2'),
                ],className="d-grid gap-2 col-2 mx-auto"),
                html.Div(id='joueur-choisi',className="d-grid gap-2 col-4 mx-auto"),
                dcc.Markdown(children=space),
                html.Div(id ='popup-defi', className="d-grid gap-2 col-4 mx-auto"),
                dcc.Markdown(children=space),
            ],
            id="popup",
            fullscreen=True,
            is_open = False
        ),
    ]
)
"""
popup = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Your Turn")),
                html.Div(
                [
                dcc.Markdown(children='Leo'),
                dbc.Button("Voir Defi", id="voir-defi"),
                ],
                className="d-grid gap-2 col-4 mx-auto"),
                html.Div(
                id = 'popup-defi',
                className="d-grid gap-2 col-4 mx-auto"),
            ],
            id="popup",
            fullscreen=True,
            is_open = False
        ),
    ]
)
"""
app.layout = dbc.Container([
    dbc.Row(
        [
        navbar,#Menu,
        dcc.Markdown(children=space),
        frequence_txt,
        dcc.Markdown(children=space),
        frequence_input,
        dcc.Markdown(children=space),
        unite_txt,
        dcc.Markdown(children=space),
        unite_input,
        dcc.Markdown(children=space),
        joueur_txt,
        dcc.Markdown(children=space),
        joueur_input,
        dcc.Markdown(children=space),
        button_add,
        button_drop,
        dcc.Markdown(children=space),
        #list_joueurs,
        dcc.Markdown(children=space),
        dcc.Markdown(children=space),
        button,
        dcc.Markdown(children=space),
        regles,
        dcc.Markdown(children=space),
        popup_bouton,
        html.Div(id = 'btn-joueur'),
        popup,
        dash.page_container
        ], align='center',className="g-0",
    )
], fluid=True)


#Fonction qui affiche les regles
@app.callback(
    Output('output-regles',"children"),
    [Input('start-game','n_clicks')],
    [State("frequence-input", "value"),State("unite-input", "value")],
    
)
def update_output(clicks,input1, input2):
    if clicks is not None:

        str_joueurs = ''
        numero = 1
        for j in joueurs:
            str_joueurs = str_joueurs +'\n - Joueur '+str(numero)+' : '+j.nom
            numero+=1

        return u'''
        Un Defi sera lancé toutes les {} {},\n
        Les joueurs sont :\n
        {}
        ''' .format(input1, input2,str_joueurs)

#Fonction qui permet de supprimer des joueurs
@app.callback(
    Output('output-joueur',"children"),
    [Input('drop','n_clicks'),Input('add','n_clicks')],
    [State("joueur-input", "value")]
)
def update_output2(click_drop,click_add,nom):

    if click_drop is not None:
        for j in joueurs:
            if j.nom == nom:
                joueurs.remove(j)
    elif click_add is not None:
        joueurs.append(Joueur(nom,0,any,any))
    
    str_joueurs = ''
    numero = 1
    for j in joueurs:
        str_joueurs = str_joueurs +'\n - Joueur '+str(numero)+' : '+j.nom
        numero+=1

    return str_joueurs

###############

@app.callback(
    Output("popup", "is_open"),
    [Input("open-game", "n_clicks")],
    State("popup", "is_open"),
)
def toggle_modal(n, is_open=False): 
    if n:
        return not is_open
    else : return is_open

@app.callback(
    [Output("popup-defi", "children")],
    Input("voir-defi", "n_clicks"),
)
def update_output3(click):
    if click is not None:

        defi = 'Le defi est de realiser une montage de chaises'
        str = html.Div(
                [
                dcc.Markdown(children=space),
                dcc.Markdown(children=defi),
                dcc.Markdown(children=space),
                dbc.Button("Joueur Suivant", id="open-game"),
                ],
                className="d-grid gap-2 col-4 mx-auto"),      
        return str

@app.callback(
    Output('joueur-choisi', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
)
def displayClick(btn1, btn2):

    #choix du defi et selection du defi dans la BDD

    if "btn-nclicks-1" == ctx.triggered_id:
        return html.Div(
                [
                    dcc.Markdown(children=space),
                    dcc.Markdown(children='premier defi random')],
                className="d-grid gap-2 col-4 mx-auto"),

    elif "btn-nclicks-2" == ctx.triggered_id:
        return html.Div(
                [   dcc.Markdown(children=space),
                    dcc.Markdown(children='deuxieme defi random')],
                className="d-grid gap-2 col-4 mx-auto"),


if __name__ == "__main__":
    app.run(debug=False)