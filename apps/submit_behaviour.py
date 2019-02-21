import dash
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
		[
			html.Hr(),
			html.H5("Report of Behaviour or Affectiveness for submission"),
			html.Div(id='submit-attitude'),
		], className="sheet padding-10mm"
	)

