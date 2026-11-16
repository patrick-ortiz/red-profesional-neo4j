from neomodel import db
from modelos import conectar_bd
import controlador


def poblar_base_de_datos(limpiar=True):
    conectar_bd()

    print("Configurando restricciones e índices en Neo4j AuraDB...")
    db.install_all_labels()

    if limpiar:
        print("Limpiando datos previos del grafo...")
        db.cypher_query("MATCH (n) DETACH DELETE n")

    print("Insertando empresas...")
    controlador.registrar_empresa("TechCorp", "Desarrollo de Software")
    controlador.registrar_empresa("DataMayab", "Analítica e Inteligencia de Negocios")
    controlador.registrar_empresa("CloudSur", "Infraestructura en la Nube")

    print("Insertando habilidades...")
    controlador.registrar_habilidad("Python", "Lenguaje de Programación")
    controlador.registrar_habilidad("Neo4j", "Bases de Datos NoSQL")
    controlador.registrar_habilidad("PostgreSQL", "Bases de Datos Relacionales")
    controlador.registrar_habilidad("Docker", "DevOps")
    controlador.registrar_habilidad("AWS", "Cloud Computing")

    print("Insertando usuarios...")
    controlador.registrar_usuario("ana@correo.com", "Ana López", "Ingeniera Backend")
    controlador.registrar_usuario("carlos@correo.com", "Carlos Ruiz", "Analista de Datos")
    controlador.registrar_usuario("sofia@correo.com", "Sofía Méndez", "Arquitecta Cloud")
    controlador.registrar_usuario("diego@correo.com", "Diego Torres", "Administrador de BD")
    controlador.registrar_usuario("valeria@correo.com", "Valeria Castro", "Desarrolladora Full Stack")
    controlador.registrar_usuario("marco@correo.com", "Marco Herrera", "Ingeniero DevOps")

    print("Creando relaciones laborales (TRABAJA_EN)...")
    controlador.asignar_empresa_usuario("ana@correo.com", "TechCorp", "Desarrolladora Backend")
    controlador.asignar_empresa_usuario("valeria@correo.com", "TechCorp", "Líder Técnico")
    controlador.asignar_empresa_usuario("carlos@correo.com", "DataMayab", "Analista Senior")
    controlador.asignar_empresa_usuario("diego@correo.com", "DataMayab", "DBA Principal")
    controlador.asignar_empresa_usuario("sofia@correo.com", "CloudSur", "Arquitecta de Soluciones")
    controlador.asignar_empresa_usuario("marco@correo.com", "CloudSur", "Especialista SRE")

    print("Creando relaciones de habilidades (TIENE_HABILIDAD)...")
    controlador.asignar_habilidad_usuario("ana@correo.com", "Python", "Avanzado")
    controlador.asignar_habilidad_usuario("ana@correo.com", "Neo4j", "Intermedio")
    controlador.asignar_habilidad_usuario("carlos@correo.com", "Python", "Intermedio")
    controlador.asignar_habilidad_usuario("carlos@correo.com", "PostgreSQL", "Avanzado")
    controlador.asignar_habilidad_usuario("diego@correo.com", "Neo4j", "Avanzado")
    controlador.asignar_habilidad_usuario("diego@correo.com", "PostgreSQL", "Avanzado")
    controlador.asignar_habilidad_usuario("sofia@correo.com", "AWS", "Avanzado")
    controlador.asignar_habilidad_usuario("marco@correo.com", "Docker", "Avanzado")
    controlador.asignar_habilidad_usuario("marco@correo.com", "AWS", "Intermedio")
    controlador.asignar_habilidad_usuario("valeria@correo.com", "Python", "Avanzado")
    controlador.asignar_habilidad_usuario("valeria@correo.com", "Docker", "Intermedio")

    print("Creando red de contactos (CONOCE_A)...")
    controlador.conectar_usuarios("ana@correo.com", "carlos@correo.com", 2023)
    controlador.conectar_usuarios("carlos@correo.com", "diego@correo.com", 2024)
    controlador.conectar_usuarios("diego@correo.com", "sofia@correo.com", 2025)
    controlador.conectar_usuarios("sofia@correo.com", "marco@correo.com", 2025)
    controlador.conectar_usuarios("ana@correo.com", "valeria@correo.com", 2024)

    print("Carga inicial completada correctamente en Neo4j AuraDB.")


if __name__ == "__main__":
    try:
        poblar_base_de_datos(limpiar=True)
    except Exception as e:
        print(f"Error durante la carga inicial: {e}")
