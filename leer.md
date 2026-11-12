# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Empresa: Software FJ — Trabajo UNAD

---

# Descripción

Sistema desarrollado en **Python** con orientación a objetos que gestiona **clientes, servicios y reservas** para la empresa Software FJ, la cual ofrece:

- Reserva de salas para reuniones y eventos
-  Alquiler de equipos tecnológicos
-  Asesorías especializadas (tecnología, finanzas, legal, marketing, RRHH)

---

##  Arquitectura del Proyecto

```
software_fj/
│
├── excepciones.py      # Jerarquía de excepciones personalizadas
├── logger.py           # Registro de eventos y errores en archivo .txt
├── entidad_base.py     # Clase abstracta base del sistema
├── cliente.py          # Clase Cliente con encapsulación y validaciones
├── servicios.py        # Clase abstracta Servicio + 3 servicios especializados
├── reserva.py          # Clase Reserva con ciclo de vida completo
├── sistema.py          # Fachada central del sistema (SistemaFJ)
├── main.py             # Programa principal con 15 operaciones demostradas
├── sistema_fj_logs.txt # Archivo de logs generado automáticamente
└── README.md           # Este archivo
```

---

# Principios POO Implementados

| Principio | Implementación |
|-----------|---------------|
| **Abstracción** | `EntidadBase` y `Servicio` son clases abstractas con `@abstractmethod` |
| **Herencia** | `Cliente`, `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` heredan de las clases base |
| **Polimorfismo** | Cada servicio implementa `calcular_costo()` de forma diferente |
| **Encapsulación** | Atributos privados (`__`) con propiedades y setters con validación |

---

# Manejo de Excepciones

# Jerarquía de excepciones personalizadas:
```
SistemaFJException (base)
├── ClienteInvalidoException
├── ParametroFaltanteException
├── ServicioNoDisponibleException
├── ReservaInvalidaException
├── OperacionNoPermitidaException
├── DuracionInvalidaException
└── CapacidadExcedidaException
```

Uso de bloques: `try/except`, `try/except/else`, `try/except/finally`, y **encadenamiento de excepciones** con `raise ... from e`.

---

# Operaciones Demostradas (15 en total)

| # | Operación | Tipo |
|---|-----------|------|
| 01 | Registro de cliente válido |  Exitosa |
| 02 | Registro de segundo cliente válido |  Exitosa |
| 03 | Registro con email inválido |  Fallo esperado |
| 04 | Registro con documento vacío |  Fallo esperado |
| 05 | Creación de 3 servicios válidos |  Exitosa |
| 06 | Creación de equipo con tipo inexistente |  Fallo esperado |
| 07 | Reserva de sala con cálculos de costo |  Exitosa |
| 08 | Reserva de asesoría urgente |  Exitosa |
| 09 | Reserva con duración negativa |  Fallo esperado |
| 10 | Reserva con capacidad excedida |  Fallo esperado |
| 11 | Reserva de equipo (proyector) |  Exitosa |
| 12 | Cancelación de reserva válida |  Exitosa |
| 13 | Cancelar reserva ya cancelada (encadenamiento) |  Fallo esperado |
| 14 | Reserva de servicio no disponible |  Fallo esperado |
| 15 | Completar reserva confirmada |  Exitosa |

---

##  Cómo Ejecutar

```bash
# Requisitos: Python 3.8 o superior (sin dependencias externas)
python main.py
```

El programa genera automáticamente el archivo `sistema_fj_logs.txt` con todos los eventos y errores del sistema.

---

# Métodos Sobrecargados (cálculo de costos)

```python
servicio.calcular_costo(duracion)                       # Costo base
servicio.calcular_costo_con_impuesto(duracion)          # + IVA 19%
servicio.calcular_costo_con_descuento(duracion, 0.10)   # - 10% descuento
servicio.calcular_costo_completo(duracion, 0.10)        # descuento + IVA
```

---
