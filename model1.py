from recyclingModel import *

# ---------- Model definition file ---------- 

from math import sqrt

# Time
ts = [ 0, 1, 2, 3, 4 ]

# Waste sources
ws = { 'W1' : wastesource(40000, 0.2, 0.7, 0.1, 0.0),
       'W2' : wastesource(30000, 0.5, 0.4, 0.0, 0.1),
       'W3' : wastesource(30000, 0.2, 0.0, 0.7, 0.1) }

# Sorting facilities
ss = { 'S1' : sorting(20000, 30, 'pgb'), # vs 20/40
       'S2' : sorting(30000, 25, 'pb') } # 30000

# Facilities
fs = { 'I1' : incinerator(15000),
       'I2' : incinerator(20000),
       'C' : compostation(20000),
       'P' : plasticrecycling(15000), # 15 vs 20
       'G' : glassrecycling(20000) } # 20 vs 40

# Landfills
ls = { 'L1' : landfill( 40000, 50),
       'L2' : landfill(500000, 70) }

# ---------- Distance and cost functions ----------

# 2D positions for the facilities
pos = { 'W1' : (25, 8), 'W2' : (80, 40), 'W3' : (22,70),
        'S1' : (37,32), 'S2' : (32,54) ,
        'I1' : (45,22), 'I2' : (60,60), 'C' : (40,40), 'P' : (20, 54), 'G' : (70,30),
        'L1' : (10,15), 'L2' : (80,80) }

ckm = 2.5
        
def cq(w,sl,t):
    return ckm*sqrt((pos[w][0]-pos[sl][0])**2.0 + (pos[w][1]-pos[sl][1])**2.0)

def cu(sf,fl,m,t):
    return ckm*sqrt((pos[sf][0]-pos[fl][0])**2.0 + (pos[sf][1]-pos[fl][1])**2.0)