import random

from core.elements.dormitory import Dormitory
from core.elements.student import Student, StudentState

class StateProcessor:
    def __init__(self, dormitory: Dormitory):
        self.dormitory = dormitory
        self.exam_difficulty = max(0.5, min(1.5, random.gauss(1, 0.4)))

    def setup_new_exam(self):
        self.exam_difficulty = max(0.5, min(1.5, random.gauss(1, 0.4)))

    def iterate(self, is_exam_season: bool):
        for floor in self.dormitory.floors:
            for student in floor.students:
                self.adjust_rates(student)
                self.process_state(student)
                if is_exam_season:
                    student.knowledge -= (1 / 24) / 2  * self.exam_difficulty # 50% knowledge modified by exam difficulty required to survive
                    if student.knowledge < 0:
                        floor.students.remove(student) # Goodbye cruel world
                student.validate_values()

    #Modifies knowledge, energy, state
    def process_state(self, student: Student):
        if student.state == StudentState.RESTING:
            self.process_resting_state(student)
        elif student.state == StudentState.PARTYING:
            self.process_partying_state(student)
        elif student.state == StudentState.LEARNING:
            self.process_learning_state(student)
        else:
            raise Exception("Student state not recognized")
        

    def process_resting_state(self, student: Student):
        student.energy += 0.1 + 0.1 * student.resting_rate
        
        if student.energy > 0.5:
            dice = random.random()
            
            if dice < 0.1 * student.eagerness_to_party:
                student.state = StudentState.PARTYING
            elif dice < student.energy:
                student.state = StudentState.LEARNING

    def process_partying_state(self, student: Student):
        student.energy -= 0.15 + 0.1 * student.stamina_rate
        
        dice = random.random()
        if student.energy < 0.35 and dice > 0.3 * student.eagerness_to_party + student.energy:
            student.state = StudentState.RESTING
        

    def process_learning_state(self, student: Student):
        student.knowledge += 0.01 + 0.01 * student.learning_rate
        student.energy -= 0.15 + 0.1 * student.stamina_rate

        dice = random.random()
        if student.energy < 0.5 and dice < 1 - student.energy:
            student.state = StudentState.RESTING
        elif dice < student.eagerness_to_party * 0.5:
            student.state = StudentState.PARTYING

    #Modifies rates
    def adjust_rates(self, student: Student):
        if student.state == StudentState.RESTING:
            student.learning_rate += 0.075 + 0.1 * student.base_resting_rate
            student.stamina_rate += 0.075 + 0.1 * student.base_stamina_rate
        elif student.state == StudentState.PARTYING:
            student.learning_rate -= 0.1 + 0.075 * student.base_resting_rate
        elif student.state == StudentState.LEARNING:
            student.learning_rate -= 0.1 + 0.075 * student.base_resting_rate
            student.stamina_rate -= 0.1 + 0.075 * student.base_stamina_rate
        else:
            raise Exception("Student state not recognized")