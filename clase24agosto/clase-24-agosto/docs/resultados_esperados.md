# Resultados de referencia

Valores obtenidos sobre `datos/clase_24agosto_dataset.csv`
con `random_state=42` donde aplica. Sirven para comprobar de un vistazo que un
estudiante llegó al resultado correcto.

Versiones usadas para generarlos: pandas 2.x, statsmodels 0.14.6, scikit-learn 1.8.0.
Los coeficientes son deterministas y no dependen de la versión; las cifras de
`GroupShuffleSplit` sí dependen de `random_state`.

Los datos son simulados; `datos/LEEME.md` y la guía docente explican con qué estructura
y cómo se comprueba.

---

## Descriptivos

| | Congruent | Incongruent |
|---|---|---|
| RT medio (ms) | 518.61 | 583.66 |
| aciertos (proporción) | 0.9400 | 0.8840 |
| ensayos | 1500 | 1500 |

- Participantes: 30, con 100 ensayos cada uno. Sin valores faltantes.
- Desviación estándar del RT (global): **83.03 ms**.
- RT medio por participante: de **433.6** a **665.0 ms**.
- Edades: 21 a 40 años.

## Efecto Stroop por participante (TU TURNO 1, cuaderno 1)

| | valor |
|---|---|
| participantes con efecto positivo | **30 de 30** |
| efecto medio | 65.1 ms |
| rango | 43.6 a 85.1 ms |
| desviación estándar | 10.5 ms |

---

## Modelo 1 — `smf.ols('RT_ms ~ C(condition)')`

| término | coef. | e.e. | p |
|---|---|---|---|
| Intercept | 518.606 | 1.973 | ~0 |
| C(condition)[T.Incongruent] | **65.057** | 2.790 | **1.13e-110** |

R² = 0.1535 · R² ajustado = 0.153 · F = 543.8

## Modelo 2 — `+ trial`

| término | coef. | e.e. | p |
|---|---|---|---|
| Intercept | 546.530 | 3.083 | ~0 |
| C(condition)[T.Incongruent] | 64.672 | 2.730 | ~0 |
| trial | **−0.549** | 0.047 | 1.6e-30 |

R² = 0.1900

## Interacción y edad (TU TURNO 2, cuaderno 1)

| término | coef. | p | lectura |
|---|---|---|---|
| `C(condition)[T.Incongruent]:trial` | +0.039 | **0.679** | la interferencia no cambia con la práctica |
| `age` (OLS, 3000 filas) | +0.278 | 0.263 | e.e. 0.248 — subestimado en un factor de 8 |
| `age` (mixto, `groups=subject`) | +0.278 | **0.891** | e.e. 2.025 — el correcto |
| `age` (regresión sobre los 30 promedios) | +0.278 | 0.892 | e.e. 2.025 |

`age` solo varía entre participantes: hay 30 observaciones independientes, no 3000. El
coeficiente es idéntico en los tres modelos y el error estándar del mixto concuerda con el
de la regresión sobre los 30 promedios hasta el tercer decimal (2.0251 vs. 2.0255).
La conclusión (sin efecto en el rango 21–40) no cambia; el valor-p que hay que citar es
0.89, no 0.26. Nota aparte: hay 18 edades distintas entre los 30 participantes.

## Modelo 3 — `smf.mixedlm(..., groups=subject)`

| término | coef. | e.e. |
|---|---|---|
| Intercept | 546.530 | 11.065 |
| C(condition)[T.Incongruent] | 64.672 | **1.688** |
| trial | −0.549 | 0.029 |

| componente de varianza | valor |
|---|---|
| entre participantes (`Group Var`) | 3564.2 |
| residual (`Scale`) | 2137.9 |
| **ICC** | **0.625** |

El coeficiente de condición es idéntico al de OLS; el error estándar baja de 2.730 a
1.688, una reducción del **38 %**.

## Pendiente aleatoria (TU TURNO 3, cuaderno 1)

`re_formula='~C(condition)'`

| componente | varianza | desv. estándar |
|---|---|---|
| intercepto (velocidad basal) | 6045.3 | ≈ 78 ms |
| pendiente (efecto Stroop) | 16.1 | ≈ 4 ms |
| covarianza | 142.2 | |

Emite `ConvergenceWarning` y converge con el segundo optimizador.

---

## Regresión logística — `smf.logit('accuracy ~ C(condition)')`

| escala | Congruent | Incongruent | efecto |
|---|---|---|---|
| log-odds | 2.7515 | 2.0309 | β₁ = **−0.7207** |
| odds | 15.667 | 7.621 | OR = **0.4864** |
| probabilidad | 0.9400 | 0.8840 | −5.6 puntos |

## Logística con `trial` (TU TURNO 4, cuaderno 1)

| término | coef. (log-odds) | p |
|---|---|---|
| Intercept | 2.5148 | 4e-61 |
| C(condition)[T.Incongruent] | −0.7185 | 1.1e-07 |
| trial | **+0.00483** | **0.033** |

Acumulado sobre los 100 ensayos: 0.48 log-odds = de 0.892 a 0.930 promediando condiciones,
es decir **+3.8 puntos porcentuales**. Empíricamente, 0.888 en los primeros 25 ensayos y
0.923 en los últimos 25. Compárese con los 5.6 puntos que cuesta la incongruencia y con
los 55 ms que la práctica vale en el RT: es un efecto del mismo orden que el de interés,
no una molestia menor.

---

## Predicción (cuaderno 2)

`GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)`

- Entrenamiento: 2400 ensayos, 24 participantes.
- Prueba: 600 ensayos, 6 participantes — **S09, S10, S16, S18, S24, S28**.

Coeficientes del `LinearRegression` dentro del pipeline:

| | valor |
|---|---|
| intercepto | 524.96 |
| incongruencia | +65.41 ms |
| ensayo | −0.58 ms/ensayo |
| edad | +0.69 ms/año |

| medida | valor |
|---|---|
| **RMSE (prueba)** | **79.97 ms** |
| **R² (prueba)** | **0.1328** |
| R² (entrenamiento) | 0.2043 |
| RMSE prediciendo la media | 86.00 ms |
| R² prediciendo la media | −0.0029 |
| desviación estándar del RT | 83.03 ms |

### TU TURNO 1 — partición al azar por ensayo

| partición | R² | RMSE |
|---|---|---|
| por participante (`GroupShuffleSplit`) | 0.1328 | 79.97 ms |
| al azar (`train_test_split`) | **0.1508** | 76.07 ms |

Diferencia pequeña **porque el modelo no tiene ninguna variable con la que identificar
al individuo**: la mejora viene de calibrar mejor la media, no de fuga propiamente dicha.
Con efectos aleatorios por sujeto, rasgos derivados del participante o un modelo flexible,
la fuga sería mucho mayor. Conviene decirlo así en clase y no dar por hecho el
*leakage* como si ya estuviera demostrado con este modelo.

### TU TURNO 2 — añadir `subject` como variable

| | R² | RMSE |
|---|---|---|
| con `subject` (`drop='first'`), participantes nuevos | 0.12791 | 80.20 ms |
| con `subject` (`drop=None`), participantes nuevos | 0.13278 | 79.97 ms |
| sin `subject`, participantes nuevos | 0.13276 | 79.97 ms |
| con `subject`, **en entrenamiento** | **0.6903** | |

Con `drop='first'` la categoría eliminada es `S01`, y un participante desconocido
codificado como todo ceros **es S01 para el modelo**, no el participante promedio
(S01 promedia 569.1 ms frente a 550.2 de la media de entrenamiento). De ahí que salga
algo peor. Quitando la categoría de referencia el resultado coincide con el del modelo
sin `subject` hasta el cuarto decimal: darle la identidad del participante no aporta
nada cuando el participante es nuevo.

El salto de 0.204 a 0.690 en entrenamiento y la ausencia de ganancia fuera de muestra son
la misma observación que el ICC de 0.625: la varianza entre personas es grande, estable e
inaccesible para alguien que no hemos medido.

---

## El contraste que resume la clase

| medida | valor |
|---|---|
| valor-p del efecto de condición | ~10⁻¹¹⁰ |
| R² en participantes nuevos | 0.13 |
| RMSE | 80 ms |
| desviación estándar del RT | 83 ms |
