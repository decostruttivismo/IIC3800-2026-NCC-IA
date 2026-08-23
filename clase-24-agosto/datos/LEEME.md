# Datos

`clase_24agosto_dataset.csv` — 3000 filas: 30 participantes × 100 ensayos de una tarea
Stroop.

| columna | tipo | descripción |
|---|---|---|
| `subject` | texto | identificador del participante (`S01`…`S30`) |
| `trial` | entero | número de ensayo dentro del participante (1–100) |
| `condition` | texto | `Congruent` / `Incongruent` |
| `RT_ms` | decimal | tiempo de reacción en milisegundos |
| `accuracy` | 0/1 | 1 = respuesta correcta |
| `age` | entero | edad del participante (21–40 años) |

Diseño balanceado (exactamente 50 ensayos por condición en cada participante), sin
valores faltantes.

## Los datos son simulados

No provienen de un experimento con personas. Se generaron con la estructura de uno, y
concretamente con una estructura muy parecida a la que la clase ajusta: efecto de
condición, efecto lineal del número de ensayo, desplazamiento por participante sacado de
una normal, ruido normal encima; y los aciertos aparte, con una probabilidad que depende
solo de la condición.

Eso está dicho en el cuaderno 1, al principio, y desarrollado al final del cuaderno 2,
donde se enumera en qué se notaría un conjunto real: distribución de RT asimétrica,
anticipaciones y despistes en las colas, errores más rápidos que los aciertos,
diferencias individuales en precisión y estructura secuencial entre ensayos. Los detalles
de cómo se comprueba cada una están en `docs/guia_docente.md`.

Para lo que la clase enseña —las decisiones de análisis— no supone ninguna limitación.
Para hablar de cognición humana, sí.
