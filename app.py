import streamlit as st
import random
import time
import base64

# ===================================
# PAGE CONFIGURATION
# ===================================
st.set_page_config(page_title="AI Study Assistant", page_icon="🎓", layout="wide")

# ===================================
# HEADER
# ===================================
st.markdown("""
    <h1 style='text-align: center; 
               color: #1E90FF; 
               font-size: 50px; 
               font-family: "Trebuchet MS", sans-serif; 
               font-weight: bold; 
               text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>
        🎓 AI Personalized Study Assistant
    </h1>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 2px solid #1E90FF;'>", unsafe_allow_html=True)

# ===================================
# BACKGROUND FUNCTION
# ===================================
def set_bg_local(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background
set_bg_local("C:/AI_Study_Assistant_Web/background.jpg")

# ===================================
# INITIALIZE SESSION STATE
# ===================================
for key in ["quiz_started", "q_index", "score", "questions", "start_time", "end_time"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key in ["q_index", "score"] else None
        if key == "quiz_started":
            st.session_state.quiz_started = False
        if key == "questions":
            st.session_state.questions = []

# ===================================
# QUIZ DATA
# ===================================
quiz_data = {
    "Mathematics": {
        "Easy": [
            {"question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "answer": "12"},
            {"question": "Value of π (pi) approximately?", "options": ["2.12", "3.14", "4.13", "3.33"], "answer": "3.14"},
            {"question": "Square of 9?", "options": ["18", "81", "27", "72"], "answer": "81"},
            {"question": "Derivative of x²?", "options": ["2x", "x", "x²", "x³"], "answer": "2x"},
            {"question": "What is sin(90°)?", "options": ["0", "1", "0.5", "-1"], "answer": "1"},
        ],
        "Medium": [
            {"question": "Integrate x dx", "options": ["x²", "x²/2 + C", "2x + C", "log(x)"], "answer": "x²/2 + C"},
            {"question": "tan(45°) equals?", "options": ["0", "1", "√3", "∞"], "answer": "1"},
            {"question": "If a=3, b=4, find √(a²+b²)", "options": ["5", "6", "7", "4"], "answer": "5"},
            {"question": "Area of circle formula?", "options": ["πr²", "2πr", "r²/π", "π/2r²"], "answer": "πr²"},
            {"question": "Limit of sin(x)/x as x→0?", "options": ["0", "1", "∞", "Undefined"], "answer": "1"},
        ],
        "Hard": [
            {"question": "d/dx (sinx + cosx)?", "options": ["cosx - sinx", "sinx - cosx", "-sinx + cosx", "-cosx + sinx"], "answer": "cosx - sinx"},
            {"question": "∫(2x³)dx =", "options": ["x⁴/2", "x⁴/4", "2x⁴", "x⁴/2 + C"], "answer": "x⁴/2 + C"},
            {"question": "What is determinant of [[2,3],[1,4]]?", "options": ["5", "2", "7", "4"], "answer": "5"},
            {"question": "Solve: log₁₀(1000) =", "options": ["1", "2", "3", "4"], "answer": "3"},
            {"question": "If f(x)=x³, f'(2)=?", "options": ["8", "12", "6", "4"], "answer": "12"},
        ],
    },
    "Physics": {
        "Easy": [
            {"question": "Unit of force?", "options": ["Joule", "Newton", "Watt", "Pascal"], "answer": "Newton"},
            {"question": "Acceleration due to gravity?", "options": ["9.8 m/s²", "8.9 m/s²", "9.0 m/s²", "10 m/s²"], "answer": "9.8 m/s²"},
            {"question": "Speed = ?", "options": ["Distance × Time", "Distance / Time", "Time / Distance", "None"], "answer": "Distance / Time"},
            {"question": "SI unit of energy?", "options": ["Watt", "Joule", "Newton", "Pascal"], "answer": "Joule"},
            {"question": "What is 1 horsepower in watts?", "options": ["746", "1000", "250", "500"], "answer": "746"},
        ],
        "Medium": [
            {"question": "Ohm’s law is?", "options": ["V=IR", "I=VR", "V=I/R", "R=V/I"], "answer": "V=IR"},
            {"question": "Power formula?", "options": ["P=IV", "P=V/I", "P=I²R", "P=V²/R"], "answer": "P=IV"},
            {"question": "Who discovered laws of motion?", "options": ["Einstein", "Newton", "Faraday", "Galileo"], "answer": "Newton"},
            {"question": "Unit of electric current?", "options": ["Ampere", "Volt", "Coulomb", "Ohm"], "answer": "Ampere"},
            {"question": "SI unit of pressure?", "options": ["Pascal", "Bar", "Torr", "Atm"], "answer": "Pascal"},
        ],
        "Hard": [
            {"question": "Work done formula?", "options": ["W=Fd", "W=F/d", "W=d/F", "W=F×v"], "answer": "W=Fd"},
            {"question": "Kinetic energy formula?", "options": ["½mv²", "mv", "mv²", "mgh"], "answer": "½mv²"},
            {"question": "1 eV = ?", "options": ["1.6×10⁻¹⁹ J", "1.6×10⁻¹⁶ J", "1.6×10⁻¹⁸ J", "1.6×10⁻²⁰ J"], "answer": "1.6×10⁻¹⁹ J"},
            {"question": "Magnetic field unit?", "options": ["Tesla", "Weber", "Henry", "Ohm"], "answer": "Tesla"},
            {"question": "Current formula?", "options": ["I=Q/t", "I=Qt", "I=VQ", "I=V/t"], "answer": "I=Q/t"},
        ],
    },
    "Chemistry": {
        "Easy": [
            {"question": "Atomic number of Oxygen?", "options": ["6", "7", "8", "9"], "answer": "8"},
            {"question": "Symbol of Sodium?", "options": ["S", "So", "Na", "N"], "answer": "Na"},
            {"question": "pH of neutral solution?", "options": ["0", "7", "14", "1"], "answer": "7"},
            {"question": "H₂O is?", "options": ["Hydrogen", "Water", "Oxygen", "Acid"], "answer": "Water"},
            {"question": "NaCl is?", "options": ["Sugar", "Salt", "Acid", "Base"], "answer": "Salt"},
        ],
        "Medium": [
            {"question": "Valency of Nitrogen?", "options": ["1", "2", "3", "4"], "answer": "3"},
            {"question": "Chemical formula of Methane?", "options": ["CH₄", "C₂H₆", "C₃H₈", "CH₃OH"], "answer": "CH₄"},
            {"question": "Periodic table was given by?", "options": ["Newton", "Mendeleev", "Curie", "Bohr"], "answer": "Mendeleev"},
            {"question": "Which is a noble gas?", "options": ["O₂", "He", "N₂", "CO₂"], "answer": "He"},
            {"question": "Acids turn litmus paper?", "options": ["Blue to Red", "Red to Blue", "No Change", "Green"], "answer": "Blue to Red"},
        ],
        "Hard": [
            {"question": "Molecular mass of CO₂?", "options": ["42", "44", "46", "48"], "answer": "44"},
            {"question": "Avogadro number?", "options": ["6.02×10²²", "6.02×10²³", "6.02×10²⁴", "6.02×10²⁵"], "answer": "6.02×10²³"},
            {"question": "Electron configuration of Neon?", "options": ["2,8", "2,6", "2,5", "2,7"], "answer": "2,8"},
            {"question": "Strongest acid?", "options": ["HCl", "H₂SO₄", "HNO₃", "HF"], "answer": "H₂SO₄"},
            {"question": "Bond type in H₂O?", "options": ["Ionic", "Hydrogen", "Covalent", "Metallic"], "answer": "Covalent"},
        ],
    },
}

# ===================================
# SUBJECT & DIFFICULTY SELECTION
# ===================================
st.markdown("### Choose subject and difficulty to begin your quiz!", unsafe_allow_html=True)
subject = st.selectbox("Select Subject", list(quiz_data.keys()))
difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])

# ===================================
# TIMER SETUP
# ===================================
if difficulty == "Easy":
    total_time = 5 * 60
elif difficulty == "Medium":
    total_time = 10 * 60
else:
    total_time = 15 * 60

# ===================================
# START QUIZ BUTTON
# ===================================
if st.button("🚀 Start Quiz"):
    st.session_state.quiz_started = True
    st.session_state.start_time = time.time()
    st.session_state.end_time = st.session_state.start_time + total_time
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.questions = random.sample(quiz_data[subject][difficulty], len(quiz_data[subject][difficulty]))

# ===================================
# DISPLAY TIMER AND QUESTIONS
# ===================================
if st.session_state.quiz_started:
    remaining = int(st.session_state.end_time - time.time())
    if remaining > 0:
        mins, secs = divmod(remaining, 60)
        st.markdown(
            f"<h3 style='text-align:center; color:#FFD700;'>⏳ Time Left: {mins:02d}:{secs:02d}</h3>",
            unsafe_allow_html=True
        )

        # DISPLAY CURRENT QUESTION
        if st.session_state.q_index < len(st.session_state.questions):
            q = st.session_state.questions[st.session_state.q_index]
            st.subheader(f"Q{st.session_state.q_index + 1}: {q['question']}")
            selected = st.radio("Choose your answer:", q["options"], key=f"q_{st.session_state.q_index}")

            if st.button("Submit Answer"):
                if selected == q["answer"]:
                    st.success("✅ Correct!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Wrong! Correct answer: {q['answer']}")
                st.session_state.q_index += 1
                st.rerun()
        else:
            # QUIZ COMPLETED
            st.balloons()
            st.success(f"🎉 Quiz Completed! Your Score: {st.session_state.score}/{len(st.session_state.questions)}")

            st.markdown("### 🌍 How this supports SDG Goals")
            st.info("""
            - **SDG 4 - Quality Education:** Helps students learn interactively.  
            - **SDG 9 - Innovation & Infrastructure:** Uses AI for better learning systems.  
            - **SDG 10 - Reduced Inequalities:** Free learning for all students.  
            - **SDG 17 - Partnerships:** Encourages collaborative study groups.
            """)

            if st.button("Restart Quiz"):
                for key in ["quiz_started", "q_index", "score", "questions"]:
                    st.session_state[key] = 0 if key in ["q_index", "score"] else False if key == "quiz_started" else []
                st.rerun()
    else:
        st.session_state.quiz_started = False
        st.markdown("<h2 style='text-align:center; color:red;'>⏰ Time’s Up!</h2>", unsafe_allow_html=True)
else:
    st.info("Select subject and difficulty, then click 🚀 **Start Quiz** to begin.")
