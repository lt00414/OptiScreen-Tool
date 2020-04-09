import dash_html_components as html
from . import app

about = """
The following tool provides the user with an initial configuration to set the 
crystallisation plates. It can be use for different crystallisation plates, although 
it was specifically designed for the MORPHEUS crystallisation plates, designed 
by Molecular Dimenstions. 
"""
about_html = [html.P(i) for i in about.split("\n\n")]



morpheus_screen_disctription = """
A MORPHEUS screen has dimensions 12x8, so in total 96 different conditions are covered. 
"""
morpheus_screen_disctription_html = [html.P(i) for i in morpheus_screen_disctription.split("\n\n")]


layout = [
    html.Div(
        [
            html.Div(html.H1(app.title), id="maintitle"),
            html.H2("About"),
            # html.Img(src="assets/images/logos_combine.png", className="ramp_logo", 
            #     height= 200, width = 380, style={'textAlign': 'justify'}),
            # html.Img(src="assets/images/eu_logo.png", className="eu_logo",
            #     height= 50, width = 80, style={'textAlign': 'justify'}),
            # html.Img(src="assets/images/surrey_logo.png", className="sur_logo",
            #     height= 70, width = 150, style={'textAlign': 'justify'}),
            html.Div(
                about_html + [
                    html.P(
                        html.A(
                            html.B("More information about the MORPHEUS screens"),
                            href='https://www2.mrc-lmb.cam.ac.uk/groups/JYL/PDF/morpheus%202009.pdf',
                            target='_blank')),
                ],
                className="info-container"),
            html.Div(
                    morpheus_screen_disctription_html + [
                    html.P(
                        html.A(
                            html.B("MORPHEUS screens are available here"), 
                            href='https://www.moleculardimensions.com/products/2734-Morpheus-HT-96',
                            target='_blank')),
                             html.Img(src="assets/images/morpheus_screen.png", className="mor_screen",
                            height= 280, width = 380, style={'textAlign': 'justify'})

                ],
                className="info-container"),
            html.H2("Steps"),
            html.Div(
                html.Ol([
                    html.Li(html.A('Compute initial condition with grid', href='maxdiv/')),
                    # html.Li(html.A('Optimise screen using latin hybercube sampling', href='maxdiv_test/')),
                ]),
                className="sycolinks"),
            html.P([
                "Find the code ",
                html.A(
                    "on github",
                    href="-- Add github here (?) --",
                    target='_blank'), "."
            ]),
            html.H2("Developed by"),
            html.Img(src="assets/images/logos_combine.png", className="ramp_logo", 
                height= 200, width = 380, style={'textAlign': 'justify'}),
        ],
        id="container",
        # tag for iframe resizer
        **{'data-iframe-height': ''}
        
     
        

    )
]
