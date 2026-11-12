"""
main.py
=======
Programa principal — Sistema Integral de Gestión de Clientes,
Servicios y Reservas de la empresa Software FJ.

Demuestra al menos 10 operaciones completas (válidas e inválidas),
el manejo avanzado de excepciones y el registro en archivo de logs.

Principios POO aplicados:
  - Abstracción        (EntidadBase, Servicio)
  - Herencia           (Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada)
  - Polimorfismo       (calcular_costo en cada servicio)
  - Encapsulación      (atributos privados con propiedades en Cliente y Reserva)
  - Manejo de excepciones: try/except/else/finally, encadenamiento, personalizadas
"""

from sistema import SistemaFJ
from excepciones import (
    SistemaFJException,
    ClienteInvalidoException,
    ServicioNoDisponibleException,
    ReservaInvalidaException,
    OperacionNoPermitidaException,
    DuracionInvalidaException,
    CapacidadExcedidaException,
    ParametroFaltanteException,
)
from logger import Logger


# Utilidades de presentación

def banner(titulo: str, num: int = None):
    """Imprime un separador visual con título para cada operación."""
    prefijo = f"OPERACIÓN {num:02d}" if num else "INFO"
    sep = "─" * 65
    print(f"\n{sep}")
    print(f"  {prefijo}: {titulo}")
    print(sep)


def ok(msg):  print(f"  ✓ {msg}")
def err(msg): print(f"  ✗ {msg}")
def nota(msg): print(f"  → {msg}")


# PROGRAMA PRINCIPAL

def main():
    logger = Logger.obtener_instancia("sistema_fj_logs.txt")
    sistema = SistemaFJ()

    print("\n" + "=" * 65)
    print("   SISTEMA INTEGRAL SOFTWARE FJ")
    print("   Gestión de Clientes, Servicios y Reservas")
    print("=" * 65)

    # Variables reutilizadas entre operaciones
    cliente1 = cliente2 = cliente3 = None
    sala_a = equipo_proy = asesoria_tech = None
    reserva1 = reserva2 = reserva3 = None

    # OPERACIÓN 01 — Registro de cliente válido
    banner("Registro de cliente válido", 1)
    try:
        cliente1 = sistema.registrar_cliente(
            "Ana", "García", "ana.garcia@email.com", "3001234567", "12345678"
        )
        ok(cliente1.describir())
    except SistemaFJException as e:
        err(f"Error inesperado: {e}")
    finally:
        nota("Bloque finally ejecutado — sistema continúa activo.")

    # OPERACIÓN 02 — Registro de segundo cliente válido
    banner("Registro de segundo cliente válido", 2)
    try:
        cliente2 = sistema.registrar_cliente(
            "Carlos", "Rodríguez", "carlos.r@correo.com", "3109876543", "87654321"
        )
        ok(cliente2.describir())
    except SistemaFJException as e:
        err(f"Error: {e}")

    # OPERACIÓN 03 — Registro de cliente con email inválido 
    banner("Registro de cliente con email inválido", 3)
    try:
        sistema.registrar_cliente(
            "Pedro", "Gomez", "email-invalido-sin-arroba", "3200000000", "99887766"
        )
    except ClienteInvalidoException as e:
        err(f"Error esperado capturado → {e}")
    except SistemaFJException as e:
        err(f"Error del sistema: {e}")
    else:
        nota("No se lanzó ninguna excepción.")
    finally:
        nota("Sistema sigue operando con normalidad.")

    # OPERACIÓN 04 — Registro de cliente con documento faltante 
    banner("Registro de cliente con documento vacío", 4)
    try:
        sistema.registrar_cliente(
            "Luis", "Pérez", "luis@email.com", "3300000000", ""
        )
    except ParametroFaltanteException as e:
        err(f"Error esperado capturado → {e}")
    except SistemaFJException as e:
        err(f"Error: {e}")
    finally:
        nota("Sistema sigue operando con normalidad.")

    # OPERACIÓN 05 — Creación de servicios válidos 
    banner("Creación de servicios válidos (Sala, Equipo, Asesoría)", 5)
    try:
        sala_a = sistema.crear_servicio_sala(
            "Sala Ejecutiva A", "SA-01", capacidad=15, precio=60_000
        )
        ok(sala_a.describir())

        equipo_proy = sistema.crear_servicio_equipo(
            "Proyector HD", "proyector", cantidad=3, precio=25_000
        )
        ok(equipo_proy.describir())

        asesoria_tech = sistema.crear_servicio_asesoria(
            "Asesoría Tecnológica", "tecnologia", "Dr. Martínez", precio=90_000
        )
        ok(asesoria_tech.describir())
    except SistemaFJException as e:
        err(f"Error al crear servicio: {e}")

    # OPERACIÓN 06 — Creación de servicio con tipo de equipo inválido
    banner("Creación de servicio con tipo de equipo inexistente", 6)
    try:
        sistema.crear_servicio_equipo("Dron de vigilancia", "dron", 2, 50_000)
    except ServicioNoDisponibleException as e:
        err(f"Error esperado capturado → {e}")
    finally:
        nota("Sistema sigue operando con normalidad.")

    # OPERACIÓN 07 — Reserva exitosa de sala con cálculos de costo
    banner("Reserva exitosa de Sala Ejecutiva A (cálculos de costo)", 7)
    try:
        reserva1 = sistema.crear_reserva(
            cliente1, sala_a, 3, numero_personas=10
        )
        ok(str(reserva1))

        # Variantes de cálculo 
        costo_iva   = reserva1.obtener_costo_con_impuesto()
        costo_desc  = reserva1.obtener_costo_con_descuento(0.10)
        costo_svc   = sala_a.calcular_costo_completo(3, 0.10)

        ok(f"  Costo base          : ${reserva1.costo:>12,.2f} COP")
        ok(f"  Costo + IVA (19 %)  : ${costo_iva:>12,.2f} COP")
        ok(f"  Costo - 10 % desc.  : ${costo_desc:>12,.2f} COP")
        ok(f"  Costo desc.+IVA     : ${costo_svc:>12,.2f} COP")
    except SistemaFJException as e:
        err(f"Error: {e}")

    # OPERACIÓN 08 — Reserva exitosa de asesoría urgente
    banner("Reserva exitosa de Asesoría Urgente", 8)
    try:
        reserva2 = sistema.crear_reserva(
            cliente2, asesoria_tech, 2, nivel_urgencia=2
        )
        ok(str(reserva2))
        ok(f"  Costo + IVA: ${reserva2.obtener_costo_con_impuesto():,.2f} COP")
    except SistemaFJException as e:
        err(f"Error: {e}")

    # OPERACIÓN 09 — Reserva con duración negativa 
    banner("Reserva con duración inválida (negativa)", 9)
    try:
        sistema.crear_reserva(cliente1, sala_a, -5)
    except DuracionInvalidaException as e:
        err(f"Error esperado capturado → {e}")
    except SistemaFJException as e:
        err(f"Error: {e}")
    finally:
        nota("Sistema sigue operando con normalidad.")

    # OPERACIÓN 10 — Reserva con capacidad excedida
    banner("Reserva de sala con capacidad excedida", 10)
    try:
        sistema.crear_reserva(cliente2, sala_a, 2, numero_personas=50)
    except CapacidadExcedidaException as e:
        err(f"Error esperado capturado → {e}")
    except SistemaFJException as e:
        err(f"Error: {e}")
    finally:
        nota("Sistema sigue operando con normalidad.")

    # OPERACIÓN 11 — Reserva exitosa de equipo
    banner("Reserva exitosa de Equipo (Proyector)", 11)
    try:
        # Registrar tercer cliente
        cliente3 = sistema.registrar_cliente(
            "María", "López", "maria.lopez@empresa.co", "3005559999", "55566677"
        )
        reserva3 = sistema.crear_reserva(
            cliente3, equipo_proy, 4, cantidad=2
        )
        ok(str(reserva3))
    except SistemaFJException as e:
        err(f"Error: {e}")

    # OPERACIÓN 12 — Cancelación de reserva exitosa
    banner("Cancelación de Reserva #1 (válida)", 12)
    try:
        sistema.cancelar_reserva(reserva1, "El cliente reprogramó la reunión.")
        ok(f"Reserva #{reserva1.id} cancelada. Estado: {reserva1.estado}")
    except SistemaFJException as e:
        err(f"Error: {e}")

    # OPERACIÓN 13 — Cancelar reserva ya cancelada  encadenamiento
    banner("Cancelar reserva ya cancelada (encadenamiento de excepciones)", 13)
    try:
        sistema.cancelar_reserva(reserva1, "Segundo intento de cancelación.")
    except OperacionNoPermitidaException as e:
        err(f"Error esperado capturado → {e}")
        # Encadenamiento: lanzar una excepción de mayor nivel
        try:
            raise ReservaInvalidaException(
                "No se pudo procesar la operación de cancelación.", "R099"
            ) from e
        except ReservaInvalidaException as re:
            err(f"Excepción encadenada → {re}")
            nota(f"Causa original      → {re.__cause__}")
    finally:
        nota("Sistema sigue operando con normalidad.")

    # OPERACIÓN 14 — Servicio marcado como no disponible  reserva fallida
    banner("Reserva de servicio no disponible (fallo esperado)", 14)
    try:
        asesoria_tech.marcar_no_disponible()
        nota("Asesoría marcada como NO DISPONIBLE.")
        sistema.crear_reserva(cliente2, asesoria_tech, 1)
    except ServicioNoDisponibleException as e:
        err(f"Error esperado capturado → {e}")
    finally:
        asesoria_tech.marcar_disponible()
        nota("Asesoría restaurada a DISPONIBLE.")
        nota("Sistema sigue operando con normalidad.")

    # OPERACIÓN 15 — Completar reserva confirmada
    banner("Completar reserva de Asesoría (reserva2)", 15)
    try:
        reserva2.completar()
        ok(f"Reserva #{reserva2.id} completada. Estado: {reserva2.estado}")
        ok(f"Historial de la reserva:")
        for entrada in reserva2.historial:
            print(f"      {entrada}")
    except SistemaFJException as e:
        err(f"Error: {e}")

    # RESUMEN FINAL
    sep = "=" * 65
    print(f"\n{sep}")
    print("  LISTADO COMPLETO DE CLIENTES")
    print(sep)
    sistema.listar_clientes()

    print(f"\n{sep}")
    print("  LISTADO COMPLETO DE SERVICIOS")
    print(sep)
    sistema.listar_servicios()

    print(f"\n{sep}")
    print("  LISTADO COMPLETO DE RESERVAS")
    print(sep)
    sistema.listar_reservas()

    sistema.resumen_sistema()

    logger.evento("Demostración del sistema completada exitosamente.")
    print("\n  ✓ Logs guardados en: sistema_fj_logs.txt")
    print("  ✓ Sistema ejecutado sin interrupciones — Software FJ\n")


if __name__ == "__main__":
    main()
