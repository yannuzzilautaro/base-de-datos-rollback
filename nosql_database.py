import copy
from typing import Dict, List, Any, Callable
from contextlib import contextmanager

class Collection:
    """Modela una colección de documentos (similar a una tabla o colección NoSQL)."""
    def __init__(self, name: str):
        self.name = name
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.indexes: Dict[str, Dict[Any, List[str]]] = {}

    def insert(self, doc_id: str, data: Dict[str, Any]):
        if doc_id in self.documents:
            raise ValueError(f"Error de integridad: El documento con ID '{doc_id}' ya existe.")
        self.documents[doc_id] = data
        self._update_indexes_on_insert(doc_id, data)

    def create_index(self, field: str):
        """Crea un índice secundario para un campo específico, optimizando búsquedas."""
        self.indexes[field] = {}
        for doc_id, data in self.documents.items():
            if field in data:
                val = data[field]
                self.indexes[field].setdefault(val, []).append(doc_id)

    def find_by_index(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """Búsqueda optimizada utilizando el índice O(1)."""
        if field not in self.indexes:
            raise KeyError(f"El campo '{field}' no está indexado en esta colección.")
        doc_ids = self.indexes[field].get(value, [])
        return [self.documents[doc_id] for doc_id in doc_ids if doc_id in doc_ids]

    def find(self, query: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """Búsqueda secuencial utilizando un predicción funcional (Lambda)."""
        return [doc for doc in self.documents.values() if query(doc)]

    def _update_indexes_on_insert(self, doc_id: str, data: Dict[str, Any]):
        for field, value in data.items():
            if field in self.indexes:
                self.indexes[field].setdefault(value, []).append(doc_id)


class Database:
    """Orquestador principal de la base de datos con control transaccional."""
    def __init__(self):
        self.collections: Dict[str, Collection] = {}

    def get_collection(self, name: str) -> Collection:
        if name not in self.collections:
            self.collections[name] = Collection(name)
        return self.collections[name]

    @contextmanager
    def transaction(self):
        """
        Gestor de contexto que implementa transacciones atómicas (ACID-lite).
        Si ocurre un error, realiza un ROLLBACK restaurando el estado previo mediante Deepcopy.
        """
        snapshot = copy.deepcopy(self.collections)
        print("\n--- [TX] Iniciando transacción atómica ---")
        try:
            yield self
            print("--- [TX] Transacción completada con éxito (COMMIT) ---")
        except Exception as e:
            print(f"--- [TX] Error detectado ({e}). Revirtiendo cambios (ROLLBACK) ---")
            self.collections = snapshot
            raise



if __name__ == "__main__":
    db = Database()
    usuarios = db.get_collection("usuarios")


    try:
        with db.transaction():
            usuarios.insert("u1", {"nombre": "Lucía", "edad": 24, "ciudad": "Buenos Aires"})
            usuarios.insert("u2", {"nombre": "Mateo", "edad": 31, "ciudad": "Córdoba"})
            usuarios.insert("u3", {"nombre": "Sofía", "edad": 27, "ciudad": "Buenos Aires"})
            

            usuarios.create_index("ciudad")
    except Exception as err:
        print(f"Fallo en transacción 1: {err}")

  
    print("\n[Búsqueda por Índice - Ciudad: Buenos Aires]:")
    for u in usuarios.find_by_index("ciudad", "Buenos Aires"):
        print(f" > Encontrado: {u['nombre']} ({u['edad']} años)")


    try:
        with db.transaction():
            usuarios.insert("u4", {"nombre": "Esteban", "edad": 22, "ciudad": "Rosario"})
            print("Insertado temporalmente: Esteban")
            

            usuarios.insert("u1", {"nombre": "Intruso", "edad": 99, "ciudad": "Rosario"})
    except ValueError:
        print("La excepción fue manejada externamente.")


    print("\n[Búsqueda por Filtro Dinámico después del Rollback]:")
    mayores_30 = usuarios.find(lambda doc: doc["edad"] > 30)
    print(f"Usuarios mayores de 30 años (Solo Mateo debe aparecer): {[u['nombre'] for u in mayores_30]}")
    
    print(f"¿Existe el usuario u4?: {'u4' in usuarios.documents}")
    
