# Juventud de Upala

Análisis por distrito de los problemas que afectan a las personas jóvenes (12 a 35 años) del cantón de Upala, Alajuela, Costa Rica: condiciones de vida, participación, educación, salud, seguridad y drogas.

Versión preliminar en revisión.

## Cómo leerlo

- Cada indicador cita su fuente y explica hacia qué lado es peor.
- Los hallazgos llevan un nivel de certeza: señal (1 fuente), hipótesis (2 fuentes independientes) o hecho (3 o más).
- Los datos de región o cantón se marcan como tales; no se presentan como datos de distrito.

## Fuentes

INEC (estimaciones del Censo 2022 y estadísticas vitales), MIDEPLAN (Índice de Desarrollo Social 2023), MEP (bases por centro educativo y censo educativo), Ministerio de Salud (ASIS Upala 2023), TSE, OIJ, Observatorio de la Violencia, ICD, MSP (Sembremos Seguridad), PNUD (Atlas de Desarrollo Humano Cantonal 2026) y Consejo de la Persona Joven.

## Estructura

- `index.html`: la página (HTML, CSS y JavaScript sin dependencias de compilación; usa Chart.js desde cdnjs).
- `data/datos.js`: datos generados.
- `data/contenido.json`: hallazgos, contexto regional y textos.
- `data/distritos_upala.geojson`: límites distritales (SNIT/IGN), simplificados.
- `scripts/build_data.py`: regenera `data/datos.js` a partir de las tablas de trabajo.
