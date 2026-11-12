"""
excepciones.py
==============
Módulo de excepciones personalizadas para el Sistema Software FJ.
Define una jerarquía de excepciones que permite identificar y manejar
de forma controlada cada tipo de error del sistema.
"""


class SistemaFJException(Exception):
    """
    Excepción base del sistema Software FJ.
    Todas las excepciones del sistema heredan de esta clase.
    """

    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        if self.codigo:
            return f"[Error {self.codigo}] {self.mensaje}"
        return self.mensaje


class ClienteInvalidoException(SistemaFJException):
    """Se lanza cuando los datos de un cliente son inválidos o incompletos."""
    pass


class ParametroFaltanteException(SistemaFJException):
    """Se lanza cuando un parámetro obligatorio no se proporciona."""
    pass


class ServicioNoDisponibleException(SistemaFJException):
    """Se lanza cuando un servicio no está disponible o sus parámetros son incorrectos."""
    pass


class ReservaInvalidaException(SistemaFJException):
    """Se lanza cuando una reserva contiene datos inválidos o no puede procesarse."""
    pass


class OperacionNoPermitidaException(SistemaFJException):
    """Se lanza cuando se intenta una operación que el estado actual no permite."""
    pass


class DuracionInvalidaException(SistemaFJException):
    """Se lanza cuando la duración proporcionada no es válida."""
    pass


class CapacidadExcedidaException(SistemaFJException):
    """Se lanza cuando se supera la capacidad máxima de un servicio."""
    pass
