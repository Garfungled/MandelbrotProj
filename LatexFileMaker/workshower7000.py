# Created by Niranjan Nair, my best pal at school

def strComplex(complex_num: complex) -> str:
    return f"{round(complex_num.real, 4)} + {round(complex_num.imag, 4)}i" if complex_num.imag >= 0 else f"{round(complex_num.real, 4)} - {abs(round(complex_num.imag, 4))}i"


def showWork(point: complex, max_iterations: int) -> str:
    iterations: list[complex] = []
    current: complex = complex(0, 0)
    work_string: str = f"Considering the point ${strComplex(point)}$..."

    for _ in range(max_iterations):
        if abs(current) > 2:
            break

        current = current ** 2 + point
        iterations.append(current)

    work_string += "\n\\begin{multline}\n"

    for index, iteration in enumerate(iterations[:-1]):
        work_string += "z_{" + str(index) + "} = " + strComplex(iteration) + "\\\\\n"
        work_string += "z_{" + str(index + 1) + "} = (" + strComplex(iteration) + ")^{2} + (" + strComplex(point) + ")\\\\\n\\Rightarrow "
        work_string += "z_{" + str(index + 1) + "} = (" + strComplex(iteration ** 2) + ") + (" + strComplex(point) + ")\\\\\n\\Rightarrow "
    
    work_string += "z_{" + str(len(iterations) - 1) + "} = " + strComplex(iterations[-1]) + "\\\\\n"

    work_string += "\\end{multline}\n"
    work_string += "The magnitude of $z_{" + str(len(iterations) - 1) + "}$ is $\sqrt{(" + str(round(iterations[-1].real, 4)) + ")^2 + (" + str(round(iterations[-1].imag, 4)) + ")^2}$ which equals " + str(round(abs(iterations[-1]), 4)) + ".\n"

    if abs(iterations[-1]) > 2:
        work_string += "We confirm that the point $" + strComplex(point) + "$ is not in the Mandelbrot set because $z_{" + str(len(iterations) - 1) + "}$ has a magnitude greater than 2.\n\n"
    else:
        work_string += "We confirm that the point $" + strComplex(point) + "$ is in the Mandelbrot set because $z_{" + str(len(iterations) - 1) + "}$ has a magnitude less than 2.\n\n"

    return work_string


def showWorkFromCoordinatePlane(coordinates: list[list[complex]], max_iterations: int) -> str:
    work_string: str = ""
    work_string += "\\section{Goals}"
    work_string += f"\nThis exercise aims to address which points on the complex plane lie in the Mandelbrot set and which do not. Calculations have been automated, and we present the results of ${max_iterations}$ iterations below.\n"
    work_string += "\\section{Calculations Over " + str(max_iterations) + " Iterations}\n"
    work_string += f"With ${max_iterations}$ iterations, we have calculated the following:\n"

    for y_axis in coordinates:
        for point in y_axis:
            work_string += "\\subsection{Evaluating the point " + strComplex(point) + "}\n"
            work_string += showWork(point, max_iterations)
    
    work_string += "\\section{Methods}"
    work_string += f"\nThis paper has been automatically generated through the use of a Python script that generates LaTeX syntax that has been rendered into this paper. Over the specified iterations, the program evaluates a specific portion of the complex plane with a specific resolution, and runs evaluations for each point. This program was written by N. Nair.\n"

    work_string += "\\section{Conclusions}"
    work_string += f"\nRunning over ${max_iterations}$ iterations, we have generated a graph of the mandelbrot set as presented by Z. Medjamia on the slideshow, and we have generated a shader that renders the graph as presented by N. Nair.\n"
    
    return work_string


def floatRange(start: float, stop: float, step: float):
    counter: float = start
    while counter < stop:
        yield counter
        counter += step


def generatePlane(bounds_x: list[float], bounds_y: list[float], resolution: float) -> list[list[complex]]:
    bottom_bound_x, top_bound_x, bottom_bound_y, top_bound_y = bounds_x[0], bounds_x[1], bounds_y[0], bounds_y[1]
    out_list: list[list[complex]] = []

    for x_coordinate in floatRange(bottom_bound_y, top_bound_y, resolution):
        horizontal: list[complex] = []

        for y_coordinate in floatRange(bottom_bound_x, top_bound_x, resolution):
            horizontal.append(complex(y_coordinate, x_coordinate))

        out_list.append(horizontal)

    return out_list


def latexHeader(title: str, authors: list[str], date: str=None) -> str:
    header: str = "\\documentclass{article}\n\\usepackage{mathtools}\n\\allowdisplaybreaks\n\n"
    header += "\\title{" + title + "}\n"
    header += "\\author{\n"

    for index, author in enumerate(authors):
        header += author
        header += "\n\\and\n" if index < len(authors) - 1 else "\n}\n"
    
    header += "\\date{"
    header += date + "}" if date else "\\today}\n\n"
    header += "\\begin{document}\n\\maketitle\n"

    return header


def latexEnding() -> str:
    return "\n\\end{document}"


def _test():
    with open("mandelbrot.tex", "w") as file:
        file.write(latexHeader("Evaluating Points of the Mandelbrot Set", ["Nair, N.", "Medjamia, Z."]))
        coordinates: list[list[complex]] = generatePlane([-1.8, 1.8 + 0.08], [-1.8, 1.8 + 0.08], 0.08)
        file.write(showWorkFromCoordinatePlane(coordinates, 6))
        file.write(latexEnding())


_test()