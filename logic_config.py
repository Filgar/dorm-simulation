EXAM_SD = 0.5       # Standard deviation of the exam difficulty. Difficulty is limited to [0.5, 1.5]


### STATE CONFIGURATION
# Resting state
REST_BASE = 0.1     # Base energy gain from resting (each hour)
REST_BONUS = 0.1    # Bonus energy gain from resting based on student's properties

PARTY_AFTER_REST = 0.1  # Probability base of partying right after resting

# Partying state
PARTY_ENERGY_LOSS_RATE = 0.15   # Energy loss rate while partying
PARTY_STAMINA_BASE = 0.1        # energy saved while partying, based on stamina rate

PARTY_ENERGY_THRESHOLD = 0.35       # Below this value it's possible to go rest
KEEP_PARTYING_BASE = 0.3        # Multiplier for the probability of keeping to party below energy threshold

# Learning state
LEARN_BASE = 0.01   # Base knowledge gain from learning
LEARN_BONUS = 0.01  # Bonus knowledge gain from learning based on student's properties

LEARN_ENERGY_LOSS_RATE = 0.15   # Energy loss rate while learning
LEARN_STAMINA_BASE = 0.1        # Energy saved while learning, based on stamina rate

PARTY_AFTER_LEARN = 0.5  # Modifier for the probability of partying after learning


### RATE MODIFIERS
# Resting state
LEARN_RATE_GAIN_REST_BASE = 0.075
LEARN_RATE_GAIN_REST_BONUS = 0.1
STAMINA_RATE_GAIN_REST = 0.075
STAMINA_RATE_GAIN_REST_BONUS = 0.1

# Party state
LEARN_RATE_GAIN_PARTY_BASE = 0.1

# Learning state
LEARN_RATE_LOSS_LEARN_BASE = 0.1
LEARN_RATE_LOSS_LEARN_BONUS = 0.075

STAMINA_RATE_LOSS_LEARN_BASE = 0.1
STAMINA_RATE_LOSS_LEARN_BONUS = 0.075
