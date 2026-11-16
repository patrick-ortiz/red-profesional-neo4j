from neomodel import db
from modelos import Usuario, Empresa, Habilidad


# --- Operaciones CRUD: Usuarios ---

def registrar_usuario(email, nombre, profesion):
    email = email.strip().lower()
    nombre = nombre.strip()
    profesion = profesion.strip()

    if not email or not nombre or not profesion:
        raise ValueError("El email, nombre y profesión son obligatorios.")

    if Usuario.nodes.get_or_none(email=email):
        raise ValueError(f"Ya existe un usuario registrado con el email {email}.")

    usuario = Usuario(email=email, nombre=nombre, profesion=profesion)
    return usuario.save()


def obtener_usuarios():
    return Usuario.nodes.all()


def buscar_usuario_por_email(email):
    email = email.strip().lower()
    usuario = Usuario.nodes.get_or_none(email=email)
    if not usuario:
        raise ValueError(f"No se encontró ningún usuario con el email {email}.")
    return usuario


def obtener_perfil_usuario(email):
    usuario = buscar_usuario_por_email(email)

    empresas_info = []
    for emp in usuario.empresas.all():
        rel = usuario.empresas.relationship(emp)
        empresas_info.append((emp.nombre, emp.industria, rel.puesto))

    habilidades_info = []
    for hab in usuario.habilidades.all():
        rel = usuario.habilidades.relationship(hab)
        habilidades_info.append((hab.nombre, hab.categoria, rel.nivel))

    query_contactos = """
    MATCH (u:Usuario {email: $email})-[r:CONOCE_A]-(c:Usuario)
    RETURN DISTINCT c.nombre, c.email, c.profesion, r.desde
    ORDER BY c.nombre
    """
    contactos_res, _ = db.cypher_query(query_contactos, {"email": usuario.email})

    return {
        "usuario": usuario,
        "empresas": empresas_info,
        "habilidades": habilidades_info,
        "contactos": contactos_res,
    }


def actualizar_usuario(email, nuevo_nombre=None, nueva_profesion=None):
    usuario = buscar_usuario_por_email(email)

    if nuevo_nombre is not None and nuevo_nombre.strip():
        usuario.nombre = nuevo_nombre.strip()
    if nueva_profesion is not None and nueva_profesion.strip():
        usuario.profesion = nueva_profesion.strip()

    return usuario.save()


def eliminar_usuario(email):
    usuario = buscar_usuario_por_email(email)
    usuario.delete()
    return True


# --- Operaciones CRUD: Empresas ---

def registrar_empresa(nombre, industria):
    nombre = nombre.strip()
    industria = industria.strip()

    if not nombre or not industria:
        raise ValueError("El nombre y la industria de la empresa son obligatorios.")

    if Empresa.nodes.get_or_none(nombre=nombre):
        raise ValueError(f"La empresa '{nombre}' ya está registrada.")

    empresa = Empresa(nombre=nombre, industria=industria)
    return empresa.save()


def obtener_empresas():
    return Empresa.nodes.all()


def buscar_empresa_por_nombre(nombre):
    empresa = Empresa.nodes.get_or_none(nombre=nombre.strip())
    if not empresa:
        raise ValueError(f"No se encontró la empresa '{nombre.strip()}'.")
    return empresa


def actualizar_empresa(nombre, nueva_industria):
    empresa = buscar_empresa_por_nombre(nombre)
    if not nueva_industria or not nueva_industria.strip():
        raise ValueError("La nueva industria no puede estar vacía.")
    empresa.industria = nueva_industria.strip()
    return empresa.save()


def eliminar_empresa(nombre):
    empresa = buscar_empresa_por_nombre(nombre)
    empresa.delete()
    return True


# --- Operaciones CRUD: Habilidades ---

def registrar_habilidad(nombre, categoria):
    nombre = nombre.strip()
    categoria = categoria.strip()

    if not nombre or not categoria:
        raise ValueError("El nombre y la categoría de la habilidad son obligatorios.")

    if Habilidad.nodes.get_or_none(nombre=nombre):
        raise ValueError(f"La habilidad '{nombre}' ya está registrada.")

    habilidad = Habilidad(nombre=nombre, categoria=categoria)
    return habilidad.save()


def obtener_habilidades():
    return Habilidad.nodes.all()


def buscar_habilidad_por_nombre(nombre):
    habilidad = Habilidad.nodes.get_or_none(nombre=nombre.strip())
    if not habilidad:
        raise ValueError(f"No se encontró la habilidad '{nombre.strip()}'.")
    return habilidad


def eliminar_habilidad(nombre):
    habilidad = buscar_habilidad_por_nombre(nombre)
    habilidad.delete()
    return True


# --- Gestión de Relaciones del Grafo ---

def conectar_usuarios(email1, email2, desde):
    u1 = buscar_usuario_por_email(email1)
    u2 = buscar_usuario_por_email(email2)

    if u1.email == u2.email:
        raise ValueError("Un usuario no puede conectarse consigo mismo.")

    try:
        anio = int(str(desde).strip())
    except ValueError:
        raise ValueError("El año de inicio de la relación debe ser un número entero.")

    query_existe = """
    MATCH (a:Usuario {email: $e1})-[r:CONOCE_A]-(b:Usuario {email: $e2})
    SET r.desde = $desde
    RETURN count(r)
    """
    res, _ = db.cypher_query(
        query_existe, {"e1": u1.email, "e2": u2.email, "desde": anio}
    )
    if res[0][0] > 0:
        return True

    u1.contactos.connect(u2, {"desde": anio})
    return True


def desconectar_usuarios(email1, email2):
    u1 = buscar_usuario_por_email(email1)
    u2 = buscar_usuario_por_email(email2)

    query = """
    MATCH (a:Usuario {email: $e1})-[r:CONOCE_A]-(b:Usuario {email: $e2})
    DELETE r
    RETURN count(r)
    """
    res, _ = db.cypher_query(query, {"e1": u1.email, "e2": u2.email})
    if res[0][0] == 0:
        raise ValueError("No existe una relación CONOCE_A entre estos usuarios.")
    return True


def asignar_empresa_usuario(email, nombre_empresa, puesto):
    usuario = buscar_usuario_por_email(email)
    empresa = buscar_empresa_por_nombre(nombre_empresa)
    puesto = puesto.strip()

    if not puesto:
        raise ValueError("El puesto no puede estar vacío.")

    if usuario.empresas.is_connected(empresa):
        rel = usuario.empresas.relationship(empresa)
        rel.puesto = puesto
        rel.save()
        return rel

    return usuario.empresas.connect(empresa, {"puesto": puesto})


def asignar_habilidad_usuario(email, nombre_habilidad, nivel):
    usuario = buscar_usuario_por_email(email)
    habilidad = buscar_habilidad_por_nombre(nombre_habilidad)
    nivel = nivel.strip()

    if not nivel:
        raise ValueError("El nivel de dominio no puede estar vacío.")

    if usuario.habilidades.is_connected(habilidad):
        rel = usuario.habilidades.relationship(habilidad)
        rel.nivel = nivel
        rel.save()
        return rel

    return usuario.habilidades.connect(habilidad, {"nivel": nivel})


# --- Consultas Especializadas de Grafo (Traversals y Caminos) ---

def recomendar_contactos(email):
    usuario = buscar_usuario_por_email(email)
    query = """
    MATCH (u:Usuario {email: $email})-[:CONOCE_A]-(contacto:Usuario)-[:CONOCE_A]-(sugerido:Usuario)
    WHERE u <> sugerido AND NOT (u)-[:CONOCE_A]-(sugerido)
    RETURN sugerido.nombre, sugerido.email, sugerido.profesion,
           count(DISTINCT contacto) AS en_comun,
           collect(DISTINCT contacto.nombre) AS contactos_comunes
    ORDER BY en_comun DESC, sugerido.nombre ASC
    """
    resultados, _ = db.cypher_query(query, {"email": usuario.email})
    return resultados


def buscar_camino_mas_corto(email_origen, email_destino):
    u1 = buscar_usuario_por_email(email_origen)
    u2 = buscar_usuario_por_email(email_destino)

    if u1.email == u2.email:
        raise ValueError("Debes ingresar dos usuarios distintos para calcular el camino.")

    query = """
    MATCH (p1:Usuario {email: $email1}), (p2:Usuario {email: $email2}),
    path = shortestPath((p1)-[*..10]-(p2))
    RETURN path
    """
    params = {"email1": u1.email, "email2": u2.email}
    results, _ = db.cypher_query(query, params)

    if not results or not results[0]:
        return None

    path = results[0][0]
    partes = []
    for i in range(len(path.nodes)):
        nodo = path.nodes[i]
        etiqueta = list(nodo.labels)[0]
        nombre = nodo.get("nombre") or nodo.get("email", "Sin nombre")
        partes.append(f"({etiqueta}: {nombre})")

        if i < len(path.relationships):
            rel = path.relationships[i]
            tipo_rel = rel.type
            props = []
            for k, v in rel.items():
                props.append(f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {v}")
            info_props = f" {{{', '.join(props)}}}" if props else ""
            partes.append(f"-[:{tipo_rel}{info_props}]-")

    return len(path), " ".join(partes)


def buscar_colegas_por_habilidad(email):
    usuario = buscar_usuario_por_email(email)
    query = """
    MATCH (u:Usuario {email: $email})-[:TIENE_HABILIDAD]->(h:Habilidad)<-[r:TIENE_HABILIDAD]-(colega:Usuario)
    WHERE u <> colega
    RETURN colega.nombre, colega.email, colega.profesion, h.nombre, r.nivel
    ORDER BY h.nombre, colega.nombre
    """
    resultados, _ = db.cypher_query(query, {"email": usuario.email})
    return resultados


def buscar_contactos_en_empresa(email, nombre_empresa):
    usuario = buscar_usuario_por_email(email)
    empresa = buscar_empresa_por_nombre(nombre_empresa)

    query = """
    MATCH (u:Usuario {email: $email})-[:CONOCE_A*1..2]-(contacto:Usuario)-[r:TRABAJA_EN]->(e:Empresa {nombre: $empresa})
    WHERE u <> contacto
    RETURN DISTINCT contacto.nombre, contacto.email, r.puesto, e.nombre
    ORDER BY contacto.nombre
    """
    resultados, _ = db.cypher_query(
        query, {"email": usuario.email, "empresa": empresa.nombre}
    )
    return resultados
