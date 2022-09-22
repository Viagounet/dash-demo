import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

from dash import html, dcc, callback, Output, Input

# Doc dash : https://dash.plotly.com/installation
# Doc dbc : https://dash-bootstrap-components.opensource.faculty.ai/docs/
# Doc bootstrap : https://getbootstrap.com/docs/4.0
# Doc plotly : https://plotly.com/python/
from compute_decay import decay

df = pd.read_csv("isotopes_list.csv", sep=";")

# Création d'une instance de l'application.
# On peut choisir un thème existant boostrap (https://bootswatch.com/) ou sa propre feuille de style css
app = dash.Dash(
    external_stylesheets=[dbc.themes.LITERA]
)

title = html.Div([html.H1("Décroissance radioactive des éléments", className="text-center"),
                  html.Hr()])
# Equivalence HTML :
# <div>
#     <h1>Décroissance radioactive des éléments</h1>
#     <hr>
# </div>


selected_values = ["Lead-202", "Plutonium-239"]
filtered_dataframe = df[df["Isotope"].isin(selected_values)]

# Widget permettant de sélectionner plusieurs options
# mb-2 ajoute une marge extérieure de taille 2rem à droite du composant (margin-bottom)
isotope_selecter = dcc.Dropdown(
    options=[{"label": isotope,
              "value": isotope} for isotope in df["Isotope"]],
    value=selected_values,
    id="select-isotope",
    className="mb-1",
    multi=True
)

# Widget permettant d'afficher des données dans un tableau
selected_isotopes_datatable = dbc.Table.from_dataframe(filtered_dataframe, striped=True,
                                                       bordered=True, hover=True)

# On affiche une courbe de décroissance radioactive pour chaque isotope sélectionné
data = []
for isotope_name, isotope_half_life in zip(filtered_dataframe["Isotope"],
                                           filtered_dataframe["Demi-vie (années)"]):
    time, nuclei_amount = decay(half_life=isotope_half_life, n_0=1000, max_half_lives=10)
    trace = go.Scatter(x=time,
                       y=nuclei_amount,
                       name=isotope_name)
    data.append(trace)

# Mise en page du graphique
layout = go.Layout(xaxis={'title': 'Time (years)'},
                   yaxis={'title': 'Nuclei amount'},
                   title="Nuclei amount according to time",
                   margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                   hovermode='closest')

nuclear_decay_graph = dcc.Graph(figure=go.Figure(data=data, layout=layout), id="nuclear-decay-graph")

# me-2 ajoute une marge extérieure de taille 2rem à droite du composant (margin-end)
left_part = html.Div(
    [isotope_selecter, html.Div(children=selected_isotopes_datatable, id="selected-isotopes-datatable")],
    className="flex-grow-1 me-2")
right_part = html.Div([nuclear_decay_graph], className="flex-grow-1")

# p-2 ajoute une marge intérieure de taille 2rem autour du composant (padding)
body = html.Div([left_part, right_part],
                className="d-flex flex-row p-2")  # d-flex flex-row permet d'aligner les éléments à l'horizontale

app.layout = html.Div([title, body])


@callback(
    Output("selected-isotopes-datatable", "children"),
    Output("nuclear-decay-graph", "figure"),
    Input("select-isotope", "value"),
    prevent_init_callback=True
)
def update_data(selected_values):  # Les arguments de la fonction correspondent aux entrées
    filtered_dataframe = df[df["Isotope"].isin(selected_values)]
    selected_isotopes_datatable = dbc.Table.from_dataframe(filtered_dataframe, striped=True,
                                                           bordered=True, hover=True)

    data = []
    for isotope_name, isotope_half_life in zip(filtered_dataframe["Isotope"],
                                               filtered_dataframe["Demi-vie (années)"]):
        time, nuclei_amount = decay(half_life=isotope_half_life, n_0=1000, max_half_lives=10)
        trace = go.Scatter(x=time,
                           y=nuclei_amount,
                           name=isotope_name)
        data.append(trace)

    nuclear_decay_figure = go.Figure(data=data, layout=layout)

    return selected_isotopes_datatable, nuclear_decay_figure  # Les valeurs retournées de la fonction correspondent aux sorties


if __name__ == "__main__":
    app.run_server(debug=True, host="localhost", port=8888)
