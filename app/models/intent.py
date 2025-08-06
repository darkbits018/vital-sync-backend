# models/intent.py

from enum import Enum

class IntentType(str, Enum):
    LOG_MEAL = "log_meal"
    LOG_WORKOUT = "log_workout"
    ADD_MEDICINE = "add_medicine"
    UPDATE_PREFERENCE = "update_preference"
    ASK_NUTRITION = "ask_nutrition"
    ASK_FITNESS = "ask_fitness"
    GENERAL_CHAT = "general_chat"