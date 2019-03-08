import os
import gspread
import dash
import dash_core_components as dcc
import dash_html_components as html
from oauth2client.service_account import ServiceAccountCredentials

#center style for table
center = {'text-align':'center'}

subject = {'TF':'Tahfidz Juz 30',
            'QR':'Qiraati (Nurul Bayan)',
            'MT':'Mathematics',
            'EN':'English',
            'WS':'Writing Skill',
            'MSC':'Motor Skill and Coordination',
            'WH':'Work Habits',
            'ES':'Environmental Studies',    
            'SMD':'Social and Moral Development'} 

sub_grade = ['{}_grade'.format(sub) for sub in subject.keys()]
sub_marks = ['{}_marks'.format(sub) for sub in subject.keys()]
sub_note = ['{}_notes'.format(sub) for sub in subject.keys()]

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
            [html.Td(html.Div(dcc.Input(id='input-name',type='text',placeholder='Input name here..')))] + 
            [html.Td(html.Div(dcc.Input(id='input-age',type='text',placeholder='Input age here..')))]
                )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-new-button')))]
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
            [html.Td(age)] +
            [html.Td(html.Div(dcc.Input(id='update-age',type='text',placeholder='Update age here..')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-update-button')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(id='container-update'),colSpan='2')]
            )]
        )

def student_info(name,dataframe,sem):
    return html.Table(
        [html.Tr([html.Td('Name',className="no-border")] + 
            [html.Td(':',style=center,className="no-border")] + 
            [html.Td(name,className="no-border")]
            )] +
        [html.Tr([html.Td('Age',className="no-border")] + 
            [html.Td(':',style=center,className="no-border")] + 
            [html.Td(dataframe['Age'],className="no-border")]
            )] +
        [html.Tr([html.Td('Semester',className="no-border")] + 
            [html.Td(':',style=center,className="no-border")] + 
            [html.Td(sem,className="no-border")]
            )], 
        className="no-border"
        )

def grades_table(dataframe):
    """return table for marks and grades of a student"""
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in ['No','Component','Grade']])] +
        # Body
        [html.Tr(
            [html.Td(no,style=center)] +
            [html.Td(sub)] +
            [html.Td(dataframe[grade],style=center)]
            ) for no,sub,grade in zip(list(range(1,len(sub_grade)+1)),subject.values(),sub_grade)
        ],className="widetable"
        )

def notes_table(dataframe):
    """return table for academic notes of a student"""
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in ['No','Component','Competency and Accomplishment']])] +
        # Body
        [html.Tr(
            [html.Td(no,style=center)] +
            [html.Td(sub)] +
            [html.Td([html.P(value) for index, value in dataframe[notes].str.split('\n',expand=True).items()])]
            ) for no,sub,notes in zip(list(range(1,len(sub_note)+1)),subject.values(),sub_note)
        ]
        )

def attitude(dataframe):
    """return table for attitude grades of a student"""
    attlist = ['Akhlaq','Discipline','Diligent','Interaction','Respect']
    return html.Table(
        #Header
        #[html.Tr([html.Th(col) for col in ['Component','Grade']])] +
        #Body
        [html.Tr(
            [html.Td(no,style=center)] + [html.Td(att,style=center)] + [html.Td(dataframe[att],style=center)]
            ) for no,att in zip(list(range(1,len(attlist)+1)),attlist)],className="widetable"
        )

def attendance(dataframe,period):
    '''return table for attendance'''
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['MONTH',period,'%']])] +
        #Body
        [html.Tr([html.Td('School days')] + [html.Td(dataframe['School days'],style=center)] + [html.Td(dataframe['Percentage'],style=center,rowSpan='3')])] +
        [html.Tr([html.Td('Days of late')] + [html.Td(dataframe['Days of late'],style=center)])] +
        [html.Tr([html.Td('Days of absent')] + [html.Td(dataframe['Days of absent'],style=center)])],className="widetable"
        )

def comments(dataframe):
    '''return table for teacher's comment on student'''
    return html.Table(
        #Header
        [html.Tr([html.Th("Teacher's Comment")])] +
        #Body
        [html.Tr([html.Td(dataframe['Comment'])])], className="fulltable"
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
            [html.Td(html.Div(dcc.Input(id='input-marks',type='number',placeholder='Input marks here..')))] + 
            [html.Td(html.Div(html.Button('Submit',id='submit-marks-button')))] +
            [html.Td(html.Div(id='container-marks'))]
            )
        ]
        )

def submit_sub_notes(dataframe,subcode,comment):
    """return table for notes submission of a student based on selected subject"""
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
            [html.Td(html.P("Notes to Submit"))] +
            [html.Td(html.Div(dcc.Textarea(id='input-notes',placeholder='Enter your notes here..',style={'width': '100%'})))] 
            )
        ] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-notes-button')))] +
            [html.Td(html.Div(id='container-notes'))]
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
            [html.Td(html.Div(dcc.Input(id='input-att-1',type='text',placeholder='Input grade here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Discipline'))] + [html.Td(dataframe['Discipline'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-2',type='text',placeholder='Input grade here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Diligent'))] + [html.Td(dataframe['Diligent'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-3',type='text',placeholder='Input grade here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Interaction'))] + [html.Td(dataframe['Interaction'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-4',type='text',placeholder='Input grade here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Respect'))] + [html.Td(dataframe['Respect'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-5',type='text',placeholder='Input grade here..')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-att-button')),colSpan='2')] +
            [html.Td(html.Div(id='container-att'))]
        )]
        )

def submit_attendance(dataframe):
    '''return table for attendance submission'''
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Component','Data before submission','Input data']])] +
        #Body
        [html.Tr(
            [html.Td(html.P('School days'))] + [html.Td(dataframe['School days'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-attend-1',type='number',placeholder='Input value here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Days of late'))] + [html.Td(dataframe['Days of late'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-attend-2',type='number',placeholder='Input value here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Days of absent'))] + [html.Td(dataframe['Days of absent'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-attend-3',type='number',placeholder='Input value here..')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-attendance-button')),colSpan='2')] +
            [html.Td(html.Div(id='container-attendance'))]
        )]
        )

def grade_range():
    return html.Table(
        [html.Tr([html.Th('Range',style=center)] + [html.Th('Grade',style=center)]
            )] +
        [html.Tr([html.Td('90 - 100',style=center)] + [html.Td('A+',style=center)]
            )] +
        [html.Tr([html.Td('80 - 89',style=center)] + [html.Td('A',style=center)]
            )] +
        [html.Tr([html.Td('70 - 79',style=center)] + [html.Td('B+',style=center)]
            )] +
        [html.Tr([html.Td('60 - 69',style=center)] + [html.Td('B',style=center)]
            )] +
        [html.Tr([html.Td('50 - 59',style=center)] + [html.Td('C',style=center)]
            )] +
        [html.Tr([html.Td('0 - 49',style=center)] + [html.Td('F',style=center)]
            )],className="narrowtable"
        )