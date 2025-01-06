EXAM_SD = 0.5       # Standard deviation of the exam difficulty. Difficulty is limited to [0.5, 1.5]


### STATE CONFIGURATION
# Resting state
REST_BASE_GAIN = 0.075     # Base energy gain from resting (each hour)
REST_BONUS_GAIN = 0.15    # Bonus energy gain from resting based on student's properties
REST_FUN_LOSS_RATE = 0.04      # Fun loss rate while resting

# Partying state
PARTY_ENERGY_BASE_LOSS = 0.25   # Energy loss rate while partying
PARTY_STAMINA_BASE_GAIN = 0.15        # energy saved while partying, based on stamina rate

PARTY_FUN_BASE_GAIN = 0.1       # Base fun gain from partying
PARTY_FUN_GAIN_PENALTY = 0.05    # Lowered fun gain for student that are hungry for partying

PARTY_ENERGY_THRESHOLD = 0.4       # Below this value it's possible to go rest
KEEP_PARTYING_BASE = 0.25        # Multiplier for the probability of keeping to party below energy threshold

# Learning state
LEARN_BASE = 0.04   # Base knowledge gain from learning
LEARN_BONUS = 0.08  # Bonus knowledge gain from learning based on student's properties

LEARN_ENERGY_BASE_LOSS = 0.1   # Energy loss rate while learning
LEARN_STAMINA_BASE_GAIN = 0.1        # Energy saved while learning, based on stamina rate

LEARN_FUN_BASE_LOSS = 0.1       # Fun loss rate while learning

### RATE MODIFIERS
# Resting state
LEARN_RATE_GAIN_REST_BASE = 0.05
LEARN_RATE_GAIN_REST_BONUS = 0.15

REST_RATE_GAIN_REST_BASE = 0.05
REST_RATE_GAIN_REST_BONUS = 0.15

# Party state
LEARN_RATE_LOSS_PARTY_BASE = 0.1

# Learning state
LEARN_RATE_LOSS_LEARN_BASE = 0.1
LEARN_RATE_LOSS_LEARN_BONUS = 0.075

EAGERNESS_TO_PARTY_LEARN_GAIN = 0.15

### NEIGHBOURS EFFECTS
NEIGHBOUR_PARTYING_PARTY_EAGERNESS_GAIN = 0.02
NEIGHBOUR_PARTYING_LEARN_RATE_LOSS = 0.03
NEIGHBOUR_PARTYING_RESTING_RATE_LOSS = 0.02

### PARTY EFFECTS
PARTY_IN_ROOM_FACTOR = 0.5      # change of rates when party is in the room

FUN_PER_STUDENT_GAIN = 0.04    # Fun gain per student in the room
REST_PER_STUDENT_LOSS = 0.02   # Energy loss per student in the room

# Party overdose (fainting)
FAINT_KNOWLEDGE_LOSS = 0.5             # Percentage of knowledge lost after fainting

