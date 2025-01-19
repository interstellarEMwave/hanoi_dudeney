import sys

def stepsNeeded(r, n):
    if n == 0:
        return 0, [0]*(r-1) 
    
    increment = 1
    pegs = [0]*(r)
    left = [1]*(r-1)
    pegs[1] = 1
    n -= 1
    
    if(n == 0):
        return 1, pegs
    
    total = 0

    
    while n > 0:
        for i in range(1, r-1):
            pegs[i+1] += min(n, left[i])
            total += increment*min(n, left[i])
            n -= min(n, left[i])
            left[i] = 1
            for j in range(1, i):
                left[i] += pegs[j+1]
                
            
        increment *= 2
    
    return 2*total+1, pegs  



def printState(state, total):
    m = 0
    for i in range(len(state)): 
        if(len(state[i]) > m): 
            m = len(state[i])
    m -= 1
    
    while m > -1:
        for i in range(len(state)): 
            if(m < len(state[i])): 
                print(state[i][m], end = "\t")
            else:
                print(" ", end = "\t")
        print()
        m -= 1
    print("¯¯¯\t"*len(state), total[0], "\n")
    

# allowed[0]: origin
# allowed[1]: destination
def solveDudeney(r, n, allowed, state, total):
    if n == 0:
        return
    elif n < len(allowed):
        for i in range(n, 0, -1):
            state[allowed[i]].append(state[allowed[0]].pop(-1))
            total[0] += 1
            printState(state, total)
        
        for i in range(2, n+1):
            state[allowed[1]].append(state[allowed[i]].pop(-1))
            total[0] += 1
            printState(state, total)
    else:
        _, towers = stepsNeeded(len(allowed), n)

        allowed_new1 = [allowed[0]]
        for a in range(2, r):
            allowed_new1.append(allowed[a])
        allowed_new1.append(allowed[1])

        b = []
        for i in range(r, 1, -1):
            solveDudeney(i, towers[i-1], allowed_new1, state, total)
            b.append(allowed_new1.pop(1))
        
        b.pop(-1)
        allowed_new2 = [allowed[0], allowed[1]]
        for i in range(3, r+1):
            allowed_new2.append(allowed_new2.pop(0))
            allowed_new2.insert(0, b.pop(-1))
            solveDudeney(i, towers[i-1], allowed_new2, state, total)



def solveExample(r, n):
    state = []
    for i in range(r):
        state.append([])
    for m in range(n, 0, -1):
        state[0].append(m)
    
    allowed = [0,r-1]
    for a in range(1, r-1):
        allowed.append(a)
    
    printState(state, [0])
    solveDudeney(r, n, allowed, state, [0])

def solveSpecific(r, n, origin, destination):
    state = []
    for i in range(r):
        state.append([])
    for m in range(n, 0, -1):
        state[origin].append(m)

    
    allowed = [origin, destination]
    for a in range(r):
        if a != origin and a != destination:
            allowed.append(a)
   
    printState(state, [0])
    solveDudeney(r, n, allowed, state, [0])
    
def minSteps(r, n_min, n_max):
    for i in range(n_min, n_max+1): 
        t, s = stepsNeeded(r, i)
        print(r, "\t", i, ":\t", t, "\t", s)



def main():
    a = []
    for i in range(1, len(sys.argv)):
        a.append(int(sys.argv[i]))
    if(a[0] < 3):
        print("Incorrect input. Minimum pegs is 3")
        return

    if(len(a) == 3):
        minSteps(a[0], a[1], a[2])
    elif(len(a) == 2):
        solveExample(a[0], a[1])
    elif(len(a) == 4):
        solveSpecific(a[0], a[1], a[2], a[3])
    else:
        print("Incorrect input.\nThe program can take 2, 3, or 4 inputs:\n\t2: r, n\n\tGive all the steps for r pegs and n disks. Goes from peg 0 to peg r-1.\n\n\t3: r, n_min, n_max\n\tGive minimum number of steps needed to solve r pegs and all n from n_min to n_max (inclusive) disks.\n\n\t4: r, n, origin, destination. \n\tGive all the steps for r pegs, with n disks on peg origin to peg destination.\n")


main()
