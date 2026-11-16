import os
from dotenv import load_dotenv
from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    IntegerProperty,
    RelationshipTo,
    db,
)

RUTA_ENV = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(RUTA_ENV)

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")


def conectar_bd():
    if not NEO4J_URI or not NEO4J_USERNAME or not NEO4J_PASSWORD:
        raise RuntimeError(
            "Faltan variables de entorno en el archivo .env "
            "(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)."
        )

    esquema, host = NEO4J_URI.split("://", 1)
    host = host.rstrip("/")
    url_conexion = f"{esquema}://{NEO4J_USERNAME}:{NEO4J_PASSWORD}@{host}"
    if NEO4J_DATABASE:
        url_conexion = f"{url_conexion}/{NEO4J_DATABASE}"

    try:
        db.set_connection(url_conexion)
        db.cypher_query("RETURN 1")
    except Exception as e:
        raise ConnectionError(
            f"No se pudo establecer conexión con Neo4j AuraDB ({NEO4J_URI}). "
            f"Verifica que la instancia esté activa en console.neo4j.io. Detalle: {e}"
        )


# Modelos de Relaciones (con propiedades)
class ConoceA(StructuredRel):
    desde = IntegerProperty(required=True)


class TrabajaEn(StructuredRel):
    puesto = StringProperty(required=True)


class TieneHabilidad(StructuredRel):
    nivel = StringProperty(required=True)


# Modelos de Nodos
class Empresa(StructuredNode):
    nombre = StringProperty(unique_index=True, required=True)
    industria = StringProperty(required=True)


class Habilidad(StructuredNode):
    nombre = StringProperty(unique_index=True, required=True)
    categoria = StringProperty(required=True)


class Usuario(StructuredNode):
    email = StringProperty(unique_index=True, required=True)
    nombre = StringProperty(required=True)
    profesion = StringProperty(required=True, index=True)

    contactos = RelationshipTo("Usuario", "CONOCE_A", model=ConoceA)
    empresas = RelationshipTo("Empresa", "TRABAJA_EN", model=TrabajaEn)
    habilidades = RelationshipTo("Habilidad", "TIENE_HABILIDAD", model=TieneHabilidad)
