# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from builtins import range  # pylint: disable=redefined-builtin
import dash_table
import collections
import os 
import fnmatch
import glob
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import xlrd   
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#import dash_table_experiments as dt
from .common import generate_table


import pandas as pd
import numpy as np
#from . import uniform
from . import maxmin
from . import app
import chart_studio.plotly as plt

# pylint: disable=redefined-builtin
script_path = os.path.dirname(os.path.realpath(__file__))
myPath= os.path.join( script_path,'MDL_screens_database')


###############################################################################
def get_controls_var(id, desc, unit, range):
    """Get controls for each variable.

    This includes
     * the description
     * range 
    """
    label_reagent = dcc.Input(
        id=id + "_label", type='text', value=desc, className="label")
    unit_reagent = dcc.Input(
        id=id + "_unit", type='text', value=unit, className="label")
    range_low = dcc.Input(
        id=id + "_low", type='number', value=range[0], className="range")
    range_high = dcc.Input(
        id=id + "_high", type='number', value=range[1], className="range")

    return html.Tr([
        html.Td(label_reagent),
        html.Td(unit_reagent),
        html.Td([range_low, html.Span('to'), range_high])], id=id + "_tr")

#------------------------------------------------------------------------------


###############################################################################
def get_controls_screen(id, desc, range):
    """ Get screen dimensions nsamples_x and nsamples_y
    """
    label = dcc.Input(id = id + "_label", type = 'text', value=desc,
        className = 'label')
    dimensions_x = dcc.Input(
        id=id + "_x", type='number', value=range[0], className="range")
    dimensions_y = dcc.Input(
        id=id + "_y", type='number', value=range[1], className="range")
    return html.Tr([
        html.Td(label),
        html.Td([dimensions_x, html.Span('\\times'), dimensions_y])], id=id + "_tr")
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------

code = collections.OrderedDict([
    ('code_number',
     dict(label=['MDL file code'])),
    ])


##############################################################################
# reagents_grid = collections.OrderedDict([
#     ('reagent_1_grid', dict(label='Reagent 1', unitslabel='[Units 1]', range=[100.0, 200.0])),
#     ('reagent_2_grid', dict(label='Reagent 2', unitslabel='[Units 2]', range=[1.0, 6.0]))])

# NVARS_DEFAULT = len(reagents_grid)


# Fill up to NVARS_MAX (needed to define callbacks)
NVARS_MAX = 10
# for i in range(len(reagents_grid), NVARS_MAX):
#     k = 'Reagent {}'.format(i + 1)
#     l = '[Units {}]'.format(i + 1)
#     reagents_grid[k] = dict(label=k,  unitslabel=l, range=[0, 1])

# var_grid_ids = list(reagents_grid.keys())
# print('var_grid_ids', var_grid_ids )

# # var_labels = [v['label'] for v in list(reagents_grid.values())]


# controls_dict = collections.OrderedDict()
# for k, v in list(reagents_grid.items()):
#     controls = get_controls_var(k, v['label'], v['unitslabel'], v['range'])
#     print("controls (l.104): \n",type(controls))
#     controls_dict[k] = controls


# head_row = html.Tr([
#     html.Th('Reagent   '),
#     html.Th('[Units]  '),
#     html.Th('Range  ')
# ])

# controls_html = html.Table(
#     [head_row] + list(controls_dict.values()), id='controls_grid')
# label_states = [State(k + "_label", 'value') for k in var_grid_ids
# ]
# unit_states = [State(l + "_label", 'value') for l in var_grid_ids
# ]
# low_states = [State(k + "_low", 'value') for k in var_grid_ids]
# high_states = [State(k + "_high", 'value') for k in var_grid_ids]
# # weight_states = [
# #     dash.dependencies.State(k + "_weight", 'value') for k in var_ids
# # ]




inp_code_hitwell = html.Tr([
    html.Td('Enter screen code (e.g. MD1-40) and hit well (e.g. B1):'),
    html.Td(dcc.Input(id='inp_code_grid',
            type='text', 
            value="MD1-40")),
    html.Td(dcc.Input(
            id='inp_hitwell_grid',
            type='text', 
            value="B1")),
    html.Div('', id='input_info_grid')])

btn_submit = html.Div([html.Td(html.Button('Search', id = 'submit-button_grid', className='action-button', n_clicks=0)),
    html.Div('', id='submit_info_grid')
    ])

###########################################################################################
grid_text = '''
Grid search is the process of searching on the nearby space of a set of data for the optimal 
parameters. Here, the search is performed by separating the two-dimensional space equally 
and then dividing the given range into equally distributed spaces. The result is a set of 96 
conditions that cover the whole range. 

In this implementation, the grid search is limited to the search of **two conditions**, depending 
on the parameters in the hit well. There is now the option to choose the two conditions that 
are to be varied, and the minimum and maximum values to vary the reagents over. By default,
salt concentrations will be multiplied and divided by 2, precipitants by 4, and buffer pH 
will be +1 and -1.
'''
grid_text_html = dcc.Markdown(grid_text)
# [html.P(i) for i in grid_text.split("\n\n")]

grid_layout = html.Div([html.H2("Grid search (2 Reagents): "),
                    dcc.Markdown(grid_text, className="text-container", id="grid_container",
                    # **{'data-iframe-height': ''}, 
                    style={ 'width': '100%','padding': '5px', 
                    'margin': '10px','justify-content': 'center','align-items': 'center'})])
lhs_text = """
Latin hypercube sampling (LHS) is a sampling method for searching for optimal 
parameters in a high dimensional space. The LHS is a near-random method, i.e. 
the optimised condtions are not completely random, instead they obey certain 
requirements. These requirements assure that the final sample points 
will be spread more evenly across the range. LHS can be used for high-dimension 
spaces, i.e. for more than two conditions.

This implementation allows you to choose as many reagents as are in the well.
At the current time, only the first three reagents chosen will allow the option
to change the minimum and maximum range to sample over. The default ranges are 
the same as for the grid search. In the future we hope to allow you to
edit the range for all reagents in the well.
"""
lhs_text_html = [html.P(i) for i in lhs_text.split("\n\n")]

lhs_layout = html.Div( [html.H2("Latin Hybercube Sampling (2+ Reagents): "),
                    dcc.Markdown(lhs_text, className="text-container", id="lhs_container",
                    # **{'data-iframe-height': ''}, 
                    style={ 'width': '100%','padding': '5px', 
                    'margin': '10px','justify-content': 'center','align-items': 'center'})])

###########################################################################################




##############################################################################
# print("label_states, type(label_states)", label_states, type(label_states))
states = [State('inp_code_grid', 'value')]
states += [State('inp_hitwell_grid', 'value')]


@app.callback(
    Output('submit_info_grid', 'children'), 
    [Input('submit-button_grid', 'n_clicks')],
    states)
def update_output_code_hitwell(n_clicks, *args):
    hitwell = args[-1]
    code_name = args[-2]


    code_name = code_name + "*"
    counter = 0
    file_list = []
    for file in os.listdir(myPath):
        if fnmatch.fnmatch(file, code_name):
            file_list.append(file)
    file_list.sort()
    print(file_list)
    if len(file_list) > 1:
        file_found = file_list[0]
    elif len(file_list) == 1:
        file_found = file_list[0]
    print ("The file you called is: \n", file_found)
    newpath = os.path.join(myPath, file_found)
    xls = pd.ExcelFile(newpath)
    df1 = pd.read_excel(xls)
    print("hitwell type: ", type(hitwell))
    searchedValue = hitwell
    print("searchedValue type: ", type(searchedValue))
    tube = df1.filter(like='Tube').columns
    print("tube:", tube)
    well = df1.filter(like='Well').columns

    if well.empty == True: 
        print('tube and tube number:', searchedValue)
        # df_searchedValue = df1[df1["Tube #"] == searchedValue]
        try:
            df_searchedValue = df1[df1["Tube #"] == int(searchedValue)]
            print("df_searchedValue \n", df_searchedValue)
        except:
            print("Something went wrong, try something new")
            df_searchedValue = df1[df1["Tube #"] == searchedValue]
            print("df_searchedValue \n", df_searchedValue)

        df_new = df1.set_index("Tube #", drop = False)
        df_new.astype('str') 
        print("df_new \n", df_new)
        df_hit_well = df_searchedValue
        print("df_hit_well \n", df_hit_well)
        print("type(df_hit_well) =  ", type(df_hit_well.index))
    else: 
        try:
            df_searchedValue = df1[df1["Well #"] == searchedValue]
            df_new = df1.set_index("Well #", drop = False)
            df_hit_well = df_new.loc[[searchedValue]]
            print("df_hit_well \n", df_hit_well)
            print("type(df_hit_well) =  ", type(df_hit_well.index))
        except:
            return ([ html.Tr([ html.Td(dcc.Textarea(
                placeholder=' ',
                value='An error occurred. Check if the inputs are correct. If there the error persists, please report at: enquiries@moleculardimensions.com',
                style={'width': '50%'}))]), 0])

    
    df_hit_well = df_hit_well.replace(r'None', np.nan)
    df_hit_well = df_hit_well.replace(r'-', np.nan)
    df_hit_values = df_hit_well.dropna(axis='columns')
            
    rows = np.shape(df_hit_values)[0]
    columns = np.shape(df_hit_values)[1]
    concentrations = df_hit_values.filter(like='Conc').columns
    kk = dash_table.DataTable(
                                id='table_grid',
                                data=df_hit_values.to_dict('records'), editable=True,
                                columns=[{"name": i, "id": i} for i in df_hit_values.columns], 
                                fixed_columns={ 'headers': True, 'data': 1}, 
                                style_cell = {
                                # all three widths are needed
                                'minWidth': '180hpx', 'width': '100px', 'maxWidth': '180px',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                },style_as_list_view=True,) 

    nvars_new = len(concentrations)

    salts_labels = df_hit_values.filter(like='Salt').columns.values
    buff_labels = df_hit_values.filter(like='Buffer').columns.values
    perci_labels = df_hit_values.filter(like='Precipitant').columns.values
    units_labels = df_hit_values.filter(like='Unit').columns.values

    reagent_name = np.concatenate([df_hit_values.iloc[0][salts_labels[:]], df_hit_values.iloc[0][buff_labels[:]], df_hit_values.iloc[0][perci_labels[:]] ])
    reagent_name = reagent_name.tolist()
    name_salts = np.concatenate([df_hit_values.iloc[0][salts_labels[:]]])
    name_salts = name_salts.tolist()
    name_buffs = np.concatenate([df_hit_values.iloc[0][buff_labels[:]]])
    name_buffs = name_buffs.tolist()
    name_precips = np.concatenate([df_hit_values.iloc[0][perci_labels[:]]])
    name_precips = name_precips.tolist()

    hidden_reagent = html.Td([
            dcc.Dropdown(
                id='hidden_dropdown',            
                options=[{'label':name, 'value':name} for name in reagent_name],
                value = reagent_name[0]
                ),
                ],style={'display':'none'})

        
    if n_clicks > 0:
        return ([html.Div([html.Tr([html.Td(kk),html.Td(hidden_reagent)])])])
#------------------------------------------------------------------------------

multi_reagents = html.Td([
    html.Span('Choose Reagents: '),
    dcc.Dropdown(
        id='multi_reagents',
        multi=True,
        style={'margin-bottom':'10px','width':'80%'}
    ),
    html.Div(id='multi_reagents_adj')
])
@app.callback(
    dash.dependencies.Output('multi_reagents','options'),
    [dash.dependencies.Input('hidden_dropdown','options')]   
)
def update_multi_reagents(opt):
    return opt
    
@app.callback(
    [dash.dependencies.Output('multi_reagents_adj','children')],
    [dash.dependencies.Input('multi_reagents','value')]   
)
def generate_adjustors(selected):
    LABELS = {}
    for each in range(len(selected)):
        if len(selected) > 3:
            break
        LABELS[each+1]= html.Tr([dcc.Input(
            id=generate_adjustor_id(each+1),
            value=selected[each],
            disabled=True,
            style={'margin-bottom':'10px'}),
        html.Span('Min: ',style={'margin-left':'5px'}),
        dcc.Input(
            id=generate_min_id(each+1),
            type='number',
            placeholder='optional',
            style={'width':'100px'}
        ),
        html.Span('Max: ',style={'margin-left':'5px'}),
        dcc.Input(
            id=generate_max_id(each+1),
            type='number',
            placeholder='optional',
            style={'width':'100px'}
        ) 
        ])
        
    List = []
    if len(selected) == 2:
        LABELS[3]= html.Tr([
            dcc.Input(
            id='min_3',
            style={'display':'none'}
        ),
        dcc.Input(
            id='max_3',
            style={'display':'none'}
        ),
        ])
    if len(selected) == 1:
        List.append(LABELS[1])
        return List
    for i in range(3):
        List.append(LABELS[i+1])
    return [html.Div(
        List
    )]

def generate_adjustor_id(value):
    return 'adjustor_{}'.format(value)
def generate_min_id(value):
    return 'min_{}'.format(value)
def generate_max_id(value):
    return 'max_{}'.format(value)


inp_nsamples = html.Tr([
    html.Td('Enter screen dimensions '),
    html.Td(
        dcc.Input(
            id='nsamples_x_grid', type='number', value=8,
            className="nsamples range")), 
    html.Td(html.Span('x')),
    html.Td(
        dcc.Input(
            id='nsamples_y_grid', type='number', value=12,
            className="nsamples range"))
])

##############################################################################
#------------------------------------------------------------------------------

grid_compute = html.Div([
    html.Button('Grid method', id='btn_compute_grid', className='action-button', n_clicks = 0),
    html.Div('', id='compute_info_grid')
])
lhs_compute = html.Div([
    html.Button('Latin Hypercube', id='btn_compute_lhs', className='action-button', 
        n_clicks = 0),
    html.Div('', id='compute_info_lhs')
])


# Creation of dash app

layout = html.Div(
    [
        html.H1(['Optimisation of Hit Conditions'],style={'text-align':'center'}),
        html.Tr([
            html.Td([grid_layout]),
            html.Td([lhs_layout])
            ]),
        html.Table([inp_code_hitwell]),
        html.Br(),
        html.Table([btn_submit]),
        html.Br(),
        html.Table([multi_reagents],style={'width':'50%'}),
        html.Br(),
        html.Table([inp_nsamples]),
        html.Tr([
            html.Td([grid_compute]),
            html.Td([lhs_compute])
            ])
    ],
    style={'padding': 20},
    id="container_grid",
    # tag for iframe resizer
    **{'data-iframe-height': ''},
)
#------------------------------------------------------------------------------

#############################################################################

#------------------------------------------------------------------------------
ninps = 11
# print("label_states, type(label_states)", label_states, type(label_states))
# states = label_states + unit_states + low_states + high_states
states = [State('max_3','value')]
states += [State('min_3','value')]
states += [State('max_2','value')]
states += [State('min_2','value')]
states += [State('max_1','value')]
states += [State('min_1','value')]
states += [State('multi_reagents','value')]
states += [State('nsamples_x_grid', 'value')]
states += [State('nsamples_y_grid', 'value')]
states += [State('inp_code_grid', 'value')]
states += [State('inp_hitwell_grid', 'value')]

# ##############################################################################


@app.callback(
    dash.dependencies.Output('compute_info_grid', 'children'),
    [dash.dependencies.Input('table_grid', 'data'),
     dash.dependencies.Input('btn_compute_grid', 'n_clicks')
     ], states)
def on_compute(submit_info, n_clicks, *args):
    print("worked")
    """Callback for clicking compute button"""
    if n_clicks is None :
        return ''

    df_hit_values = pd.DataFrame(submit_info)
    #if len(args) != ninps:
        #raise ValueError("Expected {} arguments".format(ninps))

    # parse arguments
    hitwell = args[-1]
    code_name = args[-2]
    nsamples_y = args[-3]
    nsamples_x = args[-4]
    choices = args[-5]
    first_min = args[-6]
    first_max = args[-7]
    second_min = args[-8]
    second_max = args[-9]
    

    if len(choices) > 2:
        return dcc.Textarea(
                placeholder='Wrong number of reagents...',
                value='Grid search requires exactly 2 reagents',
                style={'width': '100%'}
                )  

    n_pH = len(df_hit_values.filter(like='pH').columns)
    n_units = len(df_hit_values.filter(like='Units').columns)
    n_salts = len(df_hit_values.filter(like='Salt').columns)
    n_buff =  len(df_hit_values.filter(like='Buffer').columns)
    n_precip = len(df_hit_values.filter(like='Precipitant').columns)
    
    concentrations = df_hit_values.filter(like='Conc').columns
    var = df_hit_values[concentrations].to_numpy()
    var = var.T
    var_float = var.astype(np.float)

    pH =  df_hit_values.filter(like='pH').columns
    pH = df_hit_values[pH].to_numpy()
    
    salt_conc = var[0:n_salts]
    buff_conc = var[(n_salts):(n_salts+n_buff)]
    precip_conc = var[(n_salts+n_buff):(n_salts+n_buff+n_precip)]

    # VARY RANGE OF CONCERN: 
    # For grid we can only use two parameters. I chose the salt conconcetration
    # low_vals = np.array([args[i + NVARS_MAX] for i in range(nvars)])
    # high_vals = np.array([args[i + 2 * NVARS_MAX] for i in range(nvars)
    # NOTE: check if salt_conc, ph and precip_conc are float arrays. This check is 
    # important, cause after the user will update the number in the table, 
    # the values are parsed as str.

    # low_vals = np.array([args[i + NVARS_MAX] for i in range(nvars)])
    # high_vals = np.array([args[i + 2 * NVARS_MAX] for i in range(nvars)])

    nvars = n_salts + n_pH + n_precip
    nsamples = nsamples_x*nsamples_y

    salts_labels = df_hit_values.filter(like='Salt').columns.values
    buff_labels = df_hit_values.filter(like='Buffer').columns.values
    perci_labels = df_hit_values.filter(like='Precipitant').columns.values

    choice_types = [None,None]
    choice_index = [0,0]
    name_salts = np.concatenate([df_hit_values.iloc[0][salts_labels[:]]])
    name_salts = name_salts.tolist()
    for i in range(0,2):
        if choices[i] in name_salts:
            choice_types[i] = "salt"
            choice_index[i] = name_salts.index(choices[i])
    name_buff = np.concatenate([df_hit_values.iloc[0][buff_labels[:]]])
    name_buff = name_buff.tolist()
    for i in range(0,2):
        if choices[i] in name_buff:
            choice_types[i] = "buff"
            choice_index[i] = name_buff.index(choices[i])

    name_perci = np.concatenate([df_hit_values.iloc[0][perci_labels[:]]])
    name_perci = name_perci.tolist()
    for i in range(0,2):
        if choices[i] in name_perci:
            choice_types[i] = "precip"
            choice_index[i] = name_perci.index(choices[i])

    print("pH", pH[choice_index[1]])

    units_labels = df_hit_values.filter(like='Unit').columns.values
    units_labels_salts = units_labels[0:n_salts]
    units_labels_buff = units_labels[(n_salts):(n_salts+n_buff)]
    units_labels_perci = units_labels[(n_salts+n_buff):(n_salts+n_buff+n_precip)]
    unit_name_salts = np.concatenate([df_hit_values.iloc[0][units_labels_salts[:]]])
    unit_name_buff = np.concatenate([df_hit_values.iloc[0][units_labels_buff[:]]])
    unit_name_perci = np.concatenate([df_hit_values.iloc[0][units_labels_perci[:]]])

    print("units_labels = \n", units_labels)
    print("units_labels_salts = \n", units_labels_salts)
    print("units_labelslabels_buff = \n", units_labels_buff)
    print("units_labels_perci = \n", units_labels_perci)

    reagent_name = np.concatenate([df_hit_values.iloc[0][salts_labels[:]], df_hit_values.iloc[0][buff_labels[:]], df_hit_values.iloc[0][perci_labels[:]] ])
    reagent_name = reagent_name.tolist()

    labels = reagent_name 
    # dim = len(labels_array)
    dim = 2 # because for grid we always want two dimensions 
    styling_label_1 = [' ['] * dim
    styling_label_2 = [']'] * dim
    label = ["" for x in range(dim)]

    #Calculate the max and min values.
    #By default salts are *2 /2, precips are *4 /4 and buffers are +1 -1
    low_vals = [first_min,second_min]
    high_vals = [first_max,second_max]
    for i in range(0,2):
        if choice_types[i] == "salt":
            if low_vals[i] == None:
                low_vals[i] = salt_conc[choice_index[i]]/2
            if high_vals[i] == None:
                high_vals[i] = salt_conc[choice_index[i]]*2
            label[i] = choices[i] + styling_label_1[0] + unit_name_salts[choice_index[i]] + styling_label_2[0]
        elif choice_types[i] == "buff":
            if low_vals[i] == None:
                low_vals[i] = pH[choice_index[i]]-1
            if high_vals[i] == None:
                high_vals[i] = pH[choice_index[i]]+1
            label[i] = choices[i] + styling_label_1[0] + 'pH' + styling_label_2[0]
        elif choice_types[i] == "precip":
            if low_vals[i] == None:
                low_vals[i] = precip_conc[choice_index[i]]/4
            if high_vals[i] == None:
                high_vals[i] = precip_conc[choice_index[i]]*4
            label[i] = choices[i] + styling_label_1[0] + unit_name_perci[choice_index[i]] + styling_label_2[0]
        else:
            return dcc.Textarea(
                placeholder='Enter a value...',
                value='An error occurred. Please report at: enquiries@moleculardimensions.com',
                style={'width': '40%'}
                )  
    
    #print("Range for grid method: \n", grid_var_range[0], grid_var_range[1])
    #low_vals = np.concatenate([grid_var_range[0][0], grid_var_range[1][0]])
    #high_vals = np.concatenate([grid_var_range[0][1], grid_var_range[1][1]])

 
    # For grid the NVARS must be always 2 cause   
    samples_1 = maxmin.compute_grid(nsamples_x, nsamples_y, low_vals, high_vals,  NVARS = 2)
    df = pd.DataFrame(data=samples_1, columns=label)
    table = generate_table(df, nsamples_x, nsamples_y, download_link=True)
    np.set_printoptions(precision=3)
    if n_clicks > 0:
        try:
            return table
        except: 
            return html.Div('An error occurred')

#------------------------------------------------------------------------------

@app.callback(
    dash.dependencies.Output('compute_info_lhs', 'children'),
    [dash.dependencies.Input('table_grid', 'data'),
     dash.dependencies.Input('btn_compute_lhs', 'n_clicks'),
     ], states)
def on_lhs_compute(submit_info, n_clicks, *args):
    """Callback for clicking compute button"""
    print("worked")
    if n_clicks is None :
        return ''

    df_hit_values = pd.DataFrame(submit_info)
    #if len(args) != ninps:
        #raise ValueError("Expected {} arguments".format(ninps))

    # parse arguments
    hitwell = args[-1]
    code_name = args[-2]
    nsamples_y = args[-3]
    nsamples_x = args[-4]
    choices = args[-5]
    first_min = args[-6]
    first_max = args[-7]
    second_min = args[-8]
    second_max = args[-9]
    third_min = args[-10]
    third_max = args[-11]

    num_of_choices = len(choices)
    
    ###
    # Count how many columns from each category are on the selected file
    ###
    n_pH = len(df_hit_values.filter(like='pH').columns)
    n_units = len(df_hit_values.filter(like='Units').columns)
    n_salts = len(df_hit_values.filter(like='Salt').columns)
    n_buff =  len(df_hit_values.filter(like='Buffer').columns)
    n_precip = len(df_hit_values.filter(like='Precipitant').columns)
    
    ###
    # Only the values of concentration and pH are going to change 
    ###
    concentrations = df_hit_values.filter(like='Conc').columns
    var = df_hit_values[concentrations].to_numpy()
    var = var.T
    var_float = var.astype(np.float)

    pH =  df_hit_values.filter(like='pH').columns
    pH = df_hit_values[pH].to_numpy()
    
    ###
    # In the following lines, the values of the concentration for salt/prec/buffer are assigned. 
    # The format of the file is crucial in order the following to work.
    ###
    salt_conc = var[0:n_salts]
    buff_conc = var[(n_salts):(n_salts+n_buff)]
    precip_conc = var[(n_salts+n_buff):(n_salts+n_buff+n_precip)]

    # VARY RANGE OF CONCERN --- ATTEMPTS TO MAKE THE RANGE CHANGE 
    # low_vals = np.array([args[i + NVARS_MAX] for i in range(nvars)])
    # high_vals = np.array([args[i + 2 * NVARS_MAX] for i in range(nvars)
    # NOTE: check if salt_conc, ph and precip_conc are float arrays. This check is 
    # important, cause after the user will update the number in the table, 
    # the values are parsed as str. 

    pH = pH.astype(float)
    pH = pH.T
    salt_conc = salt_conc.astype(float)
    precip_conc = precip_conc.astype(float)

    salts_labels = df_hit_values.filter(like='Salt').columns.values
    buff_labels = df_hit_values.filter(like='Buffer').columns.values
    perci_labels = df_hit_values.filter(like='Precipitant').columns.values

    choice_types = [None]*num_of_choices
    choice_index = [0,0]*num_of_choices
    name_salts = np.concatenate([df_hit_values.iloc[0][salts_labels[:]]])
    name_salts = name_salts.tolist()
    for i in range(0,num_of_choices):
        if choices[i] in name_salts:
            choice_types[i] = "salt"
            choice_index[i] = name_salts.index(choices[i])
    name_buff = np.concatenate([df_hit_values.iloc[0][buff_labels[:]]])
    name_buff = name_buff.tolist()
    for i in range(0,num_of_choices):
        if choices[i] in name_buff:
            choice_types[i] = "buff"
            choice_index[i] = name_buff.index(choices[i])

    name_perci = np.concatenate([df_hit_values.iloc[0][perci_labels[:]]])
    name_perci = name_perci.tolist()
    for i in range(0,num_of_choices):
        if choices[i] in name_perci:
            choice_types[i] = "precip"
            choice_index[i] = name_perci.index(choices[i])

    #salt_range = [salt_conc[:]/2, salt_conc[:]*2]
    #pH_range = [pH[:]-1, pH[:]+1]
    #precip_range = [precip_conc[:]/4, precip_conc[:]*4]

    #low_vals = np.concatenate([salt_range[0], pH_range[0], precip_range[0]])
    #high_vals = np.concatenate([salt_range[1], pH_range[1], precip_range[1]])

    nvars = n_salts + n_pH + n_precip
    nsamples = nsamples_x*nsamples_y

    units_labels = df_hit_values.filter(like='Unit').columns.values
    units_labels_salts = units_labels[0:n_salts]
    units_labels_buff = units_labels[(n_salts):(n_salts+n_buff)]
    units_labels_perci = units_labels[(n_salts+n_buff):(n_salts+n_buff+n_precip)]
    unit_name_salts = np.concatenate([df_hit_values.iloc[0][units_labels_salts[:]]])
    unit_name_buff = np.concatenate([df_hit_values.iloc[0][units_labels_buff[:]]])
    unit_name_perci = np.concatenate([df_hit_values.iloc[0][units_labels_perci[:]]])

    print("units_labels = \n", units_labels)
    print("units_labels_salts = \n", units_labels_salts)
    print("units_labelslabels_buff = \n", units_labels_buff)
    print("units_labels_perci = \n", units_labels_perci)

    reagent_name = np.concatenate([df_hit_values.iloc[0][salts_labels[:]], df_hit_values.iloc[0][buff_labels[:]], df_hit_values.iloc[0][perci_labels[:]] ])
    reagent_name = reagent_name.tolist()

    labels = reagent_name
    styling_label_1 = [' ['] * num_of_choices
    styling_label_2 = [']'] * num_of_choices
    label = ["" for x in range(num_of_choices)]

    if num_of_choices == 2:
        low_vals =[first_min,second_min]
        high_vals = [first_max,second_max]
    elif num_of_choices == 3:
        low_vals =[first_min,second_min,third_min]
        high_vals = [first_max,second_max,third_max]
    else:
        low_vals = [None]*num_of_choices
        high_vals = [None]*num_of_choices
    
    for i in range(0,num_of_choices):
        if choice_types[i] == "salt":
            if low_vals[i] == None:
                low_vals[i] = salt_conc[choice_index[i]]/2
            if high_vals[i] == None:
                high_vals[i] = salt_conc[choice_index[i]]*2
            label[i] = choices[i] + styling_label_1[0] + unit_name_salts[choice_index[i]] + styling_label_2[0]
        elif choice_types[i] == "buff":
            if low_vals[i] == None:
                low_vals[i] = pH[choice_index[i]]-1
            if high_vals[i] == None:
                high_vals[i] = pH[choice_index[i]]+1
            label[i] = choices[i] + styling_label_1[0] + 'pH' + styling_label_2[0]
        elif choice_types[i] == "precip":
            if low_vals[i] == None:
                low_vals[i] = precip_conc[choice_index[i]]/4
            if high_vals[i] == None:
                high_vals[i] = precip_conc[choice_index[i]]*4
            label[i] = choices[i] + styling_label_1[0] + unit_name_perci[choice_index[i]] + styling_label_2[0]
        else:
            return dcc.Textarea(
                placeholder='Enter a value...',
                value='An error occurred. Please report at: enquiries@moleculardimensions.com',
                style={'width': '40%'}
                )  

    samples = maxmin.compute_LHS(num_samples=nsamples, 
        var_LB=low_vals, 
        var_UB=high_vals)

    df = pd.DataFrame(data=samples, columns=label)
    table = generate_table(df, nsamples_x, nsamples_y, download_link=True)
    np.set_printoptions(precision=3)
    if n_clicks > 0:
        return table