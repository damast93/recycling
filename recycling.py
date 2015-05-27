# Recycling optimization

from pulp import *
from model1 import *
from svg import *

# ---------- The LP ---------- 
# ---------- Variables ---------- 

# q is unsorted flow from waste sources to sorting facilities and landfills
qpaths = [ (w,s,t) for w in ws for s in ss for t in ts ] + \
         [ (w,l,t) for w in ws for l in ls for t in ts ]
q = LpVariable.dicts('q', qpaths, 0)

# u is sorted flow from (s|f) to (f|l), excluding loops f->f
upaths = [ (s,l,m,t)  for s in ss for l in ls for m in ms for t in ts ] + \
         [ (s,f,m,t)  for s in ss for f in fs for m in ms for t in ts ] + \
         [ (f,l,m,t)  for f in fs for l in ls for m in ms for t in ts ] + \
         [ (f,f2,m,t) for f in fs for f2 in fs if f!=f2 for m in ms for t in ts ]

u = LpVariable.dicts('u', upaths, 0)

# ---------- Objective function ---------- 
LP = LpProblem("Recycling", LpMinimize)

# Transportation costs
transportationCosts = sum(( cq(*qpath)*q[qpath] for qpath in qpaths )) + \
                      sum(( cu(*upath)*u[upath] for upath in upaths ))

# Facility costs and revenues
# Generate costs at facilities
def facilityCosts():
    for t in ts:
        for f in fs:
            for s in ss:
                uvec = { m : u[(s,f,m,t)] for m in ms }
                yield fs[f]['costs'](uvec)
                
            for f2 in fs:
                if f != f2:
                    uvec = { m : u[(f2,f,m,t)] for m in ms }
                    yield fs[f]['costs'](uvec)

# Generate costs at sorting facilities
def sortingCosts():
    for t in ts:
        for s in ss:
            for w in ws:
                yield ss[s]['costs'] * q[(w,s,t)]

# Generate costs at landfills
def landfillCosts():
    for t in ts:
        for l in ls:
            for w in ws:
                yield ls[l]['costs'] * q[(w,l,t)]

            for s in ss:
                yield ls[l]['costs'] * sum(( u[(s,l,m,t)] for m in ms ))

            for f in fs:
                yield ls[l]['costs'] * sum(( u[(f,l,m,t)] for m in ms ))

Z = transportationCosts  + \
    sum(facilityCosts()) + \
    sum(sortingCosts())  + \
    sum(landfillCosts())

LP += Z

# ---------- Constraints ----------

# Mass-balance constraints
for t in ts:

    # At waste sources:
    # All waste has to go to either sorting or landfills
    for w in ws:
        LP += sum(( q[(w,s,t)] for s in ss )) + sum(( q[(w,l,t)] for l in ls )) == ws[w]['quantity'], \
              "Mass" + w + "," + str(t)

    # At sorting facilities:
    # The estimated inflow of each material has to be disposed of at landfills or facilities
    for s in ss:
        for m in ms:
            LP += sum(( q[(w,s,t)]*ws[w][m] for w in ws )) == sum(( u[(s,f,m,t)] for f in fs )) + \
                                                                     sum(( u[(s,l,m,t)] for l in ls )), \
                  "Mass" + s + m + "," + str(t)

    # At facilities:
    # Residues of processing waste have to be disposed of
    for f in fs:
        def inflow(m):
            return sum(( u[(s,f,m,t)] for s in ss )) + sum(( u[(f2,f,m,t)] for f2 in fs if f2 != f ))
        def outflow(m):
            return sum(( u[(f,l,m,t)] for l in ls )) + sum(( u[(f,f2,m,t)] for f2 in fs if f2 != f ))

        uinflow   = { m : inflow(m) for m in ms }
        uresidues = fs[f]['processing'](uinflow)
        for m in ms:
            LP += uresidues[m] == outflow(m), \
                  "Mass" + f + m + "," + str(t)
            
# Capacity constriants (in each time step)
for t in ts:

    # At sorting facilities
    for s in ss:
        LP += sum(( q[(w,s,t)] for w in ws )) <= ss[s]['capacity'], \
              "Cap" + s + "," + str(t)

    # At facilities
    for f in fs:
        LP += sum(( u[(s,f,m,t)] for s in ss for m in ms )) + \
              sum(( u[(f2,f,m,t)] for f2 in fs if f2 != f for m in ms )) <= fs[f]['capacity'], \
              "Cap" + f + "," + str(t)

# At landfills (accumulating over time)
for l in ls:
    accum = sum(( q[(w,l,t)]   for w in ws for t in ts )) + \
            sum(( u[(s,l,m,t)] for s in ss for m in ms for t in ts )) + \
            sum(( u[(f,l,m,t)] for f in fs for m in ms for t in ts ))
    LP += accum <= ls[l]['total'], \
          "Total" + l
    
        
# Don't send illegal stuff to facilities
LP += sum(( u[(s,f,m,t)]  for f in fs for t in ts for s in ss
                          for m in ms if m not in fs[f]['legal'] )) == 0.0, \
      "IllegalS"
LP += sum(( u[(f2,f,m,t)] for f in fs for t in ts for f2 in fs if f2 != f
                          for m in ms if m not in fs[f]['legal'] )) == 0.0, \
      "IllegalF"
          
# Unsorted parts from sorting facilities may not go anywhere but to landfills
LP += sum(( u[(s,f,m,t)] for s in ss for f in fs
            for t in ts for m in ms if m not in ss[s]['materials'] )) == 0.0, \
      "DisposeUnsorted"

# Note that even though unsorted waste gets deposited on landfills in a distinguished manner,
# we don't care as it doesn't make any difference

# ---------------- Solve ----------------

LP.writeLP("recycling.lp")
status = LP.solve()
print("Status: %s" % LpStatus[status])
print("Optimal costs: %f" % value(LP.objective))

# Graphics output
t = 0

# Colors for materials
col = { 'p' : 'yellow', 'g' : 'gray', 'b' : 'green', 'l' : 'navy' }

svg = SVG("model.svg")

for w in ws:
    (x,y) = pos[w]
    svg.circle(x,y,10,'white')
    
for s in ss:
    (x,y) = pos[s]
    svg.circle(x,y,10,'green')
    
for f in fs:
    (x,y) = pos[f]
    svg.circle(x,y,10,'red')
    
for l in ls:
    (x,y) = pos[l]
    svg.circle(x,y,10,'navy')


for w in ws:
    for s in ss:
        if value(q[(w,s,t)]) > 0.0:
            svg.dashline(pos[w][0], pos[w][1],pos[s][0],pos[s][1], 'black', 1)
        
    for l in ls:
        if value(q[(w,l,t)]) > 0.0:
            svg.dashline(pos[w][0], pos[w][1],pos[l][0],pos[l][1], 'black', 1)
    

for s in ss:
    for f in fs:
        for m in ms:
            um = value(u[(s,f,m,t)])
            if um > 0.0:
                svg.line(pos[s][0], pos[s][1], pos[f][0], pos[f][1], col[m], 1)
    for l in ls:
        for m in ms:
            um = value(u[(s,l,m,t)])
            if um > 0.0:
                svg.line(pos[s][0], pos[s][1], pos[l][0], pos[l][1], col[m], 1)

for f in fs:
    for f2 in fs:
        if f2 != f:
            for m in ms:
                um = value(u[(f,f2,m,t)])
                if um > 0.0:
                    svg.line(pos[f][0], pos[f][1], pos[f2][0], pos[f2][1], col[m], 1)

    for l in ls:
        for m in ms:
            um = value(u[(f,l,m,t)])
            if um > 0.0:
                svg.line(pos[f][0], pos[f][1], pos[l][0], pos[l][1], col[m], 1)
        

svg.close()

if 1:
    for v in LP.variables():
        if(value(v) > 0.0):
            print("%s = %f" % (v.name, value(v)))


    # Dual variables
    for c in LP.constraints:
        print("%s = %f" % (c, LP.constraints[c].pi))
