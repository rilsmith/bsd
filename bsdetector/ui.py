import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from pandas import DataFrame
# from pandas_datareader import data as web
# from datetime import datetime as dt
from bsdetector.bias import compute_bias, extract_bias_features


def handle_statement(stmt, features=False):
    """handle the statement returning a dictionary to return to the client"""
    print(stmt)
    result = dict()
    result['bias'] = compute_bias(stmt)
    result['statement'] = stmt
    if features:
        features = extract_bias_features(stmt)
        result['features'] = features
    return result


app = dash.Dash('Hello World')

# noinspection PyUnresolvedReferences

app.layout = html.Div([
    html.Div(id="afscontianer1"),
    html.Script(async="async", src="http://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"),
    html.Script("""  (adsbygoogle = window.adsbygoogle || []).push({
    google_ad_client: "ca-pub-9697562934451352",
    enable_page_level_ads: true
  });"""),
    html.Script("""
    google_adtest = "on";
    google_ad_client: "ca-pub-9697562934451352";
    """),
    html.Script(src="http://pagead2.googlesyndication.com/pagead/show_ads.js"),
    dcc.Textarea(
        id='my-textarea',
        placeholder='Enter a value...',
        value='Enter text here...',
        style={'width': '100%'}
    ),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='COKE'
    ),
    dcc.Graph(id='my-graph'),
])
app.scripts.append_script("http://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js")
app.scripts.append_script()


@app.callback(
    Output('my-graph', 'figure'),
    [Input(component_id='my-textarea', component_property='value')]
)
def update_output_div(input_value):
    from newspaper import Article
    url = input_value
    print(input_value)
    if 'http' in input_value:
        print(input_value)
        article = Article(url)
        article.download()
        article.parse()
        import nltk.data
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(article.text)
        print(len(sentences))
        scores = [handle_statement(sentence) for sentence in sentences]
        df = DataFrame(scores)
        #for sentence in sentences:
        #    import json
        #
        #    return json.dumps(handle_statement(sentence))
        return {
            'data': [{
                'x':  df.index,
                'y': df.bias
            }],
            'layout': {'margin': {'1': 40, 'r': 0, 't': 20, 'b': 30}}
        }
    #results = [handle_statement(sentence) for sentence in sentences]
    return "you've entered "


"""
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    df = web.DataReader(
        selected_dropdown_value,
        'google',
        dt(2017, 1, 1),
        dt.now()
    )
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }],
        'layout': {'margin': {'1': 40, 'r': 0, 't': 20, 'b': 30}}
    }
"""


app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWlwgP.css'})
