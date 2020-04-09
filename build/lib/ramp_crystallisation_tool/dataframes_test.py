import os 
import fnmatch
import glob
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import xlrd   
import pandas as pd
import pyDOE as doe
import numpy as np
import random as rnd


def compute_grid(nsamples_x, nsamples_y, var_LB, var_UB, NVARS):
    '''
    var_LB/var_UB: vector that contains the min/max values of its parameter
    e.g. for initial example: 
    xmin = [Tmin = 100, Rac_ratio = 0.8, Micro_Pow = 150] and 
    xmax = [Tmax = 200, Rac_ratio = 1.8, MIcro_Pow = 250]
    '''
	# number of variables
    c_1 = np.linspace(var_LB[0], var_UB[0], nsamples_x)
    c_2 = np.linspace(var_LB[1], var_UB[1], nsamples_y)
            
    # print (np.shape(M))
    M = np.array(np.meshgrid([c_1], [c_2])).T

    nsamples = nsamples_x * nsamples_y
    M = M.reshape(nsamples,NVARS)
    # print("M matrix in mamin, compute grid = /n", M )
    # print("M size: ", np.shape(M))
    return (M)

def compute_LHS(num_samples, var_LB, var_UB):
	'''
	var_LB/var_UB: vector that contains the min/max values of its parameter
	e.g. for initial example: 
	xmin = [Tmin = 100, Rac_ratio = 0.8, Micro_Pow = 150] and 
	xmax = [Tmax = 200, Rac_ratio = 1.8, MIcro_Pow = 250]
	'''
	# number of variables
	dim = len(var_LB)
	lhs_set = doe.lhs(dim, num_samples)
	# Convert output to parameter space
	for j in range(dim):
		lhs_set[:,j] = var_LB[j] + lhs_set[:,j]*(var_UB[j] - var_LB[j])
	# print(np.shape(lhs_set))

	return lhs_set



myPath= r'/Users/va00173/Desktop/plate_optimiser/sycofinder-master/ramp_crystallisation_tool/MDL_screens_database'
code_name = 'MD1-40*'

for file in os.listdir(myPath):
	if fnmatch.fnmatch(file, code_name):
		print ("The file you called is: \n", file)
		file_found = file 
newpath = os.path.join(myPath, file_found) 

xls = pd.ExcelFile(newpath)
df1 = pd.read_excel(xls)
searchedValue = "B1"

df_searchedValue = df1[df1["Well #"] == searchedValue]
df_new = df1.set_index("Well #", drop = False)
df_hit_well = df_new.loc[[searchedValue]]
# df_hit_well_variables = series_hit_well_variables.to_frame()
# print(type(df_hit_well))

# print ("Conditions where we get a hit: \n", df_hit_well)
df_hit_values = df_hit_well.dropna(axis='columns')
print("df_hit_values", df_hit_values)


# exctract indexes for each component of the file 
concentrations = df_hit_values.filter(like='Conc').columns

print(concentrations, type(concentrations))
ph =  df_hit_values.filter(like='pH').columns
units = df_hit_values.filter(like='Units').columns
salts = df_hit_values.filter(like='Salt').columns
buff =  df_hit_values.filter(like='Buffer').columns
precip =  df_hit_values.filter(like='Precipitant').columns


var = np.array(len(concentrations))
print("var", var)
var = df_hit_values[concentrations].to_numpy()
reagent = np.array(len(salts)+len(buff)+len(precip))
# reagent = [df_hit_values[salts].to_numpy(), df_hit_values[buff].to_numpy(), df_hit_values[precip].to_numpy()]
print("reagents: \n", reagent)
print("reagent type", type(reagent))
var = var.T
print(len(var))
num_var = 2 
range_LB = ([var[0] - 0.01, var[1] - 0.1])
range_UB = ([var[0] + 0.1, var[1] + 0.1])
nsamples_x = 8 
nsamples_y = 12 
num_samples = nsamples_x * nsamples_y

pp = compute_grid(nsamples_x, nsamples_y, range_LB, range_UB, num_var)
print(pp)

kk = compute_LHS(num_samples, range_LB, range_UB)
