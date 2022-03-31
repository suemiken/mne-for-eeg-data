import numpy as np
def Kappa(result_arr, name, chancelevel=0.25, mode='return'):
    kappa = (result_arr - chancelevel)/(1 - chancelevel)
    if mode == 'disp':
        print(name + '_kappa:{0}'.format(kappa))
    elif mode == 'return':
        return kappa
