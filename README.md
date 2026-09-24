# Materialismo Político — Grupo de estudio

Repositorio del grupo de estudio de materialismo político: construcción colaborativa de un **vocabulario** (léxico de los fundamentos) a partir de la lectura de *La relación entre la escolástica católica y el materialismo político* de Román Hernández Suárez, y su **publicación interactiva** como wiki web.

## Propósito

El grupo lee un documento (indexado «como la Biblia», libro/capítulo/versículo) y, en las discusiones de cada sesión, produce un vocabulario que sirve como **herramienta para el intelecto**: fijar los nombres de los conceptos (gramática) antes de poder pensar con ellos (dialéctica) y, más adelante, exponerlos (retórica). Los objetivos son dos:

1. **Metodología estandarizada** para producir vocabulario a partir de los grupos de estudio y construir, de forma ordenada y metódica, las *fuentes únicas de verdad* del materialismo político — necesarias para la formación de cuadros.
2. **Plasmar ese léxico de forma interactiva** en una página web navegable (texto indexado ↔ vocabulario ↔ fuentes, todo enlazado).

El principio de división del trabajo: los camaradas construyen y pulen el contenido (las fuentes únicas de verdad); la IA hace las tareas tediosas pero necesarias (generar el HTML5, las citas, el indexado, la web).

## El método: del escrutinio al vocabulario

La metodología adapta el **escrutinio neocatecumenal** —un círculo hermenéutico— despojándolo de sus componentes espirituales:

- La **Biblia de Jerusalén** provee el *mapa de referencias*: paralelos, notas, avances y retrocesos en el canon.
- El **Vocabulario de Léon-Dufour** provee la *profundidad semántica*: las palabras dejan de ser meros sonidos y se convierten en conceptos operativos.
- Las **citas** son *puntos de anclaje nominal*.

En la adaptación materialista, esos dos instrumentos son las **instrumenta grammaticalia**:

| Instrumento | Función | Operación |
| --- | --- | --- |
| **Diccionario / vocabulario** | Es el *Lexicon*: fija los nombres. Sin nombres fijos no hay pensamiento posible. | *operatio definiens* |
| **Corpus / documento indexado** | Es la *Pars materialis*: archivo estructurado de la materia prima textual, navegable como red (referencias cruzadas, notas). Sin archivo no hay materia para la lógica; solo opinión. | *operatio archivans* |

La lógica es **recursiva**: un término lleva a una cita, la cita lleva al pasaje, el pasaje a sus paralelos y notas, y así se teje una red de sentido. No es lectura lineal, sino lectura en red: cada nodo se conecta con otros y el significado se construye por acumulación y contraste.

## Estructura del repositorio

```
├── escolastica/
│   ├── relacion entre la escolastica católica y el materialismo politico.md/   ← el "libro" (documento fuente)
│   │   ├── 0-index.md                     índice de capítulos + metadatos
│   │   ├── cap-01…cap-09.md               capítulos indexados (versículos ¹ ² ³…)
│   │   └── fuentes-y-referencias.md       fuentes citadas y usos
│   ├── La relación … (indexado).md        versión completa indexada
│   └── vocabulario/vocabulario.md         ← el LÉXICO (fuente única de verdad)
├── docs/prompts/                          reglas y plantillas para la IA (metodología)
├── html/                                  wiki estática (publicada en GitHub Pages)
│   ├── index.html · styles.css · app.js · data.js
│   └── generate_data.py                   genera data.js desde los markdown
├── build_web_data.py                      generador alternativo (html-2 / html-3)
├── 1. Introducción-al-Materialismo-Político.md    fuente de fundamentos
├── 2. Ontología.md                        fuente de fundamentos
└── Mariano-Utin-Manual-Formación-Básica-MatPol.md fuente de formación
```

## El vocabulario (fuente única de verdad)

`escolastica/vocabulario/vocabulario.md` es el archivo donde se anota **todo** término discutido. Dos tablas, ordenadas alfabéticamente:

- **Tabla 1 — Vocabulario con definición**: palabras pertinentes y necesarias. Llevan definición (con tus palabras), ejemplo, fuente/contexto, fecha, tema y marca `***sin acuerdo***` mientras la definición no esté pactada por el grupo.
- **Tabla 2 — Palabras a tener en cuenta**: el resto de términos que hay que recordar. Sin definición, pero con ejemplo, fuente, fecha y tema.

Cada término está en una tabla **o** en la otra (exclusión mutua). Las citas se escriben como la Biblia: `[La relación entre la escolástica católica y el materialismo político 2:4-5](ruta-al-capítulo.md)`. Un mismo término puede tener varias acepciones (mismo índice, subíndice correlativo).

### Cómo se llena (reglas para la IA)

1. Toda palabra nueva se inserta en **orden alfabético** dentro de su tabla (no al final).
2. Al insertar, se **renumeran los índices** siguientes de esa tabla.
3. Ejemplo ≠ Fuente: el *ejemplo* es el trozo donde se ve el término (con su cita); la *fuente* es de dónde sale el significado o la autoridad.
4. Las palabras que se discuten en el chat se anotan **en la misma interacción**, sin esperar instrucción.
5. La definición se corrige en el archivo hasta acordarla; mientras tanto lleva `***sin acuerdo***`.
6. Sin analogías salvo que se pidan explícitamente.

Las reglas completas están en `docs/prompts/desarrollar-vocabulario.md` (reglas) y `docs/prompts/hacer el vocabulario.md` (plantilla y cómo citar).

## Indexado de documentos (estilo bíblico)

Cualquier documento que se vaya a citar frase a frase se indexa así (reglas en `docs/prompts/indexar_capitulo_segun_la_biblia.md`):

- Un archivo = un **libro** (`#` sin número).
- Cada `##` = **capítulo** (`1.`, `2.`, `3.`…); cada `###` = apartado heredado (`2.1`).
- Cada frase = **versículo**, numerado al inicio con superíndice (`¹ ² ³…`), que se reinicia en cada capítulo.
- La cita es siempre `capítulo:versículo` (ej. `5:6`).

## La wiki web (HTML5)

`html/` es una página estática vanilla JS que une las tres piezas:

- **Texto**: los capítulos indexados, con sus versículos y enlaces a los términos del vocabulario.
- **Vocabulario**: las dos tablas, con chips de cita que saltan al versículo exacto.
- **Fuentes**: referencias con sus usos en el texto.

### Regenerar

```bash
python3 html/generate_data.py
```

Reescribe `html/data.js` a partir de `escolastica/relacion entre la escolastica católica y el materialismo politico.md/` y de `escolastica/vocabulario/vocabulario.md`. Al final imprime estadísticas y avisos (citas que apuntan a versículos inexistentes). **No editar `data.js` a mano.**

### Publicar

La página se publica en GitHub Pages desde la rama `gh-pages` (configurada en Settings → Pages → Deploy from a branch → `gh-pages`, carpeta `/`). URL: <https://sebastiankmilo.github.io/Materialismo-Politico/>

Para publicar una versión nueva:

```bash
git checkout gh-pages
git rm -rf --cached . -q
cp html/index.html html/styles.css html/app.js html/data.js .
git add index.html styles.css app.js data.js
git commit -m "Publicar página"
git push origin gh-pages
git checkout master
```

## Estado actual

- Documento *La relación entre la escolástica católica y el materialismo político* indexado en 9 capítulos (554 versículos) con fuentes y referencias.
- Vocabulario en construcción (Tabla 1 con definición: 23 términos; Tabla 2 a tener en cuenta: 21), varias definiciones aún con marca `***sin acuerdo***` pendientes de pactar en el grupo.
- Wiki web publicada en GitHub Pages con texto, vocabulario y fuentes enlazados.

## Notas

- `docs/prompts/` está casi todo ignorado por git: solo se versionan los prompts de **vocabulario** e **indexado** (los que definen la metodología).
- Las fuentes en PDF sin procesar (`sin preprocesar/`) y los libros con derechos de autor no se versionan.