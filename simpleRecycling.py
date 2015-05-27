from pulp import *
from math import sqrt

# Model

def source(x, y, q, r, i, c, l):
    return { 'pos': (x,y), 'quantity' : q, 'r' : r, 'i' : i, 'c' : c, 'l' : l }

def incinerator(x, y, cap):
    return { 'type' : 'i', 'pos' : (x, y), 'capacity' : cap }
def compostation(x, y, cap):
    return { 'type' : 'c', 'pos' : (x, y), 'capacity' : cap }
def recycling(x, y, cap):
    return { 'type' : 'r', 'pos' : (x, y), 'capacity' : cap }
def landfill(x, y, cap):
    return { 'type' : 'l', 'pos' : (x, y), 'capacity' : cap }

types = 'ricl'
    
# Waste sources
sources = [
    source(2, 2, 100, 0.8, 0.0, 0.0, 0.2),
    source(2, 8, 200, 0.0, 0.5, 0.5, 0.0)
]

# Facilities
facs = [
    incinerator(0, 5, 60),
    recycling(6, 11, 50),
    landfill(6, 2, 200),
    landfill(4, 8, 80)
]

# Distance
def dist(a,b):
    (xa,ya) = a['pos']
    (xb,yb) = b['pos']
    return sqrt((xa-xb)**2.0 + (ya-yb)**2.0)

# Transportation cost/unit
transportCosts = 0.25
argmin = -1000.0

# revenues['st'] = revenue of processing a unit of type 's' at facility 't'
revenues = { 'rr' : 5.0,    'ri' : 1.5,    'rc' : argmin, 'rl' : 0.0,
             'ir' : argmin, 'ii' : 2.0,    'ic' : argmin, 'il' : 0.0,
             'cr' : argmin, 'ci' : argmin, 'cc' : 1.0,    'cl' : 0.0,
             'lr' : argmin, 'li' : argmin, 'lc' : argmin, 'll' : 0.0 }
             
# Revenue of processing type t at given facility 
def revenue(fac, t):
    return revenues[t + fac['type']] 
    
# Cost for processing a unit of waste of type t from source at a given facility
# including transportation cost minus revenue
def unitcost(src, fac, t):
    return dist(src, fac) * transportCosts - revenue(fac, t)

# ----------------  LP formulation ----------------

LP = LpProblem("Recycling", LpMinimize)

ways = [ (isrc, ifac, t) 
         for isrc in range(len(sources)) 
         for ifac in range(len(facs))
         for t in types ]

# Decision variables for the amount of waste of type t transported on each way, continuous and nonnegative
ws = LpVariable.dicts('w', ways, 0)

# Set upper bounds. We can at most transport the amount of type t waste produced at the source
for w in ways:
    (isrc, ifac, t) = w
    ws[w].upBound = sources[isrc]['quantity'] * sources[isrc][t]

# Summands of objective function
def costs():
    for way in ways:
        (isrc, ifac, t) = way
        yield unitcost(sources[isrc], facs[ifac], t) * ws[way]

# Add objective function to LP
Z = sum(costs())
LP += Z

# ---------------- Constraints ----------------

# All waste has to be removed from the sources
def balanceConstraints():
    for isrc in range(len(sources)):
        yield sum(( ws[(isrc, ifac, t)] for ifac in range(len(facs)) for t in types )) == sources[isrc]['quantity']


# Total waste at facilities may not exceed capacity
def capacityConstraints():
    for ifac in range(len(facs)):
        yield sum(( ws[(isrc, ifac, t)] for isrc in range(len(sources)) for t in types )) <= facs[ifac]['capacity']

# Add constraints to the LP
for eq in balanceConstraints():
    LP += eq
for eq in capacityConstraints():
    LP += eq

# ---------------- Solve ----------------

LP.writeLP("recycling.lp")
status = LP.solve()

print("Status: %s" % LpStatus[status])
print("Optimale Kosten: %f" % value(LP.objective))
for v in LP.variables():
    if(value(v) > 0.0):
        print("%s = %f" % (v.name, value(v)))


