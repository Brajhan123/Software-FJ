"""
entidad_base.py
===============
Clase abstracta base para todas las entidades del Sistema Software FJ.
Aplica los principios de abstracción y encapsulación de la POO.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    Define la estructura común (id, nombre, fecha de creación, estado activo)
    y los métodos abstractos que cada subclase debe implementar.
    """

    _contador_global = 0

    def __init__(self, nombre: str):
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise ValueError("El nombre de la entidad debe tener al menos 2 caracteres.")
        EntidadBase._contador_global += 1
        self._id = EntidadBase._contador_global
        self._nombre = nombre.strip().title()
        self._fecha_creacion = datetime.now()
        self._activo = True

    #  Propiedades de solo lectura 
    @property
    def id(self):
        """Identificador único de la entidad."""
        return self._id

    @property
    def nombre(self):
        """Nombre de la entidad."""
        return self._nombre

    @property
    def fecha_creacion(self):
        """Fecha en que fue creada la entidad."""
        return self._fecha_creacion

    @property
    def activo(self):
        """Indica si la entidad está activa en el sistema."""
        return self._activo

    #  Métodos concretos 
    def desactivar(self):
        """Desactiva la entidad en el sistema."""
        self._activo = False

    def activar(self):
        """Activa la entidad en el sistema."""
        self._activo = True

    #  Métodos abstractos (deben ser implementados por subclases) 
    @abstractmethod
    def validar(self) -> bool:
        """Valida que la entidad tenga datos correctos y completos."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción detallada de la entidad."""
        pass

    #  Representación
    def __str__(self):
        return f"{self.__class__.__name__}[ID={self._id} | {self._nombre}]"

    def __repr__(self):
        return self.__str__()
