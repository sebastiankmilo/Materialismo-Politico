# Indexar un markdown como libro, capítulo y versículo

Cuando se pida numerar un `.md` “como la Biblia”, sigue **estas reglas**. No inventes otro esquema.

Referencia aplicada: [`plan-metros-decimales-lineo.md`](../tickets/15-Añadir%20cambio%20metros%20decimales-lineo-(ticket%23179)/planes/plan-metros-decimales-lineo.md).

---

## 1. Piezas (qué es cada título)

| Pieza | Markdown | ¿Lleva número? | Ejemplo |
| --- | --- | --- | --- |
| **Libro** | Un solo `#` por archivo | **No** | `# Plan: Metros decimales en dbo.Lineo` |
| **Capítulo** | Cada `##` | Sí: `1.`, `2.`, `3.`… en orden | `## 1. Documentos de descripción` |
| **Apartado** | Cada `###` | Sí: hereda el capítulo | Bajo `## 2.` → `### 2.1`, `### 2.2` |
| **Subapartado** | Cada `####` | Sí: hereda el apartado | Bajo `### 2.1` → `#### 2.1.1` |
| **Versículo** | Número chiquito **al inicio** de la unidad | Se reinicia **solo** en cada `##` | `¹`, `²`, `³`… |

El `#` es el **nombre del libro** (Génesis, no “1 Génesis”). La enumeración empieza en los **capítulos**.

Un archivo = un libro = **un solo `#`**. Si hace falta otro `#`, es otro documento.

Los `###` y `####` **no** reinician versículos. Son títulos dentro del mismo capítulo; el contador sigue.

---

## 2. Cómo se cita

`capítulo:versículo`

- `2:4` = capítulo 2, versículo 4
- `4:5` = capítulo 4, versículo 5 (da igual que el texto esté bajo `### 4.1`)

El apartado (`2.1`, `4.2`) orienta al lector; **no** entra en la cita del versículo. La cita es siempre `capítulo:versículo`.

---

## 3. Dónde va el número del versículo

Al **principio de cada frase**, con superíndice Unicode y un espacio. Si varias frases van **seguidas en el mismo párrafo** (punto seguido), los versículos van **en esa misma línea / párrafo**. Un versículo **no** obliga a un párrafo nuevo.

```markdown
⁵ No se crean rutas nuevas. ⁶ Cambia el tipo de metros / Meters a decimal? y se persiste en POST /api/lineos.
```

Mal (cada versículo partido a su línea, como si fuera un párrafo):

```markdown
⁵ No se crean rutas nuevas.
⁶ Cambia el tipo de metros / Meters a decimal? y se persiste en POST /api/lineos.
```

**Conserva los párrafos que ya tenía el texto.** Solo insertas el número al empezar cada frase. Párrafo nuevo solo si el original ya lo tenía (línea en blanco, título, lista, tabla, código, `---`).

Números: `¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ¹⁰ ¹¹`… (del 10 en adelante: `¹` + `⁰` = `¹⁰`).

No pongas el número después del punto. No uses `<sup>1</sup>` si el archivo ya usa Unicode.

---

## 4. Qué cuenta como un versículo

La unidad cambia según el bloque. No numeres “por punto” dentro de una tabla o de un ítem de lista.

| Bloque | Una unidad = un versículo | Ejemplo |
| --- | --- | --- |
| **Prosa** | Una **frase** (punto de cierre). Varias frases del **mismo párrafo** = varios versículos **seguidos**, no cada uno en su línea | `¹ Primera fase. ² Sin esto no se empieza código.` |
| **Tabla** | Una **fila de datos** (no la cabecera; no cada punto de la celda) | Fila 1 → `¹` en la primera celda; fila 2 → `²` |
| **Lista `-` de primer nivel** | Un **ítem** (archivo, rama, regla, “no tocar”) | `- ³ indice.md` / `- ⁴ docs/log.md` |
| **Lista numerada `1.` `2.` `3.`** | Un **paso** | `³ 1. En indice.md, añadir…` |
| **`-` anidado** bajo un paso numerado | **Ninguno** | Los hijos viven dentro del versículo del paso |
| **Rúbrica** (línea que solo presenta lo que sigue, acaba en `:`) | **Ninguno** | `Ramas:` / `En Line.cs:` |
| **Bloque de código** | **Ninguno** | Ilustra el versículo de encima |
| **El título** (`#` `##` `###`) | **Ninguno** | El título es capítulo/apartado, no versículo |
| **Navegación** (enlaces “volver al índice” sobre el `#`) | **Ninguno** | No es cuerpo del libro |
| **Separador `---`** | **Ninguno** | Solo rompe visualmente |

### 4.1 Criterio de las listas `-` (el que más se duda)

**Sí** le das versículo a un `-` cuando es un **par** (hermano) que se puede citar solo: un archivo permitido, una rama, una exclusión.

```markdown
### 2.1 Fase 0 — Documentación

- ³ [`indice.md`](../indice.md)
- ⁴ [`docs/log.md`](../../../log.md)
```

`2:3` es `indice.md`. `2:4` es `log.md`. No son la misma frase.

**No** le das versículo a un `-` cuando solo **completa** un paso de encima:

```markdown
³ 1. En [`indice.md`](../indice.md) del ticket 15, añadir a la tabla de documentos:
   - [`3-metodologia.md`](../3-metodologia.md)
   - este plan
```

Ahí el versículo es el **paso** (“añadir a la tabla”). Los dos guiones son el detalle, no citas `2:x` por “este plan”.

### 4.2 Puntos que no cierran frase

No abras versículo nuevo por un punto que **no** termina un pensamiento:

- Nombres: `dbo.Lineo`, `System.Text.Json`, `CorridorApiResponse.Lineos`
- Versiones: `v1.1`
- Decimales: `12.5`, `99999999.99`, `n.00`, `DECIMAL(10,2)`
- Extensiones: `.cs`, `.md`, `.json`
- Métodos: `Delete()`

El versículo de prosa empieza en la frase y acaba en el punto que **cierra** esa frase.

### 4.3 Tablas

```markdown
| Documento | ¿Actualizar? | Motivo |
| --- | --- | --- |
| ¹ [`1-tarea-descripcion.md`](../1-tarea-descripcion.md) | **No** | …todo el motivo de esa fila… |
| ² Otros `1-tarea-descripcion.md` de tickets | **No** | Ticket distinto; este cambio no altera su alcance. |
```

Un versículo = **toda la fila**. Aunque el motivo tenga varios puntos.

---

## 5. Reinicio del contador

1. El primer `##` del archivo abre el capítulo **1**. Los versículos de ese capítulo empiezan en `¹`.
2. El siguiente `##` abre el capítulo **2**. Los versículos **vuelven a `¹`**.
3. Un `###` **no** vuelve a `¹`. Sigue: `… ⁸`, `### 2.3`, `⁹`, `¹⁰`…
4. El texto **antes del primer `##`** (prólogo del libro) lleva versículos `¹`, `²`… propios. No es un capítulo; se cita como prólogo (`prólogo:3` o “libro, versículo 3”). No le pongas `## 0`.

---

## 6. Qué archivos se indexan

- **Sí:** planes, descripciones de ticket, metodología, marcos teóricos, cualquier `.md` de cuerpo que se vaya a citar frase a frase.
- **No, salvo que se pida:** `index.md`, `indice.md`, `llms.txt`, `log.md`. Son mapas o registros, no libro.

Si el archivo ya tiene números viejos (globales ¹…²⁸, o `<sup>` al final de la frase), **reescríbelos** con estas reglas. No mezcles los dos estilos.

Al insertar o borrar una unidad **en medio** de un capítulo, renumera **solo ese capítulo**. Los demás `##` no se tocan.

---

## 7. Orden de trabajo (cuando te pidan indexar un md)

1. Confirmar un solo `#` (libro, sin número).
2. Numerar cada `##` como `1.`, `2.`, `3.`…
3. Numerar cada `###` / `####` heredando (`2.1`, `2.1.1`).
4. Recorrer el cuerpo **capítulo a capítulo**. En cada `##`, poner el contador a 1.
5. Aplicar la tabla de la sección 4 (prosa / tabla / lista / rúbrica / código).
6. Comprobar: no hay versículos ¹…N que atraviesen dos `##`; no hay reset en un `###`.

---

## 8. Anti-patrones

- Numerar el `#` (`# 1. Plan…`).
- Tratar cada `##` como el siguiente número global (`#` → `## 2` → `## 3`). El `##` bajo el libro es `1.`, `2.`; el `###` bajo el `## 2` es `2.1`, no `3`.
- Un solo contador de versículos para todo el archivo (¹ hasta ²⁸).
- Reiniciar versículos en cada `###`.
- Poner el número **después** del punto (eso es nota al pie, no versículo).
- Partir cada versículo en su propio párrafo. En prosa es **punto seguido** dentro del párrafo original.
- Un versículo por punto **dentro** de una celda o de un `-`.
- Numerar bloques SQL/C#/JSON.
- Numerar la fila de cabecera de una tabla.
- Dar versículo a un `-` hijo de un paso `1.` `2.` `3.`
