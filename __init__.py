from flask import Flask, render_template
import json
from datetime import datetime
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    # Открываем файл, считываем станые данные
    with open('data.json') as json_file:
        data = json.load(json_file)
#    x = np.arange(0,100)
    x = data['Date']
    y = data['Parameters'][2]['Pressure']
#    print(x, len(x))
#    print(y, len(y))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=''))
    fig.update_yaxes(range=[740, 780])
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="P, мм.рт.ст",
                      xaxis_title="Дата",
                      yaxis_title="",
                      margin=dict(l=0, r=0, t=30, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Давление: %{y}<br>Дата: %{x}")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('dashboard.html',data=data, graphJSON=graphJSON, name_page='Weather Dashboard', active_page='main')

@app.route('/greenhouse/')
def greenhouse():
    # Открываем файл, считываем станые данные
    with open('data.json') as json_file:
        data = json.load(json_file)
#    x = np.arange(0,100)
    x = data['Date']
    y = data['Parameters'][2]['Pressure']
#    print(x, len(x))
#    print(y, len(y))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=''))
    fig.update_yaxes(range=[740, 780])
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="P, мм.рт.ст",
                      xaxis_title="Дата",
                      yaxis_title="",
                      margin=dict(l=0, r=0, t=30, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Давление: %{y}<br>Дата: %{x}")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('greenhouse.html',data=data, graphJSON=graphJSON, name_page='Теплица', active_page='greenhouse')

@app.route('/get_parameters/<id>') # получаем данные в виде вызова страницы http://127.0.0.1:5000/get_parameters/температура_влажность_давление
def get_parameters(id):
    current_date = datetime.now()
    current_parameters=list(map(float,id.split('_'))) # [температура, влажность, давление]
    if len(current_parameters)!=3:
        return 'ошибка'

    # Открываем файл, считываем станые данные
    with open('greenhouse.json') as json_file:
        data = json.load(json_file)


    # Обновляем данные
    data['Parameters'][0]['Temperature'].append(current_parameters[0])
    data['Parameters'][0]['Temperature'].pop(0)

    data['Parameters'][1]['Humidity'].append(current_parameters[1])
    data['Parameters'][1]['Humidity'].pop(0)

    data['Parameters'][2]['Pressure'].append(round(current_parameters[2] * 0.00750062, 2))
    data['Parameters'][2]['Pressure'].pop(0)

    data['Date'].append(current_date.isoformat())
    data['Date'].pop(0)

    # Открываем файл, сохраняем данные
    with open('greenhouse.json', 'w') as outfile:
        json.dump(data, outfile)


    print(datetime.now())
    print(data['Parameters'][0]['Temperature'])
    print(data['Parameters'][1]['Humidity'])
    print(data['Parameters'][2]['Pressure'])
    print(data['Date'])


    return 'обновлено'












# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
