 # -*- coding: utf-8 -*-
from ramp_crystallisation_tool import app, app_home, app_initial_cond, maxmin
import dash.dependencies as dep
import encodings.idna



@app.callback(
    dep.Output('page-content', 'children'), [dep.Input('url', 'pathname')])
def display_page(pathname):
    # pylint: disable=no-else-return
    if pathname is None:
        return app_home.layout

    if pathname.endswith('/maxdiv/'):
        return app_initial_cond.layout
    # if pathname.endswith('/maxdiv_test_link/'):
    #     return app_test_link.layout
    return app_home.layout

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
