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

sub_grade = ['{}_grade'.format(sub) for sub in subject.keys()]
sub_marks = ['{}_marks'.format(sub) for sub in subject.keys()]
sub_com = ['{}_comments'.format(sub) for sub in subject.keys()]

layout = html.Div(
		[
			html.Hr(),
			html.H5('Reports of all Academics Achievement'),
			html.Div(id='display-grade'),
			html.Br(),
			html.P('Select the subject you wish to submit the marks:'),
			html.Div([dcc.Dropdown(
				id='subject-dropdown',
				options=[{'label':i,'value':j} for i,j in zip(subject.values(),subject.keys())],
				placeholder="Select subject"
				)]		
			),
			html.Div(id='submit-subject-marks')
		], className="sheet padding-10mm"
	)

