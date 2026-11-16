# Red de Conexiones Profesionales con Neo4j AuraDB y Python

En este proyecto desarrollé una aplicación por consola en Python conectada a una base de datos orientada a grafos alojada en la nube con **Neo4j AuraDB**. El sistema modela una red de contactos profesionales donde es posible gestionar usuarios, empresas y habilidades técnicas, así como ejecutar recorridos de grafo para recomendar contactos y encontrar caminos más cortos entre profesionales.

## 1. Organización del Proyecto

Para mantener el código limpio y fácil de mantener, dividí la aplicación en módulos siguiendo la misma separación en tres capas:

* **`modelos.py` (Capa de Datos y Conexión Cloud):** Carga las credenciales desde variables de entorno (`.env`), establece la conexión remota cifrada (`neo4j+s://`) hacia Neo4j AuraDB y define los nodos (`Usuario`, `Empresa`, `Habilidad`) y relaciones con propiedades (`ConoceA`, `TrabajaEn`, `TieneHabilidad`) mediante **Neomodel** (sobre el driver oficial `neo4j`).
* **`controlador.py` (Capa de Lógica y Consultas):** Implementa las validaciones, las operaciones CRUD completas de nodos y relaciones, y las consultas especializadas en Cypher (`shortestPath`, recomendación de contactos a 2 saltos, coincidencia de habilidades y búsqueda de contactos por empresa).
* **`main.py` (Capa de Presentación):** Presenta los menús interactivos en consola y captura las excepciones para evitar cierres abruptos durante la ejecución.
* **`seed.py` y `script_inicial.cypher` (Carga Inicial):** Configuran los *constraints* de unicidad e índices en la base de datos e insertan un conjunto inicial de usuarios, empresas, habilidades y relaciones para probar todas las funciones desde el primer momento.

## 2. Requerimientos Previos

* **Python 3.10+**
* Una instancia activa en la nube de **Neo4j AuraDB**.
* Conexión a internet para comunicarse por el protocolo Bolt sobre TLS (`neo4j+s://`).

## 3. Guía de Instalación

1. Clonar el repositorio y entrar a la carpeta del proyecto:
   ```bash
   git clone git@github.com:patrick-ortiz/red-profesional-neo4j.git
   cd red-profesional-neo4j
   ```

2. Crear y activar un entorno virtual de Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instalar las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno copiando el archivo de ejemplo `.env.example` a `.env` y colocando las credenciales de la instancia de Neo4j AuraDB:
   ```bash
   cp .env.example .env
   ```
   Contenido esperado en `.env`:
   ```env
   NEO4J_URI=neo4j+s://tu-instancia.databases.neo4j.io
   NEO4J_USERNAME=tu_usuario
   NEO4J_PASSWORD=tu_password
   NEO4J_DATABASE=tu_base_de_datos
   ```

## 4. Ejecución del Proyecto

### Paso 1: Poblar la base de datos con datos de prueba (Seeding)
Antes de iniciar las pruebas, ejecuta el script de carga inicial para registrar las restricciones de unicidad (`UNIQUE`) e insertar los nodos y relaciones base:
```bash
python seed.py
```

### Paso 2: Iniciar la aplicación interactiva
```bash
python main.py
```

## 5. Funcionalidades Principales

1. **CRUD Completo:** Alta, consulta general y detallada, actualización y eliminación de nodos (`Usuario`, `Empresa`, `Habilidad`), además de creación, actualización y borrado de relaciones (`CONOCE_A`, `TRABAJA_EN`, `TIENE_HABILIDAD`).
2. **Recomendación de Contactos (Vecindad a 2 saltos):** Sugiere personas que el usuario aún no conoce directamente pero que son contactos de sus conocidos actuales, ordenadas por número de contactos en común.
3. **Camino Más Corto (`shortestPath`):** Calcula la cadena mínima de conexiones que enlaza a dos profesionales dentro del grafo.
4. **Recorridos por Habilidades y Empresas:** Localiza colegas que comparten tecnologías específicas o contactos de primer y segundo grado que trabajan en una empresa determinada.
