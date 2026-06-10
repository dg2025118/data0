import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="여름과 겨울은 정말 길어지고 있는가?",
    layout="wide"
)

st.title("🌏 여름과 겨울은 정말 길어지고 있는가?")
st.write("서울 장기 기온 관측 자료를 이용한 통계적 탐구")

# ==========================
# 데이터 불러오기
# ==========================
df = pd.read_csv("ta_20260601093156(1).csv")

df["날짜"] = (
    df["날짜"]
    .astype(str)
    .str.replace("\t", "", regex=False)
)

df["날짜"] = pd.to_datetime(df["날짜"])

df["연도"] = df["날짜"].dt.year

# 평균기온 사용
temp_col = "평균기온(℃)"

# ==========================
# 계절 정의
# ==========================
SUMMER_TEMP = 20
WINTER_TEMP = 5

df["여름"] = df[temp_col] >= SUMMER_TEMP
df["겨울"] = df[temp_col] < WINTER_TEMP

# ==========================
# 연도별 계절 길이
# ==========================
season_length = (
    df.groupby("연도")
      .agg(
          여름일수=("여름", "sum"),
          겨울일수=("겨울", "sum"),
          연평균기온=(temp_col, "mean")
      )
      .reset_index()
)

# ==========================
# 추세 계산
# ==========================
summer_slope = (
    (season_length["연도"] - season_length["연도"].mean())
    * (season_length["여름일수"] - season_length["여름일수"].mean())
).sum() / (
    (season_length["연도"] - season_length["연도"].mean()) ** 2
).sum()

winter_slope = (
    (season_length["연도"] - season_length["연도"].mean())
    * (season_length["겨울일수"] - season_length["겨울일수"].mean())
).sum() / (
    (season_length["연도"] - season_length["연도"].mean()) ** 2
).sum()

temp_slope = (
    (season_length["연도"] - season_length["연도"].mean())
    * (season_length["연평균기온"] - season_length["연평균기온"].mean())
).sum() / (
    (season_length["연도"] - season_length["연도"].mean()) ** 2
).sum()

# ==========================
# 결과 요약
# ==========================
st.header("📊 분석 결과")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "여름 증가 속도",
        f"{summer_slope:.2f} 일/년"
    )

with c2:
    st.metric(
        "겨울 변화 속도",
        f"{winter_slope:.2f} 일/년"
    )

with c3:
    st.metric(
        "평균기온 변화",
        f"{temp_slope:.3f} ℃/년"
    )

# ==========================
# 그래프
# ==========================
st.header("☀️ 연도별 여름 길이")

summer_chart = (
    season_length
    .set_index("연도")[["여름일수"]]
)

st.line_chart(summer_chart)

st.header("❄️ 연도별 겨울 길이")

winter_chart = (
    season_length
    .set_index("연도")[["겨울일수"]]
)

st.line_chart(winter_chart)

st.header("🌡️ 연평균기온 변화")

temp_chart = (
    season_length
    .set_index("연도")[["연평균기온"]]
)

st.line_chart(temp_chart)

# ==========================
# 데이터 보기
# ==========================
st.header("📋 연도별 통계")

st.dataframe(
    season_length,
    use_container_width=True
)

# ==========================
# 자동 결론
# ==========================
st.header("📝 탐구 결론")

if summer_slope > 0:
    summer_result = "길어지고 있다"
else:
    summer_result = "짧아지고 있다"

if winter_slope > 0:
    winter_result = "길어지고 있다"
else:
    winter_result = "짧아지고 있다"

st.success(
    f"""
분석 결과,

• 여름은 연평균 {summer_slope:.2f}일 변화하여 {summer_result}.

• 겨울은 연평균 {winter_slope:.2f}일 변화하여 {winter_result}.

• 연평균기온은 매년 약 {temp_slope:.3f}℃ 변화하였다.

장기간의 기온 자료를 이용하면 기후변화에 따라
여름과 겨울의 길이가 어떻게 변화하는지 정량적으로 확인할 수 있다.
"""
)
