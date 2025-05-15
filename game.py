import streamlit as st
import random

# Initialize session state
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "attempt" not in st.session_state:
    st.session_state.attempt = 0
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "question_bank" not in st.session_state:
    st.session_state.question_bank = []

# Generate distractors
def generate_distractors(correct, rounding=False):
    distractors = set()
    while len(distractors) < 4:
        if rounding:
            offset = random.choice([-20, -10, 10, 20])
        else:
            offset = random.randint(-10, 10)
        option = correct + offset
        if option != correct and option > 0:
            distractors.add(option)
    return list(distractors)

# Question generators
def generate_add_three_numbers():
    nums = [random.randint(10, 20) for _ in range(3)]
    correct_answer = sum(nums)
    distractors = generate_distractors(correct_answer)
    hint = "Add the first two numbers, then add the third."
    solution = (
        f"Step 1: {nums[0]} + {nums[1]} = {nums[0] + nums[1]}\n"
        f"Step 2: {nums[0] + nums[1]} + {nums[2]} = {correct_answer}"
    )
    return {
        "stem": f"What is {nums[0]} + {nums[1]} + {nums[2]}?",
        "options": distractors + [correct_answer],
        "correct": correct_answer,
        "hint": hint,
        "solution": solution,
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
        "solution": solution,
    }

def generate_rounding_question():
    num = random.randint(51, 149)
    rounded = round(num / 10) * 10
    distractors = generate_distractors(rounded, rounding=True)
    hint = "If the digit in the ones place is 5 or more, round up."
    solution = f"{num} rounds to {rounded} because the ones digit is {num % 10}."
    return {
        "stem": f"Round {num} to the nearest ten.",
        "options": distractors + [rounded],
        "correct": rounded,
        "hint": hint,
        "solution": solution,
    }

# Load question bank once
if not st.session_state.question_bank:
    st.session_state.question_bank.append(generate_add_three_numbers())
    st.session_state.question_bank.append(generate_multiplication_question())
    st.session_state.question_bank.append(generate_rounding_question())

# Display current question
if st.session_state.current_q < 3:
    q = st.session_state.question_bank[st.session_state.current_q]
    if "shuffled_options" not in q:
        q["shuffled_options"] = q["options"].copy()
        random.shuffle(q["shuffled_options"])

    st.title("🧠 Math Mania")
    st.subheader(f"Question {st.session_state.current_q + 1} of 3")
    st.write(q["stem"])

    selected = st.radio("Choose your answer:", q["shuffled_options"], key=f"q_{st.session_state.current_q}")

    if st.button("✅ Submit Answer"):
        st.session_state.selected_option = selected
        if selected == q["correct"]:
            st.success("Correct! 🎉")
        else:
            st.session_state.attempt += 1
            if st.session_state.attempt == 1:
                st.warning("Incorrect. Here's a hint:")
                st.info(q["hint"])

    # Logic for next steps after answer submission
    if st.session_state.selected_option == q["correct"]:
        # Correct answer path
        st.success("Correct! 🎉")
        if st.button("➡️ Next Question"):
            st.session_state.current_q += 1
            st.session_state.attempt = 0
            st.session_state.selected_option = None
            st.query_params.clear()

    elif st.session_state.attempt >= 2:
        # After two wrong attempts show solution automatically
        st.error("Incorrect again. Here's the solution:")
        with st.expander("📘 Step-by-Step Solution", expanded=True):
            st.markdown(q["solution"])
        if st.button("➡️ Next Question"):
            st.session_state.current_q += 1
            st.session_state.attempt = 0
            st.session_state.selected_option = None
            st.query_params.clear()

else:
    st.title("🎉 You've completed all 3 questions!")
    st.success("Great work! You finished Math Mania.")
    st.balloons()
