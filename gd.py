import numpy as np

class GDSolver:
    def __init__(self, operator, regularizer, learning_rate):
        self.A = operator
        self.reg = regularizer
        self.tau = learning_rate

    def solve(self, b, iterations):
        losses = []
        x = self.A.adjoint(b) # Inicialización

        for i in range(iterations):
            Ax = self.A.forward(x)
            residual = Ax - b
            grad_fid = self.A.adjoint(residual)
            grad_reg = self.reg.gradient(x)

            x = x - self.tau * (grad_fid + grad_reg)

            if i % 10 == 0:
                loss = 0.5 * np.sum(residual**2) + self.reg.value(x)
                losses.append(loss)

        return x, losses