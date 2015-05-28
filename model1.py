from recyclingModel import *

# ---------- Model definition file ---------- 

from math import sqrt

# Time
ts = [ 0 ]

# Waste sources
ws = { 'W1' : wastesource(50000, 0.1, 0.8, 0.1, 0.0),
       'W2' : wastesource(10000, 0.5, 0.4, 0.0, 0.1),
       'W3' : wastesource(40000, 0.1, 0.0, 0.7, 0.2) }

# Sorting facilities
ss = { 'S1' : sorting(50000, 20, 'pg'),
       'S2' : sorting(20000, 40, 'pgb') }

# Facilities
fs = { 'F1' : incinerator(15000),
       'F2' : incinerator(20000) }

# Landfills
ls = { 'L1' : landfill(100000, 50),
       'L2' : landfill(200000, 50) }

# ---------- Distance and cost functions ----------

# 2D positions for the facilities
pos = { 'W1' : (15, 8), 'W2' : (70, 40), 'W3' : (12,70),
        'S1' : (40,20), 'S2' : (25,50) ,
        'F1' : (25,5), 'F2' : (50,60),
        'L1' : (10,25), 'L2' : (80,80) }

ckm = 2
        
def cq(w,sl,t):
    return ckm*sqrt((pos[w][0]-pos[sl][0])**2.0 + (pos[w][1]-pos[sl][1])**2.0)

def cu(sf,fl,m,t):
    return ckm*sqrt((pos[sf][0]-pos[fl][0])**2.0 + (pos[sf][1]-pos[fl][1])**2.0)