"""
servicios.py
============
Módulo de servicios del Sistema Software FJ.
Contiene:
  - Servicio        : clase abstracta base.
  - ReservaSala     : reserva de salas para reuniones y eventos.
  - AlquilerEquipo  : alquiler de equipos tecnológicos.
  - AsesoriaEspecializada : asesorías en distintas áreas.

Aplica: herencia, polimorfismo, métodos sobrescritos y sobrecargados.
"""

from abc import abstractmethod
from entidad_base import EntidadBase
from excepciones import (
    ServicioNoDisponibleException,
    ParametroFaltanteException,
    CapacidadExcedidaException,
    DuracionInvalidaException,
)


# CLASE ABSTRACTA BASE — Servicio

class Servicio(EntidadBase):
    """
    Clase abstracta que representa un servicio genérico de Software FJ.
    Define la interfaz común (precio, disponibilidad, cálculo de costos)
    que todas las subclases deben implementar o extender.
    """

    TASA_IVA = 0.19  # IVA del 19 %

    def __init__(self, nombre: str, descripcion: str,
                 precio_base: float, disponible: bool = True):
        super().__init__(nombre)
        self._descripcion = descripcion
        self._disponible = disponible
        self._precio_base = None
        self.precio_base = precio_base          # Usa el setter con validación

    # Propiedades
    @property
    def precio_base(self):
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor):
        if valor is None:
            raise ParametroFaltanteException("El precio base es obligatorio.", "S001")
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ServicioNoDisponibleException(
                f"El precio debe ser un número positivo. Recibido: {valor}.", "S002"
            )
        self._precio_base = float(valor)

    @property
    def disponible(self):
        return self._disponible

    @property
    def descripcion(self):
        return self._descripcion

    #  Disponibilidad
    def marcar_disponible(self):
        self._disponible = True

    def marcar_no_disponible(self):
        self._disponible = False

    def verificar_disponibilidad(self):
        """Lanza excepción si el servicio no está disponible."""
        if not self._disponible:
            raise ServicioNoDisponibleException(
                f"El servicio '{self._nombre}' no está disponible en este momento.", "S003"
            )

    # MÉTODOS SOBRECARGADOS — cálculo de costos (variantes)

    @abstractmethod
    def calcular_costo(self, duracion_horas, **kwargs) -> float:
        """Calcula el costo base del servicio según duración y parámetros."""
        pass

    def calcular_costo_con_impuesto(self, duracion_horas,
                                     tasa_impuesto: float = None, **kwargs) -> float:
        """
        Variante sobrecargada: calcula el costo incluyendo impuestos.
        Si no se pasa tasa_impuesto, usa la tasa IVA predeterminada.
        """
        costo = self.calcular_costo(duracion_horas, **kwargs)
        tasa = tasa_impuesto if tasa_impuesto is not None else self.TASA_IVA
        return round(costo * (1 + tasa), 2)

    def calcular_costo_con_descuento(self, duracion_horas,
                                      porcentaje_descuento: float = 0, **kwargs) -> float:
        """
        Variante sobrecargada: calcula el costo aplicando un descuento.
        porcentaje_descuento: valor entre 0.0 y 1.0 (ej. 0.1 = 10 %).
        """
        if not (0 <= porcentaje_descuento <= 1):
            raise ServicioNoDisponibleException(
                "El descuento debe estar entre 0.0 y 1.0.", "S004"
            )
        costo = self.calcular_costo(duracion_horas, **kwargs)
        return round(costo * (1 - porcentaje_descuento), 2)

    def calcular_costo_completo(self, duracion_horas,
                                 porcentaje_descuento: float = 0,
                                 tasa_impuesto: float = None, **kwargs) -> float:
        """
        Variante sobrecargada: aplica descuento e impuesto en un solo paso.
        """
        costo_desc = self.calcular_costo_con_descuento(
            duracion_horas, porcentaje_descuento, **kwargs
        )
        tasa = tasa_impuesto if tasa_impuesto is not None else self.TASA_IVA
        return round(costo_desc * (1 + tasa), 2)

    # Abstractos 
    @abstractmethod
    def validar_parametros(self, duracion_horas, **kwargs):
        """Valida los parámetros específicos del servicio."""
        pass

    def validar(self) -> bool:
        if self._precio_base is None or self._precio_base <= 0:
            raise ServicioNoDisponibleException("Precio base inválido.", "S005")
        return True

    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"Servicio #{self._id}: {self._nombre} | "
            f"{self._descripcion} | "
            f"Precio/h: ${self._precio_base:,.0f} | {estado}"
        )


# SERVICIO 1 — Reserva de Sala

class ReservaSala(Servicio):
    """
    Servicio de reserva de salas para reuniones y eventos.
    Aplica cargo adicional cuando el número de personas supera los 10.
    """

    def __init__(self, nombre: str, numero_sala: str,
                 capacidad_maxima: int = 20, precio_base: float = 50_000):
        super().__init__(
            nombre=nombre,
            descripcion="Reserva de sala para reuniones y eventos corporativos",
            precio_base=precio_base,
        )
        self.__numero_sala = numero_sala
        self.__capacidad_maxima = capacidad_maxima

    @property
    def numero_sala(self):
        return self.__numero_sala

    @property
    def capacidad_maxima(self):
        return self.__capacidad_maxima

    def calcular_costo(self, duracion_horas, numero_personas: int = 1, **kwargs) -> float:
        """
        Polimorfismo: calcula el costo según horas y número de personas.
        Se aplica un recargo del 15 % cuando hay más de 10 personas.
        """
        self.validar_parametros(duracion_horas, numero_personas=numero_personas)
        costo = self._precio_base * duracion_horas
        if numero_personas > 10:
            costo *= 1.15
        return round(costo, 2)

    def validar_parametros(self, duracion_horas, **kwargs):
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise DuracionInvalidaException(
                "La duración debe ser un número mayor a 0 horas.", "RS001"
            )
        if duracion_horas > 12:
            raise DuracionInvalidaException(
                "La duración máxima de una reserva de sala es 12 horas.", "RS002"
            )
        num_personas = kwargs.get("numero_personas", 1)
        if num_personas > self.__capacidad_maxima:
            raise CapacidadExcedidaException(
                f"La sala '{self._nombre}' tiene capacidad máxima de "
                f"{self.__capacidad_maxima} personas; se solicitaron {num_personas}.",
                "RS003",
            )

    def describir(self) -> str:
        return (
            f"[SALA] #{self._id} {self._nombre} | "
            f"Sala: {self.__numero_sala} | "
            f"Cap. máx.: {self.__capacidad_maxima} pers. | "
            f"Precio/h: ${self._precio_base:,.0f}"
        )


# SERVICIO 2 — Alquiler de Equipo

class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    Verifica disponibilidad de unidades antes de confirmar.
    """

    TIPOS_VALIDOS = ["proyector", "laptop", "impresora", "camara", "microfono", "tablet"]

    def __init__(self, nombre: str, tipo_equipo: str,
                 cantidad_disponible: int = 5, precio_base: float = 30_000):
        if tipo_equipo.lower() not in self.TIPOS_VALIDOS:
            raise ServicioNoDisponibleException(
                f"Tipo de equipo '{tipo_equipo}' no existe. "
                f"Tipos válidos: {', '.join(self.TIPOS_VALIDOS)}.",
                "AE001",
            )
        super().__init__(
            nombre=nombre,
            descripcion=f"Alquiler de {tipo_equipo}",
            precio_base=precio_base,
        )
        self.__tipo_equipo = tipo_equipo.lower()
        self.__cantidad_total = cantidad_disponible
        self.__cantidad_reservada = 0

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @property
    def unidades_disponibles(self):
        return self.__cantidad_total - self.__cantidad_reservada

    def calcular_costo(self, duracion_horas, cantidad: int = 1, **kwargs) -> float:
        """
        Polimorfismo: calcula costo según horas y cantidad de unidades.
        """
        self.validar_parametros(duracion_horas, cantidad=cantidad)
        return round(self._precio_base * duracion_horas * cantidad, 2)

    def validar_parametros(self, duracion_horas, **kwargs):
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise DuracionInvalidaException(
                "La duración debe ser un número mayor a 0.", "AE002"
            )
        if duracion_horas > 168:   # 1 semana
            raise DuracionInvalidaException(
                "La duración máxima de alquiler es de 168 horas (1 semana).", "AE003"
            )
        cantidad = kwargs.get("cantidad", 1)
        if cantidad <= 0:
            raise ParametroFaltanteException(
                "La cantidad de equipos debe ser mayor a 0.", "AE004"
            )
        if cantidad > self.unidades_disponibles:
            raise CapacidadExcedidaException(
                f"Solo hay {self.unidades_disponibles} unidades disponibles "
                f"de '{self.__tipo_equipo}'; se solicitaron {cantidad}.",
                "AE005",
            )

    def reservar_unidades(self, cantidad: int):
        """Marca unidades como reservadas."""
        self.__cantidad_reservada += cantidad

    def liberar_unidades(self, cantidad: int):
        """Libera unidades previamente reservadas."""
        self.__cantidad_reservada = max(0, self.__cantidad_reservada - cantidad)

    def describir(self) -> str:
        return (
            f"[EQUIPO] #{self._id} {self._nombre} | "
            f"Tipo: {self.__tipo_equipo} | "
            f"Disponibles: {self.unidades_disponibles}/{self.__cantidad_total} | "
            f"Precio/h: ${self._precio_base:,.0f}"
        )


# SERVICIO 3 — Asesoría Especializada

class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoría especializada en distintas áreas.
    El costo varía según el área y el nivel de urgencia (1=normal, 2=urgente, 3=muy urgente).
    """

    AREAS = {
        "tecnologia": 1.0,
        "finanzas":   1.2,
        "legal":      1.5,
        "marketing":  1.1,
        "rrhh":       1.0,
    }

    def __init__(self, nombre: str, area: str,
                 asesor: str, precio_base: float = 80_000):
        area_lower = area.lower()
        if area_lower not in self.AREAS:
            raise ServicioNoDisponibleException(
                f"Área '{area}' no existe. Áreas disponibles: {', '.join(self.AREAS)}.",
                "AS001",
            )
        super().__init__(
            nombre=nombre,
            descripcion=f"Asesoría especializada en {area_lower}",
            precio_base=precio_base,
        )
        self.__area = area_lower
        self.__asesor = asesor
        self.__factor_area = self.AREAS[area_lower]

    @property
    def area(self):
        return self.__area

    @property
    def asesor(self):
        return self.__asesor

    def calcular_costo(self, duracion_horas, nivel_urgencia: int = 1, **kwargs) -> float:
        """
        Polimorfismo: calcula el costo según área, horas y nivel de urgencia.
        nivel_urgencia: 1 = normal, 2 = urgente (+30 %), 3 = muy urgente (+60 %).
        """
        self.validar_parametros(duracion_horas, nivel_urgencia=nivel_urgencia)
        costo = self._precio_base * duracion_horas * self.__factor_area
        if nivel_urgencia == 2:
            costo *= 1.30
        elif nivel_urgencia == 3:
            costo *= 1.60
        return round(costo, 2)

    def validar_parametros(self, duracion_horas, **kwargs):
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise DuracionInvalidaException(
                "La duración debe ser un número mayor a 0.", "AS002"
            )
        if duracion_horas > 8:
            raise DuracionInvalidaException(
                "Una sesión de asesoría no puede superar las 8 horas.", "AS003"
            )
        nivel = kwargs.get("nivel_urgencia", 1)
        if nivel not in (1, 2, 3):
            raise ParametroFaltanteException(
                "El nivel de urgencia debe ser 1 (normal), 2 (urgente) o 3 (muy urgente).",
                "AS004",
            )

    def describir(self) -> str:
        return (
            f"[ASESORÍA] #{self._id} {self._nombre} | "
            f"Área: {self.__area.title()} | "
            f"Asesor: {self.__asesor} | "
            f"Precio/h: ${self._precio_base:,.0f}"
        )
