import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from clickhouse_driver import Client

app = dash.Dash(__name__)
client = Client(host='localhost', port=9000)

def fetch_data():
    raw_data = client.execute("SELECT * FROM raw_data_table ORDER BY timestamp DESC LIMIT 5")
    processed_data = client.execute("SELECT * FROM processed_data_table")
    return raw_data, processed_data

app.layout = html.Div([
    html.H1("Cell Manufacturing Dashboard"),
    html.Div(id='raw-data-table'),
    html.Div(id='processed-data-table'),
    dcc.Interval(id='interval-component', interval=60000, n_intervals=0)  # Refresh every 60s
])

@app.callback(
    [Output('raw-data-table', 'children'), Output('processed-data-table', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_tables(n):
    raw_data, processed_data = fetch_data()
    raw_table = html.Table([html.Tr([html.Th(col) for col in ["timestamp", "stage", "temperature", "pressure"]])] +
                           [html.Tr([html.Td(cell) for cell in row]) for row in raw_data])
    processed_table = html.Table([html.Tr([html.Th(col) for col in ["stage", "avg_temperature", "avg_pressure"]])] +
                                 [html.Tr([html.Td(cell) for cell in row]) for row in processed_data])
    return raw_table, processed_table

if __name__ == '__main__':
    app.run_server(debug=True)
