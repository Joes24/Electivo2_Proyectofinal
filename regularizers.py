import numpy as np

class L2GradientRegularizer:
    def __init__(self, lam):
        self.lam = lam

    def gradient(self, x):
        Dx = np.roll(x, -1, axis=1) - x; Dx[:, -1] = 0
        Dy = np.roll(x, -1, axis=0) - x; Dy[-1, :] = 0

        div_x = np.pad(Dx, ((0,0),(1,0)))[:,1:] - np.pad(Dx, ((0,0),(1,0)))[:,:-1]
        div_x[:,0] = Dx[:,0]; div_x[:,-1] = -Dx[:,-2]
        div_y = np.pad(Dy, ((1,0),(0,0)))[1:,:] - np.pad(Dy, ((1,0),(0,0)))[:-1,:]
        div_y[0,:] = Dy[0,:]; div_y[-1,:] = -Dy[-2,:]

        return -2 * self.lam * (div_x + div_y)

    def value(self, x):
        Dx = np.roll(x, -1, axis=1) - x; Dx[:, -1] = 0
        Dy = np.roll(x, -1, axis=0) - x; Dy[-1, :] = 0
        return self.lam * np.sum(Dx**2 + Dy**2)

class HuberGradientRegularizer:
    def __init__(self, lam, delta=0.01):
        self.lam = lam
        self.delta = delta

    def _phi_prime(self, z):
        # Derivada de Huber: z/delta si es pequeño, sign(z) si es grande
        condition = np.abs(z) <= self.delta
        return np.where(condition, z / self.delta, np.sign(z))

    def gradient(self, x):
        Dx = np.roll(x, -1, axis=1) - x; Dx[:, -1] = 0
        Dy = np.roll(x, -1, axis=0) - x; Dy[-1, :] = 0

        Wx = self._phi_prime(Dx)
        Wy = self._phi_prime(Dy)

        div_x = np.pad(Wx, ((0,0),(1,0)))[:,1:] - np.pad(Wx, ((0,0),(1,0)))[:,:-1]
        div_x[:,0] = Wx[:,0]; div_x[:,-1] = -Wx[:,-2]
        div_y = np.pad(Wy, ((1,0),(0,0)))[1:,:] - np.pad(Wy, ((1,0),(0,0)))[:-1,:]
        div_y[0,:] = Wy[0,:]; div_y[-1,:] = -Wy[-2,:]

        return -self.lam * (div_x + div_y)

    def value(self, x):
        # Solo referencial
        return 0