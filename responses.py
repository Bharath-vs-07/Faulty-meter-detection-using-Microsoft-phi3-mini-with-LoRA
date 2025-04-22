import random
import re
from datetime import datetime

# Updated list of bad words and deviations
deviation_keywords = ["joke", "fun", "random", "off-topic", "chat"]  # Adjust based on context

def is_deviation(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in deviation_keywords)

def extract_problem_details(user_input):
    problem_keywords = [
        "timestamp", "meter tampering", "meter bypass", "incorrect calibration", "firmware manipulation", "magnetic interference", "bypass of meter", "reverse metering", "daily consumption", "peak load", "baseline consumption", 
        "seasonal trends", "autocorrelation", "moving average", 
        "meter readings", "billed consumption", "weather conditions", 
        "spike detection", "zero consumption", "negative readings", 
        "voltage", "current", "power factor", "customer classification", 
        "tamper alert", "outlier score", "customer profile", 
        "contractual demand", "label classification", "consumption anomalies", 
        "electric meter tampering", "tampering", "report tampering", 
        "unusual consumption", "utility company detection", "consequences of tampering"
    ]
    for keyword in problem_keywords:
        if keyword in user_input.lower():
            return keyword
    return None

def get_time_of_day():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Morning"
    elif 12 <= current_hour < 18:
        return "Afternoon"
    else:
        return "Evening"

def handle_how_are_you(user_input):
    if "how are you" in user_input:
        responses = [
            "I'm just a bot, thanks for your concern! How are you doing today?",
            "I'm fine and here to assist you with anything you need! How about you?",
            "Doing great, thanks for asking! How can I help you today?",
            "Thanks for your kindness, I'm ready to assist you! How's everything on your end?",
            "I'm good and ready to help! How are you doing?",
            "I'm functioning optimally, thanks! How can I be of service today?",
            "I'm operating smoothly, thank you! How can I assist you?"
        ]
        return random.choice(responses)
    return None

def respond_to_user_feelings(user_input):
    user_input = user_input.lower()
    if "i am fine" in user_input or "i'm fine" in user_input:
        responses = [
            "I'm glad to hear it! How can I assist you further today?",
            "Great to know you're fine! Let me know if you need anything.",
            "Good to hear! What can I help you with next?",
            "Happy to hear you're fine! Is there anything else you need?",
            "Awesome! How can I be of help today?"
        ]
        return random.choice(responses)
    elif "i am not fine" in user_input or "i'm not fine" in user_input:
        responses = [
            "I'm sorry to hear that. How can I assist you or make things better?",
            "I'm here to help. Can you tell me more about what's troubling you?",
            "I'm sorry you're not feeling well. What can I do to assist you?",
            "Let me know how I can support you during this time.",
            "I'm here for you. How can I help to improve the situation?"
        ]
        return random.choice(responses)
    return None

def handle_thanks(user_input):
    responses = [
        "You're welcome! If you have any more questions, just let me know.",
        "No problem! I'm here to help with anything you need.",
        "You're welcome! Feel free to ask if you need further assistance.",
        "Glad I could help! Don't hesitate to reach out if you have more questions.",
        "You're welcome! Let me know if there's anything else I can do for you."
    ]
    return random.choice(responses)

def handle_understanding(user_input):
    responses = [
        "Great! If you have any more questions or need further clarification, feel free to ask.",
        "Understood! I'm here if you need any more information or help.",
        "Got it! If there's anything else you need, just let me know.",
        "Glad to hear you understand. If you need any more assistance, I'm here to help.",
        "Perfect! Let me know if you need anything else."
    ]
    return random.choice(responses)

def handle_sorry_i_couldnt_understand(user_input):
    responses = [
        "I'm sorry, I couldn't quite understand that. Could you please clarify?",
        "I didn't quite get that. Can you provide more details or rephrase your question?",
        "My apologies, I didn't understand your message. Could you explain further?",
        "I'm having trouble understanding. Can you please provide more context?",
        "Sorry, I couldn't follow that. Could you please elaborate?"
    ]
    return random.choice(responses)

def prising_responses(user_input):
    responses = [
        "Thank you for your kind words! I'm glad I could help.",
        "I'm flattered! It's my pleasure to assist you.",
        "That means a lot. I'll do my best to continue providing excellent service.",
        "Thank you, but I'm just doing my job.",
        "I'm glad I could be helpful. It's my pleasure to assist you.",
        "I appreciate your feedback. I'm always learning and improving.",
        "Well, that's what they say about me. But don't tell the other chatbots!",
        "Aw shucks, you're making me blush!",
        "I'll take that as a compliment. Now, what can I do for you today?"
    ]
    return random.choice(responses)

def default_responses():
    responses = [
        "Hello there! How can I assist you today?",
        "Hi, human! Is there anything I can help you with?",
        "Do you need help?",
        "How can I assist you?",
        "What can I do for you today?",
        "I'm here to help! What do you need assistance with?"
    ]
    return random.choice(responses)

def generate_response(user_input):
    user_input = user_input.strip().lower()
    
    if any(message in user_input.lower() for message in ["hi","hey","hello","hey there","yo","hey man"]):
        return default_responses()
    
    # elif contains_bad_words(user_input):
    #     return "I notice some inappropriate language. Let's keep our conversation respectful. How can I assist you better?"
    
    elif is_deviation(user_input):
        return "It seems like we're going off-topic. Please let me know how I can assist you with your current issue."
    
    elif (problem_keyword := extract_problem_details(user_input)):
        responses = {
            "meter tampering": "Meter Tampering refers to any unauthorized alteration or interference with an electric meter with the intent to manipulate its readings. This illegal activity can lead to inaccurate billing and has legal repercussions.",
            "meter bypass": "Meter Bypass refers to the illegal practice of redirecting electricity around the meter to avoid accurate measurement. This method results in underreporting of electricity usage, leading to reduced billing.",
            "incorrect calibration": "Incorrect Calibration occurs when a meter's settings are either faulty or deliberately tampered with, causing incorrect readings. This tampering can either overestimate or underestimate the actual electricity consumption.",
            "firmware manipulation": "Firmware Manipulation involves altering the software that controls the electric meter to under-report electricity usage. This practice can reduce the recorded consumption, resulting in lower bills.",
            "magnetic interference": "Magnetic Interference uses magnets to disrupt the operation of the meter, causing it to record inaccurate readings. This tampering technique leads to a reduction in the recorded electricity consumption.",
            "bypass of meter": "Bypass of Meter is the practice of creating a direct path for electricity to bypass the meter altogether. This method is used to steal electricity without it being measured by the meter.",
            "reverse metering": "Reverse Metering involves tampering with the meter to make it run backward, thereby recording negative consumption. This practice reduces the recorded amount of electricity used.",
            "timestamp": "The timestamp indicates the date and time when the data was recorded, allowing you to track your consumption over time.",
            "daily consumption": "Your daily consumption is recorded in kilowatt-hours (kWh) and shows the amount of electricity you used each day.",
            "peak load": "Peak load refers to the maximum electricity consumption recorded during a specific period, helping to identify high usage times.",
            "baseline consumption": "Baseline consumption is the typical level of electricity usage without any spikes or additional demand, serving as a reference for normal behavior.",
            "seasonal trends": "Seasonal trends indicate how different seasons (like summer or winter) impact power consumption patterns due to heating or cooling needs.",
            "autocorrelation": "Autocorrelation measures how the current electricity consumption correlates with its past values, helping to identify patterns over time.",
            "moving average": "A moving average smooths out daily consumption data over a specified time window to identify trends and reduce noise.",
            "meter readings": "Meter readings refer to the actual amount of electricity measured by your meter.",
            "billed consumption": "Billed consumption is the amount of electricity you are charged for, which should match the meter readings unless there are discrepancies.",
            "weather conditions": "Weather conditions, such as temperature, can significantly influence your electricity usage patterns, especially for heating and cooling.",
            "spike detection": "Spike detection identifies sudden increases in power consumption, which may indicate unusual activity or potential tampering.",
            "zero consumption": "Zero consumption periods are times when no electricity usage is recorded, which could indicate a power outage or meter issues.",
            "negative readings": "Negative readings may indicate an error in the meter or data collection process, as they typically should not occur in normal usage.",
            "voltage": "Voltage (V) readings provide insights into the electrical potential, which is essential for calculating overall power consumption.",
            "current": "Current (A) readings indicate the flow of electricity, which, combined with voltage, helps calculate power consumption.",
            "power factor": "The power factor measures how effectively electrical power is being used. A higher factor indicates more efficient usage.",
            "customer classification": "Customer types may include Residential, Commercial, or Industrial, affecting your electricity rates and consumption patterns.",
            "tamper alert": "A tamper alert signals whether tampering with the meter has been detected, which is crucial for preventing fraud.",
            "outlier score": "An outlier score indicates how much a particular observation deviates from the normal consumption pattern, helping to identify anomalies.",
            "customer profile": "Your customer profile describes your typical consumption pattern, such as whether it is consistent or variable.",
            "contractual demand": "Contractual demand is the maximum amount of electricity (in kW) that you have agreed to use, often impacting your billing.",
            "label classification": "Label classifications categorize data points, such as 'Normal', helping to quickly identify the state of your consumption.",
            "consumption anomalies": "The root cause of consumption anomalies may include issues like equipment malfunction, tampering, or changes in usage behavior.",
            "electric meter tampering": "Electric meter tampering refers to any unauthorized alteration or interference with the meter to manipulate readings.",
            "report tampering": "You can report suspected tampering by contacting your utility provider's customer service or using their designated reporting channels.",
            "unusual consumption": "Signs of unusual electricity consumption include sudden spikes, unexplained increases, or irregular patterns compared to historical data.",
            "utility company detection": "The utility company detects tampering through monitoring and analysis of meter readings for inconsistencies or anomalies.",
            "consequences of tampering": "Tampering with an electric meter can result in legal consequences, fines, and potentially being charged for unauthorized electricity use."
        }
        return responses.get(problem_keyword, "I'm not sure about that topic. Could you please provide more details or ask something else?")
    
    elif any(greeting in user_input.lower() for greeting in ["good morning", "good afternoon", "good evening"]):
        time_of_day = get_time_of_day()
        return f"Good {time_of_day}! How can I assist you today?"
    
    elif "how are you" in user_input.lower():
        return handle_how_are_you(user_input.lower())
    
    elif "i am fine" in user_input.lower() or "i'm fine" in user_input.lower():
        return respond_to_user_feelings(user_input.lower())
    
    elif "i am not fine" in user_input.lower() or "i'm not fine" in user_input.lower():
        return respond_to_user_feelings(user_input.lower())
    
    elif any(thanks_phrase in user_input.lower() for thanks_phrase in ["thanks", "thank you", "thank you very much", "thanks a lot","wow","fantastic"]):
        return handle_thanks(user_input)
    
    elif any(understanding_phrase in user_input.lower() for understanding_phrase in ["i understand", "i got it", "understood", "i see", "i see what you mean"]):
        return handle_understanding(user_input)
    
    elif any(sorry_phrase in user_input.lower() for sorry_phrase in ["sorry", "i apologize", "i'm sorry", "sorry i couldn't understand", "i'm sorry i didn't understand","i cant understand","i couldn't understand"]):
        return handle_sorry_i_couldnt_understand(user_input)
    
    elif any(prising_response in user_input.lower() for prising_response in ["top-notch","outstanding","ideal","that's great","best","your the best","your cute","that's cute"]):
        return prising_responses(user_input)
    
    return "I'm not sure how to respond to that. Can you provide more details or ask something else?"

# Example usage
print(generate_response("What is peak load?"))
print(generate_response("Can you tell me how to check my daily consumption in kWh?"))
