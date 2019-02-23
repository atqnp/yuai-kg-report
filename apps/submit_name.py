import dash
import dash_core_components as dcc
import dash_html_components as html

selection = {
    'UP' : 'Update an existing student',
    'SUB' : 'Submit a new student information'
}

layout = html.Div(
    [
        html.Hr(),
        html.H5("Submit/Update new student"),
        html.Div([dcc.Dropdown(
                id='update-dropdown',
                options=[{'label':i,'value':j} for i,j in zip(selection.values(),selection.keys())],
                placeholder="Select an item",
                )]),
        html.Div(id='display-submit'),
    ], className="sheet padding-10mm"
    )
