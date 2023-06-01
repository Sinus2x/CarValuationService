import numpy as np


class MedianAPE:
    def __init__(self, f=lambda x: x, inv_f=lambda x: x):
        self.f = f
        self.inv_f = inv_f


    def get_final_error(self, error, weight=1.0):
        return error

    def is_max_optimal(self):
        # the lower metric value the better
        return False

    def evaluate(self, approxes, target, weight=None):
        assert len(approxes) == 1
        assert len(target) == len(approxes[0])

        approx = approxes[0]

        preds = self.inv_f(np.array(approx))
        target = self.inv_f(np.array(target))
        error = np.median((np.abs(np.subtract(target, preds) / target))) * 100
        return (error, 1.0)


class MedianAPE_scale:
    def __init__(self, f, inv_f, val_prices_approxes, val_prices_target, prices_approxes, prices_target):
        self.f = f
        self.inv_f = inv_f
        self.val_prices_approxes = val_prices_approxes
        self.val_prices_target = val_prices_target
        self.prices_approxes = prices_approxes
        self.prices_target = prices_target


    def get_final_error(self, error, weight=1.0):
        return error

    def is_max_optimal(self):
        # the lower metric value the better
        return False

    def evaluate(self, approxes, target, weight=None):
        assert len(approxes) == 1
        assert len(target) == len(approxes[0])

        approx = approxes[0]

        preds = self.inv_f(np.array(approx))
        target = self.inv_f(np.array(target))

        if preds.shape == self.prices_approxes.shape:
            preds = preds * self.prices_approxes
            target = target * self.prices_target
        else:
            preds = preds * self.val_prices_approxes
            target = target * self.val_prices_target

        error = np.median((np.abs(np.subtract(target, preds) / target))) * 100
        return (error, 1.0)
