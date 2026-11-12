"""
sistema.py
==========
Módulo central del Sistema Software FJ.
Coordina el registro de clientes, la creación de servicios
y la gestión de reservas, delegando el manejo de errores al Logger.
"""

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import SistemaFJException
from logger import Logger


class SistemaFJ:
    """
    Clase principal del sistema.
    Actúa como fachada (Facade) que centraliza todas las operaciones
    y garantiza el registro de eventos en el archivo de logs.
    """

    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        self.__logger = Logger.obtener_instancia()
        self.__logger.evento("Sistema Software FJ inicializado correctamente.")

    # GESTIÓN DE CLIENTES
    

    def registrar_cliente(self, nombre, apellido, email, telefono, documento) -> Cliente:
        """Registra un nuevo cliente con manejo completo de excepciones."""
        try:
            cliente = Cliente(nombre, apellido, email, telefono, documento)
            cliente.validar()
            self.__clientes.append(cliente)
            self.__logger.evento(f"Cliente registrado: {cliente}")
            return cliente
        except SistemaFJException as e:
            self.__logger.error(f"Error al registrar cliente '{nombre} {apellido}': {e}")
            raise
        except Exception as e:
            self.__logger.error(f"Error inesperado al registrar cliente: {e}")
            raise SistemaFJException(f"Error inesperado: {e}", "SYS001")

    # GESTIÓN DE SERVICIOS

    def crear_servicio_sala(self, nombre, numero_sala,
                             capacidad=20, precio=50_000) -> ReservaSala:
        """Crea un servicio de reserva de sala."""
        try:
            srv = ReservaSala(nombre, numero_sala, capacidad, precio)
            self.__servicios.append(srv)
            self.__logger.evento(f"Servicio creado: {srv.describir()}")
            return srv
        except SistemaFJException as e:
            self.__logger.error(f"Error al crear servicio de sala '{nombre}': {e}")
            raise

    def crear_servicio_equipo(self, nombre, tipo_equipo,
                               cantidad=5, precio=30_000) -> AlquilerEquipo:
        """Crea un servicio de alquiler de equipos."""
        try:
            srv = AlquilerEquipo(nombre, tipo_equipo, cantidad, precio)
            self.__servicios.append(srv)
            self.__logger.evento(f"Servicio creado: {srv.describir()}")
            return srv
        except SistemaFJException as e:
            self.__logger.error(f"Error al crear servicio de equipo '{nombre}': {e}")
            raise

    def crear_servicio_asesoria(self, nombre, area,
                                 asesor, precio=80_000) -> AsesoriaEspecializada:
        """Crea un servicio de asesoría especializada."""
        try:
            srv = AsesoriaEspecializada(nombre, area, asesor, precio)
            self.__servicios.append(srv)
            self.__logger.evento(f"Servicio creado: {srv.describir()}")
            return srv
        except SistemaFJException as e:
            self.__logger.error(f"Error al crear servicio de asesoría '{nombre}': {e}")
            raise

    # GESTIÓN DE RESERVAS

    def crear_reserva(self, cliente, servicio, duracion_horas, **kwargs) -> Reserva:
        """Crea y confirma una reserva. Registra el evento en el log."""
        try:
            reserva = Reserva(cliente, servicio, duracion_horas, **kwargs)
            costo = reserva.confirmar()
            self.__reservas.append(reserva)
            self.__logger.evento(
                f"Reserva #{reserva.id} confirmada | "
                f"Cliente: {cliente.nombre_completo} | "
                f"Servicio: {servicio.nombre} | "
                f"Duración: {duracion_horas}h | "
                f"Costo: ${costo:,.2f}"
            )
            return reserva
        except SistemaFJException as e:
            self.__logger.error(f"Error al crear reserva: {e}")
            raise
        except Exception as e:
            self.__logger.error(f"Error inesperado en reserva: {e}")
            raise

    def cancelar_reserva(self, reserva: Reserva, motivo: str):
        """Cancela una reserva existente y registra el evento."""
        try:
            reserva.cancelar(motivo)
            self.__logger.evento(
                f"Reserva #{reserva.id} cancelada. Motivo: {motivo}"
            )
        except SistemaFJException as e:
            self.__logger.error(f"Error al cancelar reserva #{reserva.id}: {e}")
            raise

    # REPORTES Y CONSULTAS

    def listar_clientes(self):
        """Imprime todos los clientes registrados."""
        self.__logger.info(f"Clientes registrados: {len(self.__clientes)}")
        for c in self.__clientes:
            print(f"    → {c.describir()}")

    def listar_servicios(self):
        """Imprime todos los servicios disponibles."""
        self.__logger.info(f"Servicios disponibles: {len(self.__servicios)}")
        for s in self.__servicios:
            print(f"    → {s.describir()}")

    def listar_reservas(self):
        """Imprime todas las reservas del sistema."""
        self.__logger.info(f"Total de reservas: {len(self.__reservas)}")
        for r in self.__reservas:
            print(f"    → {r}")

    def resumen_sistema(self):
        """Imprime el resumen general del sistema."""
        confirmadas = sum(1 for r in self.__reservas if r.estado == "CONFIRMADA")
        canceladas  = sum(1 for r in self.__reservas if r.estado == "CANCELADA")
        completadas = sum(1 for r in self.__reservas if r.estado == "COMPLETADA")
        total_ingresos = sum(
            r.costo for r in self.__reservas
            if r.costo is not None and r.estado in ("CONFIRMADA", "COMPLETADA")
        )

        sep = "=" * 65
        print(f"\n{sep}")
        print("  RESUMEN GENERAL — SISTEMA SOFTWARE FJ")
        print(sep)
        print(f"  Clientes registrados  : {len(self.__clientes)}")
        print(f"  Servicios en sistema  : {len(self.__servicios)}")
        print(f"  Total reservas        : {len(self.__reservas)}")
        print(f"    ✓ Confirmadas       : {confirmadas}")
        print(f"    ✓ Completadas       : {completadas}")
        print(f"    ✗ Canceladas        : {canceladas}")
        print(f"  Ingresos acumulados   : ${total_ingresos:,.2f} COP")
        print(sep)
