import streamlit as st
import random

st.set_page_config(page_title="신나는 수학연습", page_icon="🧮")

st.title("🧮 신나는 수학연습")
st.write("사칙연산을 연습하는 페이지 입니다. 수많은 문제들로 당신의 실력을 업그레이드 시키세요!")

# 사이드바 설정
st.sidebar.header("설정")
ops = st.sidebar.multiselect("문제 유형 선택", ["덧셈", "뺄셈", "곱셈", "나눗셈"], default=["덧셈", "뺄셈", "곱셈", "나눗셈"])
max_operand = st.sidebar.selectbox("최대 숫자", [10, 20, 50, 100], index=0)
show_solution = st.sidebar.checkbox("정답과 풀이 보기", value=True)

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "level" not in st.session_state:
    st.session_state.level = 0
if "a" not in st.session_state:
    st.session_state.a = 0
if "b" not in st.session_state:
    st.session_state.b = 0
if "op" not in st.session_state:
    st.session_state.op = "+"
if "correct" not in st.session_state:
    st.session_state.correct = None
if "problem" not in st.session_state:
    st.session_state.problem = ""


def gen_problem():
    if not ops:
        return
    choice = random.choice(ops)
    if choice == "덧셈":
        a = random.randint(0, max_operand)
        b = random.randint(0, max_operand)
        op = "+"
        correct = a + b
    elif choice == "뺄셈":
        a = random.randint(0, max_operand)
        b = random.randint(0, a)  # 음수 방지
        op = "-"
        correct = a - b
    elif choice == "곱셈":
        a = random.randint(0, max_operand)
        b = random.randint(0, max_operand)
        op = "×"
        correct = a * b
    else:  # 나눗셈
        b = random.randint(1, max_operand)
        mult = random.randint(0, max_operand // b if b!=0 else 0)
        a = b * mult
        op = "÷"
        correct = a // b

    st.session_state.a = a
    st.session_state.b = b
    st.session_state.op = op
    st.session_state.correct = correct
    st.session_state.problem = f"{a} {op} {b}"
    if "answer_input" in st.session_state:
        st.session_state.answer_input = ""


col1, col2 = st.columns(2)
with col1:
    if st.button("문제 생성"):
        gen_problem()
with col2:
    if st.button("다음 문제"):
        gen_problem()

st.write("---")

# 레벨 표시 (배터리 상태)
battery = "🟩" * st.session_state.level + "⬜" * (5 - st.session_state.level)
st.markdown(f"### 📊 레벨: {battery} ({st.session_state.level}/5)")

st.write("### 현재 문제")
if st.session_state.problem == "":
    st.info("문제 생성을 누르고 시작하세요.")
else:
    st.write(st.session_state.problem)
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_input = st.text_input("정답을 입력하세요", key="answer_input")
    with col_btn:
        st.write("")  # 여백 추가
        if st.button("정답확인", use_container_width=True):
            try:
                # 정답 비교는 정수로 처리
                user_val = int(user_input.strip())
            except Exception:
                try:
                    user_val = float(user_input.strip())
                except Exception:
                    user_val = None
            if user_val is None:
                st.error("숫자를 입력해주세요.")
            else:
                st.session_state.total += 1
                if user_val == st.session_state.correct:
                    st.session_state.score += 1
                    st.session_state.level += 1
                    st.success("정답입니다! 🎉")
                    
                    # 5레벨 달성 시 트로피 표시
                    if st.session_state.level == 5:
                        st.balloons()
                        st.markdown("<h1 style='text-align: center;'>🏆</h1>", unsafe_allow_html=True)
                        st.markdown("<h2 style='text-align: center;'>축하합니다! 5레벨을 완성했습니다!</h2>", unsafe_allow_html=True)
                        st.session_state.level = 0  # 레벨 초기화
                else:
                    st.error(f"틀렸습니다. 정답: {st.session_state.correct}")
                if show_solution:
                    st.write(f"풀이: {st.session_state.a} {st.session_state.op} {st.session_state.b} = {st.session_state.correct}")
st.write("---")
st.write(f"점수: {st.session_state.score} / {st.session_state.total}")

if st.button("초기화"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.level = 0
    st.session_state.problem = ""
    st.session_state.correct = None
    st.session_state.a = 0
    st.session_state.b = 0
    st.session_state.op = "+"
