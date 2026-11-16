from modelos import conectar_bd
import controlador


def menu_usuarios():
    while True:
        print("\n--- Módulo de Usuarios (CRUD) ---")
        print("1. Registrar Usuario (Create)")
        print("2. Listar Usuarios (Read)")
        print("3. Ver Perfil Completo de Usuario (Read)")
        print("4. Modificar Usuario (Update)")
        print("5. Eliminar Usuario (Delete)")
        print("6. Regresar al Menú Principal")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                email = input("Email: ")
                nombre = input("Nombre completo: ")
                profesion = input("Profesión: ")
                controlador.registrar_usuario(email, nombre, profesion)
                print("Usuario registrado exitosamente.")

            elif opcion == "2":
                usuarios = controlador.obtener_usuarios()
                if not usuarios:
                    print("No hay usuarios registrados.")
                for u in usuarios:
                    print(f"[{u.email}] {u.nombre} - {u.profesion}")

            elif opcion == "3":
                email = input("Email del usuario a consultar: ")
                perfil = controlador.obtener_perfil_usuario(email)
                u = perfil["usuario"]
                print(f"\nPerfil de {u.nombre} ({u.email}) | Profesión: {u.profesion}")

                print("  Empresas:")
                if not perfil["empresas"]:
                    print("    - Sin empresa registrada")
                for emp_nom, ind, puesto in perfil["empresas"]:
                    print(f"    - {emp_nom} ({ind}) | Puesto: {puesto}")

                print("  Habilidades:")
                if not perfil["habilidades"]:
                    print("    - Sin habilidades registradas")
                for hab_nom, cat, nivel in perfil["habilidades"]:
                    print(f"    - {hab_nom} [{cat}] | Nivel: {nivel}")

                print("  Contactos directos:")
                if not perfil["contactos"]:
                    print("    - Sin contactos directos")
                for c_nom, c_email, c_prof, desde in perfil["contactos"]:
                    print(f"    - {c_nom} ({c_email}) - {c_prof} (Desde: {desde})")

            elif opcion == "4":
                email = input("Email del usuario a modificar: ")
                nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ")
                profesion = input("Nueva profesión (dejar en blanco para no cambiar): ")
                controlador.actualizar_usuario(email, nombre, profesion)
                print("Usuario modificado exitosamente.")

            elif opcion == "5":
                email = input("Email del usuario a eliminar: ")
                controlador.eliminar_usuario(email)
                print("Usuario eliminado exitosamente.")

            elif opcion == "6":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"Error: {e}")


def menu_empresas_habilidades():
    while True:
        print("\n--- Módulo de Empresas y Habilidades (CRUD) ---")
        print("1. Registrar Empresa")
        print("2. Consultar Empresas")
        print("3. Modificar Industria de Empresa")
        print("4. Eliminar Empresa")
        print("5. Registrar Habilidad")
        print("6. Consultar Habilidades")
        print("7. Eliminar Habilidad")
        print("8. Regresar al Menú Principal")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                nombre = input("Nombre de la empresa: ")
                industria = input("Industria: ")
                controlador.registrar_empresa(nombre, industria)
                print("Empresa registrada exitosamente.")

            elif opcion == "2":
                empresas = controlador.obtener_empresas()
                if not empresas:
                    print("No hay empresas registradas.")
                for e in empresas:
                    print(f"- {e.nombre} | Industria: {e.industria}")

            elif opcion == "3":
                nombre = input("Nombre de la empresa a modificar: ")
                industria = input("Nueva industria: ")
                controlador.actualizar_empresa(nombre, industria)
                print("Empresa actualizada exitosamente.")

            elif opcion == "4":
                nombre = input("Nombre de la empresa a eliminar: ")
                controlador.eliminar_empresa(nombre)
                print("Empresa eliminada exitosamente.")

            elif opcion == "5":
                nombre = input("Nombre de la habilidad: ")
                categoria = input("Categoría (ej. Lenguaje, Base de Datos, Cloud): ")
                controlador.registrar_habilidad(nombre, categoria)
                print("Habilidad registrada exitosamente.")

            elif opcion == "6":
                habilidades = controlador.obtener_habilidades()
                if not habilidades:
                    print("No hay habilidades registradas.")
                for h in habilidades:
                    print(f"- {h.nombre} | Categoría: {h.categoria}")

            elif opcion == "7":
                nombre = input("Nombre de la habilidad a eliminar: ")
                controlador.eliminar_habilidad(nombre)
                print("Habilidad eliminada exitosamente.")

            elif opcion == "8":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"Error: {e}")


def menu_relaciones():
    while True:
        print("\n--- Módulo de Relaciones del Grafo ---")
        print("1. Conectar dos Usuarios (CONOCE_A)")
        print("2. Asignar o Actualizar Empresa de un Usuario (TRABAJA_EN)")
        print("3. Asignar o Actualizar Habilidad de un Usuario (TIENE_HABILIDAD)")
        print("4. Eliminar Conexión entre dos Usuarios")
        print("5. Regresar al Menú Principal")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                e1 = input("Email del primer usuario: ")
                e2 = input("Email del segundo usuario: ")
                desde = input("Año desde que se conocen (ej. 2024): ")
                controlador.conectar_usuarios(e1, e2, desde)
                print("Relación CONOCE_A guardada exitosamente.")

            elif opcion == "2":
                email = input("Email del usuario: ")
                empresa = input("Nombre de la empresa: ")
                puesto = input("Puesto o rol: ")
                controlador.asignar_empresa_usuario(email, empresa, puesto)
                print("Relación TRABAJA_EN guardada exitosamente.")

            elif opcion == "3":
                email = input("Email del usuario: ")
                habilidad = input("Nombre de la habilidad: ")
                nivel = input("Nivel (Básico / Intermedio / Avanzado): ")
                controlador.asignar_habilidad_usuario(email, habilidad, nivel)
                print("Relación TIENE_HABILIDAD guardada exitosamente.")

            elif opcion == "4":
                e1 = input("Email del primer usuario: ")
                e2 = input("Email del segundo usuario: ")
                controlador.desconectar_usuarios(e1, e2)
                print("Conexión eliminada exitosamente.")

            elif opcion == "5":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"Error: {e}")


def menu_consultas_grafo():
    while True:
        print("\n--- Consultas Especializadas de Grafo ---")
        print("1. Recomendar contactos ('Personas que quizás conozcas' - 2 saltos)")
        print("2. Buscar camino más corto entre dos usuarios (shortestPath)")
        print("3. Buscar profesionales con habilidades en común")
        print("4. Buscar contactos (1er o 2do grado) que trabajen en una empresa")
        print("5. Regresar al Menú Principal")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                email = input("Email del usuario: ")
                sugerencias = controlador.recomendar_contactos(email)
                if not sugerencias:
                    print("No se encontraron recomendaciones nuevas para este usuario.")
                else:
                    print("\nPersonas que quizás conozcas:")
                    for nom, em, prof, comun, lista_comun in sugerencias:
                        puentes = ", ".join(lista_comun)
                        print(
                            f"- {nom} ({em}) | {prof} | "
                            f"{comun} contacto(s) en común: {puentes}"
                        )

            elif opcion == "2":
                origen = input("Email del usuario origen: ")
                destino = input("Email del usuario destino: ")
                resultado = controlador.buscar_camino_mas_corto(origen, destino)
                if not resultado:
                    print("No se encontró ningún camino entre los usuarios indicados.")
                else:
                    saltos, ruta_texto = resultado
                    print(f"\nCamino más corto encontrado ({saltos} saltos):")
                    print(ruta_texto)

            elif opcion == "3":
                email = input("Email del usuario: ")
                colegas = controlador.buscar_colegas_por_habilidad(email)
                if not colegas:
                    print("No se encontraron otros usuarios con habilidades compartidas.")
                else:
                    print("\nProfesionales con habilidades compartidas:")
                    for nom, em, prof, hab, nivel in colegas:
                        print(f"- {nom} ({em}) - {prof} | Habilidad: {hab} ({nivel})")

            elif opcion == "4":
                email = input("Email del usuario: ")
                empresa = input("Nombre de la empresa objetivo: ")
                contactos = controlador.buscar_contactos_en_empresa(email, empresa)
                if not contactos:
                    print("No tienes contactos de 1er o 2do grado en esa empresa.")
                else:
                    print(f"\nContactos cercanos en {empresa.strip()}:")
                    for nom, em, puesto, emp in contactos:
                        print(f"- {nom} ({em}) | Puesto: {puesto} en {emp}")

            elif opcion == "5":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"Error: {e}")


def menu_principal():
    print("Conectando a Neo4j AuraDB en la nube...")
    try:
        conectar_bd()
        print("Conexión establecida correctamente.")
    except Exception as e:
        print(f"Error crítico de conexión: {e}")
        return

    while True:
        print("\n=== RED DE CONEXIONES PROFESIONALES (NEO4J AURADB) ===")
        print("1. Gestión de Usuarios (CRUD)")
        print("2. Gestión de Empresas y Habilidades (CRUD)")
        print("3. Gestión de Relaciones del Grafo")
        print("4. Consultas de Grafo y Recomendaciones")
        print("5. Salir")

        opcion = input("Seleccione un módulo: ").strip()

        if opcion == "1":
            menu_usuarios()
        elif opcion == "2":
            menu_empresas_habilidades()
        elif opcion == "3":
            menu_relaciones()
        elif opcion == "4":
            menu_consultas_grafo()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_principal()
