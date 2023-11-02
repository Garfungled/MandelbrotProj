import math
from decimal import Decimal as D
import colorsys

# non-inclusive
def clamp (n:float, lower_bound: float, upper_bound: float):
    return n if n > lower_bound and n < upper_bound else (0 if n <= lower_bound else 1)

# z_n+1 = (z_n)^2 + z_0
# |z_n| = magniute of the complex number
def mandelBrot(z_0: complex, max_iterations: int):
    iteration = 0
    magnitude = 0
    z_n = complex(0, 0)
    
    while iteration < max_iterations+1 and magnitude < 2:
        iteration += 1
        z_n = (z_n * z_n) + z_0
        magnitude = abs(z_n)
    
    return (iteration-1, magnitude)


# Change to: (a + b * cos(6.28318*(c*t+d)))*1.3 -> vect3
    # t float: frac(sn + 0.5)
        # sn: iteration/max_iterations * colorfullness
            # colorfullness int: any num
    # a vect3: vect3(.5)
        # vect3(n) = (n, n, n)
    # b vect3: vect3(.5)
    # c vect3: vect3(1)
    # d vect3: vect3(.0, .1, .2) 
def colorful_mandel(iteration: int, max_iteration: int, colorfulness: int):
    if iteration == max_iteration:
        return (0, 0, 0)
    
    clamp_col = lambda c_vec: tuple(c if c >= 0 and c <= 1 else (0 if c < 0 else 1) for c in c_vec)
    add_vec = lambda vec1, vec2: tuple(comp1 + comp2 for comp1, comp2 in zip(vec1, vec2))
    dot_vec = lambda vec1, vec2: tuple(comp1 * comp2 for comp1, comp2 in zip(vec1, vec2))
    scale_vec = lambda vec, scale: tuple(comp * scale for comp in vec)
    cos_vec = lambda vec: tuple(math.cos(comp) for comp in vec)
    frac = lambda f: f - math.floor(f)
    
    a = (0.5, 0.5, 0.5)
    b = (0.5, 0.5, 0.5)
    c = (1, 1, 1)
    d = (0, 0.1, 0.2)
    sn = iteration/(max_iteration * colorfulness)
    t = frac(sn + 0.5)
    
    return clamp_col(scale_vec(add_vec(a, dot_vec(b, cos_vec(scale_vec(scale=6.28318, vec=add_vec(scale_vec(c, t), d))))), 1.3))

def mandel_color(iterations: int, max_iterations: int):
    hue = int(255 * iterations / max_iterations)
    saturation = 255
    value = 255 if iterations < max_iterations else 0
    return colorsys.hsv_to_rgb(hue/255, saturation/255, value/255)

"""
General idea of what the parameters should be:
    dimension = int(input("Dimension: "))
    step = D(input("Step (between 0 -> 1): "))
    max_iterations = int(input("max iterations: "))
"""
def getMandelSet (dimension: float, step: D, max_iterations: int):
    # Get the complex nums array
    dimension = D(dimension)
    arr_size = math.ceil(dimension/step) * 2 + math.ceil(dimension/step) % 2
    coefficients = [[(float(D(a - arr_size / 2 + (arr_size % 2) / 2) * step), float(D(b + 1 - arr_size / 2 - (arr_size % 2) / 2) * step)) for b in range(arr_size)] for a in range(arr_size)]
    complex_nums = [[complex(coefficients[i][j][0], coefficients[i][j][1]) for i in range(arr_size)] for j in range(arr_size)]
    complex_nums.reverse()

    # Get iterations and magniutes of each complex number
    iterations = [[mandelBrot(z_0=complex_nums[j][i], max_iterations=max_iterations)[0] for i in range(arr_size)] for j in range(arr_size)]
    magnitudes = [[mandelBrot(z_0=complex_nums[j][i], max_iterations=max_iterations)[1] for i in range(arr_size)] for j in range(arr_size)]
    
    return complex_nums, iterations, magnitudes
