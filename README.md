# Proyecto Final: Super-Resolución de imagenes 2D

Este proyecto implementa una solución numérica al problema inverso de Super-Resolución (SR) utilizando métodos de optimización (Descenso de Gradiente) y una interfaz web construida con Flask.

## Integrantes:
* José Gormaz, Octavio Marchant, Miguel Quispe, Stefany Urzua

## Descripción del Problema:
El objetivo es reconstruir una imagen de alta resolución $x$ a partir de una observación degradada $y$.
Resolvemos el siguiente problema de minimización:

$$ \min_x J(x) = rac{1}{2} ||Ax - y||^2 + \lambda R(x) $$

Donde:
* **$A$ (Operador de Degradación):** Modela el desenfoque (Blur Gaussiano) y el submuestreo (Downsampling) de la imagen.
* **$y$:** Es la imagen de baja resolución observada (Input).
* **$R(x)$:** Es el término de regularización para estabilizar la solución.

## Regularizadores Implementados
El código permite seleccionar entre dos tipos de regularización:
1. **L2 (Tikhonov):** Penaliza la norma cuadrada del gradiente ($||
abla x||^2$). Suaviza la imagen globalmente.
2. **Huber (TV Suavizada):** Penaliza el gradiente usando la función de Huber. Preserva mejor los bordes (aristas) de la imagen que L2.

## Instrucciones de Instalación y Ejecución

Sigue estos pasos para poder ejecutar el proyecto en tu máquina local:

### 1. Crear el Entorno Virtual (Opcional pero recomendado)
Es buena práctica aislar las dependencias:
```bash
# En Windows
python -m venv venv
vita\Scriptsctivate

# En Mac/Linux
python3 -m venv venv
source venv/bin/activate
