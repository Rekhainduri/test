import streamlit as st
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Utility functions
def generate_add_three_numbers():
    nums = [random.randint(10, 20) for _ in range(3)]
    correct_answer = sum(nums)
    distractors = generate_distractors(correct_answer)
    hint = f"Add {nums[0]} + {nums[1]} first, then add {nums[2]}"
    solution = f"Step 1: {nums[0]} + {nums[1]} = {nums[0] + nums[1]}\n" \
               f"Step 2: {nums[0] + nums[1]} + {nums[2]} = {correct_answer}"
    return {
        "stem": f"What is {nums[0]} + {nums[1]} + {nums[2]}?",
        "options": distractors + [correct_answer],
        "correct": correct_answer,
        "hint": hint,
        "solution": solution
    }

def generate_multiplication_question():
    base = random.randint(2, 12)
    multiplier = random.choice([3, 6])
    correct_answer = base * multiplier
    distractors = generate_distractors(correct_answer)
    hint = f"Think of {base} groups of {multiplier}"
    solution = f"{base} × {multiplier} = {correct_answer}"
    return {
        "stem": f"What is {base} × {multiplier}?",
        "options": distractors + [correct_answer],
        "correct": correct_answer,
        "hint": hint,
        "solution": solution
    }

def generate_rounding_question():
    num = random.randint(51, 149)
    rounded = round(num / 10) * 10
    distractors = generate_distractors(rounded, rounding=True)
    hint = "Look at the digit in the ones place. If it's 5 or more, round up."
    solution = f"{num} rounds to {rounded} because the ones digit is {num % 10}."
    return {
        "stem": f"Round {num} to the nearest ten.",
        "options": distractors + [rounded],
        "correct": rounded,
        "hint": hint,
        "solution": solution
    }

def generate_distractors(correct, rounding=False):
    distractors = set()
    while len(distractors) < 4:
        if rounding:
            offset = random.choice([-20, -10, 10, 20])
            option = correct + offset
        else:
            offset = random.randint(-10, 10)
            option = correct + offset
        if option != correct and option >= 0:
            distractors.add(option)
    return list(distractors)

# App layout
st.set_page_config(page_title="Math Mania - Initial Assignment", layout="centered")
st.title("🎯 Math Mania - Initial Assignment Questions")

question_type = st.selectbox("Select Question Type", [
    "Add Three Numbers (10-20)",
    "Multiply by 3 or 6",
    "Round to Nearest 10"
])

if st.button("Generate Question"):
    if question_type == "Add Three Numbers (10-20)":
        q = generate_add_three_numbers()
    elif question_type == "Multiply by 3 or 6":
        q = generate_multiplication_question()
    elif question_type == "Round to Nearest 10":
        q = generate_rounding_question()
    else:
        st.error("Unknown question type.")
        q = None

    if q:
        random.shuffle(q["options"])
        st.subheader("📝 Question:")
        st.write(q["stem"])
        st.radio("Choose your answer:", q["options"], key="options")
        st.info("💡 Hint: " + q["hint"])
        with st.expander("📘 Show Solution"):
            st.markdown(q["solution"])
