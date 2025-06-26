import sympy as sp

def metodo_momentos(f_expr, n, base_phi=None):
    x = sp.Symbol('x')
    a = sp.symbols(f'a1:{n+1}')
    
    if base_phi is None:
        base_phi = [x*(1 - x)*x**i for i in range(n)]

    u_aprox = sum(a[i]*base_phi[i] for i in range(n))
    R = -sp.diff(u_aprox, x, 2) - f_expr

    eqs = []
    for phi_j in base_phi:
        eqs.append(sp.integrate(R * phi_j, (x, 0, 1)))
    
    sol = sp.solve(eqs, a)
    u_aprox_sol = u_aprox.subs(sol)
    return u_aprox_sol, sol
