#Sakura Hashimoto
import random

COMPLIMENT = [
    "Task done! That's a huge win.",
    "Finished it! Keep that momentum.",
    "Completed! Time for the next level.",
    "Success! You closed that loop.",
    "Nailed it! Nothing stops you now.",
    "Checked off! Move on and build.",
    "Done. Small victory, big impact.",
    "Zero hesitation. Pure execution.",
    "Forward progress confirmed. Great job!",
    "One more down. You're unstoppable.",
    "Your practice is clearly working.",
    "That effort is going to pay off huge.",
    "Well done! You committed and finished.",
    "Excellent focus! Keep that intensity.",
    "That's solid, consistent work.",
    "You're building great habits.",
    "No shortcuts needed. True dedication.",
    "That's the sound of progress!",
    "Your commitment is showing results.",
    "Hard work done right. Fantastic.",
]

def get_random_compliment_quote():
    return random.choice(COMPLIMENT)