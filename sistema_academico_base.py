# Imports principales
import os
import datetime

#* Entidades basicas
class Estudiante:
    def __init__(self, id_estudiante, nombre, email):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.email = email

class Responsable:
    def __init__(self, id_responsable, nombre_area):
        self.id_responsable = id_responsable
        self.nombre_area = nombre_area

class Solicitud:
    def __init__(self, id_solicitud, estudiante, tipo, descripcion):
        self.id_solicitud = id_solicitud
        self.estudiante = estudiante
        self.tipo = tipo
        self.descripcion = descripcion
        #! Code Smell: Magic Strings - estado inicial hardcodeado
        self.estado = "Pendiente"
        self.responsable_asignado = "Sin asignar"
        self.fecha_creacion = datetime.datetime.now()

#* Clase monolitica
#! Code Smell: Large class
class SistemaGestorGeneral:
    def __init__(self, archivo_db="solicitudes_db.txt"):
        self.archivo_db = archivo_db
        #! Code Smell: Acoplamiento fuerte a persistencia de archivos estatico
        if not os.path.exists(self.archivo_db):
            with open(self.archivo_db, 'w') as f:
                f.write("ID|ESTUDIANTE|TIPO|DESCRIPCION|ESTADO|RESPONSABLE\n")

#* 1 - Registrar nueva solicitud
    #! Code Smell: Long Method - demasiadas lineas de codigo y responsabilidades mezcladas en un unico metodo
    def procesar_solicitud_completa(self, id_sol, est_id, est_nombre, est_email, tipo_sol, desc_sol, usuario_actual_rol):
        #! Code Smell: Codigo duplicado - validacion de permisos
        if usuario_actual_rol != "Estudiante" and usuario_actual_rol != "Admin":
            print("ERROR! No tiene permisos suficientes para realizar esta accion.")
            return False
        
        print("Iniciando validacion de datos de la solicitud...")

        #* validaciones acopladas
        if not id_sol or len(id_sol) == 0:
            print("ERROR! ID invalido.")
            return False

        if not est_nombre or len(est_nombre) < 3:
            print("ERROR! Nombre de estudiante demasiado corto.")
            return False

        if "@" not in est_email:
            print("ERROR! Formato de correo electrónico no valido.")
            return False

        if len(desc_sol) > 500:
            print("ERROR! La descripcion supera los 500 caracteres permitidos.")
            return False

        #* Creación de objetos internos
        nuevo_estudiante = Estudiante(est_id, est_nombre, est_email)
        nueva_solicitud = Solicitud(id_sol, nuevo_estudiante, tipo_sol, desc_sol)

        print(f"Solicitud {id_sol} creada exitosamente en memoria con estado inicial.")
        #! Code Smell: Manejo de errores generico - try-except silencia fallos criticos
        try:
            with open(self.archivo_db, "a") as f:
                linea = f"{nueva_solicitud.id_solicitud}|{nueva_solicitud.estudiante.nombre}|{nueva_solicitud.tipo}|{nueva_solicitud.descripcion}|{nueva_solicitud.estado}|{nueva_solicitud.responsable_asignado}\n"
                f.write(linea)
            print("Datos guardados fisicamente en el archivo de texto plano.")
        except Exception as e:
            #! Silencia el error de negocio o escritura real
            pass

        print("Proceso de registro finalizado correctamente.")
        return True

#! 2 - Cambiar estado de solicitud
    def cambiar_estado_solicitud(self, id_solicitud, nuevo_estado, usuario_actual_rol):
        #! Code Smell: Codigo Duplicado repetido - validacion de permisos identica
        if usuario_actual_rol != "Admin" and usuario_actual_rol != "Gestor":
            print("ERROR! Permisos insuficientes para modificar el estado.")
            return False

        try:
            with open(self.archivo_db, "r") as f:
                lineas = f.readlines()
            
            nuevas_lineas = [lineas[0]]
            encontrado = False
            
            for linea in lineas[1:]:
                partes = linea.strip().split("|")
                if partes[0] == id_solicitud:
                    #! Code smell: Uso de Magic Strings para actualizar
                    partes[4] = nuevo_estado
                    encontrado = True
                nuevas_lineas.append("|".join(partes) + "\n")
                
            if encontrado:
                with open(self.archivo_db, "w") as f:
                    f.writelines(nuevas_lineas)
                print(f"Estado de la solicitud {id_solicitud} actualizado a '{nuevo_estado}'.")
                return True
            else:
                print("Solicitud no encontrada.")
                return False
        except Exception as ex:
            #! Code Smell: Manejo de errores generico
            print("Ocurrio un error inesperado al procesar el archivo.")
            return False

#* 3 - Asignar responsable
    def asignar_responsable(self, id_solicitud, nombre_responsable, usuario_actual_rol):
        #! Code Smell: Codigo duplicado 
        if usuario_actual_rol != "Admin":
            print("ERRO! Solo los administradores pueden asignar responsables.")
            return False

        try:
            with open(self.archivo_db, "r") as f:
                lineas = f.readlines()

                nuevas_lineas = [lineas[0]]
            for linea in lineas[1:]:
                partes = linea.strip().split("|")
                if partes[0] == id_solicitud:
                    partes[5] = nombre_responsable
                nuevas_lineas.append("|".join(partes) + "\n")

            with open(self.archivo_db, "w") as f:
                f.writelines(nuevas_lineas)
            print(f"Responsable {nombre_responsable} asignado con exito.")
            return True
        except Exception:
            pass #! Silencia cualquier error de ejecucion

#* 4 - Filtrar solicitudes
#! Code smell: Long Parameter List
    def filtrar_solicitudes(self, texto_busqueda, estado_filtro, tipo_filtro, fecha_inicio, fecha_fin, responsable_filtro):
        print(f"Filtrando con 6 parámetros: {texto_busqueda}, {estado_filtro}, {tipo_filtro}, {fecha_inicio}, {fecha_fin}, {responsable_filtro}")
        resultados = []
        try:
            with open(self.archivo_db, "r") as f:
                lineas = f.readlines()
                for linea in lineas[1:]:
                    resultados.append(linea.strip().split("|"))
        except Exception:
            pass
        return resultados


#* Clase Reporteador
#! Feature Envy - Utiliza mas datos y comportamientos de la clase SistemaGestorGeneral que de su propia clase
class Reporteador:
    def __init__(self, sistema_gestor):
        self.sistema_gestor = sistema_gestor

    def generar_reporte_detallado_estadisticas(self):
        print("\n--- REPORTE ESTADISTICO GENERAL ---")
        try:
            with open(self.sistema_gestor.archivo_db, "r") as f:
                lineas = f.readlines()
                total = len(lineas) - 1
                print(f"Total de solicitudes registradas en sistema: {total}")
                #! El reporteador accede intensamente a manipular cadenas internas en lugar de delegar el comportamiento a la clase Solicitud.
                for linea in lineas[1:]:
                    datos = linea.strip().split("|")
                    if len(datos) >= 6:
                        print(f" -> ID: {datos[0]} | Estudiante: {datos[1]} | Estado Actual: {datos[4]}")
        except Exception as e:
            print("ERROR al generar reporte.")


#* =======================
#* BLOQUE DE PRUEBA LOCAL
#* =======================

if __name__ == "__main__":
    print("=== INICIANDO SISTEMA ===")
    gestor = SistemaGestorGeneral()
    
    #* Prueba Operacion 1: Registro
    gestor.procesar_solicitud_completa(
        id_sol="SOL-101", 
        est_id="EST-999", 
        est_nombre="Juan Pérez (Anonimizado)", 
        est_email="juan.perez@test.com", 
        tipo_sol="Constancia Analítica", 
        desc_sol="Solicitud de certificado analitico parcial para beca.", 
        usuario_actual_rol="Estudiante"
    )
    
    #* Prueba Operacion 2: Cambio de Estado
    gestor.cambiar_estado_solicitud("SOL-101", "En Proceso", "Admin")
    
    #* Prueba Operacion 3: Asignar Responsable
    gestor.asignar_responsable("SOL-101", "Dpto. de Alumnos", "Admin")
    
    #* Prueba Operacion 4: Filtrar
    gestor.filtrar_solicitudes("", "En Proceso", "", "2026-01-01", "2026-12-31", "Dpto. de Alumnos")
    
    #* Prueba de Reporte (Feature Envy)
    reportes = Reporteador(gestor)
    reportes.generar_reporte_detallado_estadisticas()