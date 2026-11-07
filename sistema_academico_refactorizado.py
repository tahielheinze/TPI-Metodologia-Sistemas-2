# Imports principales
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


#* -- 1. ENUMS Y OBJETOS DE PARAMETROS --
class EstadoSolicitud:
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"

@dataclass
class FiltroSolicitudDTO:
    #* Code Smell Resuelto: Se reemplaza la larga lista de parametros por un DTO estructurado
    texto_busqueda: Optional[str] = None
    estado: Optional[str] = None
    tipo: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    responsable: Optional[str] = None

#* -- 2. ENTIDADES DE DOMINIO --
class Estudiante:
    def __init__(self, id_estudiante: str, nombre: str, email: str):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.email = email

    def validar(self) -> bool:
        return len(self.nombre) >= 3 and "@" in self.email


class Solicitud:
    def __init__(self, id_solicitud: str, estudiante: Estudiante, tipo: str, descripcion: str):
        self.id_solicitud = id_solicitud
        self.estudiante = estudiante
        self.tipo = tipo
        self.descripcion = descripcion
        self.estado = EstadoSolicitud.PENDIENTE
        self.responsable_asignado = "Sin Asignar"
        self.fecha_creacion = datetime.now()

    #* Code Smell Resuelto (Feature Envy): La logica de negocio recae en la entidad misma
    def actualizar_estado(self, nuevo_estado: str) -> None:
        self.estado = nuevo_estado

    def asignar_responsable(self, responsable: str) -> None:
        self.responsable_asignado = responsable

#* -- 3. ABSTRACCION DE PERSISTENCIA --
class ISolicitudRepository(ABC):
    @abstractmethod
    def guardar(self, solicitud: Solicitud) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id_solicitud: str) -> Optional[Solicitud]:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Solicitud]:
        pass

class SolicitudMemoryRepository(ISolicitudRepository):
    #* Code Smell Resuelto: Se desacopla de archivos planos fijos y se usa memoria estructurada limpia
    def __init__(self):
        self._almacen: List[Solicitud] = []

    def guardar(self, solicitud: Solicitud) -> None:
        #* Si ya existe una solicitud la actualiza, sino la agrega.
        existente = self.obtener_por_id(solicitud.id_solicitud)
        if existente:
            self._almacen.remove(existente)
        self._almacen.append(solicitud)

    def obtener_por_id(self, id_solicitud: str) -> Optional[Solicitud]:
        for s in self._almacen:
            if s.id_solicitud == id_solicitud:
                return s
        return None

    def obtener_todos(self) -> List[Solicitud]:
        return list(self._almacen)

#* -- 4. SERVICIOS ESPECIALIZADOS --
class PermisoService:
    #* Code Smell Resuelto: Codigo duplicado de permisos centralizado en un unico servicio
    @staticmethod
    def verificar_permiso(rol_usuario: str, accion: str) -> bool:
        roles_permitidos = {
            "registrar": ["Estudiante", "Admin"],
            "cambiar_estado": ["Admin", "Gestor"],
            "asignar": ["Admin"]
        }
        return rol_usuario in roles_permitidos.get(accion, [])


class SolicitudService:
    def __init__(self, repository: ISolicitudRepository):
        self.repository = repository

    #* Code Smell Resuelto (Long Method): Metodo descompuesto en funciones pequenias (Extract Method)
    def registrar_solicitud(self, id_sol: str, estudiante: Estudiante, tipo: str, desc: str, rol: str) -> bool:
        if not PermisoService.verificar_permiso(rol, "registrar"):
            raise PermissionError("Acceso denegado: permisos insuficientes.")

        self._validar_datos(id_sol, estudiante, desc)

        nueva_solicitud = Solicitud(id_sol, estudiante, tipo, desc)
        self.repository.guardar(nueva_solicitud)
        return True

    def _validar_datos(self, id_sol: str, estudiante: Estudiante, desc: str) -> None:
        if not id_sol:
            raise ValueError("El ID de solicitud no puede estar vacio.")
        if not estudiante.validar():
            raise ValueError("Datos del estudiante invalidos.")
        if len(desc) > 500:
            raise ValueError("La descripcion excede los 500 caracteres.")

    def cambiar_estado(self, id_solicitud: str, nuevo_estado: str, rol: str) -> None:
        if not PermisoService.verificar_permiso(rol, "cambiar_estado"):
            raise PermissionError("Permisos insuficientes para modificar estado.")

        solicitud = self.repository.obtener_por_id(id_solicitud)
        if not solicitud:
            raise LookupError(f"Solicitud {id_solicitud} no encontrada.")

        solicitud.actualizar_estado(nuevo_estado)
        self.repository.guardar(solicitud)

    def asignar_responsable(self, id_solicitud: str, responsable: str, rol: str) -> None:
        if not PermisoService.verificar_permiso(rol, "asignar"):
            raise PermissionError("Solo los administradores pueden asignar responsables.")

        solicitud = self.repository.obtener_por_id(id_solicitud)
        if not solicitud:
            raise LookupError(f"Solicitud {id_solicitud} no encontrada.")

        solicitud.asignar_responsable(responsable)
        self.repository.guardar(solicitud)

    #* Code Smell Resuelto (Long parameter list): Utiliza el objeto FiltroSolicitudDTO
    def filtrar(self, filtro: FiltroSolicitudDTO) -> List[Solicitud]:
        todas = self.repository.obtener_todos()
        resultado = []
        for s in todas:
            if filtro.estado and s.estado != filtro.estado:
                continue
            if filtro.responsable and s.responsable_asignado != filtro.responsable:
                continue
            resultado.append(s)
        return resultado

class ReporteService:
    def __init__(self, repository: ISolicitudRepository):
        self.repository = repository

    def generar_reporte_estadistico(self) -> None:
        solicitudes = self.repository.obtener_todos()
        print(f"\n--- REPORTE ESTADISTICO PROFESIONAL ---")
        print(f"Total de solicitudes: {len(solicitudes)}")
        for s in solicitudes:
            print(f" -> ID: {s.id_solicitud} | Estudiante: {s.estudiante.nombre} | Estado: {s.estado}")

#* =======================
#* BLOQUE DE PRUEBA LOCAL
#* =======================

if __name__ == "__main__":
    print("=== INICIANDO SISTEMA REFACTORIZADO (ESTADO REFACTORIZADO) ===")
    
    repo = SolicitudMemoryRepository()
    servicio = SolicitudService(repo)
    reporteador = ReporteService(repo)

    est = Estudiante("EST-999", "Alumno Demo", "alumnodemo@test.com")

    #* Prueba Operacion 1: Registro
    servicio.registrar_solicitud("SOL-101", est, "Constancia", "Certificado parcial de notas.", "Estudiante")
    
    #* Prueba Operacion 2: Cambio de Estado
    servicio.cambiar_estado("SOL-101", EstadoSolicitud.EN_PROCESO, "Admin")
    
    #* Prueba Operacion 3: Asignar Responsable
    servicio.asignar_responsable("SOL-101", "Dpto. Alumnos", "Admin")
    
    #* Prueba Operacion 4: Filtrar con DTO
    filtro = FiltroSolicitudDTO(estado=EstadoSolicitud.EN_PROCESO)
    filtrados = servicio.filtrar(filtro)
    print(f"Solicitudes filtradas encontradas: {len(filtrados)}")

    #* Prueba de Reporte
    reporteador.generar_reporte_estadistico()