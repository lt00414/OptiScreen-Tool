 # -*- coding: utf-8 -*-
from ramp_crystallisation_tool import app, app_home, app_initial_cond_grid, app_initial_cond_lhs, maxmin, app_notes_and_tips, app_database
import dash.dependencies as dep

'''
This is the main script that compile to run the app.
When you want to deploy the app with google cloud, 
cp this file to main.py
'''


@app.callback(
    dep.Output('page-content', 'children'), [dep.Input('url', 'pathname')])
        
#####
# Depending on the pathway, a different part of the app will appear. 
# If you want to add new pages or change the path of the existent ones, 
# go to app_home.py and change the href, e.g. find  href='/grid/' and 
# cahnge it accordingly.
#####


def display_page(pathname):
    if pathname is None:
        return app_home.layout
    if pathname.endswith('/grid/'):
        return app_initial_cond_grid.layout
    elif pathname.endswith('/lhs/'):
        return app_initial_cond_lhs.layout
    elif pathname.endswith('/notes+tips/'):
        return app_notes_and_tips.layout
    elif pathname.endswith('/MDL_files/'):
        return app_database.layout
    return app_home.layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
