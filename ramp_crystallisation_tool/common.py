# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position,import-error,multiple-imports
from __future__ import print_function
from builtins import range  # pylint: disable=redefined-builtin
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import dash_html_components as html
import dash_table_experiments as dt
import base64
import io
import pandas as pd
import numpy as np\


'''
This script contains funtions that are used from different operation of the app 
during the use of the app. That is why common.py is exported in the beginning of the scripts. 
'''


def generate_table(dataframe, nsamples_x, nsamples_y, max_rows=100, download_link=True):
    '''
    This function is used from app_initia_cond_lhd.py nad app_initial_cond_grid.py 
    The function generate a numver of location for a 96-well screen and the respective 
    conditions. It is also produce a CVS file that can be dowloaded.  
    '''

    # print("dataframe.columns = ", len(dataframe.columns))
    components = []
    if download_link:

        letters = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
        numbers = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])

        total_nsamples = nsamples_x*nsamples_y
        well = ["" for x in range(total_nsamples)]
        
        well_x = [letters[i] for i in range(nsamples_x)]
        well_y = [numbers[j] for j in range(nsamples_y)]

        ll = 0
        for i in range(nsamples_x):
            for j in range(nsamples_y):
                ll = ll+1
                counter = well_x[i] + well_y[j]
                well[ll-1] = counter


        # well = np.array(['A1', 'A2', 'A3', 'A4','A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
        #                 'B1', 'B2', 'B3', 'B4','B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
        #                 'C1', 'C2', 'C3', 'C4','C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
        #                 'D1', 'D2', 'D3', 'D4','D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
        #                 'E1', 'E2', 'E3', 'E4','E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
        #                 'F1', 'F2', 'F3', 'F4','F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
        #                 'G1', 'G2', 'G3', 'G4','G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',
        #                 'H1', 'H2', 'H3', 'H4','H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12'])
        dataframe.insert(0, 'Well #', well, True)
        csv_string = dataframe.to_csv(
            index=False, encoding='utf-8', float_format='%.2f')
        link = html.Tr([html.Td(html.A(
                                            'Download CSV',
                                            download="initial_crytallisation_conditions.csv",
                                            href="data:text/csv;charset=utf-8," +
                                            urllib.parse.quote(csv_string),
                                            target="_blank",
                                            className='button'))])
        components.append(link)

    components.append(
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in dataframe.columns])] +

            # Body
            [
                html.Tr([
                    html.Td(cell_format(dataframe.iloc[i][col]))
                    for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ]))
    return components


def cell_format(value):
    if isinstance(value, float):
        return "{:.3f}".format(value)
    return value


# pylint: disable=unused-variable,unused-argument
''' 
Un-comment the following in case you want to use the option of uploading a cvs or xlxs file 
in the app. 
'''

# def parse_contents(contents, filename, date):
#     content_type, content_string = contents.split(',')

#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div(['There was an error processing this file.'])

#     return df


# def parse_data(content, name, date):
#     if content is None:
#         return None, None

#     try:
#         df = parse_contents(content, name, date)
#         validate_df(df)
#     except ValueError as e:
#         return None, html.P(str(e), className="error")

#     nrows = len(df)
#     fitness = df.iloc[:, -1]
#     msg = "Found {} experiments, with fitness from {} to {}.".format(
#         nrows, fitness.min(), fitness.max())

#     return df.to_json(date_format='iso', orient='split'), html.P(msg)


# styles
HIDE = {'display': 'none'}
SHOW = {}

#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})
