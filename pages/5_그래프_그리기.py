import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.express as px
from pathlib import Path

font_path = Path(__file__).resolve().parent.parent / "fonts" / "NotoSansKR-ExtraBold.ttf"
if font_path.exists():
    fm.fontManager.addfont(str(font_path))
    font_prop = fm.FontProperties(fname=str(font_path))
    plt.rcParams["font.family"] = font_prop.get_name()
    plt.rcParams["axes.unicode_minus"] = False
else:
    st.warning("fonts/NotoSansKR-ExtraBold.ttf 폰트 파일을 찾을 수 없습니다. 기본 폰트로 표시됩니다.")

st.set_page_config(page_title="그래프 그리기 예시", page_icon="📈")

st.title("📊 그래프 예시 페이지")
st.write("matplotlib, seaborn, plotly를 활용한 그래프 예시입니다. 모두 한글로 표시됩니다.")

# 데이터 준비
x = np.arange(1, 11)
y = x ** 2
cats = ["사과", "바나나", "체리", "포도", "오렌지"]
values = [10, 25, 15, 20, 18]

st.header("1. matplotlib 선 그래프")
fig1, ax1 = plt.subplots()
ax1.plot(x, y, marker="o", color="#2E86AB", linewidth=2)
ax1.set_title("숫자별 제곱값", fontsize=16)
ax1.set_xlabel("입력값", fontsize=12)
ax1.set_ylabel("제곱값", fontsize=12)
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.set_xticks(x)
st.pyplot(fig1)

st.header("2. seaborn 막대 그래프")
data_bar = pd.DataFrame({"과일": cats, "수량": values})
fig2, ax2 = plt.subplots()
sns.barplot(data=data_bar, x="과일", y="수량", palette="pastel", ax=ax2)
ax2.set_title("과일별 수량", fontsize=16)
ax2.set_xlabel("과일", fontsize=12)
ax2.set_ylabel("수량", fontsize=12)
for p in ax2.patches:
    ax2.annotate(int(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha="center", va="bottom", fontsize=11)
st.pyplot(fig2)

st.header("3. plotly 원형 그래프")
pie_data = pd.DataFrame({"과일": cats, "비율": values})
fig3 = px.pie(
    pie_data,
    names="과일",
    values="비율",
    title="과일 점유율",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig3.update_traces(textposition="inside", textinfo="percent+label")
fig3.update_layout(title_font_size=18, legend_title_text="과일")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.write("위 예시는 `matplotlib`, `seaborn`, `plotly`를 모두 사용하여 한글 레이블과 제목을 가진 그래프를 보여줍니다.")
