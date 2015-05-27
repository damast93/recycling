from recyclingModel import *

# ---------- Model definition file ---------- 

from math import sqrt

# Time
ts = [ 0 ]

# Waste sources
ws = { 'W1' : wastesource(200, 0.8, 0.0, 0.0, 0.2),
       'W2' : wastesource(100, 0.0, 0.0, 0.5, 0.5) }

# Sorting facilities
ss = { 'S1' : sorting(100, 1, 'pg'),
       'S2' : sorting(300, 2, 'pgb') }

# Facilities
fs = { 'F1' : incinerator(210) }

# Landfills
ls = { 'L1' : landfill(200, 30),
       'L2' : landfill(2000, 25)}


# ---------- Distance and cost functions ----------

# Ad-hoc euclidean distance
pos = { 'W1' : (20.0, 20.0), 'W2' : (250.0, 200.0) ,
        'S1' : (50, 100), 'S2' : (100,10) ,
        'F1' : (100, 80),
        'L1' : (200,50), 'L2' : (250,50) }

def cq(w,sl,t):
    return 0.005*sqrt((pos[w][0]-pos[sl][0])**2.0 + (pos[w][1]-pos[sl][1])**2.0)

def cu(sf,fl,m,t):
    return 0.005*sqrt((pos[sf][0]-pos[fl][0])**2.0 + (pos[sf][1]-pos[fl][1])**2.0)