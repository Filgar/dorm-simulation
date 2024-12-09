import random

from core.elements.dormitory import Dormitory
from core.elements.student import Student, StudentState
import logic_config as lc

class StateProcessor:
    def __init__(self, dormitory: Dormitory):
        self.dormitory = dormitory
        self.exam_difficulty = max(0.5, min(1.5, random.gauss(1, lc.EXAM_SD)))

    def setup_new_exam(self):
        self.exam_difficulty = max(0.5, min(1.5, random.gauss(1, lc.EXAM_SD)))

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
            student.time_resting += 1
            self.process_resting_state(student)
        elif student.state == StudentState.PARTYING:
            student.time_partying += 1
            self.process_partying_state(student)
        elif student.state == StudentState.LEARNING:
            student.time_learning += 1
            self.process_learning_state(student)
        else:
            raise Exception("Student state not recognized")
        

    def process_resting_state(self, student: Student):
        student.energy += lc.REST_BASE + lc.REST_BONUS * student.resting_rate
        
        if student.energy > 0.5:
            dice = random.random()
            
            if dice < lc.PARTY_AFTER_REST * student.eagerness_to_party:
                student.state = StudentState.PARTYING
            elif dice < student.energy:
                student.state = StudentState.LEARNING

    def process_partying_state(self, student: Student):
        student.energy -= lc.PARTY_ENERGY_LOSS_RATE + lc.PARTY_STAMINA_BASE * student.stamina_rate
        
        dice = random.random()
        if student.energy < lc.PARTY_ENERGY_THRESHOLD and dice > lc.KEEP_PARTYING_BASE * student.eagerness_to_party + student.energy:
            student.state = StudentState.RESTING
        

    def process_learning_state(self, student: Student):
        student.knowledge += lc.LEARN_BASE + lc.LEARN_BONUS * student.learning_rate
        student.energy -= lc.LEARN_ENERGY_LOSS_RATE + lc.LEARN_STAMINA_BASE * student.stamina_rate

        dice = random.random()
        if student.energy < 0.5 and dice < 1 - student.energy:
            student.state = StudentState.RESTING
        elif dice < student.eagerness_to_party * lc.PARTY_AFTER_LEARN:
            student.state = StudentState.PARTYING

    #Modifies rates
    def adjust_rates(self, student: Student):
        if student.state == StudentState.RESTING:
            student.learning_rate += lc.LEARN_RATE_GAIN_REST_BASE + lc.LEARN_RATE_GAIN_REST_BONUS * student.base_resting_rate
            student.stamina_rate += lc.STAMINA_RATE_GAIN_REST + lc.STAMINA_RATE_GAIN_REST_BONUS * student.base_stamina_rate
        elif student.state == StudentState.PARTYING:
            student.learning_rate += lc.LEARN_RATE_GAIN_PARTY_BASE
        elif student.state == StudentState.LEARNING:
            student.learning_rate -= lc.LEARN_RATE_LOSS_LEARN_BASE + lc.LEARN_RATE_LOSS_LEARN_BONUS * student.base_resting_rate
            student.stamina_rate -= lc.STAMINA_RATE_LOSS_LEARN_BASE + lc.STAMINA_RATE_LOSS_LEARN_BONUS * student.base_stamina_rate
        else:
            raise Exception("Student state not recognized")