import dash_html_components as html
from . import app

about = """
In this page you can find useful tips of how to use the tool and get inform about updates, 
issues adn changes. The app is heavily depending on your contributions, either that is 
an new idea of how to make the tool more useful or reports of issues. Feel free to contact 
me at  enquiries@moleculardimensions.com for any issues regarding this tool. 
"""

notes = """The tool is under development and unfortunately there some 
MDL screens that are not yet available for optimisation. These screens are 
the following:
"""

tips = """ Some tips when using the tool: """

about_html = [html.P(i) for i in about.split("\n\n")]
notes_html = [html.P(i) for i in notes.split("\n\n")]
tips_html = [html.P(i) for i in notes.split("\n\n")]

layout = [
 html.Div(
        [
            html.Div(html.H1(app.secondary_title), id="secondary_itle"),
            html.H2("About"),
            # html.Img(src="assets/images/logos_combine.png", className="ramp_logo", 
            #     height= 200, width = 380, style={'textAlign': 'justify'}),
            # html.Img(src="assets/images/eu_logo.png", className="eu_logo",
            #     height= 50, width = 80, style={'textAlign': 'justify'}),
            # html.Img(src="assets/images/surrey_logo.png", className="sur_logo",
            #     height= 70, width = 150, style={'textAlign': 'justify'}),
            html.Div(about_html, className="basic_info_container"),

            html.H2("Tips"),
            html.Div(tips_html + [
                            html.Ol([
                                html.Li(html.P('Be careful when typing the code name of the screen and the hitwell. Spaces or misuse of capital letters might effect on the performance.')),
                                html.Li(html.P('An error message will appear when something is not working right, but we might have missed a case. If nothing appears on your screen, it means that came across a bug. That is great, it means that we can now receive your input and improve the tool.')),
                                html.Li([html.P('We are looking forward on impoving the tool by receiving your feedback. For all enquires of how to use the tool, suggestions and reports of errors please contact:'),
                                html.A('enquiries@moleculardimensions.com', href=' ',target="_blank")])
                            ])], className="notes"),

            html.H2("Notes"),
            html.Div(notes_html + [
                            html.Ol([
                                html.Li(html.P('CryoSol')),
                                html.Li(html.P('MD1-47')),
                                html.Li(html.P('MD1-48')),
                                # html.Li(html.P('MD1-68')),
                                # html.Li(html.P('MD1-91-92')), 
                                html.Li(html.P('MD1-93')),
                                html.Li(html.P('MD1-100')),
                                # html.Li(html.P('MD1-116_117')),
                                html.Li(html.P('MD1-118')),
                                html.Li(html.P('MD1-123')),

                            ])], className="notes")], id="main_container",
                    **{'data-iframe-height': ''}, style={ 'width': '60%',
            'padding': '20px',
            'margin': '20px',
            'justify-content': 'center','align-items': 'center',
        # 'width': '60%', 
        # 'margin': 'auto', 'padding': '10px'
        }
    )
]

