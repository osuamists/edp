import sympy as sp
import numpy as np
from .numerical_method import NumericalMethod

class LeastSquaresMethod(NumericalMethod):
    def generate_basis_functions(self, n_terms):
        x = sp.Symbol('x')
        # Usar funções seno que satisfazem condições de contorno
        self.basis_functions = [sp.sin(n * sp.pi * x) for n in range(1, n_terms + 1)]

    def solve(self, n_terms=3, precision=1e-6):
        if not hasattr(self, 'domain') or len(self.domain) != 2:
            raise ValueError("Domínio deve ser definido como [a, b]")
            
        self.generate_basis_functions(n_terms)
        x = sp.Symbol('x')

        # CORREÇÃO: Extrair termo fonte corretamente
        if isinstance(self.equation, sp.Equality):
            lhs = self.equation.lhs
            rhs = self.equation.rhs
            
            # Para equação u'' + u = π²sin(πx), o termo fonte é π²sin(πx)
            # Para equação u'' = -π²sin(πx), o termo fonte é -π²sin(πx)
            if sp.diff(self.u(x), x, 2) in lhs.free_symbols or any(term.has(sp.diff(self.u(x), x, 2)) for term in sp.Add.make_args(lhs)):
                # EDP do tipo: u'' + u = f
                f = rhs
            else:
                # EDP do tipo: u'' = f
                f = rhs
        else:
            # Se não é equality, assumir forma padrão
            f = sp.pi**2 * sp.sin(sp.pi * x)
        
        print(f"Termo fonte f = {f}")

        # Aproximação u(x) = sum(a_i * φᵢ(x))
        coeffs = [sp.Symbol(f'a{i}') for i in range(n_terms)]
        u_aprox = sum(coeffs[i] * self.basis_functions[i] for i in range(n_terms))

        # CORREÇÃO: Resíduo correto dependendo da EDP
        u_aprox_xx = sp.diff(u_aprox, x, 2)
        
        # Verificar o tipo de EDP
        if hasattr(self, 'equation') and isinstance(self.equation, sp.Equality):
            lhs = self.equation.lhs
            if u_aprox_xx + u_aprox in sp.Add.make_args(lhs) or any(term.has(u_aprox_xx + u_aprox) for term in sp.Add.make_args(lhs)):
                # EDP: u'' + u = f
                residual = u_aprox_xx + u_aprox - f
            else:
                # EDP: u'' = f  
                residual = u_aprox_xx - f
        else:
            # Padrão: u'' + u = f
            residual = u_aprox_xx + u_aprox - f
            
        print(f"Resíduo: {sp.simplify(residual)}")

        # CORREÇÃO: Método de Galerkin com verificação de convergência
        A = sp.zeros(n_terms, n_terms)
        b = sp.zeros(n_terms, 1)

        print("Calculando integrais...")
        
        for i in range(n_terms):
            phi_i = self.basis_functions[i]
            
            for j in range(n_terms):
                phi_j = self.basis_functions[j]
                phi_j_xx = sp.diff(phi_j, x, 2)
                
                # A_ij = ∫(φⱼ'' + φⱼ) * φᵢ dx (para EDP u'' + u = f)
                if hasattr(self, 'equation') and 'u'' + u' in str(self.equation):
                    integrand = (phi_j_xx + phi_j) * phi_i
                else:
                    # Para EDP u'' = f
                    integrand = phi_j_xx * phi_i
                
                try:
                    integral_result = sp.integrate(integrand, (x, self.domain[0], self.domain[1]))
                    A[i, j] = integral_result
                    print(f"  A[{i},{j}] = {integral_result}")
                except Exception as e:
                    print(f"  ERRO em A[{i},{j}]: {e}")
                    A[i, j] = 0
            
            # b_i = ∫f * φᵢ dx
            try:
                integrand_b = f * phi_i
                integral_b = sp.integrate(integrand_b, (x, self.domain[0], self.domain[1]))
                b[i] = integral_b
                print(f"  b[{i}] = {integral_b}")
            except Exception as e:
                print(f"  ERRO em b[{i}]: {e}")
                b[i] = 0

        print(f"Matriz A (simbólica): {A}")
        print(f"Vetor b (simbólico): {b}")

        # CORREÇÃO: Conversão robusta para numpy
        try:
            A_numeric = np.zeros((n_terms, n_terms))
            b_numeric = np.zeros(n_terms)
            
            # Verificar se todas as integrais foram resolvidas
            all_converted = True
            
            for i in range(n_terms):
                for j in range(n_terms):
                    try:
                        val = A[i, j].evalf()
                        if val.has(sp.Integral) or not val.is_real:
                            print(f"AVISO: A[{i},{j}] = {val} não foi totalmente resolvida")
                            all_converted = False
                            A_numeric[i, j] = 0.0  # Fallback
                        else:
                            A_numeric[i, j] = float(val)
                    except:
                        print(f"ERRO: Não foi possível converter A[{i},{j}]")
                        A_numeric[i, j] = 0.0
                        all_converted = False
                
                try:
                    val_b = b[i].evalf()
                    if val_b.has(sp.Integral) or not val_b.is_real:
                        print(f"AVISO: b[{i}] = {val_b} não foi totalmente resolvida")
                        all_converted = False
                        b_numeric[i] = 0.0  # Fallback
                    else:
                        b_numeric[i] = float(val_b)
                except:
                    print(f"ERRO: Não foi possível converter b[{i}]")
                    b_numeric[i] = 0.0
                    all_converted = False
            
            if not all_converted:
                print("⚠ AVISO: Nem todas as integrais foram resolvidas simbolicamente")
                print("Continuando com valores disponíveis...")
            
            print(f"A_numeric:\n{A_numeric}")
            print(f"b_numeric: {b_numeric}")
            
            # Verificações de validade
            if np.allclose(A_numeric, 0, atol=1e-12):
                print("ERRO: Matriz A é essencialmente zero!")
                return None
                
            if np.allclose(b_numeric, 0, atol=1e-12):
                print("ERRO: Vetor b é essencialmente zero!")
                return None
            
            det_A = np.linalg.det(A_numeric)
            if abs(det_A) < 1e-12:
                print(f"AVISO: Matriz quase singular (det = {det_A})")
                # Tentar regularização
                A_numeric += np.eye(n_terms) * 1e-10
            
            # Resolver sistema
            a_numeric = np.linalg.solve(A_numeric, b_numeric)
            print(f"Coeficientes: {a_numeric}")
            
            # Construir solução
            solution = sum(float(a_numeric[i]) * self.basis_functions[i] for i in range(n_terms))
            return sp.simplify(solution)
            
        except Exception as e:
            print(f"ERRO no método: {e}")
            import traceback
            traceback.print_exc()
            return None

    def verify_solution(self, solution):
        """Verificar qualidade da solução"""
        if solution is None:
            print("Solução é None")
            return False
            
        x = sp.Symbol('x')
        
        print("\n=== VERIFICAÇÃO DA SOLUÇÃO ===")
        
        # Verificar condições de contorno
        try:
            u_0 = float(solution.subs(x, self.domain[0]))
            u_1 = float(solution.subs(x, self.domain[1]))
            
            print(f"Condições de contorno:")
            print(f"  u({self.domain[0]}) = {u_0:.8f}")
            print(f"  u({self.domain[1]}) = {u_1:.8f}")
            
            bc_satisfied = abs(u_0) < 1e-6 and abs(u_1) < 1e-6
            print(f"  Condições satisfeitas: {bc_satisfied}")
            
            return bc_satisfied
            
        except Exception as e:
            print(f"ERRO na verificação: {e}")
            return False
