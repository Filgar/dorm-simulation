EXAM_SD = 0.5       # Standard deviation of the exam difficulty. Difficulty is limited to [0.5, 1.5]


### STATE CONFIGURATION
# Resting state
REST_BASE_GAIN = 0.1     # Base energy gain from resting (each hour)
REST_BONUS_GAIN = 0.1    # Bonus energy gain from resting based on student's properties
REST_FUN_LOSS_RATE = 0.05      # Fun loss rate while resting

# Partying state
PARTY_ENERGY_BASE_LOSS = 0.15   # Energy loss rate while partying
PARTY_STAMINA_BASE_GAIN = 0.1        # energy saved while partying, based on stamina rate

PARTY_FUN_BASE_GAIN = 0.25       # Base fun gain from partying
PARTY_FUN_GAIN_PENALTY = 0.1    # Lowered fun gain for student that are hungry for partying

PARTY_ENERGY_THRESHOLD = 0.5       # Below this value it's possible to go rest
KEEP_PARTYING_BASE = 0.3        # Multiplier for the probability of keeping to party below energy threshold

# Learning state
LEARN_BASE = 0.01   # Base knowledge gain from learning
LEARN_BONUS = 0.05  # Bonus knowledge gain from learning based on student's properties

LEARN_ENERGY_LOSS_RATE = 0.15   # Energy loss rate while learning
LEARN_STAMINA_BASE = 0.1        # Energy saved while learning, based on stamina rate

LEARN_FUN_BASE_LOSS = 0.15       # Fun loss rate while learning

### RATE MODIFIERS
# Resting state
LEARN_RATE_GAIN_REST_BASE = 0.075
LEARN_RATE_GAIN_REST_BONUS = 0.1

# Party state
LEARN_RATE_GAIN_PARTY_BASE = 0.1

# Learning state
LEARN_RATE_LOSS_LEARN_BASE = 0.1
LEARN_RATE_LOSS_LEARN_BONUS = 0.075


### NEIGHBOURS EFFECTS
NEIGHBOUR_PARTYING_PARTY_EAGERNESS_GAIN = 0.005
NEIGHBOUR_PARTYING_LEARN_RATE_LOSS = 0.01
NEIGHBOUR_PARTYING_RESTING_RATE_LOSS = 0.01

# Party overdose
PARTY_OVERDOSE_KNOWLEDGE_LOSS = 0.1             # Percentage of knowledge lost after party overdose
