import dash
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
    [
        html.Hr(),
        html.H5("Submit attendance"),
        html.Div(id='display-attendance'),
        html.Br(),
        html.Div(id='submit-attendance')
    ], className="sheet padding-10mm"
    )
