import numpy as np
from scipy.ndimage import convolve

class BlurDownsampleOperator:
    def __init__(self, kernel_size, sigma, s):
        self.s = s
        self.kernel = self._gaussian_kernel(kernel_size, sigma)

    def _gaussian_kernel(self, size, sigma):
        ax = np.arange(-size // 2 + 1., size // 2 + 1.)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
        return kernel / np.sum(kernel)

    def forward(self, x):
        blurred = convolve(x, self.kernel, mode='wrap')
        return blurred[::self.s, ::self.s]

    def adjoint(self, y):
        H_lr, W_lr = y.shape
        H_hr, W_hr = H_lr * self.s, W_lr * self.s
        y_upsampled = np.zeros((H_hr, W_hr))
        y_upsampled[::self.s, ::self.s] = y
        return convolve(y_upsampled, self.kernel, mode='wrap')
