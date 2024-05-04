import numpy as np

# Configuración inicial
num_servidores = 3
tasa_llegada = 5  # clientes por minuto
tasa_servicio = 7  # clientes por minuto
tiempo_simulacion = 60  # minutos

# Estado inicial del sistema
estado_servidores = [0] * num_servidores  # 0 indica que el servidor está libre
cola = []
tiempo_en_sistema = []

# Simulación
np.random.seed(42)
tiempo_actual = 0
while tiempo_actual < tiempo_simulacion:
    # Determinar el próximo evento
    llegada_cliente = np.random.exponential(1/tasa_llegada)
    salida_cliente = [np.random.exponential(1/tasa_servicio) if servidor > 0 else float('inf') for servidor in estado_servidores]
    
    proximo_evento = min([llegada_cliente] + salida_cliente)
    
    # Actualizar el tiempo actual
    tiempo_actual += proximo_evento
    
    # Procesar llegada de cliente
    if proximo_evento == llegada_cliente:
        # Verificar si hay un servidor libre
        servidor_libre = -1
        for i, servidor in enumerate(estado_servidores):
            if servidor == 0:
                servidor_libre = i
                break
        
        if servidor_libre >= 0:
            # Asignar cliente al servidor libre
            estado_servidores[servidor_libre] = tiempo_actual
        else:
            # Añadir cliente a la cola
            cola.append(tiempo_actual)
    
    # Procesar salida de cliente
    else:
        # Identificar el servidor que completó el servicio
        servidor = salida_cliente.index(proximo_evento)
        estado_servidores[servidor] = 0
        
        # Registrar el tiempo en el sistema
        tiempo_en_sistema.append(tiempo_actual - estado_servidores[servidor])
        
        if cola:
            # Asignar el siguiente cliente en la cola al servidor que se liberó
            estado_servidores[servidor] = tiempo_actual
            tiempo_en_sistema.append(tiempo_actual - cola.pop(0))

# Métricas
tiempo_promedio_en_sistema = np.mean(tiempo_en_sistema)
utilizacion_servidores = sum([1 for servidor in estado_servidores if servidor > 0]) / num_servidores

print(f"Tiempo promedio en el sistema: {tiempo_promedio_en_sistema:.2f} minutos")
print(f"Utilización de los servidores: {utilizacion_servidores:.2f}")