import dash
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
        [
            html.Section([
                html.Div(id='display-student-info'),
                html.Hr(),
                html.H6('Academics Achievement'),
                html.Div(id='display-grade'),
                html.Hr(),
                html.H6("Behaviour/Affectiveness"),
                html.Div(id='display-attitude'),
                ], className="sheet padding-10mm"),
            html.Section([
                html.H6("Academics Achievement - Teacher's Note"),
                html.Div(id='display-notes'),
                ], className="sheet padding-10mm"),
            html.Section([
                html.H6("Attendance"),
                html.Div(id='display-attendance'),
                html.Hr(),
                html.Div(id='display-comments'),
                html.Hr(),
                html.Div(id='display-date'),
                html.Br(),
                html.Div(id='display-tname'),
                html.Br(),
                html.P('Headmistress : Yetti Dalimi'),
                html.Br(),
                html.P('Signature :'),
                ], className="sheet padding-10mm"),
        ]
    )

