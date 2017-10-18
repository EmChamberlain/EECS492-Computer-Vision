class Shape:

    def __init__(self, input_str):
        self.id = None
        self.type = None
        self.size = None
        self.size_num = -1
        self.center = [-1, -1]
        self.sides = -1

        self.id = input_str[:input_str.find(" = ")]
        self.type = input_str[input_str.find(" = ") + 3:input_str.find("('")]
        paren_str = input_str[input_str.find("(") + 1:input_str.find(")")]
        paren_list = [x.strip() for x in paren_str.split(",")]
        self.size = paren_list[0][1:-1]
        if self.size == "small":
            self.size_num = 0
        if self.size == "medium":
            self.size_num = 1
        if self.size == "large":
            self.size_num = 2

        self.center[0] = int(paren_list[1])
        self.center[1] = int(paren_list[2])
        if self.type == "scc":
            self.sides = paren_list[3]

    def __str__(self):
        to_return = self.id + " = " + self.type + "('" + self.size + "', " + str(self.center[0]) + ", " + str(self.center[1])
        if self.type == "scc":
            to_return += ", " + self.sides
        return to_return + ")"

    def similar(self, other):
        return (self.type == other.type) and (self.size == other.size) and (self.sides == other.sides)



