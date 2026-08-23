# Publicar el material en GitHub

Todo el material está preparado para vivir en
`github.com/decostruttivismo/IIC3800-2026-NCC-IA`, dentro de la carpeta
`clase-24-agosto`. Las direcciones que abren Colab y la que sirve el CSV ya apuntan ahí,
así que no hay que editar nada si respetas esos dos nombres.

Un aviso antes de empezar: GitHub sustituye por guiones los caracteres que no admite en
el nombre de un repositorio. Si escribes `IIC3800-2026-NCC+IA`, el repositorio quedará
creado como `IIC3800-2026-NCC-IA` — que es el nombre para el que está preparado este
material. Si acabas usando otro nombre, `configurar.py --repo OTRO-NOMBRE` reescribe
todas las direcciones de una vez.

---

## Crear el repositorio

En <https://github.com/new>, con la sesión de `decostruttivismo` iniciada:

- **Repository name:** `IIC3800-2026-NCC-IA`
- **Visibility:** **Public**. Es imprescindible — Colab lee el cuaderno desde GitHub y
  el CSV se sirve por `raw.githubusercontent.com`, y ninguno de los dos funciona con un
  repositorio privado.
- **Add a README file:** déjalo sin marcar; el material ya trae uno.

## Subir la carpeta desde el navegador

En la página del repositorio recién creado, entra en **uploading an existing file**
(o ve a `github.com/decostruttivismo/IIC3800-2026-NCC-IA/upload/main`).

Arrastra **la carpeta `clase-24-agosto` entera** a la zona de subida. El navegador
conserva la estructura interna, así que quedará `clase-24-agosto/notebooks/…`,
`clase-24-agosto/datos/…` y `clase-24-agosto/docs/…` sin tener que crear nada a mano.
Escribe un mensaje en **Commit changes** y confirma.

## O bien, desde la terminal

```bash
cd carpeta-que-contiene/clase-24-agosto/..
git init -b main
git add clase-24-agosto
git commit -m "Material de la clase del 24 de agosto"
git remote add origin https://github.com/decostruttivismo/IIC3800-2026-NCC-IA.git
git push -u origin main
```

Con la CLI de GitHub, los dos últimos pasos son
`gh repo create IIC3800-2026-NCC-IA --public --source=. --push`.

---

## Comprobar que funciona

Abre una **ventana de incógnito** —sin sesión de GitHub ni de Google— y prueba el
enlace del cuaderno de prueba:

```
https://colab.research.google.com/github/decostruttivismo/IIC3800-2026-NCC-IA/blob/main/clase-24-agosto/notebooks/00_prueba.ipynb
```

Ejecuta las celdas. Si aparece el gráfico, los estudiantes no tendrán problemas.

Comprueba también que el CSV se sirve directamente:

```
https://raw.githubusercontent.com/decostruttivismo/IIC3800-2026-NCC-IA/main/clase-24-agosto/datos/clase_24agosto_dataset.csv
```

Debe mostrarse como texto plano o descargarse. Si da 404, el repositorio quedó privado,
la rama no se llama `main`, o el nombre del repositorio no es el que esperan las
direcciones.

---

## El enlace para la clase

El patrón de las direcciones de Colab es siempre el mismo:

```
https://colab.research.google.com/github/USUARIO/REPO/blob/RAMA/RUTA/AL/CUADERNO.ipynb
```

No hay que subir nada a Colab ni dar permisos: Colab lee el cuaderno de GitHub en el
momento en que alguien abre el enlace, y cada estudiante trabaja sobre su propia copia
en memoria. Para conservar lo que escriba, `Archivo → Guardar una copia en Drive`.

Para proyectar, `python configurar.py --qr` genera `docs/qr_colab.png` con el enlace del
cuaderno de prueba (requiere `pip install qrcode[pil]`; si no, cualquier generador web
sirve con la URL de arriba).

---

## Las clases siguientes

Cada clase nueva es una carpeta más en el mismo repositorio: `clase-31-agosto`,
`clase-07-septiembre`, y así. Para partir de esta, copia la carpeta, renómbrala y corre
`python configurar.py --carpeta clase-31-agosto` dentro de la copia: reescribe las
direcciones de los cuadernos y del README.

---

## Actualizar el material

Editar en GitHub —o hacer `git push`— basta: el enlace de Colab sirve siempre la versión
actual de la rama, así que no hay que reenviar nada a los estudiantes.

Si quieres congelar la versión que se usó en clase, crea una etiqueta y enlaza a ella:

```bash
git tag clase-24ago && git push --tags
```

Cambiando `main` por `clase-24ago` en la dirección de Colab, el enlace queda fijo aunque
después edites el material.
