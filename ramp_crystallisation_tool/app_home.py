import dash_html_components as html
from . import app

'''
This script is setting up the home page of the app.
Any changes in the home page are controlled form here. 
Suggestion: big text blocks to be written using Markdown. 
'''

about = """
The purpose of this web tool is to help experimentalists working on the 
crystallisation of proteins to optimise their hit conditions by efficiently 
exploring the nearby crystallisation conditions. 
In initial crystallisation trials, researchers count on the commercial 
screens to obtain crystals. 
Once a crystal is obtained, the idea is to optimise these conditions again and 
again, until they have optimal crystallisation conditions, which give big, 
well-diffracted crystals most of the times.  
On each step of this process, we search for conditions in a close range 
around the hit conditions. 

A common struggle during protein crystallisation is that once an initial 
crystal has been obtained from a commercial screen, the optimisation of 
the hit conditions is not trivial. The task becomes even more challenging 
when users try to optimise some of the newest, more sophisticated screens. These screens 
have many complex conditions and a large number of variables (salts, 
buffers, precipitant, additives, pH, temperature…). The drawback of 
these screens are that as the complexity increases, the strangles of 
designing an optimisation strategy increases as well.
This tool is aiming to address this issue using condition search methods: 
grid search and Latin hypercube sampling. 
"""

list_text = '''
A list of all the MDL compatible with the tool can be found below
'''

notes_tips = """ To learn more on how to use the app, common bugs, and exceptions click the link below:
"""


about_html = [html.P(i) for i in about.split("\n\n")]

how_to_use = """ii 
 """

list_html = [html.P(i) for i in list_text.split("\n\n")]


notes_tips_html = [html.P(i) for i in notes_tips.split("\n\n")]


how_to_use_html = [html.P(i) for i in how_to_use.split("\n\n")]



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
                            html.B("More information about Molecular Dimensions crystallisation screens"),
                            href='https://www.moleculardimensions.com/products/c255-Crystallization-Screens/',
                            target='_blank')),
                            html.Img(src="assets/images/morpheus_screen.png", className="mor_screen",
                            height= 280, width = 380, style={'textAlign': 'justify'})
                ],
                className="info-container"),
            # html.Div(

            html.H2("How to use"),
            html.Div(
                html.Ol([
                    html.Li(html.P('Insert the code of the MDL screen (e.g. MD1-40) and the number of well of which conditions are to be optimised and press the SUBMIT button.')),
                    html.Li(html.P('A table containing the hit conditions will appear on the screen. Each element of the screen is editable. Simply press on the condition you wish and type. The number of reagents will be updated accordingly.')),
                    html.Li(html.P('The dimensions of the screen is set on 12x8, to cover in total 96 different crystallisation conditions. The user can enter the dimensions of the screen manually.')),
                    html.Li(html.P('Press the button to compute the optimised set of conditions. Then, download the CVS file that contain the suggested conditions.')), 
                ]),
                className="how_to-container"),

            html.H2("Tools"),
            html.Div(
                html.Ol([
                    html.Li(html.A('Compute initial condition', href='/grid/')),
                ]),
                className="sycolinks"),
            # html.P([
            #     "Find the code ",
            #     html.A(
            #         "on github",
            #         href="-- Add github here (?) --",
            #         target='_blank'), "."
            # ]),


            html.H2("Notes + Tips"),
            html.Div(notes_tips_html + [html.A('Notes + Tips',href='/notes+tips/')],
            className="notes_tips"),

            html.H2("MDL files"),
            html.Div(list_html + [html.A('MDL files',href='/MDL_files/')],
            className="mdl_files"),


            html.H2("Developed by"),
            html.Img(src="/assets/images/logos_combine.png", className="ramp_logo", 
                height= 200, width = 380, style={'textAlign': 'justify'}),
            html.H2("Affiliations"),
            html.Div(html.Ol([
                    html.Li(html.A('The initial version of the web app was based on the Synthesis Condition Finder.', 
                                        href='https://www.materialscloud.org/work/tools/sycofinder')), 

                    # html.Li('Special thanks to Dr Fabrice Gorrec for his useful advise and guidance during the initial stages of the project.')
                ]),
                className="affil")


        ],
        id="container",
        # tag for iframe resizer
        **{'data-iframe-height': ''}, style={ 'width': '60%',
            'padding': '20px',
            'margin': '20px',
            'justify-content': 'center','align-items': 'center',
        # 'width': '60%', 
        # 'margin': 'auto', 'padding': '10px'
        }
    )
]
