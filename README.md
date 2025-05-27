# CODIGOS-PROYECTO-FINAL


# Simulador de Pipeline de Procesador con Caché, Hazards e Interrupciones

Este proyecto simula un procesador con pipeline de 5 etapas (IF, ID, EX, MEM, WB), con manejo de hazards, memoria caché parametrizable, soporte de entrada/salida programada e interrupciones.

---

## Características

- ✅ ISA básica (ADD, SUB, MUL, LOAD, STORE, BEQ, READDEV, RETI)
- ✅ Pipeline de 5 etapas
- ✅ Forwarding y stall para resolver data hazards
- ✅ Flush por control hazards (salto condicional)
- ✅ Caché de datos:
  - Mapeo directo o asociativo 2-way
  - Tamaño y bloques configurables
- ✅ Dispositivo de E/S ficticio con interrupciones programadas
- ✅ Estadísticas de desempeño (CPI, hit rate de caché)

---




simulador-pipeline/
├── main.py
├── README.md
├── cpu/
│   ├── __init__.py
│   ├── isa.py             # Definición de instrucciones (ISA)
│   └── pipeline.py        # Implementación del pipeline con hazards
├── memoria/
│   ├── __init__.py
│   └── cache.py           # Simulación de caché (directo y 2-way)
├── io/
│   ├── __init__.py
│   ├── dispositivo.py     # Dispositivo ficticio de entrada de datos
│   └── interrupciones.py  # Manejador de interrupciones del sistema
├── tests/
│   ├── __init__.py
│   └── benchmark1.py      # Programa de prueba (benchmark simple)


