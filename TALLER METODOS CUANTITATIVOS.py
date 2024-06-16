import pulp

# Definición de los datos del problema
professores = ["A", "B", "C", "D", "E"]
cursos = ["C1", "C2", "C3", "C4", "C5"]
preferencias = {
    "A": [5, 7, 9, 8, 6],
    "B": [8, 2, 10, 7, 9],
    "C": [5, 3, 8, 9, 9],
    "D": [9, 8, 8, 10, 10],
    "E": [7, 7, 5, 9, 5]
}

# Crear el problema de optimización
problem = pulp.LpProblem("Asignacion_Profesores_Cursos", pulp.LpMaximize)

# Definir las variables de decisión
x = pulp.LpVariable.dicts("x", [(i, j) for i in professores for j in cursos], cat='Binary')

# Función objetivo
problem += pulp.lpSum(preferencias[i][j.index(c)] * x[(i, c)] for i in professores for j, c in enumerate(cursos)), "Total_Preferencias"

# Restricciones
for i in professores:
    problem += pulp.lpSum(x[(i, c)] for c in cursos) == 1, f"Profesor_{i}"

for c in cursos:
    problem += pulp.lpSum(x[(i, c)] for i in profesores) == 1, f"Curso_{c}"

# Resolver el problema
problem.solve()

# Imprimir los resultados
print("Estado:", pulp.LpStatus[problem.status])
for i in profesores:
    for c in cursos:
        if x[(i, c)].value() == 1:
            print(f"Profesor {i} asignado al curso {c} con preferencia {preferencias[i][cursos.index(c)]}")

# Imprimir el valor óptimo de la función objetivo
print("Valor óptimo total de preferencias:", pulp.value(problem.objective))
