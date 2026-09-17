# In-Memory NoSQL Database with Transactions

Motor de base de datos documental en memoria desarrollado en Python. Permite manipular documentos estilo JSON, implementar índices secundarios para optimizar búsquedas y gestionar transacciones atómicas con soporte de rollback.

## Características Principales

* **Almacenamiento Documental:** Gestión de documentos mediante IDs únicos.
* **Índices Secundarios:** Búsquedas optimizadas en tiempo constante $O(1)$ sobre campos específicos.
* **Consultas Flexibles:** Filtrado dinámico utilizando predicados y funciones lambda.
* **Control Transaccional (ACID-lite):** Garantiza la atipicidad de operaciones mediante gestores de contexto (`contextmanager`) y copias de estado (`deepcopy`).

## Estructura del Código

* `Collection`: Modela la colección de documentos e índices secundarios.
* `Database`: Administrador general que maneja el ciclo de vida de las colecciones y las transacciones (`commit` / `rollback`).

## Requisitos y Ejecución

* **Python 3.7+** (no requiere librerías externas).

Para probar el proyecto, cloná el repositorio y ejecutá el script principal:

```bash
python nosql_database.py
