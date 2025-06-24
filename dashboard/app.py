import os
from dash import Dash, dcc, html, Input, Output
from pymongo import MongoClient
import pandas as pd

app = Dash(__name__)
server = app.server

client = MongoClient(os.getenv("COSMOS_URI"))
collection = client["iot"]["data"]

def fetch_data():
    cursor = collection.find().sort("payload.timestamp", -1).limit(100)
    data = [doc["payload"] for doc in cursor]
    df = pd.DataFrame(data)
    return df

app.layout = html.Div([
    html.H1("IoT Dashboard"),
    dcc.Interval(id='interval', interval=5*1000, n_intervals=0),
    dcc.Graph(id='chart')
])

@app.callback(Output('chart', 'figure'), [Input('interval', 'n_intervals')])
def update(n):
    df = fetch_data()
    fig = {
        "data": [{"x": df["timestamp"], "y": df["temperature"], "type": "line"}],
        "layout": {"title": "Temperature Over Time"}
    }
    return fig

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
