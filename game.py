import streamlit as st

st.set_page_config(page_title="🧠 Math Mania", page_icon="🧠")

questions = [
    {
        "question": "Add these three numbers: 12 + 15 + 18",
        "options": [45, 43, 44, 46, 42],
        "correct": 45,
        "hint": "Try adding two numbers first, then add the third number.",
        "solution": """
Let's add step by step:

1️⃣ Add 12 and 15: 12 + 15 = 27

2️⃣ Now add 18 to 27: 27 + 18 = 45

So, the answer is 45.
"""
    },
    {
        "question": "What is 2 × 6?",
        "options": [9, 13, 22, 12, 7],
        "correct": 12,
        "hint": "Multiplying means adding the same number multiple times. Think of 2 groups of 6 or 6 groups of 2.",
        "solution": """
Let's multiply step by step:

1️⃣ Multiply 2 by 6: 2 × 6 = 12

So, the answer is 12.
"""
    },
    {
        "question": "Round 74 to the nearest 10.",
        "options": [70, 80, 75, 65, 60],
        "correct": 70,
        "hint": "Look at the ones digit. If it is 5 or more, round up. Otherwise, round down.",
        "solution": """
Let's round step by step:

1️⃣ Look at the ones digit in 74, which is 4.

2️⃣ Since 4 is less than 5, we round down.

3️⃣ So, 74 rounded to the nearest 10 is 70.
"""
    }
]

def main():
    st.title("🧠 Math Mania")

    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "attempt" not in st.session_state:
        st.session_state.attempt = 0
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None

    total_q = len(questions)

    if st.session_state.current_q < total_q:
        q = questions[st.session_state.current_q]

        st.write(f"Question {st.session_state.current_q + 1} of {total_q}")
        st.write(q["question"])

        st.session_state.selected_option = st.radio(
            "Choose your answer:", q["options"], key="answer_radio"
        )

        if st.button("Submit Answer"):
            st.session_state.attempt += 1

            if st.session_state.selected_option == q["correct"]:
                st.success("Correct! 🎉")
                st.session_state.attempt = 0  # reset attempts

                if st.button("➡️ Next Question"):
                    st.session_state.current_q += 1
                    st.session_state.selected_option = None
                    st.experimental_rerun()

            else:
                if st.session_state.attempt == 1:
                    st.warning(f"Oops! That's not right. Hint: {q['hint']}")
                elif st.session_state.attempt == 2:
                    st.error("Let's go through the steps to find the answer:")
                    with st.expander("📘 Step-by-Step Solution", expanded=True):
                        st.markdown(q["solution"])
                    if st.button("➡️ Next Question"):
                        st.session_state.current_q += 1
                        st.session_state.attempt = 0
                        st.session_state.selected_option = None
                        st.experimental_rerun()

    else:
        st.balloons()
        st.success("🎉 Congratulations! You completed all questions!")

        if st.button("Restart Quiz"):
            st.session_state.current_q = 0
            st.session_state.attempt = 0
            st.session_state.selected_option = None
            st.experimental_rerun()


if __name__ == "__main__":
    main()
