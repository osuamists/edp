"""
Configurações para integração de métodos numéricos com EDPs
"""

# Mapeamento de compatibilidade: quais métodos funcionam bem com quais problemas
METHOD_COMPATIBILITY = {
    "poisson": {
        "galerkin": {"priority": 1, "description": "Método robusto para problemas elípticos"},
        "rayleigh_ritz": {"priority": 1, "description": "Excelente para problemas variacionais"},
        "least_squares": {"priority": 2, "description": "Alternativa estável"},
        "colocacao": {"priority": 3, "description": "Funciona mas pode ser menos preciso"},
        "moments": {"priority": 3, "description": "Aplicável mas não ideal"},
        "subregions": {"priority": 2, "description": "Útil para geometrias complexas"}
    },
    "onda_1d": {
        "galerkin": {"priority": 1, "description": "Método padrão para problemas hiperbólicos"},
        "colocacao": {"priority": 2, "description": "Alternativa viável"},
        "least_squares": {"priority": 3, "description": "Pode funcionar com adaptações"},
        "rayleigh_ritz": {"priority": 3, "description": "Menos comum para ondas"},
        "moments": {"priority": 3, "description": "Aplicável mas complexo"},
        "subregions": {"priority": 2, "description": "Para condições complexas"}
    },
    "calor": {
        "galerkin": {"priority": 1, "description": "Excelente para problemas parabólicos"},
        "colocacao": {"priority": 2, "description": "Boa alternativa"},
        "least_squares": {"priority": 2, "description": "Estável numericamente"},
        "rayleigh_ritz": {"priority": 3, "description": "Funciona mas não é comum"},
        "moments": {"priority": 3, "description": "Aplicável"},
        "subregions": {"priority": 2, "description": "Para geometrias específicas"}
    },
    "helmholtz": {
        "galerkin": {"priority": 1, "description": "Método padrão para Helmholtz"},
        "rayleigh_ritz": {"priority": 1, "description": "Muito eficaz para este tipo"},
        "least_squares": {"priority": 2, "description": "Alternativa robusta"},
        "colocacao": {"priority": 2, "description": "Funciona bem"},
        "moments": {"priority": 3, "description": "Aplicável"},
        "subregions": {"priority": 2, "description": "Para domínios 2D complexos"}
    }
}

# Parâmetros padrão para cada método
DEFAULT_PARAMETERS = {
    "galerkin": {
        "n_terms": 5,
        "precision": 1e-6,
        "basis_type": "polynomial"
    },
    "rayleigh_ritz": {
        "n_terms": 5,
        "precision": 1e-6,
        "energy_functional": "standard"
    },
    "least_squares": {
        "n_terms": 5,
        "precision": 1e-6,
        "residual_points": 10
    },
    "colocacao": {
        "n_terms": 5,
        "collocation_points": "chebyshev",
        "precision": 1e-6
    },
    "moments": {
        "n_terms": 5,
        "moment_order": 3,
        "precision": 1e-6
    },
    "subregions": {
        "n_subregions": 3,
        "n_terms_per_region": 3,
        "precision": 1e-6
    }
}

# Validações específicas por tipo de problema
PROBLEM_VALIDATIONS = {
    "poisson": {
        "required_bc": ["dirichlet"],
        "optional_bc": ["neumann", "robin"],
        "dimension": 1,
        "time_dependent": False
    },
    "onda_1d": {
        "required_bc": ["dirichlet", "initial"],
        "optional_bc": ["neumann"],
        "dimension": 1,
        "time_dependent": True,
        "required_initial": ["u", "ut"]
    },
    "calor": {
        "required_bc": ["dirichlet", "initial"],
        "optional_bc": ["neumann"],
        "dimension": 1,
        "time_dependent": True,
        "required_initial": ["u"]
    },
    "helmholtz": {
        "required_bc": ["dirichlet"],
        "optional_bc": ["neumann", "robin"],
        "dimension": 2,
        "time_dependent": False
    }
}

# Configurações de visualização
VISUALIZATION_CONFIG = {
    "1d_problems": {
        "plot_type": "line",
        "x_points": 100,
        "show_analytical": True,
        "show_error": True
    },
    "2d_problems": {
        "plot_type": "contour",
        "x_points": 50,
        "y_points": 50,
        "colormap": "viridis"
    },
    "time_dependent": {
        "animation": True,
        "time_steps": 50,
        "fps": 10
    }
}
