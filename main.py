import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import requests
import json

# Initialize the Dash app
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'])
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'],
                suppress_callback_exceptions=True)

# Load and process the KML file
gdf = gpd.read_file('assets/subdistrict_small_2.kml', driver='KML')
geojson = json.loads(gdf.to_json())



# Basemap options
basemap_options = [
    {'label': 'OpenStreetMap', 'value': 'open-street-map'},
    {'label': 'Carto Positron', 'value': 'carto-positron'},
    {'label': 'Stamen Terrain', 'value': 'stamen-terrain'},
]

# Function to create the menu bar
def create_menu_bar():
    return dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src="/assets/logo.png", height="60px")),
                ], align="center", className="g-0"),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Beranda", href="/", className="nav-link")),
                    dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard", className="nav-link")),
                    dbc.NavItem(dbc.NavLink("Lapor Pelanggaran", href="/report", className="nav-link")),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
        ]),
        color="#ED243E",
        dark=True,
        className="mb-5 custom-navbar",
    )
# Layout for the landing page
landing_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Jakarta Nyaman", className="display-4 fw-bold"),
                html.P("Laporkan pelanggaran dan bantu kami menjadikan Jakarta lebih nyaman untuk semua.", className="lead"),
                #dbc.Button("Mulai Lapor", color="primary", href="/report", className="me-2"),
                #dbc.Button("Pelajari Lebih Lanjut", color="secondary", href="#", outline=True),
            ], md=6, className="mb-4"),
            dbc.Col([
                html.Img(src="/assets/landing1.png", className="img-fluid")
            ], md=6, className="mb-4"),
        ], className="align-items-center"),
        
        html.Hr(),
        
        dbc.Row([
            dbc.Col([
                html.A([
                    html.Div([
                        html.I(className="fas fa-bullhorn fa-2x text-primary"),
                        html.H4("Laporkan", className="mt-3"),
                        html.P("Laporkan pelanggaran yang Anda temui"),
                    ], className="text-center p-4 bg-light rounded card-hover")
                ], href="/report", className="text-decoration-none text-reset"),
            ], md=3, className="mb-4"),
            dbc.Col([
                html.A([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x text-primary"),
                        html.H4("Pantau", className="mt-3"),
                        html.P("Pantau perkembangan laporan Anda"),
                    ], className="text-center p-4 bg-light rounded card-hover")
                ], href="/dashboard", className="text-decoration-none text-reset"),
            ], md=3, className="mb-4"),
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-users fa-2x text-primary"),
                    html.H4("Berpartisipasi", className="mt-3"),
                    html.P("Ikut serta dalam memperbaiki kota"),
                ], className="text-center p-4 bg-light rounded")
            ], md=3, className="mb-4"),
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-city fa-2x text-primary"),
                    html.H4("Jakarta Lebih Baik", className="mt-3"),
                    html.P("Bersama menciptakan Jakarta yang nyaman"),
                ], className="text-center p-4 bg-light rounded")
            ], md=3, className="mb-4"),
        ]),
        
        html.Hr(),
        
        dbc.Row([
            dbc.Col([
                html.H2("Tentang Kami", className="mb-4"),
                html.P("Jakarta Nyaman adalah platform yang memungkinkan warga untuk melaporkan pelanggaran dan masalah di kota Jakarta. Kami berkomitmen untuk membuat Jakarta menjadi tempat yang lebih baik untuk semua."),
                dbc.Button("Pelajari Lebih Lanjut", color="primary", href="#"),
            ], md=6, className="mb-4"),
            dbc.Col([
                #html.Img(src="/assets/about-image.png", className="img-fluid")
            ], md=6, className="mb-4"),
        ], className="align-items-center"),
    ], className="py-5")
])

# Layout for the dashboard page
dashboard_layout = html.Div([
    html.H1("Dashboard", className="text-center my-4"),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Jumlah Laporan", className="card-title"),
                        html.P("100", className="card-text display-4"),
                    ])
                ], className="mb-4 dashboard-card"),
            ], xs=12, md=6, lg=4, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Laporan Selesai", className="card-title"),
                        html.P("75", className="card-text display-4"),
                    ])
                ], className="mb-4 dashboard-card"),
            ], xs=12, md=6, lg=4, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Laporan Dalam Proses", className="card-title"),
                        html.P("25", className="card-text display-4"),
                    ])
                ], className="mb-4 dashboard-card"),
            ], xs=12, md=6, lg=4, className="mb-4"),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Map", className="card-title"),
                        dcc.Dropdown(
                            id='basemap-dropdown',
                            options=basemap_options,
                            value='open-street-map',
                            style={'marginBottom': '10px'}
                        ),
                        dcc.Graph(id='map', style={'height': '60vh'})
                    ])
                ])
            ], width=12),
        ]),
    ], fluid=True, className="dashboard-container"),
])

# Layout for the report form page
report_layout = html.Div([
    html.H1("Lapor Pelanggaran", className="text-center mb-5"),
    dbc.Form([
        dbc.Row([
            dbc.Col([
                dbc.Label("Nama"),
                dbc.Input(type="text", placeholder="Masukkan nama Anda"),
            ], width=6),
            dbc.Col([
                dbc.Label("Email"),
                dbc.Input(type="email", placeholder="Masukkan email Anda"),
            ], width=6),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Jenis Pelanggaran"),
                dbc.Select(
                    options=[
                        {"label": "Parkir Liar", "value": "parkir_liar"},
                        {"label": "Vandalisme", "value": "vandalisme"},
                        {"label": "Pembuangan Sampah Sembarangan", "value": "sampah"},
                    ],
                ),
            ], width=6),
            dbc.Col([
                dbc.Label("Lokasi"),
                dbc.Input(type="text", placeholder="Masukkan lokasi kejadian"),
            ], width=6),
        ], className="mb-3"),
        dbc.Label("Deskripsi"),
        dbc.Textarea(placeholder="Jelaskan detail pelanggaran", className="mb-3"),
        dbc.Button("Kirim Laporan", color="primary"),
    ]),
])

# Main app layout
app.layout = html.Div([
    create_menu_bar(),
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
    html.Footer("© 2023 Jakarta Nyaman!", className="text-center mt-5"),
])

# Callback to update page content
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dashboard":
        return dashboard_layout
    elif pathname == "/report":
        return report_layout
    else:
        return landing_layout

# Callback to toggle navbar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [dash.State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Callback to update the map
@app.callback(
    Output('map', 'figure'),
    Input('basemap-dropdown', 'value')
)
def update_map(selected_basemap):
    fig = px.choropleth_mapbox(
        geojson=geojson,
        locations=gdf.index,
        mapbox_style=selected_basemap,
        zoom=9,
        center={"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()},
        opacity=0.5,
    )
    
    fig.update_layout(
        mapbox=dict(
            style=selected_basemap,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600,
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)