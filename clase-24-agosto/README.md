# Interferencia cognitiva (Stroop) — práctica con datos

Material práctico de la clase del **24 de agosto** del curso
**Modelos de Aprendizaje en Neurociencia Cognitiva e Inteligencia Artificial**
(Pontificia Universidad Católica de Chile, segundo semestre 2026).

Los cuadernos recorren, sobre datos reales de un experimento Stroop, el camino que va
de una tabla de tiempos de reacción a dos afirmaciones distintas: *cuán fiable es un
efecto* (inferencia) y *cuánto sirve para anticipar a alguien nuevo* (predicción).

---

## Abrir los cuadernos

No hay que instalar nada. Haz clic en un botón y se abre en Google Colab.

| | cuaderno | contenido |
|---|---|---|
| 0 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/decostruttivismo/IIC3800-2026-NCC-IA/blob/main/clase-24-agosto/notebooks/00_prueba.ipynb) | **Prueba de humo.** Comprueba que tu entorno funciona. |
| 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/decostruttivismo/IIC3800-2026-NCC-IA/blob/main/clase-24-agosto/notebooks/01_inferencia.ipynb) | **Del comportamiento al modelo.** Medias, regresión lineal, modelos mixtos, regresión logística. |
| 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/decostruttivismo/IIC3800-2026-NCC-IA/blob/main/clase-24-agosto/notebooks/02_prediccion.ipynb) | **Inferencia y predicción.** Validación por participante, *pipeline*, RMSE y R² fuera de muestra. |

Las soluciones de los ejercicios están en [`notebooks/soluciones/`](notebooks/soluciones)
y se publican después de la clase.

> **Consejo:** en Colab, `Archivo → Guardar una copia en Drive` para conservar lo que
> escribas. Sin eso, los cambios se pierden al cerrar la pestaña.

El instructivo de la sesión —qué se hace, cómo se corre y qué se espera de cada uno— está
en [`Instructivo_clase_24agosto.docx`](Instructivo_clase_24agosto.docx), dos páginas.

---

## Descargar el material

Para la clase no hace falta: los botones de arriba abren los cuadernos en Colab y el CSV
se lee solo. Pero si quieres tener los archivos en tu computador:

- **Todo de una vez.** En la portada del repositorio, botón verde **Code → Download ZIP**.
  Descarga el repositorio completo; la carpeta de esta clase es `clase-24-agosto`.
- **Un archivo suelto.** Ábrelo en GitHub y usa **Download raw file** (el icono de la
  flecha, arriba a la derecha del archivo). Sirve para bajar solo el CSV o un cuaderno.
- **Con git**, si lo usas:

  ```bash
  git clone https://github.com/decostruttivismo/IIC3800-2026-NCC-IA.git
  ```

Si abres un cuaderno descargado en tu propio Jupyter, déjalo junto a la carpeta `datos/`
tal como viene: los cuadernos buscan el CSV en disco antes de recurrir a internet.

---

## Los datos

[`datos/clase_24agosto_dataset.csv`](datos/clase_24agosto_dataset.csv)
— 3000 filas: 30 participantes × 100 ensayos.

| columna | tipo | descripción |
|---|---|---|
| `subject` | texto | identificador del participante (`S01`…`S30`) |
| `trial` | entero | número de ensayo dentro del participante (1–100) |
| `condition` | texto | `Congruent` / `Incongruent` |
| `RT_ms` | decimal | tiempo de reacción en milisegundos |
| `accuracy` | 0/1 | 1 = respuesta correcta |
| `age` | entero | edad del participante (21–40 años) |

Diseño balanceado (1500 ensayos por condición), sin valores faltantes.

**Los datos son simulados.** No vienen de un experimento con personas: se generaron con
la estructura de uno, y de hecho con una estructura muy parecida a la que los cuadernos
ajustan. Para lo que la clase practica —las decisiones de análisis— da igual; para hablar
de cognición humana, no. Está dicho en el cuaderno 1 y desarrollado al final del cuaderno
2, donde se enumera en qué se notaría un conjunto real.

Los cuadernos leen el CSV **por URL** desde este repositorio, así que funcionan en Colab
sin subir archivos ni montar Google Drive:

```python
URL = "https://raw.githubusercontent.com/decostruttivismo/IIC3800-2026-NCC-IA/main/clase-24-agosto/datos/clase_24agosto_dataset.csv"
data = pd.read_csv(URL)
```

Si clonas el repositorio, los cuadernos detectan el archivo local y lo usan en su lugar.

---

## Qué se ve en cada cuaderno

**01 · Inferencia** — `Y = f(X, θ) + ε` aplicado paso a paso:

1. Medias por condición: el efecto Stroop son ~65 ms y ~5.6 puntos de precisión.
2. `smf.ols('RT_ms ~ C(condition)')`: el mismo número, ahora con error estándar y valor-p.
3. `+ trial`: la práctica acelera 0.55 ms por ensayo.
4. `smf.mixedlm(..., groups=subject)`: los ensayos no son independientes; el error
   estándar cae un 38 % y el ICC resulta 0.62.
5. `smf.logit('accuracy ~ C(condition)')`: log-odds, odds ratios y probabilidades, y por
   qué un OR de 0.49 corresponde a bajar de 0.940 a 0.884 de acierto.

**02 · Predicción** — el mismo modelo lineal, otra pregunta:

1. `GroupShuffleSplit` por participante, y por qué partir al azar por ensayo responde a
   una pregunta distinta.
2. `ColumnTransformer` + `Pipeline`, y por qué el preprocesamiento va dentro del pipeline.
3. El resultado: p ≈ 10⁻¹¹⁰ y R² fuera de muestra = 0.13, sin contradicción entre ambos.
4. Qué haría falta para predecir mejor — y de ahí el paso a
   `Condición → Conectividad cerebral → Conducta`.

---

## Requisitos

En Colab, ninguno: `pandas`, `numpy`, `matplotlib`, `statsmodels` y `scikit-learn` vienen
preinstalados y los cuadernos no ejecutan ningún `pip install`.

Para correrlos localmente:

```bash
git clone https://github.com/decostruttivismo/IIC3800-2026-NCC-IA.git
cd IIC3800-2026-NCC-IA/clase-24-agosto
pip install -r requirements.txt
jupyter lab
```

---

## Para el equipo docente

La preparación, el guion de aula y los números de referencia están en
[`docs/guia_docente.md`](docs/guia_docente.md) y
[`docs/resultados_esperados.md`](docs/resultados_esperados.md). Los pasos para subirlo a GitHub están en [`docs/publicar.md`](docs/publicar.md).

Las direcciones de este material ya apuntan a
`decostruttivismo/IIC3800-2026-NCC-IA`, carpeta `clase-24-agosto`. Si alguno de esos
nombres cambia, `configurar.py` los reescribe en todos los archivos de una vez:

```bash
python configurar.py --repo OTRO-NOMBRE
```

---

## Licencia

Material docente bajo [CC BY 4.0](LICENSE). Código de ejemplo, MIT.
