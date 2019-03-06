import dash
import dash_core_components as dcc
import dash_html_components as html

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

layout = html.Div(
		[
			html.Hr(),
			html.H5("Reports of all Academics Achievement - Teacher's Note"),
			html.Div(id='display-notes'),
			html.Hr(),
			html.P('Select the subject you wish to submit the notes:'),
			html.Div([dcc.Dropdown(
				id='subject-dropdown',
				options=[{'label':i,'value':j} for i,j in zip(subject.values(),subject.keys())],
				placeholder="Select subject"
				)]		
			),
            html.Br(),
			html.Div(id='submit-subject-notes')
		], className="sheet padding-10mm"
		)
		
