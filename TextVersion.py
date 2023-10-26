import MandelBrot 
from decimal import Decimal as D

#### Functions ####

def create_mandel(iterations, max_iterations: int):
    for i in iterations:
        for j in i:
            print((" " if j != max_iterations else "#"), end="")
        print()

#### Main ####
if __name__ == '__main__':
    #### Inputs ####
    complex_dimension = float(D(input("Input a dimension for the square (must be a single integer greater than or equal to 1): ")))
    step = D(input("Input a step for the Mandelbrot function (positive real number): "))
    max_iterations = int(input("Input a max iteration for the Mandelbrot function (a positive integer): "))
    
    #### Logic ####
    iterations = MandelBrot.getMandelSet(complex_dimension, step, max_iterations)[1]
    create_mandel(iterations, max_iterations)
    