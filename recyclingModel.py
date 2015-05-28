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
        ret = u0.copy()
        ret['l'] = 0.1*u['p'] + 0.05*u['b'] + u['g'] + u['l']
        return ret
        
    def costs(u):
        return 40.0*u['p'] + 70.0*u['b'] + 100.0*u['g'] + 100.0*u['l']
    
    return { 'capacity' : cap, 'processing' : processing, 'costs' : costs, 'legal' : 'pbgl' }

# Create a glass recycling facility of given capacity
def glassrecycling(cap):
    def processing(u):
        ret = u0.copy()
        ret['l'] = 0.05*u['g']
        return ret
        
    def costs(u):
        return -250.0*u['g']
    
    return { 'capacity' : cap, 'processing' : processing, 'costs' : costs, 'legal' : 'g' }

# Create a compostation facility of given capacity
def compostation(cap):
    def processing(u):
        ret = u0.copy()
        return ret
        
    def costs(u):
        return 50*u['b']
    
    return { 'capacity' : cap, 'processing' : processing, 'costs' : costs, 'legal' : 'b' }

# Create a plastic recycling facility of given capacity
def plasticrecycling(cap):
    def processing(u):
        ret = u0.copy()
        ret['l'] = 0.05*u['p']
        return ret
        
    def costs(u):
        return -400*u['p']
    
    return { 'capacity' : cap, 'processing' : processing, 'costs' : costs, 'legal' : 'p' }
    
# ---------- Landfills ----------
# Create landfill with given total capacity and depositing costs
def landfill(total, costs):
    return { 'total' : total, 'costs' : costs }

