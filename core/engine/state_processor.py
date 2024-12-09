import random

from core.elements.dormitory import Dormitory
from core.elements.floor import Floor
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
            for student in floor.get_active_students():
                self.adjust_rates(student, floor)
                self.process_state(student)
                if is_exam_season:
                    student.knowledge -= (1 / 24) / 2  * self.exam_difficulty # 50% knowledge modified by exam difficulty required to survive
                    if student.knowledge < 0:
                        student.dropout = True # Goodbye cruel world
                student.validate_values()

    #Modifies knowledge, energy, fun, state
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
        student.energy += lc.REST_BASE_GAIN + lc.REST_BONUS_GAIN * student.resting_rate
        student.fun -= lc.REST_FUN_LOSS_RATE
        
        if student.energy > 0.5:
            dice = random.random()
            if dice < student.energy * ((1 - student.fun) / 4 + student.eagerness_to_party / 4):
                student.state = StudentState.PARTYING
            elif dice < student.energy:
                student.state = StudentState.LEARNING

    def process_partying_state(self, student: Student):
        student.energy -= lc.PARTY_ENERGY_BASE_LOSS - lc.PARTY_STAMINA_BASE_GAIN * student.stamina_rate
        student.fun += lc.PARTY_FUN_BASE_GAIN - lc.PARTY_FUN_GAIN_PENALTY * student.eagerness_to_party
        
        dice = random.random()
        if student.energy < lc.PARTY_ENERGY_THRESHOLD and dice > lc.KEEP_PARTYING_BASE * student.energy + student.energy:
            if student.energy <= 0:
                student.party_overdose += 1
                student.learning_rate = 0
                student.knowledge *= (1 - lc.PARTY_OVERDOSE_KNOWLEDGE_LOSS)
            student.state = StudentState.RESTING
        

    def process_learning_state(self, student: Student):
        student.knowledge += lc.LEARN_BASE * student.fun + lc.LEARN_BONUS * student.learning_rate
        student.energy -= lc.LEARN_ENERGY_BASE_LOSS + lc.LEARN_STAMINA_BASE * student.stamina_rate
        student.fun -= lc.LEARN_FUN_BASE_LOSS

        dice = random.random()
        if student.energy < 0.5 and dice < 1 - student.energy:
            student.state = StudentState.RESTING
        elif dice < (1 - student.fun) / 4 + student.eagerness_to_party / 4:
            student.state = StudentState.PARTYING

    #Modifies rates
    def adjust_rates(self, student: Student, floor: Floor):
        if student.state == StudentState.RESTING:
            self.apply_neighbours_effects(student, floor)
            student.learning_rate += lc.LEARN_RATE_GAIN_REST_BASE + lc.LEARN_RATE_GAIN_REST_BONUS * student.base_resting_rate
        elif student.state == StudentState.PARTYING:
            student.learning_rate += lc.LEARN_RATE_GAIN_PARTY_BASE
        elif student.state == StudentState.LEARNING:
            self.apply_neighbours_effects(student, floor)
            student.learning_rate -= lc.LEARN_RATE_LOSS_LEARN_BASE + lc.LEARN_RATE_LOSS_LEARN_BONUS * student.base_resting_rate
        else:
            raise Exception("Student state not recognized")
        
    def apply_neighbours_effects(self, student: Student, floor: Floor):
        partying_neighbours = floor.partying_neighbours_count(student.current_room)

        student.eagerness_to_party += lc.NEIGHBOUR_PARTYING_PARTY_EAGERNESS_GAIN * partying_neighbours
        student.learning_rate -= lc.NEIGHBOUR_PARTYING_LEARN_RATE_LOSS * partying_neighbours
        student.resting_rate -= lc.NEIGHBOUR_PARTYING_RESTING_RATE_LOSS * partying_neighbours