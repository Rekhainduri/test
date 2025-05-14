import random
import streamlit as st

# -----------------------------
# Question Generators
# -----------------------------
def generate_addition_question():
    numbers = [random.randint(10, 20) for _ in range(3)]
    correct_answer = sum(numbers)
    distractors = generate_distractors(correct_answer)

    return {
        "type": "Addition",
        "question": f"What is {numbers[0]} + {numbers[1]} + {numbers[2]}?",
        "correct_answer": correct_answer,
        "distractors": distractors,
        "hint": "First, add the first two numbers together, then add the third number.",
        "solution": (
            f"Step 1: {numbers[0]} + {numbers[1]} = {numbers[0] + numbers[1]}\n"
            f"Step 2: {numbers[0] + numbers[1]} + {numbers[2]} = {correct_answer}\n"
            f"Answer: {correct_answer}"
        )
    }

def generate_multiplication_question():
    multiplier = random.choice([3, 6])
    number = random.randint(2, 12)
    correct_answer = number * multiplier
    distractors = generate_distractors(correct_answer)

    return {
        "type": "Multiplication",
        "question": f"What is {number} × {multiplier}?",
        "correct_answer": correct_answer,
        "distractors": distractors,
        "hint": f"Think about {multiplier} groups of {number}.",
        "solution": (
            f"Step 1: Multiply {number} × {multiplier} = {correct_answer}\n"
            f"Answer: {correct_answer}"
        )
    }

def generate_rounding_question():
    number = random.randint(21, 99)
    correct_answer = round(number / 10) * 10
    distractors = generate_distractors(correct_answer, rounding=True)

    return {
        "type": "Rounding",
        "question": f"Round {number} to the nearest 10.",
        "correct_answer": correct_answer,
        "distractors": distractors,
        "hint": "Look at the ones place. If it's 5 or more, round up; else, round down.",
        "solution": (
            f"Step 1: Ones digit of {number} is {number % 10}\n"
            f"Step 2: Round to {correct_answer}\n"
            f"Answer: {correct_answer}"
        )
    }

# -----------------------------
# Distractor Generator
# -----------------------------
def generate_distractors(correct_answer, rounding=False):
    distractors = set()
    attempts = 0
    while len(distractors) < 4 and attempts < 100:
        offset = random.choice([-15, -10, -5, 5, 10, 15])
        candidate = correct_answer + offset
        if rounding:
            candidate = round(candidate / 10) * 10
        if candidate != correct_answer:
            distractors.add(candidate)
        attempts += 1
    return list(distractors)

# -----------------------------
# Streamlit UI Logic
# -----------------------------
def ask_question(question_data, question_key):
    st.subheader(f"📘 {question_data['question']}")
    
    options = question_data["distractors"] + [question_data["correct_answer"]]
    random.shuffle(options)

    lettered_options = {chr(65 + i): option for i, option in enumerate(options)}
    selected = st.radio("Choose your answer:", list(lettered_options.keys()), key=f"{question_key}_choice")

    if st.button("Submit", key=f"{question_key}_submit"):
        chosen_value = lettered_options[selected]
        if chosen_value == question_data["correct_answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Hint: {question_data['hint']}")
            if st.button("Show Solution", key=f"{question_key}_solution"):
                st.info(f"➡ Solution:\n{question_data['solution']}")

# -----------------------------
# Main Streamlit App
# -----------------------------
def main():
    st.title("🧠 Interactive Math Quiz")
    st.write("Answer the following questions:")

    question_generators = [
        generate_addition_question,
        generate_multiplication_question,
        generate_rounding_question
    ]

    for i, generate in enumerate(question_generators):
        q_data = generate()
        ask_question(q_data, f"q{i}")

if __name__ == "__main__":
    main()
