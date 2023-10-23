import math
from decimal import Decimal as D
import colorsys

# z_n+1 = (z_n)^2 + z_0
# |z_n| = magniute of the complex number
def mandelBrot(z_0: complex, max_iterations: int):
    iteration = 0
    magnitude = 0
    z_n = complex(0, 0)
    
    while iteration < max_iterations and magnitude < 2:
        iteration += 1
        z_n = (z_n * z_n) + z_0
        magnitude = abs(z_n)
    
    return (iteration, magnitude)

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
