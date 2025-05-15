import streamlit as st
import random

# Session state initialization
if "question" not in st.session_state:
    st.session_state.question = None
if "attempt" not in st.session_state:
    st.session_state.attempt = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "show_solution" not in st.session_state:
    st.session_state.show_solution = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# ----------------------------- #
# Question Generators
# ----------------------------- #
def generate_add_three_numbers():
    nums = [random.randint(10, 20) for _ in range(3)]
    correct_answer = sum(nums)
    distractors = generate_distractors(correct_answer)
    hint = f"Add the first two numbers, then add the third one."
    solution = f"Step 1: {nums[0]} + {nums[1]} = {nums[0] + nums[1]}<br>" \
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
    hint = f"Multiply {base} by {multiplier}."
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
    hint = "Look at the ones digit. If it's 5 or more, round up."
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
        offset = random.choice([-20, -10, 10, 20]) if rounding else random.randint(-10, 10)
        option = correct + offset
        if option != correct and option > 0:
            distractors.add(option)
    return list(distractors)

# ----------------------------- #
# UI and Logic
# ----------------------------- #
st.title("🎯 Math Mania Quiz")
question_type = st.selectbox("Choose a question type", [
    "Add Three Numbers (10–20)",
    "Multiply by 3 or 6",
    "Round to Nearest 10"
])

def generate_new_question():
    st.session_state.attempt = 0
    st.session_state.feedback = ""
    st.session_state.show_solution = False
    st.session_state.selected_option = None
    if question_type == "Add Three Numbers (10–20)":
        st.session_state.question = generate_add_three_numbers()
    elif question_type == "Multiply by 3 or 6":
        st.session_state.question = generate_multiplication_question()
    elif question_type == "Round to Nearest 10":
        st.session_state.question = generate_rounding_question()
    random.shuffle(st.session_state.question["options"])

if st.button("🔁 Start New Question"):
    generate_new_question()

if st.session_state.question:
    q = st.session_state.question
    st.subheader("🧮 Question")
    st.write(q["stem"])
    
    # Option select
    selected = st.radio("Choose your answer:", q["options"], index=None)

    if st.button("✅ Submit Answer"):
        st.session_state.selected_option = selected
        if selected == q["correct"]:
            st.success("Correct! 🎉")
            st.session_state.feedback = ""
            st.session_state.show_solution = False
        else:
            st.session_state.attempt += 1
            if st.session_state.attempt == 1:
                st.warning("Oops! Try again 💡")
                st.info("Hint: " + q["hint"])
            else:
                st.error("Incorrect again ❌")
                st.session_state.show_solution = True

    # Solution display after second attempt
    if st.session_state.show_solution:
        with st.expander("📘 Step-by-Step Solution"):
            st.markdown(q["solution"], unsafe_allow_html=True)

    # Show next question button
    if st.session_state.selected_option == q["correct"] or st.session_state.show_solution:
        if st.button("➡️ Next Question"):
            generate_new_question()
