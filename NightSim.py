import random

class NightSim:
    TOTAL_MOV_OP = 107
    MOV_OP_BEFORE_2AM = 36
    MOV_OP_BEFORE_3AM = 53
    MOV_OP_BEFORE_4AM = 71

    BONNIE_PATH = {"1A": ["5", "1B"], "1B": ["5", "2A"], "5": ["1B", "2A"], "2A": ["3", "2B"], "3": ["2A", "D"],
                   "2B": ["3", "D"], "D": ["1B", "1B"]}
    CHICA_PATH = {"1A": ["1B", "1B"], "1B": ["7", "6"], "7": ["4A", "6"], "6": ["7", "4A"], "4A": ["1B", "4B"],
                  "4B": ["4A", "D"], "D": ["4A", "4A"]}

    def __init__(self, bonnie_ai, chica_ai):
        self.bonnie_ai = bonnie_ai
        self.chica_ai = chica_ai

        self.bonnie_pos = "1A"
        self.chica_pos = "1A"
        self.current_mov_op = 1

        self.two_am = False
        self.three_am = False
        self.four_am = False

        self.bonnie_at_door = []
        self.chica_at_door = []

    def update_movement(self):
        bonnie_roll = random.randint(1, 20)
        if (self.bonnie_ai + self.two_am + self.three_am + self.four_am >= bonnie_roll):
            self.bonnie_pos = self.BONNIE_PATH[self.bonnie_pos][random.randint(0, 1)]

        chica_roll = random.randint(1, 20)
        if (self.chica_ai + self.three_am + self.four_am >= chica_roll):
            self.chica_pos = self.CHICA_PATH[self.chica_pos][random.randint(0, 1)]

    def check_at_door(self):
        if (self.bonnie_pos == "D"):
            self.bonnie_at_door.append(self.current_mov_op)

        if (self.chica_pos == "D"):
            self.chica_at_door.append(self.current_mov_op)

    def update_ai(self):
        if (self.current_mov_op > self.MOV_OP_BEFORE_2AM):
            self.two_am = True

        if (self.current_mov_op > self.MOV_OP_BEFORE_3AM):
            self.three_am = True

        if (self.current_mov_op > self.MOV_OP_BEFORE_4AM):
            self.four_am = True

    def update(self):
        self.update_ai()
        self.update_movement()
        self.check_at_door()
        self.current_mov_op += 1

    def simulate(self):
        while (self.current_mov_op <= self.TOTAL_MOV_OP):
            self.update()
        return [self.bonnie_at_door, self.chica_at_door]