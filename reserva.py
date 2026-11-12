"""
reserva.py
==========
Módulo de gestión de reservas del Sistema Software FJ.
Integra: Cliente, Servicio, duración y estado.
Implementa: confirmación, cancelación y procesamiento con manejo de excepciones.
"""

from datetime import datetime
from excepciones import (
    ReservaInvalidaException,
    OperacionNoPermitidaException,
    ParametroFaltanteException,
    DuracionInvalidaException,
)


class Reserva:
    """
    Clase que representa una reserva dentro del sistema Software FJ.
    Gestiona el ciclo de vida completo: PENDIENTE → CONFIRMADA → COMPLETADA
                                                              ↘ CANCELADA
    """

    ESTADOS_VALIDOS = ("PENDIENTE", "PROCESANDO", "CONFIRMADA", "COMPLETADA", "CANCELADA")
    _contador = 0

    def __init__(self, cliente, servicio, duracion_horas: float,
                 fecha_reserva: datetime = None, **kwargs):
        self._validar_inputs(cliente, servicio, duracion_horas)

        Reserva._contador += 1
        self.__id = Reserva._contador
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion_horas = duracion_horas
        self.__fecha_reserva = fecha_reserva or datetime.now()
        self.__kwargs = kwargs              # Parámetros extras del servicio
        self.__estado = "PENDIENTE"
        self.__costo = None
        self.__fecha_confirmacion = None
        self.__fecha_cancelacion = None
        self.__motivo_cancelacion = None
        self.__historial = []

        self.__registrar(f"Reserva #{self.__id} creada en estado PENDIENTE.")

    # VALIDACIÓN INTERNA

    def _validar_inputs(self, cliente, servicio, duracion_horas):
        """Valida los parámetros obligatorios de la reserva."""
        if cliente is None:
            raise ParametroFaltanteException("El cliente es obligatorio.", "R001")
        if servicio is None:
            raise ParametroFaltanteException("El servicio es obligatorio.", "R002")
        if duracion_horas is None or not isinstance(duracion_horas, (int, float)):
            raise DuracionInvalidaException(
                "La duración debe ser un número válido.", "R003"
            )
        if duracion_horas <= 0:
            raise DuracionInvalidaException(
                "La duración debe ser mayor a 0 horas.", "R004"
            )

    def __registrar(self, mensaje: str):
        """Agrega una entrada al historial interno de la reserva."""
        entrada = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}"
        self.__historial.append(entrada)

    # PROPIEDADES

    @property
    def id(self):
        return self.__id

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def estado(self):
        return self.__estado

    @property
    def duracion_horas(self):
        return self.__duracion_horas

    @property
    def costo(self):
        return self.__costo

    @property
    def historial(self):
        """Retorna una copia del historial de la reserva."""
        return list(self.__historial)

    # OPERACIONES PRINCIPALES

    def confirmar(self) -> float:
        """
        Confirma la reserva: verifica disponibilidad, calcula costo
        y cambia el estado a CONFIRMADA.
        Retorna el costo calculado.
        """
        try:
            if self.__estado != "PENDIENTE":
                raise OperacionNoPermitidaException(
                    f"Solo se pueden confirmar reservas en estado PENDIENTE. "
                    f"Estado actual: '{self.__estado}'.",
                    "R005",
                )

            # Verificar disponibilidad del servicio
            self.__servicio.verificar_disponibilidad()

            # Cambiar a estado PROCESANDO mientras se calcula
            self.__estado = "PROCESANDO"
            self.__registrar("Estado cambiado a PROCESANDO.")

            # Calcular costo (puede lanzar excepciones del servicio)
            self.__costo = self.__servicio.calcular_costo(
                self.__duracion_horas, **self.__kwargs
            )

            # Confirmar
            self.__estado = "CONFIRMADA"
            self.__fecha_confirmacion = datetime.now()
            self.__registrar(
                f"Reserva CONFIRMADA. Costo: ${self.__costo:,.2f} COP."
            )

            # Registrar en el cliente
            self.__cliente.agregar_reserva(self)

            return self.__costo

        except Exception as e:
            # Si falla, dejar en PENDIENTE para reintentar
            self.__estado = "PENDIENTE"
            self.__registrar(f"ERROR al confirmar: {e}")
            raise

    def cancelar(self, motivo: str = "Sin motivo especificado"):
        """
        Cancela la reserva. No se puede cancelar si ya está CANCELADA o COMPLETADA.
        """
        try:
            if self.__estado == "CANCELADA":
                raise OperacionNoPermitidaException(
                    "La reserva ya se encuentra cancelada.", "R006"
                )
            if self.__estado == "COMPLETADA":
                raise OperacionNoPermitidaException(
                    "No se puede cancelar una reserva que ya fue completada.", "R007"
                )

            estado_anterior = self.__estado
            self.__estado = "CANCELADA"
            self.__fecha_cancelacion = datetime.now()
            self.__motivo_cancelacion = motivo
            self.__registrar(
                f"Reserva CANCELADA (antes: {estado_anterior}). Motivo: {motivo}"
            )

        except Exception as e:
            self.__registrar(f"ERROR al cancelar: {e}")
            raise

    def completar(self):
        """Marca la reserva como COMPLETADA (solo desde CONFIRMADA)."""
        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaException(
                f"Solo se pueden completar reservas CONFIRMADAS. "
                f"Estado actual: '{self.__estado}'.",
                "R008",
            )
        self.__estado = "COMPLETADA"
        self.__registrar("Reserva COMPLETADA exitosamente.")

    # MÉTODOS SOBRECARGADOS — cálculo con variantes

    def obtener_costo_con_impuesto(self, tasa: float = None) -> float:
        """Retorna el costo de la reserva incluyendo impuestos."""
        if self.__costo is None:
            raise ReservaInvalidaException(
                "El costo aún no ha sido calculado (reserva no confirmada).", "R009"
            )
        tasa_real = tasa if tasa is not None else self.__servicio.TASA_IVA
        return round(self.__costo * (1 + tasa_real), 2)

    def obtener_costo_con_descuento(self, porcentaje: float = 0) -> float:
        """Retorna el costo de la reserva con descuento aplicado."""
        if self.__costo is None:
            raise ReservaInvalidaException(
                "El costo aún no ha sido calculado (reserva no confirmada).", "R010"
            )
        if not (0 <= porcentaje <= 1):
            raise ReservaInvalidaException(
                "El porcentaje de descuento debe estar entre 0.0 y 1.0.", "R011"
            )
        return round(self.__costo * (1 - porcentaje), 2)

    # REPRESENTACIÓN

    def __str__(self):
        costo_str = f"${self.__costo:,.2f}" if self.__costo is not None else "Por calcular"
        return (
            f"Reserva #{self.__id} | "
            f"Cliente: {self.__cliente.nombre_completo} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion_horas}h | "
            f"Estado: {self.__estado} | "
            f"Costo: {costo_str}"
        )

    def __repr__(self):
        return self.__str__()
