"""
cliente.py
==========
Módulo de gestión de clientes del Sistema Software FJ.
Aplica encapsulación robusta y validaciones estrictas en cada campo.
"""

import re
from entidad_base import EntidadBase
from excepciones import ClienteInvalidoException, ParametroFaltanteException


class Cliente(EntidadBase):
    """
    Clase Cliente con encapsulación de datos personales y validaciones estrictas.
    Hereda de EntidadBase e implementa sus métodos abstractos.
    """

    def __init__(self, nombre: str, apellido: str, email: str,
                 telefono: str, documento: str):
        super().__init__(nombre)
        # Atributos privados inicializados a None antes de usar setters
        self.__apellido = None
        self.__email = None
        self.__telefono = None
        self.__documento = None
        self.__reservas = []

        # Asignación mediante setters con validación
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.documento = documento

    # PROPIEDADES CON ENCAPSULACIÓN

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        if not valor:
            raise ParametroFaltanteException("El apellido es obligatorio.", "C001")
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ClienteInvalidoException(
                "El apellido debe tener al menos 2 caracteres.", "C002"
            )
        self.__apellido = valor.strip().title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if not valor:
            raise ParametroFaltanteException("El email es obligatorio.", "C003")
        patron = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron, str(valor).strip()):
            raise ClienteInvalidoException(
                f"El email '{valor}' no tiene un formato válido (ej: user@dominio.com).", "C004"
            )
        self.__email = str(valor).strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor:
            raise ParametroFaltanteException("El teléfono es obligatorio.", "C005")
        limpio = str(valor).replace(" ", "").replace("-", "").replace("+", "")
        if not limpio.isdigit():
            raise ClienteInvalidoException(
                "El teléfono solo puede contener dígitos.", "C006"
            )
        if not (7 <= len(limpio) <= 15):
            raise ClienteInvalidoException(
                "El teléfono debe tener entre 7 y 15 dígitos.", "C007"
            )
        self.__telefono = limpio

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteException("El número de documento es obligatorio.", "C008")
        doc = str(valor).strip()
        if len(doc) < 6:
            raise ClienteInvalidoException(
                "El documento debe tener al menos 6 caracteres.", "C009"
            )
        self.__documento = doc

    @property
    def nombre_completo(self):
        """Retorna nombre y apellido concatenados."""
        return f"{self._nombre} {self.__apellido}"

    @property
    def reservas(self):
        """Lista de reservas del cliente (copia defensiva)."""
        return list(self.__reservas)

    # MÉTODOS PÚBLICOS

    def agregar_reserva(self, reserva):
        """Registra una reserva en el historial del cliente."""
        self.__reservas.append(reserva)

    def validar(self) -> bool:
        """Verifica que todos los datos del cliente estén completos."""
        errores = []
        if not self._nombre:
            errores.append("nombre")
        if not self.__apellido:
            errores.append("apellido")
        if not self.__email:
            errores.append("email")
        if not self.__telefono:
            errores.append("teléfono")
        if not self.__documento:
            errores.append("documento")
        if errores:
            raise ClienteInvalidoException(
                f"Faltan campos obligatorios: {', '.join(errores)}.", "C010"
            )
        return True

    def describir(self) -> str:
        return (
            f"Cliente #{self._id}: {self.nombre_completo} | "
            f"Doc: {self.__documento} | "
            f"Email: {self.__email} | "
            f"Tel: {self.__telefono} | "
            f"Reservas: {len(self.__reservas)}"
        )

    def __str__(self):
        return f"Cliente[{self._id}]: {self.nombre_completo} ({self.__documento})"
