import os
import gspread
import dash
import dash_core_components as dcc
import dash_html_components as html
from oauth2client.service_account import ServiceAccountCredentials

#center style for table
center = {'text-align':'center'}

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

def access_wsheet(item):
    """accessing worksheet based on item(input)"""
    access = 'all {}'.format(item)
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    SHEET_PRIVATE_KEY = os.environ['SHEET_PRIVATE_KEY']
    SHEET_PRIVATE_KEY = SHEET_PRIVATE_KEY.replace('\\n', '\n')

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

    file = gspread.authorize(credentials)
    sheet = file.open("Semester 1 report card (KG) 2018/2019")
    wks = sheet.worksheet(access)
    return wks

def new_name():
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Name','Age']])] +
        #Body
        [html.Tr(
            [html.Td(html.Div(dcc.Input(id='input-name',type='text')))] + 
            [html.Td(html.Div(dcc.Input(id='input-age',type='text')))]
                )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-new-button')))] +
            )] +
        [html.Tr(
            [html.Td(html.Div(id='container-new'),colSpan='2')]
            )]
        )

def update_name(name,age):
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Name','Age (Previously submitted)', 'Age']])] +
        #Body
        [html.Tr(
            [html.Td(name)] + 
            [html.Td(age)]
            [html.Td(html.Div(dcc.Input(id='update-age',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-update-button')))] +
            )] +
        [html.Tr(
            [html.Td(html.Div(id='container-update'),colSpan='2')]
            )]
        )

def grades_table(dataframe):
    """return table for marks and grades of a student"""
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in ['Component','Grade','Marks']])] +
        # Body
        [html.Tr(
            [html.Td(sub)] +
            [html.Td(dataframe[grade],style=center)] +
            [html.Td(dataframe[marks],style=center)]
            ) for sub,grade,marks in zip(subject.values(),sub_grade,sub_marks)
        ]
        )

def comments_table(dataframe):
    """return table for notes/comments of a student"""
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in ['Component','Competency and Accomplishment']])] +
        # Body
        [html.Tr(
            [html.Td(sub)] +
            [html.Td([html.P(value) for index, value in dataframe[comments].str.split('\n',expand=True).items()])]
            ) for sub,comments in zip(subject.values(),sub_com)
        ]
        )

def attitude(dataframe):
    """return table for attitude grades of a student"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Component','Grade']])] +
        #Body
        [html.Tr(
            [html.Td(att)] + [html.Td(dataframe[att],style=center)]
            ) for att in ['Akhlaq','Discipline','Diligent','Interaction','Respect']]
        )

def submit_sub_marks(dataframe,subcode,grade,marks):
    """return table for marks submission of a student based on selected subject"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Component to Submit','Grade (Before submission)','Marks (Before submission)']])] +
        #Body
        [html.Tr(
            [html.Td(subject.get(subcode))] + 
            [html.Td(dataframe[grade],style=center)] +
            [html.Td(dataframe[marks],style=center)] +
            [html.Td(html.Div(dcc.Input(id='input-marks',type='number')))] + 
            [html.Td(html.Div(html.Button('Submit',id='submit-marks-button')))] +
            [html.Td(html.Div(id='container-marks'))]
            )
        ]
        )

def submit_sub_comments(dataframe,subcode,comment):
    """return table for notes/comments submission of a student based on selected subject"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Component to Submit','Notes (Before submission)']])] +
        #Body
        [html.Tr(
            [html.Td(subject.get(subcode))] + 
            [html.Td([html.P(value) for index, value in dataframe[comment].str.split('\n',expand=True).items()])]
            )
        ] +
        [html.Tr(
            [html.Td(html.P("Notes/Comments to Submit"))] +
            [html.Td(html.Div(dcc.Textarea(id='input-comments',placeholder='Enter your notes/comments here..',style={'width': '100%'})))] 
            )
        ] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-comments-button')))] +
            [html.Td(html.Div(id='container-comments'))]
            )]
        )

def submit_attitude(dataframe):
    """return table for attitude grades submission of a student"""
    return html.Table(
        [html.Tr(html.Th(html.P('Changes/Input for submission'),colSpan='3'))] +
        #Header
        [html.Tr([html.Th(col) for col in ['Component','Grade (Before submission)','']])] +
        #Body
        [html.Tr(
            [html.Td(html.P('Akhlaq'))] + [html.Td(dataframe['Akhlaq'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-1',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Discipline'))] + [html.Td(dataframe['Discipline'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-2',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Diligent'))] + [html.Td(dataframe['Diligent'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-3',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Interaction'))] + [html.Td(dataframe['Interaction'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-4',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Respect'))] + [html.Td(dataframe['Respect'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-5',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-att-button')),colSpan='2')] +
            [html.Td(html.Div(id='container-att'))]
        )]
        )
