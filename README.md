# base-de-datos-rollback
Es un prototipo de base de datos NoSQL en memoria escrito en Python. Permite guardar documentos, indexar campos para búsquedas rápidas y utilizar bloques with para garantizar que las operaciones sean atómicas: si algo falla dentro de una transacción, se hace un rollback automático para no corromper los datos.
