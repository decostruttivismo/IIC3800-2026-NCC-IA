# Modelos bayesianos del aprendizaje — tres actividades

Material práctico de la clase del **31 de agosto** del curso
**Modelos de Aprendizaje en Neurociencia Cognitiva e Inteligencia Artificial**
(Pontificia Universidad Católica de Chile, segundo semestre 2026).

Tres cuadernos cortos, cada uno con código que ya corre y tareas para extenderlo. Cada
uno implementa un modelo distinto de la misma familia —hipótesis, prior, verosimilitud,
posterior— sobre un problema de aprendizaje diferente.

**Cómo están pensados.** En cada cuaderno, las **tareas 1 y 2 son para la clase**: unos
15 minutos por cuaderno. La **tarea 3 queda para la casa** — es la pregunta conceptual que
conecta cada actividad con la siguiente, y no se alcanza a hacer bien en clase.

---

## Abrir los cuadernos

No hay que instalar nada. Haz clic en un botón y se abre en Google Colab.

| | cuaderno | contenido |
|---|---|---|
| 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/decostruttivismo/IIC3800-2026-NCC-IA/blob/main/clase-31-agosto/notebooks/actividad1_principio_del_tamano.ipynb) | **El principio del tamaño.** El *number game* de Tenenbaum y Griffiths: muestreo fuerte y promedio de hipótesis. |
| 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/decostruttivismo/IIC3800-2026-NCC-IA/blob/main/clase-31-agosto/notebooks/actividad2_coincidencia_sospechosa.ipynb) | **La coincidencia sospechosa.** Xu y Tenenbaum (2007): árbol taxonómico, prior de longitud de rama. |
| 3 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/decostruttivismo/IIC3800-2026-NCC-IA/blob/main/clase-31-agosto/notebooks/actividad3_formas_estructurales.ipynb) | **¿De dónde viene el espacio de hipótesis?** Kemp y Tenenbaum (2008): se infiere también la forma estructural. |

> **Consejo:** en Colab, `Archivo → Guardar una copia en Drive` para conservar lo que
> escribas. Sin eso, los cambios se pierden al cerrar la pestaña.

---

## Descargar el material

Para la clase no hace falta: los botones de arriba abren los cuadernos en Colab.
Pero si quieres tener los archivos en tu computador:

- **Todo de una vez.** En la portada del repositorio, botón verde **Code → Download ZIP**.
  Descarga el repositorio completo; la carpeta de esta clase es `clase-31-agosto`.
- **Un archivo suelto.** Ábrelo en GitHub y usa **Download raw file** (el icono de la
  flecha, arriba a la derecha del archivo).
- **Con git**, si lo usas:

  ```bash
  git clone https://github.com/decostruttivismo/IIC3800-2026-NCC-IA.git
  cd IIC3800-2026-NCC-IA/clase-31-agosto/notebooks
  jupyter lab
  ```

Los tres cuadernos son autocontenidos: cada uno trae su propio código de modelo en la
primera celda, así que corren igual en Colab, en Jupyter local o copiados a un script. El
archivo [`forms_model.py`](notebooks/forms_model.py) es la versión de referencia del
modelo de la actividad 3 como módulo suelto, por si prefieres importarlo en vez de correr
la celda.

---

## Requisitos

En Colab, ninguno: `numpy`, `matplotlib` y `scipy` vienen preinstalados y los cuadernos
no ejecutan ningún `pip install`.

Para correrlos localmente:

```bash
pip install numpy matplotlib scipy
```

---

## Licencia

Material docente bajo [CC BY 4.0](LICENSE). Código de ejemplo, MIT.
