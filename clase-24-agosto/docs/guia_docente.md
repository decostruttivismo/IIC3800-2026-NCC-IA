# Guía docente — práctica del 24 de agosto

Uso interno. Qué preparar, qué conviene subrayar en cada cuaderno, y qué hacer cuando
algo falla.

---

## Preparación

Los pasos para subir la carpeta a GitHub están en
[`publicar.md`](publicar.md). Lo único que hay que ejecutar aquí es el QR para
proyectar:

```bash
python configurar.py --qr
```

Después de subir el material, comprueba desde una ventana de incógnito que el botón de
Colab del cuaderno de prueba abre y ejecuta. Es la única comprobación que importa: si
funciona sin haber iniciado sesión con tu cuenta, funcionará para los estudiantes.

El repositorio tiene que ser público. Colab lee el cuaderno desde GitHub y el CSV se
sirve por `raw.githubusercontent.com`; ninguno de los dos funciona con un repositorio
privado sin autenticación.

Para proyectar basta una lámina con el enlace del repositorio y el QR. Conviene dejarla
visible desde el principio, para que quien tenga un problema lo descubra mientras aún
estás hablando y no cuando ya necesitas que todos estén corriendo código.

La carpeta `notebooks/soluciones/` va en el repositorio desde el principio. Si prefieres
que no esté disponible durante la clase, súbela después o mantenla en una rama aparte.

---

## Cuaderno de inferencia

El hilo es que cada modelo arregla un problema concreto del anterior, y que el último
—el mixto— no cambia la respuesta sino la confianza en ella.

Al cargar los datos conviene insistir en algo que va a hacer falta todo el rato: cada
fila es un ensayo, no una persona. Cuando aparezcan las medias por condición y el
histograma, el número que interesa no es solo los 65 ms de diferencia sino el solapamiento
de las dos distribuciones. Ese solapamiento es exactamente lo que el segundo cuaderno va
a intentar predecir, y la razón de que le salga mal.

El primer ejercicio pide el efecto por participante. Salen 30 de 30, entre 44 y 85 ms.
Merece pedir el número en voz alta: dice algo más fuerte que la diferencia de medias, y
es que el efecto no lo produce un subgrupo extremo.

Del `summary()` del primer modelo hay dos filas que conviene leer juntas y dejar
escritas en la pizarra: p ≈ 10⁻¹¹⁰ y R² = 0.154. Un efecto puede ser certísimo y pequeño
a la vez, y esos dos números vuelven al final del segundo cuaderno.

Al añadir `trial` aparece la práctica (−0.55 ms por ensayo) y, sobre todo, el hecho de
que β₁ casi no se mueve. Eso pasa porque el diseño está aleatorizado; en datos
observacionales no pasaría.

El segundo ejercicio tiene una trampa deliberada. El OLS le da a la edad p = 0.26, pero
ese valor-p es incorrecto: la edad solo varía entre participantes, hay 30 observaciones
independientes y no 3000, y el error estándar está subestimado en un factor de ocho (el
modelo mixto da p = 0.89). Conviene que lo vean aquí, en un caso donde el error no cambia
la conclusión, porque es exactamente el problema que la sección siguiente resuelve.

El gráfico por participante lo prepara: de 434 a 665 ms entre personas, tres veces el
efecto que queremos medir. El modelo mixto deja el efecto igual (64.67) y baja el error
estándar de 2.73 a 1.69, con ICC = 0.62. Ese 0.62 es el número que hay que dejar
guardado para el segundo cuaderno.

En la regresión logística, el aviso que conviene dar explícito es que un odds ratio de
0.49 no significa «la mitad de probabilidad»: la probabilidad solo baja de 0.940 a 0.884.
Y en el último ejercicio, que `trial` valga 3.8 puntos de precisión frente a los 5.6 que
cuesta la incongruencia no es un detalle: es un efecto de dos tercios del que estudiamos,
y omitirlo lo manda entero al término de error.

---

## Cuaderno de predicción

Antes de correr `GroupShuffleSplit` vale la pena hacer la pregunta y dejar que la
contesten ellos: si partimos al azar por ensayo, ¿qué está midiendo el resultado? La
conexión con el ICC = 0.62 del cuaderno anterior es directa: ese es el margen que puede
filtrarse. Cuánto se filtra de hecho depende del modelo, y el primer ejercicio lo mide
para el nuestro.

Sobre el `Pipeline`, la idea que no es burocracia: ajustar el codificador dentro del
pipeline es lo que impide que el conjunto de prueba entre en la preparación. Con dos
categorías el riesgo es nulo, pero con una imputación o un escalado no lo sería.

El resultado —RMSE 80 ms, R² 0.13— es el momento de la clase. Compáralo con la
desviación estándar del RT (83 ms) y con la línea base de predecir la media (86 ms), y
deja un silencio antes de explicar. El gráfico de predicho contra observado lo remata:
las predicciones se apiñan en dos columnas y los datos se extienden por cientos de
milisegundos.

En el primer ejercicio, el R² sube de 0.133 a 0.151 al partir al azar. La diferencia es
pequeña y el matiz es el punto de la actividad: este modelo no tiene con qué reconocer al
individuo, así que la mejora viene de calibrar la media. No conviene presentarlo como
fuga de información demostrada; con efectos aleatorios por sujeto o con un modelo
flexible sí lo sería.

El segundo ejercicio cierra el argumento. Con `drop='first'` un participante desconocido
se codifica como la categoría de referencia (`S01`), no como el promedio, y por eso el
resultado sale algo peor. La celda siguiente quita la referencia y da 0.1328, idéntico al
modelo sin `subject`. Ese es el número que hay que subrayar: darle al modelo la identidad
del participante no aporta nada cuando el participante es nuevo.

De ahí sale el puente a `Condición → Conectividad → Conducta`, con la precaución de que
esas dos regresiones no demuestran un mecanismo: la condición está aleatorizada, la
conectividad no.

---

## Contingencias

Si vas justo de tiempo, en el primer cuaderno la regresión logística es autocontenida y
puede quedar de tarea, igual que el ejercicio de la pendiente aleatoria. Lo que no
conviene saltar es el modelo mixto: sin el ICC de 0.62, el segundo cuaderno pierde su
explicación. En el segundo, el ejercicio de `subject` es el que cierra el argumento; el
de la partición al azar es el prescindible.

Si el wifi falla, los cuadernos buscan el CSV en disco antes de recurrir a la URL, así
que basta dejar el `.ipynb` y el `.csv` juntos en la carpeta compartida del curso.
Conviene tener también una copia de las soluciones para proyectar desde tu máquina.

Si alguien no puede entrar en Colab —cuentas institucionales con restricciones, o sin
sesión de Google—, lo rápido es que trabaje con un compañero. La alternativa es
[kaggle.com/code](https://www.kaggle.com/code), que importa un cuaderno por URL y trae
las mismas bibliotecas.

Tres avisos aparecerán en pantalla y no son errores. `ConvergenceWarning: Maximum
Likelihood optimization failed to converge` en el ejercicio de la pendiente aleatoria: el
segundo optimizador converge y el resultado se imprime, y merece medio minuto de
comentario, porque estimar una covarianza completa con 30 grupos es difícil.
`Optimization terminated successfully` de `smf.logit` es una línea informativa normal. Y
`UserWarning: Found unknown categories in columns [1] during transform` en el ejercicio de
`subject` es justamente lo que ese ejercicio quiere mostrar: vale la pena leerlo en voz
alta.

---

## Preguntas que van a salir

**«¿Por qué no usamos simplemente el modelo mixto para predecir?»**
Porque para un participante nuevo el efecto aleatorio $u_j$ no está estimado. La mejor
predicción que puede dar es $u_j = 0$, o sea la media poblacional: exactamente lo que
hace el modelo sin `subject`. La estructura mixta ayuda a inferir mejor, no a predecir a
alguien nuevo.

**«Entonces, ¿el valor-p está mal?»**
No. Dos distribuciones tienen dos propiedades independientes: dónde están sus centros y
cuánto se solapan. La significación habla de la separación de los centros y mejora
indefinidamente con el tamaño muestral; la calidad predictiva habla del solapamiento y no
mejora por medir a más gente. El dato que cierra la duda, y que descarta la explicación
fácil de que el modelo sobreajusta: partiendo al azar por ensayo, el R² de entrenamiento
es 0.191 y el de prueba 0.183, una brecha de 0.008. El modelo generaliza sin problema a
ensayos nuevos; lo que no generaliza es a personas nuevas.

**«¿Es fiable ese 0.13?»**
Poco, y conviene decirlo. Solo hay seis participantes en el conjunto de prueba, así que
el número depende de cuáles toquen. Repitiendo la partición con 200 semillas, la mediana
del R² es 0.10 y la mitad central va de −0.03 a 0.15: con estos predictores, predecir a
una persona nueva es a menudo igual o peor que predecir la media. El `random_state=42`
que usamos cae en la parte favorable.

**«¿Y si añadimos más variables?»**
Es la pregunta correcta, y la respuesta condiciona el resto del curso: hay que añadir
variables de la persona, medibles en la persona nueva. La conectividad funcional es un
candidato; unos ensayos de calibración son otro, con el matiz de que entonces el
participante ya no es del todo nuevo.

**«¿Este dataset es real?»**
No, y está dicho en el propio material: el cuaderno 1 lo anuncia al principio y el
cuaderno 2 dedica su última sección a en qué se notaría la diferencia. Conviene no
esconderlo, porque la evidencia es visible en los propios datos y algún estudiante la va
a encontrar.

Si alguien quiere comprobarlo, estos son los indicios, ordenados de más a menos
concluyentes. La distribución del RT es gaussiana —asimetría −0.01 y −0.07 en las dos
condiciones, curtosis nula, Shapiro sin rechazar en incongruente—, cuando los tiempos de
reacción humanos son sistemáticamente asimétricos hacia la derecha; de las 60 celdas
sujeto × condición, solo 28 tienen asimetría positiva, que es una moneda al aire. No hay
colas: nada por debajo de 250 ms ni por encima de 1000, en un rango de −2.9 a +3.3
desviaciones estándar. Los errores tardan lo mismo que los aciertos (+5.3 y −4.2 ms,
p ≈ 0.5), cuando en datos reales los errores son marcadamente más rápidos. Y los 30
participantes aciertan con la misma probabilidad: la desviación estándar observada de la
precisión por sujeto (0.026) es *menor* que la que produciría el puro azar binomial
(0.028), con un chi² de homogeneidad de p = 0.73.

Hay más, si hace falta. La autocorrelación de retardo 1 de los residuos dentro de sujeto
es 0.003 y el Durbin-Watson 1.99, es decir cero estructura secuencial; el efecto de
secuencia de congruencia queda en +6.7 ms y el enlentecimiento post-error en +2.7,
cuando ambos suelen ser de decenas de milisegundos. Faltan las leyes de escala: la
correlación entre el RT basal de cada persona y su efecto Stroop es exactamente +0.000,
la de la media con la dispersión es +0.22 y no significativa, y las varianzas de las dos
condiciones son idénticas (razón 1.03) pese a que una es 65 ms más lenta. El diseño es
exacto —100 ensayos por persona, 50 y 50, sin faltantes ni duplicados—, los 3000 valores
tienen exactamente un decimal, y la curva de práctica es lineal (R² = 0.69 sobre el
ensayo frente a 0.51 sobre su logaritmo) en vez de seguir una ley de potencia.

Todo apunta al mismo generador, que es casi literalmente la ecuación de las láminas.
Merece la pena decirlo en voz alta: los estudiantes están recuperando el modelo que
generó los datos, que es un ejercicio útil pero distinto de estudiar un fenómeno.
