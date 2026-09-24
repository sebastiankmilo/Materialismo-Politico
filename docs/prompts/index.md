# Prompts y comportamiento del equipo

> Plantillas y reglas reutilizables para trabajar con la IA en este repo. Volver al [índice raíz](../index.md).

- [Comportamiento (marco teórico, metodología, pruebas)](comportamiento.md): Reglas que debe seguir el agente al documentar, responder preguntas en markdown y hacer pruebas (no crear archivos de código sin permiso, validar la rama del ticket, etc.).
- [Plantilla de marco teórico](plantilla%20para%20marco-teorico.md): Esqueleto de preguntas por capa (Dominio, Aplicación, Infraestructura, API) para documentar qué archivos intervienen en un ticket.
- [Onboarding con IA (deep research)](onboarding%20con%20ia%20-%20deepresearch.md): Metodología por fases (mapeo arquitectónico → reglas de negocio → interiorización → dominio) para incorporarse a un proyecto existente con ayuda de IA.
- [Mensaje de ejemplo para nueva feature](mensaje%20de%20ejemplo%20para%20nueva%20feature.md): Ejemplo real de anuncio de PR (paginación opcional) con la regla de negocio y ejemplos de response JSON paginada.
- [Agregar nueva migración](agregar-nueva-migracion.md): Reglas para encadenar una migración `V0xx` nueva al final de la cadena sin romper `parentMigration` (nunca reordenar, reusar números ni modificar migraciones aplicadas).
- [Desarrollar marco teórico](desarrollar-marco_teorico.md): Reglas para responder las preguntas del `2-marco-teorico.md` de un ticket (no implementar, solo responder lo preguntado, enlaces clickeables).
- [Desarrollar metodología](desarrollar-metodologia.md): Reglas para redactar `3-metodologia.md` y guardar planes detallados en `planes/` del ticket (no crear contenido sin pregunta que lo solicite).
- [Desarrollar plan de test](desarrollar-plan-test.md): Prompt para encargarse de los tests de un ticket: analizar por qué falla y proponer antes de tocar, sin flexibilizar tests para que pasen.
- [Documentar bugs](documentar-bugs.md): Plantilla `BUG-XXX` con metadatos, comportamiento actual vs esperado, análisis de desviación (fallo de implementación / omisión / ambigüedad) y plan de corrección SDD.
- [Planes para solucionar bugs](como-hacer-planes-solucionar-bugs-qa.md): Prompt CNL-P para redactar un plan por bug (docs → código → plan de pruebas), sin sección de tests ni riesgos.
- [Guardar session ID](guardar_session_id.md): Pasos para registrar el `session_id` de la sesión actual de OpenCode en `docs/opencode/sessions.md`.
- [Indexar capítulo según la Biblia](indexar_capitulo_segun_la_biblia.md): Libro (`#` sin número), capítulos (`##` 1, 2, 3), apartados (`###` 2.1), versículos al inicio que se reinician solo en cada `##`; una unidad por frase, fila de tabla o ítem `-` de primer nivel.
- [Desarrollar vocabulario](desarrollar-vocabulario.md): Reglas para anotar términos del ticket en `vocabulario/vocabulario.md` (orden alfabético, cita libro/capítulo/versículo, sin analogías). Se anota al preguntar la palabra; la definición lleva ***sin acuerdo*** hasta pactarla.
- [Hacer el vocabulario](hacer%20el%20vocabulario.md): Plantilla de dos tablas (1: con definición; 2: a tener en cuenta, sin definición). Índice, subíndice, temas, orden a–z. Cómo citar: Ejemplo ≠ Fuente; referencias tipo Biblia (`4:6`, `4:6-7`, `4:6...`, `4:6,9`, `4:6; 2:5`).

## Optional

- [Plantilla "crear buen índice"](crear-buen-indice.md): Archivo de prompt actualmente vacío, reservado para una guía de índices.
