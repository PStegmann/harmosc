#!/usr/bin/env python
# coding=UTF-8
#
# FEM solution of the stationary Schroedinger equation
# for the harmonic oscillator potential.
#
#   Dependancies:
#   - FEnICS
#   - PETSc
#   - SLEPc
#
#   Revisions:
#
#   2014-10-11  pstegmann   Creation of draft from formula
#   2014-10-12  pstegmann   Modification of draft to first working solution


from dolfin import *
import time
import math
import matplotlib.pyplot as plit

#define mesh and function space
mesh = IntervalMesh(200, -10, 10)
V = FunctionSpace(mesh, 'Lagrange', 3)

#define boundary
def boundary(x, on_boundary):
    return on_boundary

#apply essential boundary conditions
bc = DirichletBC(V, 0, boundary)

#define functions
u = TrialFunction(V)
v = TestFunction(V)

x2 = Expression('x[0]*x[0]')

#define problem
a = (inner(grad(u), grad(v)) \
     + x2*u*v)*dx
m = u*v*dx

#assemble stiffness matrix
A = PETScMatrix()
assemble(a, tensor=A)
M = PETScMatrix()
assemble(m, tensor=M)

#create eigensolver
eigensolver = SLEPcEigenSolver(A,M)
eigensolver.parameters['spectrum'] = 'smallest magnitude'
eigensolver.parameters['solver'] = 'lapack'
eigensolver.parameters['tolerance'] = 1.e-15

#solve for eigenvalues
max = 10
eigensolver.solve(max)

#extract first eigenpair
r, c, rx, cx = eigensolver.get_eigenpair(0)
print 'eigenvalue:', r, 'Ground state ', 0

#assign eigenvector to function
u = Function(V)
u.vector()[:] = rx

#plot eigenfunction and probability density
plt = plot(u)
#interactive()
time.sleep(2)   # 3 seconds pause

print ' Maximum converged eigenvalue: ', eigensolver.get_number_converged()

i = 1
#while i < eigensolver.get_number_converged():
while i < max:
    # extract next eigenpair
    r, c, rx, cx = eigensolver.get_eigenpair(i)
    print 'eigenvalue:', r, i

    #assign eigenvector to function
    u.vector()[:] = rx
    
    #plot eigenfunction
    plt.plot(u)
    #interactive()
    time.sleep(2)
    #print 'next plot'
    #increment i
    i = i + 1
print 'Finished.'

# extract last eigenpair
r, c, rx, cx = eigensolver.get_eigenpair(max)
print 'eigenvalue:', r, max
    
#assign eigenvector to function
u.vector()[:] = rx
    
#plot eigenfunction
plt.plot(u)
interactive()
##### EOF #############
