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
                self.process_state(student, floor)

                if is_exam_season:
                    student.knowledge -= (1 / 24) / 2  * self.exam_difficulty # 50% knowledge modified by exam difficulty required to survive
                    if student.knowledge < 0:
                        student.dropout = True # Goodbye cruel world
                student.validate_values()

    #Modifies knowledge, energy, fun, state
    def process_state(self, student: Student, floor: Floor):
        if student.state == StudentState.RESTING:
            student.time_resting += 1
            state = self.process_resting_state(student)
        elif student.state == StudentState.PARTYING:
            student.time_partying += 1
            party_size = floor.room_partying_count(student.current_room)
            state = self.process_partying_state(student, party_size)
        elif student.state == StudentState.LEARNING:
            student.time_learning += 1
            state = self.process_learning_state(student)
        else:
            raise Exception("Student state not recognized")
        if (state is not None):
            self.switch_student_state(student, state, floor)
        

    def process_resting_state(self, student: Student) -> StudentState:
        student.energy += lc.REST_BASE_GAIN + lc.REST_BONUS_GAIN * student.resting_rate
        student.fun -= lc.REST_FUN_LOSS_RATE
        
        if student.energy > 0.75:
            dice = random.random()
            if dice < student.energy * ((1 - student.fun) / 10 + student.eagerness_to_party / 4):
                student.partied_recently = True
                return StudentState.PARTYING
            elif dice < student.energy:
                student.partied_recently = False
                return StudentState.LEARNING
        return None

    def process_partying_state(self, student: Student, party_size: int) -> StudentState:
        student.energy -= lc.PARTY_ENERGY_BASE_LOSS - lc.PARTY_STAMINA_BASE_GAIN * student.stamina_rate + party_size * lc.REST_PER_STUDENT_LOSS
        student.fun += lc.PARTY_FUN_BASE_GAIN - lc.PARTY_FUN_GAIN_PENALTY * student.eagerness_to_party + party_size * lc.FUN_PER_STUDENT_GAIN
        
        dice = random.random()
        if student.energy < lc.PARTY_ENERGY_THRESHOLD and dice > lc.KEEP_PARTYING_BASE * student.energy + student.energy:
            if student.energy <= 0:
                student.party_overdose += 1
                student.learning_rate = 0.05
                student.knowledge *= (1 - lc.PARTY_OVERDOSE_KNOWLEDGE_LOSS)
            student.eagerness_to_party = student.eagerness_to_party_base
            return StudentState.RESTING
        
        return None

        

    def process_learning_state(self, student: Student):
        student.knowledge += (lc.LEARN_BASE + lc.LEARN_BONUS * student.learning_rate) * student.fun
        student.energy -= lc.LEARN_ENERGY_BASE_LOSS + lc.LEARN_STAMINA_BASE * student.stamina_rate
        student.fun -= lc.LEARN_FUN_BASE_LOSS

        dice = random.random()
        if student.energy < 0.5 and dice < 1 - student.energy:
            return StudentState.RESTING
        elif dice < (1 - student.fun) + student.eagerness_to_party / 6:
            student.partied_recently = True
            return StudentState.PARTYING

        return None


    #Modifies rates
    def adjust_rates(self, student: Student, floor: Floor):
        self.apply_party_effects(student, floor)
        
        if student.state == StudentState.RESTING:
            self.apply_neighbours_effects(student, floor)
            student.learning_rate += lc.LEARN_RATE_GAIN_REST_BASE + lc.LEARN_RATE_GAIN_REST_BONUS * student.base_resting_rate
        elif student.state == StudentState.PARTYING:
            student.learning_rate -= lc.LEARN_RATE_LOSS_PARTY_BASE
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
        student.validate_rates()

    def apply_party_effects(self, student: Student, floor: Floor):
        if not floor.room_is_partying(student.current_room) and not student.partied_recently:
            student.eagerness_to_party = max(student.eagerness_to_party, student.eagerness_to_party_base * 0.75)
            student.learning_rate = max(student.learning_rate, student.base_learning_rate * 0.75)
            student.resting_rate = max(student.resting_rate, student.base_resting_rate* 0.75)
            return

        student.eagerness_to_party += student.eagerness_to_party * lc.PARTY_IN_ROOM_FACTOR
        student.learning_rate -= student.learning_rate * lc.PARTY_IN_ROOM_FACTOR
        student.resting_rate -= student.resting_rate * lc.PARTY_IN_ROOM_FACTOR
        student.validate_rates()

    def switch_student_state(self, student: Student, new_state: StudentState, floor: Floor):
        student.state = new_state
        if new_state == StudentState.RESTING:
            student.travel_to_room(student.native_room)
        elif new_state == StudentState.PARTYING:
            room = floor.find_partying_place()
            if room is not None:
                student.travel_to_room(room)
        elif new_state == StudentState.LEARNING:
            student.travel_to_room(student.native_room)
        else:
            raise Exception("Student state not recognized")