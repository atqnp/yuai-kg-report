import time
import os
import dash
import gspread
import pandas as pd
import appfunction
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from oauth2client.service_account import ServiceAccountCredentials
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from apps import report, submit1, submit2, submit5, submit6

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

SHEET_PRIVATE_KEY = os.environ['SHEET_PRIVATE_KEY']
SHEET_PRIVATE_KEY = SHEET_PRIVATE_KEY.replace('\\n', '\n')

username = os.environ['BASIC_USER']
password = os.environ['BASIC_PASS']

VALID_USERNAME_PASSWORD_PAIRS = [[username,password]]

credential = {
                "type": "service_account",
                "project_id": os.environ['SHEET_PROJECT_ID'],
                "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
                "private_key": SHEET_PRIVATE_KEY,
                "client_email": os.environ['SHEET_CLIENT_EMAIL'],
                "client_id": os.environ['SHEET_CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
             }

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential,scope)

UPDATE_INTERVAL = 30

#DataFrame spreadsheet
def get_data():
    #updates the data
    global df
    file = gspread.authorize(credentials)
    sheet = file.open("Semester 1 report card (KG) 2018/2019")
    wks = sheet.worksheet("master")
    df = pd.DataFrame(wks.get_all_records())

def get_new_update(period=UPDATE_INTERVAL):
    while True:
        get_data()
        time.sleep(period)

select_sem = ['{}/2018/19'.format(num) for num in range(1,4)]

#List of subject
subject = {'MT':'Mathematics',
            'EN':'English',
            'WS':'Writing Skill',
            'MSC':'Motor Skill and Coordination',    
            'SMD':'Social and Moral Development',    
            'ES':'Environmental Studies',   
            'WH':'Work Habits',
            'TF':'Tahfidz Juz 30',  
            'QR':'Qiraati (Nurul Bayan)'} 

sub_grade = ['{}_grade'.format(sub) for sub in subject.keys()]
sub_marks = ['{}_marks'.format(sub) for sub in subject.keys()]
sub_com = ['{}_comments'.format(sub) for sub in subject.keys()]

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>YUAI KG - Report Card</title>
        {%favicon%}
        {%css%}
    </head>
    <body class="A4">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
    </body>
</html>
'''

app.config.suppress_callback_exceptions = True
server = app.server
get_data()

def serve_layout():
    return html.Div([
        html.H3('YUAI International Islamic School - Kindergarten Progress Report Card', className="no-print"),
        #header,
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='name-dropdown',
                    placeholder="Select name",
                    options=[{'label':i,'value':i} for i in list(df['Name'])],
                    ),
                dcc.Dropdown(
                    id='semester-dropdown',
                    options=[{'label':i,'value':i} for i in select_sem],
                    placeholder="Select semester"
                    ),
                html.Hr(),
                html.Div(id='display-value')
                ], className="no-print sheet padding-10mm"),
                    html.Br(),       
            dcc.Tabs(id='tabs-id', value='tab-report',children=[
                dcc.Tab(label='Full Report', value='tab-report'),
                dcc.Tab(label='Submit Marks and Grade (Academics)', value='tab-submit-grade'),
                dcc.Tab(label='Submit Notes (Academics)', value='tab-submit-note'),
                dcc.Tab(label='Submit Behaviour or Affectiveness', value='tab-submit-behaviour'),
                dcc.Tab(label='Submit or Update Student', value='tab-submit-name'),
                ])], className="no-print"),
        html.Div(id='tab-contents')
        ])

executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_new_update)

#app.css.append_css({"external_url": "https://codepen.io/atiq_np/pen/aXNWWG.css"})

app.layout = serve_layout

@app.callback(Output('tab-contents','children'),
            [Input('tabs-id','value')])
def render_content(tab):
    if tab == 'tab-report':
        return report.layout
    elif tab == 'tab-submit-grade':
        return submit1.layout
    elif tab == 'tab-submit-note':
        return submit2.layout
    elif tab == 'tab-submit-behaviour':
        return submit5.layout
    elif tab == 'tab-submit-name':
        return submit6.layout

#selected person
@app.callback(
    Output('display-value','children'), 
    [Input('name-dropdown','value')])
def display_value(name):
    dfi = df[df.Name.isin([name])]
    age = dfi['Age']
    return html.P('You have selected:'), html.P('{} - Age {}'.format(name, age))

#full report page - student's data
@app.callback(
    Output('display-student-info','children'), 
    [Input('name-dropdown','value'),
    Input('semester-dropdown','value')])
def display_info(name,sem):
    dfi = df[df.Name.isin([name])]
    age = dfi['Age']
    return html.Div([html.P('Name : {}'.format(name)),
        html.Br(), html.P('Age : {}'.format(age)),
        html.Br(), html.P('Semester : {}'.format(sem)),
        ])

#full report page - grades and marks table
@app.callback(
    Output('display-grade','children'),
    [Input('name-dropdown','value')])
def display_grade(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.grades_table(dfi)

#full report page - full academics table
@app.callback(
    Output('display-report','children'),
    [Input('name-dropdown','value')])
def display_fullgrade(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.academic_report(dfi)

#full report page - academic teacher's note table
@app.callback(
    Output('display-comments','children'),
    [Input('name-dropdown','value')])
def display_comments(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.comments_table(dfi)

#full report page - behaviour attitude table
@app.callback(
    Output('display-attitude','children'),
    [Input('name-dropdown','value')])
def display_attitude(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.attitude(dfi)

#submit_grade - selected subject for submitting (marks table output)
@app.callback(
    Output('submit-subject-marks','children'),
    [Input('subject-dropdown','value'),
    Input('name-dropdown','value')])
def marks_submit_table(subcode,name):
    dfi = df[df.Name.isin([name])]
    grade = '{}_grade'.format(subcode)
    marks = '{}_marks'.format(subcode)
    return appfunction.submit_sub_marks(dfi,subcode,grade,marks)

#submit_grade - update cell (marks)
@app.callback(
    Output('container-marks','children'),
    [Input('submit-marks-button','n_clicks'),
    Input('name-dropdown','value'),
    Input('subject-dropdown','value')],
    [State('input-marks','value')])
def submit_marks(clicks, name, subcode, value):
    works = appfunction.access_wsheet('marks')
    sub_row = works.find(name).row
    sub_col = works.find((subject.get(subcode)).upper()).col
    works.update_cell(sub_row,sub_col,value)

#submit_notes - selected subject for submitting (comments table output)
@app.callback(
    Output('submit-subject-comments','children'),
    [Input('subject-dropdown','value'),
    Input('name-dropdown','value')])
def comments_submit_table(subcode,name):
    dfi = df[df.Name.isin([name])]
    comments = '{}_comments'.format(subcode)
    return appfunction.submit_sub_comments(dfi,subcode,comments)

#submit_notes - update cell (notes/comments)
@app.callback(
    Output('container-comments','children'),
    [Input('submit-comments-button','n_clicks'),
    Input('name-dropdown','value'),
    Input('subject-dropdown','value')],
    [State('input-comments','value')])
def submit_comments(clicks, name, subcode, value):
    works = appfunction.access_wsheet('com')
    sub_row = works.find(name).row
    sub_col = works.find((subject.get(subcode)).upper()).col
    works.update_cell(sub_row,sub_col,value)

#submit_behaviour - selected name for submitting (comments table output)
@app.callback(
    Output('submit-attitude','children'),
    [Input('name-dropdown','value')])
def submit_attitude(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.submit_attitude(dfi)

#submit_behaviour - update cell (attitude/behaviour)
@app.callback(
    Output('container-att','children'),
    [Input('submit-att-button','n_clicks'),
    Input('name-dropdown','value')],
    [State('input-att-1','value'), State('input-att-2','value'), State('input-att-3','value'),
    State('input-att-4','value'), State('input-att-5','value')])
def submit_comments(clicks, name, val1, val2, val3, val4, val5):
    works = appfunction.access_wsheet('att behaviour')
    sub_row = works.find(name).row
    works.update_cell(sub_row, works.find('Akhlaq').col, val1)
    works.update_cell(sub_row, works.find('Discipline').col, val2)
    works.update_cell(sub_row, works.find('Diligent').col, val3)
    works.update_cell(sub_row, works.find('Interaction').col, val4)
    works.update_cell(sub_row, works.find('Respect').col, val5)

#submit_name - selection
@app.callback(
    Output('display-submit','children'), 
    [Input('update-dropdown','value'),
    Input('name-dropdown','value')])
def display_selection(value,name):
    dfi = df[df.Name.isin([name])]
    if value == 'UP':
        return appfunction.update_name(name,dfi['Age'])
    elif value == 'SUB':
        return appfunction.new_name()

#submit_name - new student submission
@app.callback(
    Output('container-new','children'),
    [Input('submit-new-button','n_clicks'),
    Input('submit-new-button','n_submit')],
    [State('input-name','value'),
    State('input-age','value')])
def submit_name(clicks, submit, name, age):
    def next_available_row(worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))
        return len(str_list)+1

    next_row = next_available_row(wks)
    #column, row, input item
    if not name in list(df['Name']):
        wks.update_cell(next_row,1,name)
        wks.update_cell(next_row,2,age)
        return html.P('You have added:'), html.P('{} - Age: {}'.format(name, age))
    else:
        return html.P('The name is already available.')

#submit_name - update student info
@app.callback(
    Output('container-update','children'),
    [Input('submit-update-button','n_clicks'),
    Input('submit-update-button','n_submit'),
    Input('name-dropdown','value')],
    [State('update-age','value')])
def submit_update(clicks, submit, name, age):
    sub_row = wks.find(name).row
    wks.update_cell(sub_row, 2, age)

if __name__ == '__main__':
    app.run_server(debug=True)
