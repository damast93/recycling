from pulp import *

# Material types
ms = 'pgbl'

# ---------- Waste sources ---------- 
# Create waste source with given quantity and presumed composition of waste (p,g,b,l)
def wastesource(quantity, p, g, b, l):
    return { 'quantity': quantity, 'p' : p, 'g' : g, 'b' : b, 'l' : l }

ws = { 'W1' : wastesource(100, 0.5, 0.3, 0.2, 0.0) }

# ---------- Sorting facilities ---------- 
# Create sorting facility with given capacity, extracting given materials
def sorting(cap, materials):
    return { 'capacity' : cap, 'materials' : materials }

ss = { 'S1' : sorting(80, 'pg') }

# ---------- Facilities ---------- 
# A facility comes with given capacities, processing and cost functions (linear!)

# Create an incinerator of given capacity
def incinerator(cap):
    def processing(u):
        (p,g,b,l) = u
        return (0.0,
                g,
                0.0,
                0.1*p + 0.05*b)
        
    def costs(u):
        (p,g,b,l) = u
        return -1.0*p - 0.5*b 
    
    return { 'capacity' : cap, 'processing' : processing, 'costs' : costs }

fs = { 'F1' : incinerator(50) }

# ---------- Landfills ----------
# Create landfill with given total capacity
def landfill(total):
    return { 'total' : total }

ls = { 'L1' : landfill(1000) }

# ---------- Time ---------- 
ts = [ 0, 1 ]

# ---------- The constants ----------
# ---------- Transportation costs ----------
def cq(w,sl,t):
    return 1

def cu(sf,fl,m,t):
    return 2


# ---------- The LP ---------- 
# ---------- Variables ---------- 

# q is unsorted flow from waste sources to sorting facilities and landfills
qpaths = [ (w,s,t) for w in ws.keys() for s in ss.keys() for t in ts ] + \
         [ (w,l,t) for w in ws.keys() for l in ls.keys() for t in ts ]
q = LpVariable.dicts('q', qpaths, 0)

# u is sorted flow from (s|f) to (f|l), excluding loops f->f
upaths = [ (s,l,m,t)  for s in ss.keys() for l in ls.keys() for m in ms for t in ts ] + \
         [ (s,f,m,t)  for s in ss.keys() for f in fs.keys() for m in ms for t in ts ] + \
         [ (f,l,m,t)  for f in fs.keys() for l in ls.keys() for m in ms for t in ts ] + \
         [ (f,f2,m,t) for f in fs.keys() for f2 in fs.keys() if f!=f2 for m in ms for t in ts ]

u = LpVariable.dicts('u', upaths, 0)

# ---------- Objective function ---------- 
LP = LpProblem("Recycling", LpMinimize)

# Transportation costs
c = sum(( cq(*qpath)*q[qpath] for qpath in qpaths )) + sum(( cu(*upath)*u[upath] for upath in upaths ))

# Facility costs and revenues
# Costs for facilities
def facilityCosts():
    for t in ts:
        for f in fs.keys():
            for s in ss.keys():
                uvec = (u[(s,f,'p',t)], u[(s,f,'g',t)], u[(s,f,'b',t)], u[(s,f,'l',t)])
                yield fs[f]['costs'](uvec)
                
            for f2 in fs.keys():
                if f != f2:
                    uvec = (u[(f2,f,'p',t)], u[(f2,f,'g',t)], u[(f2,f,'b',t)], u[(f2,f,'l',t)])
                    yield fs[f]['costs'](uvec)

# Costs at sorting facilities
def sortingCosts():
    for t in ts:
        for s in ss.keys():
            for w in ws.keys():


