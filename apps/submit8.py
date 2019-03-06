import dash
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
    [
        html.Hr(),
        html.H5("Submit teacher's comment"),
        html.Div(id="display-comments"),
        html.Hr(),
        html.Div(dcc.Textarea(id='input-comment',
            placeholder='Enter your comments here..',
            style={'width': '100%'})),
        html.Div(html.Button('Submit',id='submit-comment-button')),
    ], className="sheet padding-10mm"
    )
