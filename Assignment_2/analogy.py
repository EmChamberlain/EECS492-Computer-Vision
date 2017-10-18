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
    if len(a_diagrams) == 1:
        return a_diagrams[0]

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


# both a and b are diagrams
def find_actions(a, b):
    actions = []

    correspondences = []

    for a_shape in a.shapes:
        match_shape = None
        max_match_score = 0
        for b_shape in b.shapes:
            match_score = 0
            if a_shape.type == b_shape.type and a_shape.sides == b_shape.sides:
                match_score += 1
                if a_shape.size == b_shape.size:
                    match_score += 1
                if a_shape.center == b_shape.center:
                    match_score += 1
                if match_score > max_match_score:
                    max_match_score = match_score
                    match_shape = b_shape
        correspondences.append((a_shape, match_shape))

    for corr in correspondences:
        if corr[1] is None:
            actions.append(("delete", corr[0], 0))
            continue
        if corr[0].size != corr[1].size:
            if corr[0].size_num > corr[1].size_num:
                actions.append(("reduction", corr[0], corr[1]))
            else:
                actions.append(("enlargement", corr[0], corr[1]))
        if corr[0].center != corr[1].center:
            if corr[0].center[0] > corr[1].center[0]:
                actions.append(("move_left", corr[0], corr[1]))
            elif corr[0].center[0] < corr[1].center[0]:
                actions.append(("move_right", corr[0], corr[1]))

            if corr[0].center[1] > corr[1].center[1]:
                actions.append(("move_up", corr[0], corr[1]))
            elif corr[0].center[1] < corr[1].center[1]:
                actions.append(("move_down", corr[0], corr[1]))

    return actions, correspondences


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

    a_b_actions, a_b_correspondences = find_actions(a_diagram, b_diagram)

    scores = [0] * len(k_diagrams)
    actions_normal = [(None, None)] * len(k_diagrams)
    for index in range(len(k_diagrams)):
        actions, correspondences = find_actions(c_diagram, k_diagrams[index])
        actions_normal[index] = (actions, correspondences)
        if len(a_b_actions) == len(actions):
            scores[index] += 1
        for action in actions:
            for a_b_action in a_b_actions:
                if action[0] == a_b_action[0]:
                    scores[index] += 1
                    if action[1].type == a_b_action[1].type:
                        scores[index] += 1
                    if action[1].size == a_b_action[1].size:
                        scores[index] += 1
                    if action[1].sides == a_b_action[1].sides:
                        scores[index] += 1
                    if action[1].center == a_b_action[1].center:
                        scores[index] += 1
                    if action[2] is Shape:
                        if action[2].type == a_b_action[2].type:
                            scores[index] += 1
                        if action[2].size == a_b_action[2].size:
                            scores[index] += 1
                        if action[2].sides == a_b_action[2].sides:
                            scores[index] += 1
                        if action[2].center == a_b_action[2].center:
                            scores[index] += 1

    k_diagram = None
    max_score = 0
    max_ind = -1
    for index in range(len(scores)):
        if scores[index] > max_score:
            max_score = scores[index]
            k_diagram = k_diagrams[index]
            max_ind = index

    fileOut.write("Answer: " + k_diagram.name[:k_diagram.name.find("_")] + "\n")
    fileOut.write("\n")
    fileOut.write("T_AB\n")
    corr_str = []
    for corr in a_b_correspondences:
        if corr[1] is None:
            corr_str.append("(" + corr[0].id + ", " + str(0) + ")")
        else:
            corr_str.append("(" + corr[0].id + ", " + corr[1].id + ")")
    corr_print = "["
    for corr in sorted(corr_str):
        corr_print += corr + ", "
    corr_print = corr_print[:-2]
    fileOut.write(corr_print + "\n")
    for action in a_b_actions:
        fileOut.write("action('" + action[0] + "', " + action[1].id + ")\n")
    fileOut.write("\n")

    fileOut.write("T_CK" + k_diagram.name[1:k_diagram.name.find("_")] + "\n")
    corr_str = []
    for corr in actions_normal[max_ind][1]:
        if corr[1] is None:
            corr_str.append("(" + corr[0].id + ", " + str(0) + ")")
        else:
            corr_str.append("(" + corr[0].id + ", " + corr[1].id + ")")
    corr_print = "["
    for corr in sorted(corr_str):
        corr_print += corr + ", "
    corr_print = corr_print[:-2]
    fileOut.write(corr_print + "\n")
    for action in actions_normal[max_ind][0]:
        fileOut.write("action('" + action[0] + "', " + action[1].id + ")\n")

    return




if __name__ == "__main__":
    main()
