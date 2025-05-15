import streamlit as st
import random

# Initialize session state
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "attempt" not in st.session_state:
    st.session_state.attempt = 0
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "show_solution" not in st.session_state:
    st.session_state.show_solution = False
if "question" not in st.session_state:
    st.session_state.question = None
if "go_next" not in st.session_state:
    st.session_state.go_next = False

# Handle navigation logic without rerun error
if st.session_state.go_next:
    st.session_state.current_q += 1
    st.session_state.attempt = 0
    st.session_state.selected_option = None
    st.session_state.show_solution = False
    st.session_state.go_next = False
    if st.session_state.current_q < 3:
        st.session_state.question = None

# Generate distractors
def generate_distractors(correct, rounding=False):
    distractors = set()
    while len(distractors) < 4:
        offset = random.choice([-20, -10, 10, 20]) if rounding else random.randint(-10, 10)
        option = correct + offset
        if option != correct and option > 0:
            distractors.add(option)
    return list(distractors)

# Define fixed questions
def generate_add_three_numbers():
    nums = [random.randint(10, 20) for _ in range(3)]
    correct_answer = sum(nums)
    distractors = generate_distractors(correct_answer)
    hint = "Add the first two numbers, then the third."
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
    hint = "Check the ones digit. If it's 5 or more, round up."
    solution = f"{num} rounds to {rounded} because the ones digit is {num % 10}."
    return {
        "stem": f"Round {num} to the nearest ten.",
        "options": distractors + [rounded],
        "correct": rounded,
        "hint": hint,
        "solution": solution
    }

# Get question based on index
def get_question_by_index(index):
    if index == 0:
        return generate_add_three_numbers()
    elif index == 1:
        return generate_multiplication_question()
    elif index == 2:
        return generate_rounding_question()

# Load current question
if st.session_state.current_q < 3:
    if not st.session_state.question:
        st.session_state.question = get_question_by_index(st.session_state.current_q)
        random.shuffle(st.session_state.question["options"])

    q = st.session_state.question

    st.title("🎯 Math Mania - 3 Question Quiz")
    st.subheader(f"Question {st.session_state.current_q + 1} of 3")
    st.write(q["stem"])

    selected = st.radio("Choose your answer:", q["options"], index=None, key=f"q_{st.session_state.current_q}")

    if st.button("✅ Submit Answer"):
        st.session_state.selected_option = selected
        if selected == q["correct"]:
            st.success("Correct! 🎉")
            st.session_state.show_solution = False
        else:
            st.session_state.attempt += 1
            if st.session_state.attempt == 1:
                st.warning("Oops! Try again 💡")
                st.info("Hint: " + q["hint"])
            else:
                st.error("Incorrect again ❌")
                st.session_state.show_solution = True

    if st.session_state.selected_option == q["correct"]:
        if st.button("➡️ Next"):
            st.session_state.go_next = True
            st.experimental_rerun()

    if st.session_state.show_solution:
        with st.expander("📘 Step-by-Step Solution"):
            st.markdown(q["solution"], unsafe_allow_html=True)
        if st.button("➡️ Next Question"):
            st.session_state.go_next = True
            st.experimental_rerun()

else:
    st.title("🎉 You've completed all 3 questions!")
    st.balloons()
    st.success("Great job! You’ve reached the end of this Math Mania session.")
