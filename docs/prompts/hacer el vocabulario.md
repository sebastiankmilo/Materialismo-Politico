# Vocabulario

> Hay **dos tablas**, cada una **ordenada alfabéticamente por término**. El `Índice` se numera **aparte** en cada tabla.
>
> **Índice + Subíndice:** el `Índice` es el número de la palabra según su posición alfabética **dentro de su tabla**; el `Subíndice` es el número de acepción. La misma palabra repite `Índice` y solo cambia el `Subíndice`.
>
> | Tabla | Para qué | ¿Lleva Definición? |
> | --- | --- | --- |
> | **1. Vocabulario con definición** | Palabras pertinentes y necesarias para entender el ticket. | Sí. |
> | **2. Palabras a tener en cuenta** | Todas las demás que hay que recordar. | No. Sí lleva Índice, Subíndice, Término, Ejemplo, Fuente/Contexto, Fecha y Tema. |
>
> **Exclusión:** cada término está en **una tabla o en la otra**. Si está en la Tabla 1, no puede estar en la Tabla 2, y al revés. Al cambiar de tabla se borra de la de origen, se inserta en la de destino (orden alfabético) y se renumeran solo los `Índice` de las tablas tocadas.

## Temas / Etiquetas

| Etiqueta | Descripción / Alcance |
|----------|------------------------|
| ontologia | -- |
| escolastica | -- |
| materialismo-filosofico | -- |
| fundamentos-materialismo-politico | -- |
| materialismo-historico | -- |

*(Agrega tus etiquetas aquí y usa exactamente estos nombres en las dos tablas.)*

## Tabla 1 — Vocabulario con definición (ejemplo)

Palabras pertinentes y necesarias para desarrollar entendimiento. Una fila por acepción.

| Índice | Subíndice | Término | Definición (con tus palabras) | Ejemplo | Fuente/Contexto | Fecha | Tema | Término-con-IA (dejar en blanco si no se generó con IA) |
|--------|-----------|---------|-------------------------------|---------|-----------------|-------|------|------|
| 1 | 1 | actuador | Dispositivo que convierte energía en movimiento mecánico. | El brazo del robot usa actuadores hidráulicos para levantar carga. | [Wikipedia – Actuador](https://es.wikipedia.org/wiki/Actuador) | 2026-08-28 | robotica | |
| 2 | 1 | amortización | Reducción gradual de una deuda mediante pagos periódicos. | La amortización del préstamo se calcula a 5 años. | [Investopedia – Amortization](https://www.investopedia.com/terms/a/amortization.asp) | 2026-08-28 | finanzas | |
| 2 | 2 | amortización | Pérdida de valor de un activo intangible con el tiempo (contable). | La patente se amortiza en 10 años ([notas de contabilidad](./notas/contabilidad.md)). | [Investopedia – Amortization](https://www.investopedia.com/terms/a/amortization.asp) | 2026-08-28 | finanzas | |
| | | | | | | | | |
| | | | | | | | | |

## Tabla 2 — Palabras a tener en cuenta (ejemplo)

Todas las palabras que hay que tener presentes. **Sin** columna Definición. Ejemplo, Fuente/Contexto y Tema se llenan igual que en la Tabla 1 (misma forma de citar; mismos nombres de etiqueta).

| Índice | Subíndice | Término | Ejemplo | Fuente/Contexto | Fecha | Tema |
|--------|-----------|---------|---------|-----------------|-------|------|
| 1 | 1 | payload | El body JSON lleva el `payload` de la petición. | [Investopedia – Payload](https://www.investopedia.com/) | 2026-08-28 | API |
| | | | | | | |
| | | | | | | |

## Reglas de ordenamiento e indexación

1. **Toda palabra nueva se inserta en su posición alfabética dentro de su tabla** (no al final). Orden: a–z, sin distinguir mayúsculas ni acentos (`á` va con `a`).
2. **Las acepciones de una misma palabra van juntas**, una debajo de la otra, con el mismo `Índice` y `Subíndice` correlativo (`1`, `2`, `3`...). En la Tabla 2 el `Subíndice` distingue ocurrencias o usos, no definiciones.
3. **Al insertar una palabra nueva, se renumeran los `Índice` siguientes de esa tabla.** La otra tabla no se renumera.
4. **Índice y Subíndice son solo referencia**, no datos de estudio: sirven para citar ("revisa la tabla 1, 14.2" o "tabla 2, 3.1") y para detectar duplicados.
5. **Una palabra está en la Tabla 1 o en la Tabla 2, nunca en las dos.** Si está en la 1, no puede estar en la 2, y viceversa. Al definirla: se borra de la 2 y se inserta en la 1. Si deja de definirse y solo se tiene en cuenta: se borra de la 1 y se inserta en la 2. En ambos casos, orden alfabético y renumerar solo las tablas tocadas.

## Cómo citar

La numeración de cada `.md` (libro, capítulo, versículo) sigue [indexar capítulo según la biblia](indexar_capitulo_segun_la_biblia.md). Esta sección dice **cómo se escribe la cita** en **las dos tablas**.

### Ejemplo y Fuente son dos celdas distintas

Como en una edición de la Biblia: el **ejemplo** es el texto que se toma; la **fuente** es de dónde sale la definición o la autoridad.

| Columna | Qué lleva | Qué cita |
| --- | --- | --- |
| **Ejemplo** | El trozo (sentencia, frase, fila) donde se ve el término. Al final, la cita del sitio de ese trozo. | Dónde aparece esa ocurrencia. |
| **Fuente/Contexto** | Tabla 1: de dónde se saca el **significado**. Tabla 2: de dónde sale el **término o el contexto** (no hay definición). No copies aquí el mismo enlace del Ejemplo salvo que el mismo versículo también sea esa autoridad. | El libro del ticket y/o la página externa. |

No pongas en Ejemplo solo un enlace suelto `[4:6](...)`. Primero el trozo, después la cita.

### Forma del enlace a un libro del ticket

Un solo enlace. Texto = **nombre del libro** (el `#` del archivo, sin el carácter `#`) + espacio + la referencia. Destino = ruta al `.md` **sin ancla** (`#4`, `#cómo-citar`).

Desde `vocabulario/vocabulario.md` el plan es hermano (`../planes/...`). **No** pongas el nombre de la carpeta `ticket#179` en el href (ni `%20` ni `%23`): esa carpeta no se llama así en disco y el clic falla.

```markdown
[Plan: Metros decimales en dbo.Lineo 4:6](../planes/plan-metros-decimales-lineo.md)
```

Mal (href con `%23` / el nombre de la carpeta; no existe esa ruta):

```markdown
[Plan: Metros decimales en dbo.Lineo 4:6](../../15-Añadir%20cambio%20metros%20decimales-lineo-(ticket%23179)/planes/plan-metros-decimales-lineo.md)
```

Un `[término]` suelto en una celda (ejemplo `[Range]`) se lee como enlace. Escríbelo entre backticks: `` `[Range]` ``.

### Referencia (como la Biblia)

El libro se escribe una vez, en el texto del enlace. Después va la referencia:

| Caso | Referencia | Cuándo |
| --- | --- | --- |
| Un versículo | `4:6` | Una sola unidad. |
| Rango seguido | `4:6-7` | Varios versículos correlativos del mismo capítulo. |
| Hasta el final del capítulo | `4:6...` | El versículo 6 y todos los que siguen en el capítulo 4, hasta el último. Tres puntos, sin espacio. |
| Varios puntos del mismo capítulo | `4:6,9` | Versículos que no van seguidos. |
| Combinación en un capítulo | `4:6-7,9` | Un rango y otro versículo del mismo capítulo. |
| Varios capítulos | `4:6; 2:5` | Punto y coma entre capítulos. El número de capítulo se repite en cada grupo. |
| Combinación amplia | `4:6-7,9; 2:5...` | Rangos, sueltos, `...` y más de un capítulo. |

Dos libros distintos = dos enlaces, separados por coma y espacio.

### Enlace externo

Sin `capítulo:versículo`. El texto es el título de la página.

```markdown
[GO](https://learn.microsoft.com/sql/t-sql/language-elements/sql-server-utilities-statements-go)
```

### Varios destinos en una celda

Coma y espacio entre enlaces. El libro del ticket va primero.

```markdown
[Plan: Metros decimales en dbo.Lineo 4:3](../planes/plan-metros-decimales-lineo.md), [GO](https://learn.microsoft.com/sql/t-sql/language-elements/sql-server-utilities-statements-go)
```

### Bien y mal

Bien (Ejemplo: trozo + cita del sitio; Fuente: autoridad de la definición):

```markdown
SET NOCOUNT ON; [Plan: Metros decimales en dbo.Lineo 4:3](../planes/plan-metros-decimales-lineo.md)
```

```markdown
[SET NOCOUNT (Transact-SQL)](https://learn.microsoft.com/sql/t-sql/statements/set-nocount-transact-sql)
```

Bien (varios versículos o capítulos en **un** enlace):

```markdown
[Plan: Metros decimales en dbo.Lineo 4:3,7](../planes/plan-metros-decimales-lineo.md)
[Plan: Metros decimales en dbo.Lineo 4:3...](../planes/plan-metros-decimales-lineo.md)
[Plan: Metros decimales en dbo.Lineo 4:3; 2:5](../planes/plan-metros-decimales-lineo.md)
```

Mal (libro y referencia partidos en dos enlaces):

```markdown
[Plan: Metros decimales en dbo.Lineo](../planes/plan-metros-decimales-lineo.md) [4:3](../planes/plan-metros-decimales-lineo.md)
```

Mal (solo `capítulo:versículo`, sin el nombre del libro):

```markdown
[4:3](../planes/plan-metros-decimales-lineo.md)
```

Mal (ancla en la ruta):

```markdown
[4. Fase 1 — Infraestructura](../planes/plan-metros-decimales-lineo.md#4-fase-1--infraestructura) 4:3
```

Mal (Ejemplo y Fuente con el mismo enlace y sin trozo en Ejemplo).

Si no hay versículo en un libro del ticket, cita solo la página externa.

## Notas de uso

- **Tabla 1:** una acepción = una fila. Si una palabra tiene dos sentidos distintos, repite el término en dos filas con su definición y ejemplo propios (ver `amortización` arriba).
- **Tabla 2:** no se escribe definición. Si hace falta más de una fila (otro ejemplo o otro sitio), mismo `Índice` y `Subíndice` correlativo.
- **Sin acuerdo:** solo en la Tabla 1. Si la definición aún no está pactada, la celda Definición empieza por ***sin acuerdo*** (negrita y cursiva). Al acordarla, se quita esa marca.
- **Enlaces clickeables en Ejemplo y Fuente/Contexto:** ver la sección **Cómo citar**.
- Si la fuente no tiene enlace (un libro físico, una clase), escribe el texto plano.
- La columna **Tema** admite varias etiquetas separadas por coma: `legal, finanzas`. Las etiquetas válidas se definen en la sección **Temas / Etiquetas**.
- **Término-con-IA** (solo Tabla 1, última columna): se deja en blanco si el término no se generó con IA; si se generó, se anota ahí.
- Este archivo se puede abrir directo en Excel/Google Sheets pegando la tabla, o convertir a CSV para Anki/Quizlet.
