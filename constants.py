SI_RATE = 0.4 # Default 0.4 = 40% chance of infection when interacting with infected individual (holy alliteration)
IR_RATE = 0.071 # Default 0.071 = 14 days
POPULATION = 80000
INITIAL_INFECTED = 100

### Network (NOT ACTIVE YET) ###
LOGN_STDEV = 0.655
LOGN_MU = 1.386 + LOGN_STDEV ** 2 # 1.386 is ln(4) for 4 people, asked ai how this is derived