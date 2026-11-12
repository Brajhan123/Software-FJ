"""
logger.py
=========
Módulo de registro de eventos y errores del Sistema Software FJ.
Implementa el patrón Singleton para garantizar un único archivo de logs
durante toda la ejecución del programa.
"""

from datetime import datetime


class Logger:
    """
    Clase para el manejo del archivo de logs del sistema.
    Registra todos los eventos, errores y advertencias.
    Implementa el patrón Singleton.
    """

    _instancia = None

    def __init__(self, archivo_log="sistema_fj_logs.txt"):
        self.archivo_log = archivo_log
        self._inicializar_archivo()

    @classmethod
    def obtener_instancia(cls, archivo_log="sistema_fj_logs.txt"):
        """Retorna la instancia única del Logger (Singleton)."""
        if cls._instancia is None:
            cls._instancia = cls(archivo_log)
        return cls._instancia

    def _inicializar_archivo(self):
        """Escribe el encabezado de sesión en el archivo de logs."""
        try:
            with open(self.archivo_log, "a", encoding="utf-8") as f:
                f.write("\n" + "=" * 65 + "\n")
                f.write("  SISTEMA SOFTWARE FJ — INICIO DE SESIÓN\n")
                f.write(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 65 + "\n")
        except Exception as e:
            print(f"[ADVERTENCIA] No se pudo inicializar el archivo de logs: {e}")

    def _escribir(self, nivel, mensaje):
        """Método interno: escribe una línea en el archivo de logs y en consola."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] [{nivel:<11}] {mensaje}"
        try:
            with open(self.archivo_log, "a", encoding="utf-8") as f:
                f.write(linea + "\n")
        except Exception as e:
            print(f"[ADVERTENCIA] No se pudo escribir en el log: {e}")
        print(linea)

    def info(self, mensaje):
        """Registra un mensaje informativo."""
        self._escribir("INFO", mensaje)

    def error(self, mensaje):
        """Registra un mensaje de error."""
        self._escribir("ERROR", mensaje)

    def advertencia(self, mensaje):
        """Registra una advertencia."""
        self._escribir("ADVERTENCIA", mensaje)

    def evento(self, mensaje):
        """Registra un evento relevante del sistema."""
        self._escribir("EVENTO", mensaje)
