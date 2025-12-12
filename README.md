# Proyecto Final: Super-Resolución de imagenes 2D

Este proyecto implementa una solución numérica al problema inverso de Super-Resolución (SR) utilizando métodos de optimización (Descenso de Gradiente) y una interfaz web construida con Flask.

## Integrantes:
* José Gormaz, Octavio Marchant, Miguel Quispe, Stefany Urzua

## Descripción del Problema:
El objetivo es reconstruir una imagen de alta resolución $x$ a partir de una observación degradada $y$.
Resolvemos el siguiente problema de minimización:

$$ \min_x J(x) = 1/2 * ||Ax - y||^2 + \lambda R(x) $$

Donde:
* **$A$ (Operador de Degradación):** Modela el desenfoque (Blur Gaussiano) y el submuestreo (Downsampling) de la imagen.
* **$y$:** Es la imagen de baja resolución observada (Input).
* **$R(x)$:** Es el término de regularización para estabilizar la solución.

## Regularizadores Implementados
El código permite seleccionar entre dos tipos de regularización:
1. **L2 (Tikhonov):** Penaliza la norma cuadrada del gradiente ($||
abla x||^2$). Suaviza la imagen globalmente.
2. **Huber (TV Suavizada):** Penaliza el gradiente usando la función de Huber. Preserva mejor los bordes (aristas) de la imagen que L2.

## Instrucciones de Instalación y Ejecución (la forma más rapida)

Para probar el proyecto en tu computadora, solo necesitas una terminal y Python instalado.

### Paso 1: Instalar Dependencias
Abre tu terminal en la carpeta del proyecto y ejecuta:
pip install -r requirements.txt

### Paso 2: Activar la aplicación web:
Inicie el servidor web con este comando:
python app.py
Verá un mensaje que dice: "Running on https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:5000"
### Paso 3:Acceder a la web:
1. Abra su navegador de internet (Chrome, Firefox, Edge).
2. Escriba o pegue esta dirección: http://127.0.0.1:5000
Verá la interfaz para subir tu imagen.

### Guía para poder la web:
Una vez dentro de la web:
1. Haz clic en "Seleccionar archivo" y sube una imagen (JPG/PNG).
2. Selecciona el Regularizador (L2 o Huber).
3. Presiona "Procesar".
4. Espera unos segundos y verás la comparación entre la imagen degradada y la recuperada.
