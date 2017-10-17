class Diagram:


    def __init__(self, name_in, num_in, shapes_in, relations_in):
        self.name = None
        self.num = -1
        self.shapes = None
        self.relations = None


        self.name = name_in
        self.num = num_in
        self.shapes = shapes_in
        self.relations = relations_in

    def __str__(self):
        to_return = self.name + "\n"
        for shape in self.shapes:
            to_return += str(shape) + "\n"
        for relation in self.relations:
            to_return += str(relation) + "\n"
        return to_return



