import dash
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
		[
			html.Hr(),
			html.H5("Submit new student"),
			html.Div(id='submit-name'),
		], className="sheet padding-10mm"
	)
