## Define constructors for building our recycling model

# ---------- Material types ---------- 
ms = 'pgbl'

# Sorted material flow is represented through named vectors
u0 = { m : 0.0 for m in ms }

# ---------- Waste sources ---------- 
# Create waste source with given quantity and presumed composition of waste (p,g,b,l)
def wastesource(quantity, p, g, b, l):
    return { 'quantity': quantity, 'p' : p, 'g' : g, 'b' : b, 'l' : l }


# ---------- Sorting facilities ---------- 
# Create sorting facility with given capacity, processing costs, extracting given materials
def sorting(cap, costs, materials): 
    return { 'capacity' : cap, 'costs': costs, 'materials' : materials }

# ---------- Facilities ---------- 
# A facility comes with fields
# - capacity   : capacity limiting the total inflow per time step
# - processing : a linear processing function on material flow vectors
# - costs      : a linear processing cost/revenue function on material vectors
# - legal      : legal materials which the facility accepts

# Create an incinerator of given capacity
def incinerator(cap):
    def processing(u):
        ret = u0
        ret['l'] = 0.1*u['p'] + 0.05*u['b']
        return ret
        
    def costs(u):
        return -1.0*u['p'] - 0.5*u['b'] 
    
    return { 'capacity' : cap, 'processing' : processing, 'costs' : costs, 'legal' : 'pb' }

# ---------- Landfills ----------
# Create landfill with given total capacity and depositing costs
def landfill(total, costs):
    return { 'total' : total, 'costs' : costs }

