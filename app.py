from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io, base64
from PIL import Image

from superres.operators import BlurDownsampleOperator
from superres.regularizers import L2GradientRegularizer, HuberGradientRegularizer
from superres.gd import GDSolver

app = Flask(__name__)

def load_image(file_storage):
    # Carga imagen, pasa a grises, redimensiona (para rapidez) y normaliza
    img = Image.open(file_storage).convert('L')
    img.thumbnail((256, 256)) # Limitamos tamaño para que Colab no explote
    return np.array(img, dtype=np.float32) / 255.0

def plot_to_base64(original, observed, recovered, losses):
    fig, ax = plt.subplots(1, 4, figsize=(16, 4))
    ax[0].imshow(original, cmap='gray'); ax[0].set_title("Original (Subida)")
    ax[1].imshow(observed, cmap='gray'); ax[1].set_title("Observada (Blur+Sub)")
    ax[2].imshow(recovered, cmap='gray'); ax[2].set_title("Recuperada (HR)")
    ax[3].plot(losses); ax[3].set_title("Convergencia")
    for a in ax[:3]: a.axis('off')
    ax[3].grid(True)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None
    if request.method == 'POST':
        try:
            # 1. Verificar Imagen
            if 'file' not in request.files: return "No se subió archivo"
            file = request.files['file']
            if file.filename == '': return "Archivo vacío"

            # 2. Cargar parámetros
            x_true = load_image(file)
            reg_type = request.form.get('reg_type', 'L2')
            iters = int(request.form.get('iters', 300))
            lam = float(request.form.get('lam', 0.01))
            tau = float(request.form.get('tau', 1.5))
            s = int(request.form.get('s', 2))
            delta = float(request.form.get('delta', 0.01))

            # 3. Simular Problema (Degradar la foto subida)
            op = BlurDownsampleOperator(kernel_size=5, sigma=1.0, s=s)
            y = op.forward(x_true)

            # 4. Seleccionar Regularizador
            if reg_type == 'Huber':
                reg = HuberGradientRegularizer(lam, delta)
            else:
                reg = L2GradientRegularizer(lam)

            # 5. Resolver
            solver = GDSolver(op, reg, learning_rate=tau)
            x_rec, losses = solver.solve(y, iters)

            img_data = plot_to_base64(x_true, y, x_rec, losses)

        except Exception as e:
            return f"<h2>Error:</h2><p>{e}</p>"

    return render_template('index.html', img_data=img_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)