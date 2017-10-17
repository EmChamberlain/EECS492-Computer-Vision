import sys
from Shape import Shape
from Diagram import Diagram

def read_diagrams(file):
    diagrams = []

    while True:
        name = file.readline()
        if not name: break
        if name == "\n": continue
        name = name.rstrip("\n")
        num = int(name[-1:])

        shapes = []
        shape_str = file.readline()
        while True:
            if "=" not in shape_str: break
            shapes.append(Shape(shape_str))
            shape_str = file.readline()

        relations = []
        relation_str = shape_str
        while True:
            if not relation_str: break
            if relation_str == "\n": break
            relations.append(relation_str.rstrip("\n"))
            relation_str = file.readline()

        diagrams.append(Diagram(name, num, shapes, relations))
    return diagrams


def find_diagram_a_for_b(b_diagram, a_diagrams):
    for diagram in a_diagrams:
        d_match = True
        for b_shape in b_diagram.shapes:
            s_match = False
            for a_shape in diagram.shapes:
                if b_shape.similar(a_shape):
                    s_match = True
                    break
            if not s_match:
                d_match = False
                break
        if d_match:
            return diagram
    return None

def find_diagram_c_for_a(a_diagram, c_diagrams):
    if len(c_diagrams) == 1:
        return c_diagrams[0]

    valid_diagrams = []

    for diagram in c_diagrams:
        d_match = True
        for a_relation in a_diagram.relations:
            r_match = False
            for c_relation in diagram.relations:
                if a_relation[:a_relation.find("(")] == c_relation[:c_relation.find("(")]:
                    r_match = True
                    break
            if not r_match:
                d_match = False
                break
        if d_match:
            valid_diagrams.append(diagram)

    final_diagrams = []
    for diagram in valid_diagrams:
        d_match = True
        for a_shape in a_diagram.shapes:
            s_match = False
            for c_shape in diagram.shapes:
                if a_shape.size == c_shape.size:
                    s_match = True
                    break
            if not s_match:
                d_match = False
                break
        if d_match:
            final_diagrams.append(diagram)

    return final_diagrams[0]


def main():
    base_name = sys.argv[1]
    input_directory = sys.argv[2]
    output_directory = sys.argv[3]
    fileIn = open(input_directory + "/" + base_name + ".txt", "r")
    fileOut = open(output_directory + "/" + base_name + "_solution.txt", "w+")
    diagrams = read_diagrams(fileIn)

    a_diagrams = []
    b_diagrams = []
    c_diagrams = []
    k_diagrams = []
    for diagram in diagrams:
        if diagram.name[:1] == "A":
            a_diagrams.append(diagram)
        elif diagram.name[:1] == "B":
            b_diagrams.append(diagram)
        elif diagram.name[:1] == "C":
            c_diagrams.append(diagram)
        elif diagram.name[:1] == "K":
            k_diagrams.append(diagram)
        else:
            print("Diagram has name: " + str(diagram.name))
            sys.exit(1)

    a_diagram = find_diagram_a_for_b(b_diagrams[0], a_diagrams)
    b_diagram = b_diagrams[0]
    c_diagram = find_diagram_c_for_a(a_diagram, c_diagrams)
    pass




if __name__ == "__main__":
    main()
