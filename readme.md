# Proyecto Final — Bases de Datos

**Curso:** COM-12101-001 · Bases de Datos · Primavera 2026
**Dataset:** FBI Hate Crime Statistics (Crime Data Explorer)
**Equipo:** Valentina García Ramírez | Aniel Orihuela | Diego Manrique | Diego Hinojosa
**Profesor:** Marco Augusto Vásquez Beltran.
**Se hizo uso de Claude AI para la organización, limpieza y para cualquier gráfico o tabla que se encuentra en este Readme.md**

---

## 1. Enlaces directos al conjunto de datos

- **Portal principal (CDE — Crime Data Explorer):** https://cde.ucr.cjis.gov/
- **Sección de descargas (Documents & Downloads):** https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads
- **Archivo usado:** `hate_crime.csv` dentro del paquete comprimido *"Hate Crime"* listado en **Additional Datasets**.
- **Página explicativa del programa:** https://www.fbi.gov/how-we-can-help-you/more-fbi-services-and-information/ucr/hate-crime
- **Publicación anual más reciente (prensa):** https://www.fbi.gov/news/press-releases/fbi-releases-2023-hate-crime-statistics
- **Libro de referencia académica sobre la estructura del dato:** *Decoding FBI Crime Data*, cap. 9 — https://ucrbook.com/hate_crimes.html
- **Código fuente del frontend del CDE (referencia técnica):** https://github.com/fbi-cde/crime-data-frontend

---

## 2. Descripción del conjunto de datos

### 2.1 Resumen

`hate_crime.csv` contiene un registro por **incidente** de crimen de odio reportado a la División de Servicios de Información de Justicia Criminal del FBI (CJIS) a través del programa **Uniform Crime Reporting (UCR)**. Cada fila describe un incidente ocurrido en un lugar y fecha específicos, reportado por una agencia de orden público de EE. UU., e incluye información sobre:

- La **agencia** reportante (identificador ORI, nombre, tipo, estado, región, grupo poblacional).
- El **incidente** (fecha, identificador, cuenta de víctimas y ofensores, indicadores de sesgo múltiple u ofensa múltiple).
- Las **ofensas** cometidas (una o varias, separadas por `;` dentro de la celda `OFFENSE_NAME`).
- Las **motivaciones de sesgo** (una o varias, separadas por `;` en `BIAS_DESC`; p. ej. *Anti-Black or African American*, *Anti-Jewish*, *Anti-Gay (Male)*).
- Los **tipos de víctima** (individuo, negocio, institución religiosa, sociedad, etc.).
- La **demografía del ofensor** (raza, etnicidad, conteos de adultos y menores).
- El **tipo de ubicación** donde ocurrió el hecho (residencia, vía pública, escuela, casa de culto, etc.).

### 2.2 Origen y autoría

Los datos son recolectados por la **Federal Bureau of Investigation (FBI)**, específicamente por la *Criminal Justice Information Services Division (CJIS)*, dentro del programa **Uniform Crime Reporting (UCR)**. El reporte es nutrido por más de 18,000 agencias locales, estatales, tribales, federales y universitarias de orden público que envían información voluntariamente al FBI, ya sea mediante el esquema **SRS** (Summary Reporting System, usado históricamente) o el esquema **NIBRS** (National Incident-Based Reporting System, el estándar vigente desde 2021).

El programa UCR opera desde 1930. La recolección sistemática de crímenes de odio comenzó en **1991** como resultado del *Hate Crime Statistics Act* de 1990, que obligó al Procurador General a recopilar estadísticas sobre crímenes motivados por prejuicio.

### 2.3 Justificación

La recolección responde a un mandato legal federal (*Hate Crime Statistics Act*, 1990, y sus reformas posteriores: inclusión del sesgo anti-discapacidad en 1994, anti-gender identity y anti-gender en 2013, anti-árabe como categoría separada en 2015, etc.). El objetivo declarado del programa es:

1. **Cuantificar** la incidencia y naturaleza de crímenes motivados por prejuicio racial, religioso, étnico, de orientación sexual, identidad de género, discapacidad o género, para informar políticas públicas.
2. **Apoyar investigaciones** federales, estatales y locales.
3. **Producir transparencia** frente a víctimas, organizaciones civiles y medios de comunicación.
4. **Retroalimentar** programas de prevención y capacitación policial.

### 2.4 Disponibilidad y acceso

- **Fuente canónica:** FBI Crime Data Explorer — https://cde.ucr.cjis.gov/
- **Licencia:** Dominio público (obra del gobierno federal estadounidense; *Title 17 U.S.C. § 105*). Libre para usar, redistribuir y transformar, con la recomendación explícita de citar al FBI UCR como origen.
- **Formato:** CSV dentro de un archivo comprimido (`.zip`).
- **Costo:** Gratuito.
- **Registro requerido:** No.

### 2.5 Periodicidad de actualización

**Anual.** El FBI publica una nueva entrega alrededor del tercer o cuarto trimestre del año siguiente al reportado (por ejemplo, los datos completos de 2023 se publicaron en el otoño de 2024). En ocasiones emite **suplementos** a mitad de año cuando agencias tardías completan sus envíos. La revisión 2024 ampliada está prevista para finales de 2025 / inicios de 2026.

### 2.6 Dimensiones (tabla hecha por Claude AI)

- **Alcance temporal seleccionado por el equipo:** 1991 – último año disponible.
- **Volumen aproximado de registros:** ≈ **250,000 incidentes** acumulados de 1991 a 2023 (el número crece con cada entrega anual; un año típico reciente aporta entre 8,000 y 12,000 incidentes).
- **Número de atributos:** **28 columnas** en el archivo desnormalizado.
- **Cumplimiento de la rúbrica:**

  | Requisito de la rúbrica | Mínimo | Este dataset | ¿Cumple? |
  |---|---|---|---|
  | Registros | 5,000 | ≈ 250,000 | Sí |
  | Atributos | 15 | 28 | Sí |
  | Entidades identificables | 5 | ≥ 7 (Agencia, Ubicación geopolítica, Incidente, Ofensa, Sesgo/Bias, TipoDeVíctima, PerfilDeOfensor) | Sí |
  | Estado | No normalizado | Sí — contiene columnas multivaluadas separadas por `;`, redundancia jerárquica (estado/región/división) y repetición de descripciones de agencia por incidente | Sí |
  | Datos públicos y reales | Sí | Sí (FBI CDE, dominio público) | Sí |

### 2.7 Justificación del alcance temporal (esta sección se hizo bajo las recomendaciones de Claude AI)

Se recomienda **cargar el archivo histórico completo** (1991 hasta el año más reciente disponible) por tres razones:

1. **Volumen manejable.** ~250k filas × 28 columnas ≈ 60 MB en CSV y < 200 MB una vez cargado en PostgreSQL; Docker en una laptop de desarrollo lo soporta sin problema.
2. **Riqueza analítica.** Permite responder preguntas de series temporales, comparar evolución de categorías de sesgo (varias se introdujeron en 2013 y 2015) y evaluar la transición SRS → NIBRS (2021).
3. **Aporta al paso 3 (normalización).** El rango histórico hace evidentes las dependencias funcionales (p. ej. `ORI → STATE_NAME → REGION_NAME`) y las multivaluadas (`INCIDENT_ID →→ BIAS_DESC`), insumo directo para 4NF.

> **Advertencia documental importante (se menciona en 2.13):** los registros previos a 2013 no contienen las categorías de sesgo por identidad de género ni género, y los de 2021–2022 presentan cobertura reducida por la transición a NIBRS-only. Esto debe contemplarse al hacer comparaciones longitudinales.

---

## 3. Diccionario de datos (tabla hecha por Claude AI)

Las 28 columnas del archivo desnormalizado, en el orden en que aparecen en el CSV. El tipo propuesto es el que se usará en las tablas de *staging* en PostgreSQL; los valores finales podrán ajustarse tras el análisis exploratorio (paso 2).

| # | Columna | Tipo SQL (staging) | Naturaleza | Descripción | Ejemplo | Notas de calidad |
|---|---|---|---|---|---|---|
| 1 | `INCIDENT_ID` | `BIGINT` | Cuantitativa (identificador) | Identificador único del incidente asignado por el FBI. | `1` | Clave candidata. |
| 2 | `DATA_YEAR` | `SMALLINT` | Cuantitativa (discreta) / serie temporal | Año del reporte UCR. | `2023` | Rango 1991 – último año disponible. |
| 3 | `ORI` | `CHAR(9)` | Cualitativa (identificador) | *Originating Agency Identifier*: código único de 9 posiciones de la agencia (letras del estado + 7 dígitos). | `CA0194200` | Clave foránea a la entidad Agencia. |
| 4 | `PUB_AGENCY_NAME` | `VARCHAR(120)` | Cualitativa (texto corto) | Nombre público de la agencia reportante. | `Los Angeles` | Dependiente funcional de `ORI`. |
| 5 | `PUB_AGENCY_UNIT` | `VARCHAR(120)` | Cualitativa (texto corto) | Unidad o sub-agencia reportante (mayormente nula). | `Transit` | Alta proporción de nulos (>90 %). |
| 6 | `AGENCY_TYPE_NAME` | `VARCHAR(60)` | Cualitativa (categórica) | Tipo de agencia. | `City`, `County`, `University or College`, `State Police` | Categórica con ~10 valores. |
| 7 | `STATE_ABBR` | `CHAR(2)` | Cualitativa (categórica) | Abreviatura de estado (ISO-style USPS). | `CA`, `TX`, `NY` | Dependiente funcional de `ORI`. |
| 8 | `STATE_NAME` | `VARCHAR(40)` | Cualitativa (categórica) | Nombre completo del estado. | `California` | Redundante respecto a `STATE_ABBR`. |
| 9 | `DIVISION_NAME` | `VARCHAR(40)` | Cualitativa (categórica) | División del Census Bureau. | `Pacific`, `Mountain`, `South Atlantic` | 9 valores. Dependiente funcional de `STATE_ABBR`. |
| 10 | `REGION_NAME` | `VARCHAR(20)` | Cualitativa (categórica) | Región del Census Bureau. | `West`, `South`, `Northeast`, `Midwest` | 4 valores. Dependiente funcional de `DIVISION_NAME`. |
| 11 | `POPULATION_GROUP_CODE` | `VARCHAR(4)` | Cualitativa (categórica) | Código de grupo poblacional UCR. | `1A`, `2`, `9` | ~12 valores. |
| 12 | `POPULATION_GROUP_DESC` | `VARCHAR(120)` | Cualitativa (categórica) | Descripción del grupo poblacional (p. ej. tamaño de ciudad). | `Cities 250,000 thru 499,999` | Dependiente funcional de `POPULATION_GROUP_CODE`. |
| 13 | `INCIDENT_DATE` | `DATE` | Serie temporal | Fecha del incidente (formato `DD-MON-YY`). | `15-JUN-23` | Requiere parseo explícito durante la carga. |
| 14 | `ADULT_VICTIM_COUNT` | `SMALLINT` | Cuantitativa (discreta) | Número de víctimas adultas (≥ 18 años). | `2` | Puede ser nulo. |
| 15 | `JUVENILE_VICTIM_COUNT` | `SMALLINT` | Cuantitativa (discreta) | Número de víctimas menores de 18. | `0` | Puede ser nulo. |
| 16 | `TOTAL_OFFENDER_COUNT` | `SMALLINT` | Cuantitativa (discreta) | Total de ofensores conocidos. `0` indica ofensor desconocido. | `1` | |
| 17 | `ADULT_OFFENDER_COUNT` | `SMALLINT` | Cuantitativa (discreta) | Ofensores adultos. | `1` | Puede ser nulo. |
| 18 | `JUVENILE_OFFENDER_COUNT` | `SMALLINT` | Cuantitativa (discreta) | Ofensores menores de 18. | `0` | Puede ser nulo. |
| 19 | `OFFENDER_RACE` | `VARCHAR(60)` | Cualitativa (categórica) | Raza del ofensor (o raza predominante). | `White`, `Black or African American`, `Unknown`, `Asian` | Incluye `Unknown` y `Not Specified`. |
| 20 | `OFFENDER_ETHNICITY` | `VARCHAR(60)` | Cualitativa (categórica) | Etnicidad del ofensor. | `Hispanic or Latino`, `Not Hispanic or Latino`, `Unknown`, `Multiple` | Muy alta proporción de `Unknown`. |
| 21 | `VICTIM_COUNT` | `SMALLINT` | Cuantitativa (discreta) | Número total de víctimas del incidente (individuos + entidades). | `1` | |
| 22 | `OFFENSE_NAME` | `VARCHAR(500)` | Cualitativa (multivaluada) / texto semiestructurado | Nombre(s) de la(s) ofensa(s) NIBRS / SRS. Multivaluada: varios valores separados por `;`. | `Intimidation;Simple Assault` | Requiere *split* a tabla hija (4NF). |
| 23 | `TOTAL_INDIVIDUAL_VICTIMS` | `SMALLINT` | Cuantitativa (discreta) | Víctimas individuales (personas físicas) involucradas. | `1` | Puede diferir de `VICTIM_COUNT` cuando hay víctimas tipo *Business* o *Society*. |
| 24 | `LOCATION_NAME` | `VARCHAR(200)` | Cualitativa (multivaluada) | Tipo(s) de ubicación NIBRS. Multivaluada con `;`. | `Residence/Home`, `School - Elementary/Secondary;Parking Lot/Drop Lot/Garage` | 46 tipos posibles en NIBRS. |
| 25 | `BIAS_DESC` | `VARCHAR(500)` | Cualitativa (multivaluada) | Motivación(es) de sesgo. Multivaluada con `;`. | `Anti-Black or African American`, `Anti-Jewish;Anti-Arab` | Categorías nuevas en 2013 y 2015. |
| 26 | `VICTIM_TYPES` | `VARCHAR(200)` | Cualitativa (multivaluada) | Tipo(s) de víctima (Individual, Business, Society, Government, etc.). Multivaluada con `;`. | `Individual`, `Religious Organization;Individual` | |
| 27 | `MULTIPLE_OFFENSE` | `CHAR(1)` | Cualitativa (booleana) | `S` = Single offense, `M` = Multiple offenses. | `S` | Derivable de `OFFENSE_NAME`. |
| 28 | `MULTIPLE_BIAS` | `CHAR(1)` | Cualitativa (booleana) | `S` = Single bias, `M` = Multiple biases. | `S` | Derivable de `BIAS_DESC`. |

### 3.1 Clasificación rápida de variables

**Cuantitativas (numéricas):** `INCIDENT_ID`, `DATA_YEAR`, `ADULT_VICTIM_COUNT`, `JUVENILE_VICTIM_COUNT`, `TOTAL_OFFENDER_COUNT`, `ADULT_OFFENDER_COUNT`, `JUVENILE_OFFENDER_COUNT`, `VICTIM_COUNT`, `TOTAL_INDIVIDUAL_VICTIMS`.

**Cualitativas (categóricas):** `ORI`, `PUB_AGENCY_NAME`, `PUB_AGENCY_UNIT`, `AGENCY_TYPE_NAME`, `STATE_ABBR`, `STATE_NAME`, `DIVISION_NAME`, `REGION_NAME`, `POPULATION_GROUP_CODE`, `POPULATION_GROUP_DESC`, `OFFENDER_RACE`, `OFFENDER_ETHNICITY`, `MULTIPLE_OFFENSE`, `MULTIPLE_BIAS`.

**Multivaluadas (texto semi-estructurado con separador `;`):** `OFFENSE_NAME`, `LOCATION_NAME`, `BIAS_DESC`, `VICTIM_TYPES`. Son el insumo clave para justificar la descomposición hasta **4NF** en el paso 3.

**Series temporales:** `INCIDENT_DATE` (fecha), `DATA_YEAR` (año). No hay timestamps a nivel de hora.

**Texto no estructurado:** estrictamente hablando no hay campos de texto libre tipo *narrative*. Los campos de 500 caracteres (`OFFENSE_NAME`, `BIAS_DESC`) son semi-estructurados: son listas de categorías controladas unidas por `;`. El campo `PUB_AGENCY_NAME` contiene nombres propios con variabilidad ortográfica histórica (ayuntamientos que cambian de nombre, fusiones), y es el único candidato a tratamiento tipo texto libre.

---

## 4. Visión estratégica

### 4.1 Objetivo principal del proyecto

**Construir una base de datos relacional normalizada a 4NF que permita analizar la evolución, distribución geográfica y composición demográfica de los crímenes de odio reportados al FBI entre 1991 y la entrega más reciente, para identificar patrones accionables de política pública.**

### 4.2 Preguntas analíticas que el diseño deberá poder responder

1. ¿Cómo ha cambiado la tasa anual de crímenes de odio por estado y región entre 1991 y el presente?
2. ¿Qué motivaciones de sesgo muestran aumentos o disminuciones significativas año a año? ¿Qué categorías introducidas después de 2013 han crecido con más velocidad?
3. ¿Qué tipos de ubicación concentran la mayor proporción de incidentes por cada categoría de sesgo (p. ej. casas de culto para sesgo religioso, escuelas para sesgo étnico)?
4. ¿Cuál es la distribución de ofensas (`OFFENSE_NAME`) por categoría de sesgo y región?
5. ¿Hay asociaciones observables entre grupo poblacional de la jurisdicción (`POPULATION_GROUP_DESC`) y tipología del incidente?
6. ¿Qué agencias reportan con mayor consistencia y cuáles presentan lagunas grandes (años sin reporte) en el período NIBRS?

### 4.3 Implementación

El objetivo se abordará en los cinco pasos de la rúbrica:

1. **Selección del conjunto de datos** *(este documento)*.
2. **Limpieza y carga preliminar** a tablas de *staging* en PostgreSQL + análisis exploratorio SQL.
3. **Normalización** intuitiva → 4NF, con diagrama entidad-relación y scripts DDL.
4. **Análisis de resultados** con consultas SQL avanzadas (ventanas, agregaciones, filtrado).
5. **APIs REST** con FastAPI para operaciones CRUD sobre el esquema normalizado.

### 4.4 Entidades preliminares identificadas

A partir del análisis del CSV desnormalizado se identifican al menos **7 entidades** candidatas:

1. **Agencia** (`ORI`, nombre, unidad, tipo, grupo poblacional).
2. **UbicaciónGeopolítica** (estado, división, región) — jerarquía derivable por dependencia funcional.
3. **Incidente** (id, fecha, año, flags `MULTIPLE_*`, agencia reportante).
4. **Ofensa** y **IncidenteOfensa** (catálogo NIBRS + tabla puente).
5. **Sesgo** (*Bias*) y **IncidenteSesgo** (catálogo + tabla puente).
6. **TipoUbicaciónIncidente** y **IncidenteUbicación** (catálogo NIBRS + tabla puente).
7. **PerfilOfensor** (conteos adultos/menores, raza, etnicidad del bloque de ofensor).
8. **TipoVíctima** y **IncidenteTipoVíctima** (catálogo + tabla puente).

Las tres últimas categorías son precisamente las columnas multivaluadas que justifican ir hasta **4NF** (dependencias multivaluadas no triviales: un incidente tiene varios sesgos y, de forma independiente, varios tipos de víctima).

---

## 5. Consideraciones éticas

### 5.1 Sesgos y limitaciones conocidos de la fuente

- **Sub-reporte estructural.** Estudios del Bureau of Justice Statistics estiman que los crímenes de odio reales podrían ser **varias veces** mayores a los reportados al FBI (véase la *National Crime Victimization Survey*). Ninguna cifra del dataset debe interpretarse como “total de crímenes de odio ocurridos”, solo como “total de crímenes *reportados al UCR*”.
- **Participación voluntaria de agencias.** No todas las agencias participan ni lo hacen con la misma periodicidad. Estados y ciudades completas pueden ausentarse durante años. Comparaciones transversales requieren controlar por cobertura.
- **Transición SRS → NIBRS.** En 2021 el FBI retiró el SRS. Varias agencias grandes (incluidas NYPD y LAPD por periodos) tuvieron gaps durante la transición. **Los años 2021 y 2022 muestran caídas artificiales de volumen** que no representan una reducción real de incidentes.
- **Categorías no estables en el tiempo.** El *Matthew Shepard and James Byrd Jr. Act* (2009) expandió las categorías a partir de 2013. El sesgo anti-árabe se separó como categoría independiente en 2015. Los sesgos por género e identidad de género comenzaron a capturarse en 2013. Comparar series largas exige agrupar o filtrar con cuidado.
- **Clasificación del sesgo depende de la policía que reporta.** Dos agencias distintas pueden clasificar el mismo hecho de forma distinta. Hay un sesgo humano en la asignación del `BIAS_DESC`.

### 5.2 Datos sensibles

- El dataset **no contiene identificadores directos** (nombres, direcciones, DNI) de víctimas ni de ofensores. Trabaja con conteos agregados a nivel de incidente.
- La variable `OFFENDER_RACE` y `OFFENDER_ETHNICITY` registran la *raza/etnicidad del ofensor conocido*. El campo `Unknown` predomina cuando no hay arresto. Usar estas variables para inferir conclusiones sobre grupos raciales completos es **incorrecto y estadísticamente inadmisible** — miden composición del ofensor en casos con ofensor identificado, no propensidad del grupo a delinquir.
- Las motivaciones de sesgo (`BIAS_DESC`) involucran **categorías protegidas**: raza, origen nacional, religión, orientación sexual, identidad de género, discapacidad, género. El equipo se compromete a tratarlas con cuidado analítico y descriptivo, evitando lenguaje estigmatizante en los productos finales.

### 5.3 Compromiso del equipo

- Citar al **FBI CJIS / UCR Program** como fuente original en todos los entregables (README, presentación, API).
- Incluir en cualquier análisis público una **nota metodológica** sobre sub-reporte y transición NIBRS.
- Evitar narrativas causales del tipo *“el grupo X comete más crímenes que el grupo Y”* a partir de este dataset.
- No redistribuir los datos modificándolos sin preservar las notas del README original del FBI.
- Documentar en el repo cualquier transformación que combine, derive o inferencie categorías.

---

## 6. Estructura del repositorio (el formato de abajo se hizo con Claude AI)

```
├─ README.md                      ← este documento
├─ data/
│  ├─ raw/                        ← hate_crime.csv tal como fue descargado
│  └─ README.md                   ← origen, fecha de descarga, checksum
├─ docker/
│  ├─ docker-compose.yml          ← servicio postgres:16 con volumen persistente
│  └─ .env.example                ← variables de conexión (sin secretos reales)
├─ sql/
│  ├─ 01_staging/                 ← DDL de tablas staging + COPY de carga
│  ├─ 02_exploracion/             ← consultas de análisis exploratorio (paso 2)
│  ├─ 03_normalizacion/           ← DDL del esquema 4NF + migración de datos (paso 3)
│  └─ 04_analisis/                ← consultas analíticas (paso 4)
├─ api/                           ← FastAPI (paso 5)
├─ docs/
│  ├─ diccionario_datos.md        ← versión extendida/imprimible de la sección 3
│  ├─ ER_diagram.png              ← diagrama entidad-relación (paso 3)
│  └─ normalizacion.md            ← justificación 1NF → 4NF (paso 3)
└─ .gitignore
```

---

## 7. Créditos

> Federal Bureau of Investigation, Criminal Justice Information Services Division (CJIS). *Uniform Crime Reporting Program — Hate Crime Statistics*. Crime Data Explorer. https://cde.ucr.cjis.gov/
