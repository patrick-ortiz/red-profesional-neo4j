// =========================================================================
// Script de Base de Datos y Datos Iniciales (Neo4j AuraDB - Cypher)
// Proyecto: Red de Conexiones Profesionales
// Alumno: Ortiz Meron Patrick Rafael
// =========================================================================

// 1. Restricciones de unicidad (Constraints) e Índices
CREATE CONSTRAINT constraint_unique_Usuario_email IF NOT EXISTS
FOR (u:Usuario) REQUIRE u.email IS UNIQUE;

CREATE CONSTRAINT constraint_unique_Empresa_nombre IF NOT EXISTS
FOR (e:Empresa) REQUIRE e.nombre IS UNIQUE;

CREATE CONSTRAINT constraint_unique_Habilidad_nombre IF NOT EXISTS
FOR (h:Habilidad) REQUIRE h.nombre IS UNIQUE;

CREATE INDEX index_Usuario_profesion IF NOT EXISTS
FOR (u:Usuario) ON (u.profesion);

// 2. Limpieza opcional antes de poblar pruebas
MATCH (n) DETACH DELETE n;

// 3. Creación de nodos Empresa
CREATE (:Empresa {nombre: 'TechCorp', industria: 'Desarrollo de Software'});
CREATE (:Empresa {nombre: 'DataMayab', industria: 'Analítica e Inteligencia de Negocios'});
CREATE (:Empresa {nombre: 'CloudSur', industria: 'Infraestructura en la Nube'});

// 4. Creación de nodos Habilidad
CREATE (:Habilidad {nombre: 'Python', categoria: 'Lenguaje de Programación'});
CREATE (:Habilidad {nombre: 'Neo4j', categoria: 'Bases de Datos NoSQL'});
CREATE (:Habilidad {nombre: 'PostgreSQL', categoria: 'Bases de Datos Relacionales'});
CREATE (:Habilidad {nombre: 'Docker', categoria: 'DevOps'});
CREATE (:Habilidad {nombre: 'AWS', categoria: 'Cloud Computing'});

// 5. Creación de nodos Usuario
CREATE (:Usuario {email: 'ana@correo.com', nombre: 'Ana López', profesion: 'Ingeniera Backend'});
CREATE (:Usuario {email: 'carlos@correo.com', nombre: 'Carlos Ruiz', profesion: 'Analista de Datos'});
CREATE (:Usuario {email: 'sofia@correo.com', nombre: 'Sofía Méndez', profesion: 'Arquitecta Cloud'});
CREATE (:Usuario {email: 'diego@correo.com', nombre: 'Diego Torres', profesion: 'Administrador de BD'});
CREATE (:Usuario {email: 'valeria@correo.com', nombre: 'Valeria Castro', profesion: 'Desarrolladora Full Stack'});
CREATE (:Usuario {email: 'marco@correo.com', nombre: 'Marco Herrera', profesion: 'Ingeniero DevOps'});

// 6. Creación de relaciones laborales (:TRABAJA_EN)
MATCH (u:Usuario {email: 'ana@correo.com'}), (e:Empresa {nombre: 'TechCorp'})
CREATE (u)-[:TRABAJA_EN {puesto: 'Desarrolladora Backend'}]->(e);

MATCH (u:Usuario {email: 'valeria@correo.com'}), (e:Empresa {nombre: 'TechCorp'})
CREATE (u)-[:TRABAJA_EN {puesto: 'Líder Técnico'}]->(e);

MATCH (u:Usuario {email: 'carlos@correo.com'}), (e:Empresa {nombre: 'DataMayab'})
CREATE (u)-[:TRABAJA_EN {puesto: 'Analista Senior'}]->(e);

MATCH (u:Usuario {email: 'diego@correo.com'}), (e:Empresa {nombre: 'DataMayab'})
CREATE (u)-[:TRABAJA_EN {puesto: 'DBA Principal'}]->(e);

MATCH (u:Usuario {email: 'sofia@correo.com'}), (e:Empresa {nombre: 'CloudSur'})
CREATE (u)-[:TRABAJA_EN {puesto: 'Arquitecta de Soluciones'}]->(e);

MATCH (u:Usuario {email: 'marco@correo.com'}), (e:Empresa {nombre: 'CloudSur'})
CREATE (u)-[:TRABAJA_EN {puesto: 'Especialista SRE'}]->(e);

// 7. Creación de relaciones de habilidades (:TIENE_HABILIDAD)
MATCH (u:Usuario {email: 'ana@correo.com'}), (h:Habilidad {nombre: 'Python'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Avanzado'}]->(h);

MATCH (u:Usuario {email: 'ana@correo.com'}), (h:Habilidad {nombre: 'Neo4j'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Intermedio'}]->(h);

MATCH (u:Usuario {email: 'carlos@correo.com'}), (h:Habilidad {nombre: 'Python'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Intermedio'}]->(h);

MATCH (u:Usuario {email: 'carlos@correo.com'}), (h:Habilidad {nombre: 'PostgreSQL'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Avanzado'}]->(h);

MATCH (u:Usuario {email: 'diego@correo.com'}), (h:Habilidad {nombre: 'Neo4j'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Avanzado'}]->(h);

MATCH (u:Usuario {email: 'diego@correo.com'}), (h:Habilidad {nombre: 'PostgreSQL'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Avanzado'}]->(h);

MATCH (u:Usuario {email: 'sofia@correo.com'}), (h:Habilidad {nombre: 'AWS'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Avanzado'}]->(h);

MATCH (u:Usuario {email: 'marco@correo.com'}), (h:Habilidad {nombre: 'Docker'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Avanzado'}]->(h);

MATCH (u:Usuario {email: 'marco@correo.com'}), (h:Habilidad {nombre: 'AWS'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Intermedio'}]->(h);

MATCH (u:Usuario {email: 'valeria@correo.com'}), (h:Habilidad {nombre: 'Python'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Avanzado'}]->(h);

MATCH (u:Usuario {email: 'valeria@correo.com'}), (h:Habilidad {nombre: 'Docker'})
CREATE (u)-[:TIENE_HABILIDAD {nivel: 'Intermedio'}]->(h);

// 8. Creación de relaciones entre profesionales (:CONOCE_A)
MATCH (u1:Usuario {email: 'ana@correo.com'}), (u2:Usuario {email: 'carlos@correo.com'})
CREATE (u1)-[:CONOCE_A {desde: 2023}]->(u2);

MATCH (u1:Usuario {email: 'carlos@correo.com'}), (u2:Usuario {email: 'diego@correo.com'})
CREATE (u1)-[:CONOCE_A {desde: 2024}]->(u2);

MATCH (u1:Usuario {email: 'diego@correo.com'}), (u2:Usuario {email: 'sofia@correo.com'})
CREATE (u1)-[:CONOCE_A {desde: 2025}]->(u2);

MATCH (u1:Usuario {email: 'sofia@correo.com'}), (u2:Usuario {email: 'marco@correo.com'})
CREATE (u1)-[:CONOCE_A {desde: 2025}]->(u2);

MATCH (u1:Usuario {email: 'ana@correo.com'}), (u2:Usuario {email: 'valeria@correo.com'})
CREATE (u1)-[:CONOCE_A {desde: 2024}]->(u2);
