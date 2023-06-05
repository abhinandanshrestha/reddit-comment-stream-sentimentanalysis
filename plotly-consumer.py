from dash import Dash, html, dcc, Output, Input
import plotly.graph_objects as go
from confluent_kafka import Consumer
import json

sentiment_count={'positive': 0, 'negative': 0, 'neutral': 0}

# Create a Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'soccer'
}

# Create a Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to the Kafka topic
consumer.subscribe(['soccer'])

app = Dash(__name__)


# Define colors for each sentiment
sentiment_colors = {
    'positive': 'green',
    'negative': 'red',
    'neutral': 'blue'
}

# Create a bar trace for sentiment count
bar_trace = go.Bar(x=list(sentiment_count.keys()), y=list(sentiment_count.values()), marker=dict(color=[sentiment_colors[sentiment] for sentiment in sentiment_count.keys()]))
layout = go.Layout(height=1000, width=1920, title="Sentiment Analysis")
fig = go.Figure(data=[bar_trace], layout=layout)# Create a bar trace for sentiment count

# Define the app layout
app.layout = html.Div([
    dcc.Graph(id='sentiment-chart', figure=fig),
    dcc.Interval(id='interval-component', interval=4000, n_intervals=0)
])

# Create a callback function to update the plot
@app.callback(Output('sentiment-chart', 'figure'), Input('interval-component', 'n_intervals'))
def update_plot(n):
    print(n)
    msg = consumer.poll(0)
    if msg is not None:
        value = msg.value().decode('utf-8')
        data = json.loads(value)
        print(data)
        # Update sentiment count
        global sentiment_count
        sentiment_count = data

    fig.data[0].y = list(sentiment_count.values())
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,port=8888)