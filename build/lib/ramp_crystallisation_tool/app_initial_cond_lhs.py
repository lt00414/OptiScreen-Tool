# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from builtins import range  # pylint: disable=redefined-builtin

import collections

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#import dash_table_experiments as dt

import pandas as pd
import numpy as np
#from . import uniform
from . import maxmin_grid, maxmin_lhs
from . import app
import chart_studio.plotly as plt

# pylint: disable=redefined-builtin


###############################################################################
def get_controls_var(id, desc, range):
    """Get controls for each variable.

    This includes
     * the description
     * range 
    """
    label_reagent = dcc.Input(
        id=id + "_label", type='text', value=desc[0], className="label")
    label_unit = dcc.Input(
        id=id + "_units", type='text', value=desc[1], className="label")
    range_low = dcc.Input(
        id=id + "_low", type='number', value=range[0], className="range")
    range_high = dcc.Input(
        id=id + "_high", type='number', value=range[1], className="range")

    return html.Tr([
        html.Td(label_reagent),
        html.Td(label_unit),
        html.Td([range_low, html.Span('to'), range_high])
         ,
         # html.Td([
         #    # html.Span(slider, className="slider")
         #    # ,
         #    # html.Span('', id=id + "_weight_label")
         # ])
    ], id=id + "_tr")

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
        html.Td([dimensions_x, html.Span('\\times'), dimensions_y])
         ,
         # html.Td([
         #    # html.Span(slider, className="slider")
         #    # ,
         #    # html.Span('', id=id + "_weight_label")
         # ])
    ], id=id + "_tr")
#------------------------------------------------------------------------------

##############################################################################




#------------------------------------------------------------------------------



##############################################################################
reagents = collections.OrderedDict([
    ('reagent_1',
     dict(label=['Reagent 1 [Units]', 'Units 1'], range=[100.0, 200.0])),
    ('reagent_2', dict(label=['Reagent 2 [Units]', 'Units 2'], range=[1.0, 6.0])),
    ])

NVARS_DEFAULT = len(reagents)

# Fill up to NVARS_MAX (needed to define callbacks)
NVARS_MAX = 10
for i in range(len(reagents), NVARS_MAX):
    k = 'Reagent {} [Units]'.format(i + 1)
    reagents[k] = dict(label=k, range=[0, 1])




var_ids = list(reagents.keys())
print('var_ids', var_ids )
var_labels = [v['label'] for v in list(reagents.values())]


controls_dict = collections.OrderedDict()
for k, v in list(reagents.items()):
    controls = get_controls_var(k, v['label'], v['range'])
    controls_dict[k] = controls

head_row = html.Tr([
    html.Th('Reagent   '),
    html.Th('Units   '),
    html.Th('Range  ')
])
controls_html = html.Table(
    [head_row] + list(controls_dict.values()), id='controls')
label_states = [State(k + "_label", 'value') for k in var_ids
]
unit_states = [State(k + "_units", 'value') for k in var_ids
]
low_states = [State(k + "_low", 'value') for k in var_ids]
high_states = [State(k + "_high", 'value') for k in var_ids]
# weight_states = [
#     dash.dependencies.State(k + "_weight", 'value') for k in var_ids
# ]

inp_nvars = html.Tr([
    html.Td('Number of reagents: '),
    html.Td(
        dcc.Input(
            id='inp_nvars',
            type='number',
            value=NVARS_DEFAULT,
            max=NVARS_MAX,
            min=1,
            className="nvars range"))
])
print("inp_nvars = ", inp_nvars)

inp_nsamples = html.Tr([
    html.Td('Enter screen dimensions '),
    html.Td(
        dcc.Input(
            id='nsamples_x', type='number', value=8,
            className="nsamples range")), 
    html.Td(html.Span('x')),
    html.Td(
        dcc.Input(
            id='nsamples_y', type='number', value=12,
            className="nsamples range"))
])
ninps = len(label_states + low_states + high_states) + 3
print("ninps = ", ninps)

#------------------------------------------------------------------------------


##############################################################################
btn_compute = html.Div([
    html.Button('compute using LHS', id='btn_compute', className='action-button', 
        n_clicks_timestamp = 0),
    html.Button('compute using grid', id='btn_compute_2', className='action-button', 
        n_clicks_timestamp = 0),
    html.Div('', id='compute_info')
])

# Creation of dash app
layout = html.Div(
    [
        html.Table([inp_nvars, inp_nsamples]),
        controls_html,
        btn_compute,
        #graph, hover_info,
    ],
    id="container",
    # tag for iframe resizer
    **{'data-iframe-height': ''},
)
#------------------------------------------------------------------------------


##############################################################################
# Callbacks to hide unselected reagents
for i in range(NVARS_MAX):

    @app.callback(
        dash.dependencies.Output(var_ids[i] + "_tr", 'style'),
         [dash.dependencies.Input('inp_nvars', 'value')])
    def toggle_visibility(nvars, i=i):
        """Callback for setting variable visibility"""
        style = {}

        if i + 1 > nvars:
            style['display'] = 'none'

        return style
#------------------------------------------------------------------------------


##############################################################################
states = label_states + low_states + high_states 
states += [State('inp_nvars', 'value')]
states += [State('nsamples_x', 'value')]
states += [State('nsamples_y', 'value')]


@app.callback(
    dash.dependencies.Output('compute_info', 'children'),
    [dash.dependencies.Input('btn_compute', 'n_clicks_timestamp'), 
     dash.dependencies.Input('btn_compute_2', 'n_clicks_timestamp')], states)
#------------------------------------------------------------------------------



##############################################################################
def on_compute(btn_compute, btn_compute_2, *args):
    """Callback for clicking compute button"""
    # if n_clicks is None :
    #     return ''

    print("len(args) = ", len(args) )
    if len(args) != ninps:
        raise ValueError("Expected {} arguments".format(ninps))


    # parse arguments
    nsamples_y = args[-1]
    nsamples_x = args[-2]
    nvars = args[-3]

    nsamples = nsamples_x*nsamples_y
    labels = args[:nvars]
    print("labes (i'm in line 236) = ", labels)

    low_vals = np.array([args[i + NVARS_MAX] for i in range(nvars)])
    high_vals = np.array([args[i + 2 * NVARS_MAX] for i in range(nvars)])
    print ("NVARS_MAX = ", NVARS_MAX)
    print ("low_vals = ", low_vals)
    print ("high_vals = ", high_vals)

    # print("int(btn_compute) = ", int(btn_compute))

    from .common import generate_table

    if int(btn_compute) > int(btn_compute_2):

        samples = maxmin.compute_LHS(num_samples=nsamples, 
            var_LB=low_vals, 
            var_UB=high_vals)
        print (samples)
        df = pd.DataFrame(data=samples, columns=labels)
        table = generate_table(df, download_link=True)
        return table
    elif int(btn_compute_2) > int(btn_compute):
        
        samples_1 = maxmin.compute_grid(nsamples_x, nsamples_y, low_vals, high_vals, 
            NVARS = len(low_vals))
        df = pd.DataFrame(data=samples_1, columns=labels)
        # print ("samples_1 (l 249) = \n", samples_1)
        table = generate_table(df, download_link=True)
        return table
#------------------------------------------------------------------------------


