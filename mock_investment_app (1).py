import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ───────────────────────────────────────────────
# 페이지 설정 (갤럭시 탭 최적화)
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="📈 모의투자 프로젝트",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────────────────────────────
# 전역 CSS (갤럭시 탭 터치 친화적 UI)
# ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a237e 0%, #283593 100%);
    min-width: 220px !important;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stSelectbox label { font-size: 13px !important; }

/* 메인 배경 */
[data-testid="stAppViewContainer"] { background: #f5f7ff; }

/* 카드 스타일 */
.card {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(26,35,126,0.07);
    border: 1px solid #e8ecff;
}
.card-title {
    font-size: 16px;
    font-weight: 700;
    color: #1a237e;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e8ecff;
}

/* 배지 */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}
.badge-green { background: #e8f5e9; color: #2e7d32; }
.badge-red   { background: #ffebee; color: #c62828; }
.badge-blue  { background: #e3f2fd; color: #1565c0; }

/* 수익률 색상 */
.profit  { color: #c62828; font-weight: 700; }
.loss    { color: #1565c0; font-weight: 700; }

/* 버튼 터치 영역 크게 */
[data-testid="stButton"] > button {
    height: 48px !important;
    font-size: 15px !important;
    border-radius: 12px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* 입력 필드 */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    font-size: 15px !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* 메트릭 카드 */
[data-testid="stMetric"] {
    background: white;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 2px 8px rgba(26,35,126,0.06);
    border: 1px solid #e8ecff;
}

/* 타이틀 */
h1 { color: #1a237e !important; font-size: 22px !important; }
h2 { color: #283593 !important; font-size: 18px !important; }
h3 { color: #3949ab !important; font-size: 16px !important; }

/* 진행 바 */
.progress-wrap {
    background: #e8ecff;
    border-radius: 8px;
    height: 10px;
    margin: 6px 0 2px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #3949ab, #1e88e5);
    transition: width 0.5s;
}

/* 로그인 화면 */
.login-box {
    max-width: 420px;
    margin: 60px auto;
    background: white;
    border-radius: 24px;
    padding: 40px 36px;
    box-shadow: 0 8px 32px rgba(26,35,126,0.12);
    border: 1px solid #e8ecff;
    text-align: center;
}
.login-title {
    font-size: 26px;
    font-weight: 700;
    color: #1a237e;
    margin-bottom: 6px;
}
.login-sub { font-size: 14px; color: #666; margin-bottom: 28px; }

/* 포트폴리오 테이블 */
.port-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.port-table th {
    background: #e8ecff;
    color: #1a237e;
    font-weight: 700;
    padding: 10px 8px;
    text-align: center;
}
.port-table td { padding: 9px 8px; text-align: center; border-bottom: 1px solid #f0f2ff; }
.port-table tr:hover td { background: #f8f9ff; }

/* 타임캡슐 봉인 */
.capsule-sealed {
    background: linear-gradient(135deg, #1a237e, #283593);
    color: white;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    font-size: 16px;
    font-weight: 500;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# 데이터 저장 / 불러오기 (JSON 파일 기반)
# ───────────────────────────────────────────────
DATA_FILE = "student_data.json"

def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_student(name: str) -> dict:
    data = load_data()
    if name not in data:
        data[name] = default_student()
        save_data(data)
    return data[name]

def update_student(name: str, student: dict):
    data = load_data()
    data[name] = student
    save_data(data)

def default_student() -> dict:
    return {
        "created": datetime.now().isoformat(),
        "budget": 10_000_000,
        "activities": {str(i): {} for i in range(1, 13)},
        "portfolio_v1": [],   # 활동 5: 1차 포트폴리오
        "portfolio_v2": [],   # 활동 7: 수정 포트폴리오
        "current_prices": {}, # 활동 6·8: 현재가 입력
        "timecapsule_sealed": False,
        "teacher_requests": [],
    }

# ───────────────────────────────────────────────
# 세션 초기화
# ───────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "group" not in st.session_state:
    st.session_state.group = ""

# ───────────────────────────────────────────────
# 로그인 화면
# ───────────────────────────────────────────────
def show_login():
    st.markdown("""
    <div class='login-box'>
        <div style='font-size:52px;margin-bottom:8px;'>📈</div>
        <div class='login-title'>모의투자 프로젝트</div>
        <div class='login-sub'>이름과 모둠을 입력하면 바로 시작할 수 있어요!<br>계정이 필요 없어요 😊</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("👤 내 이름", placeholder="예: 홍길동", key="login_name")
        group = st.text_input("👥 우리 모둠", placeholder="예: 1모둠", key="login_group")

        if st.button("🚀 투자 시작하기!", use_container_width=True):
            if name.strip():
                st.session_state.logged_in = True
                st.session_state.student_name = name.strip()
                st.session_state.group = group.strip()
                # 학생 데이터 초기화(없으면 생성)
                get_student(name.strip())
                st.rerun()
            else:
                st.error("이름을 입력해 주세요!")

        st.caption("💡 같은 이름으로 다시 접속하면 이전 내용이 그대로 유지돼요.")

# ───────────────────────────────────────────────
# 공통 유틸
# ───────────────────────────────────────────────
BUDGET = 10_000_000

def fmt(n):
    return f"{int(n):,}원"

def rate_badge(r):
    if r > 0:
        return f'<span class="badge badge-red">▲ {r:.2f}%</span>'
    elif r < 0:
        return f'<span class="badge badge-blue">▼ {abs(r):.2f}%</span>'
    else:
        return f'<span class="badge">— 0.00%</span>'

def save_act(student, act_num, key, value):
    student["activities"][str(act_num)][key] = value

# ───────────────────────────────────────────────
# 실시간 포트폴리오 위젯 (사이드바)
# ───────────────────────────────────────────────
def sidebar_portfolio(student):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💼 내 포트폴리오")

    portfolio = student.get("portfolio_v2") or student.get("portfolio_v1") or []
    prices    = student.get("current_prices", {})

    if not portfolio:
        st.sidebar.caption("아직 포트폴리오가 없어요.\n활동(5)에서 설계해 보세요!")
        return

    total_buy = sum(p["price"] * p["qty"] for p in portfolio)
    total_cur = 0
    for p in portfolio:
        cur = prices.get(p["name"], p["price"])
        total_cur += cur * p["qty"]

    gain = total_cur - total_buy
    rate = (gain / total_buy * 100) if total_buy else 0

    color = "#c62828" if rate >= 0 else "#1565c0"
    st.sidebar.metric(
        "총 평가금액",
        fmt(total_cur),
        delta=f"{'+' if gain>=0 else ''}{fmt(gain)} ({rate:+.2f}%)",
    )

    st.sidebar.markdown("**보유 종목**")
    for p in portfolio:
        cur  = prices.get(p["name"], p["price"])
        r    = ((cur - p["price"]) / p["price"] * 100) if p["price"] else 0
        sign = "🔴" if r > 0 else ("🔵" if r < 0 else "⚪")
        st.sidebar.markdown(
            f"{sign} **{p['name']}** {r:+.1f}%  \n"
            f"<small style='color:#aaa'>{p['qty']}주 · {fmt(cur)}</small>",
            unsafe_allow_html=True,
        )

    remain = BUDGET - total_buy
    pct    = int(total_buy / BUDGET * 100) if BUDGET else 0
    st.sidebar.markdown(f"**투자비율** {pct}%")
    st.sidebar.markdown(f"""
    <div class='progress-wrap'>
      <div class='progress-fill' style='width:{pct}%;'></div>
    </div>
    <small style='color:#ccc;'>잔여 {fmt(remain)}</small>
    """, unsafe_allow_html=True)

# ───────────────────────────────────────────────
# 활동지 1 — 저축과 투자
# ───────────────────────────────────────────────
def page_act1(student):
    st.title("활동(1) 저축과 투자")
    act = student["activities"]["1"]

    st.markdown("<div class='card'><div class='card-title'>1. 저축을 하는 이유</div>", unsafe_allow_html=True)
    reason = st.text_area("저축을 해야 하는 이유는 무엇일까요?",
                          value=act.get("reason", ""), height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>2. 이자율 비교 — 현재 vs 1997년</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    rate_now  = c1.number_input("현재 이자율 (%)", value=float(act.get("rate_now",  3.5)),
                                 min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
    rate_1997 = c2.number_input("1997년 이자율 (%)", value=float(act.get("rate_1997", 24.0)),
                                 min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
    col1, col2 = st.columns(2)
    col1.markdown(f"""
    <div style='background:#e3f2fd;border-radius:12px;padding:14px;text-align:center;'>
        <div style='font-size:12px;color:#1565c0;'>현재 이자율</div>
        <div style='font-size:28px;font-weight:700;color:#1565c0;'>{rate_now}%</div>
    </div>""", unsafe_allow_html=True)
    col2.markdown(f"""
    <div style='background:#fff3e0;border-radius:12px;padding:14px;text-align:center;'>
        <div style='font-size:12px;color:#e65100;'>1997년 이자율</div>
        <div style='font-size:28px;font-weight:700;color:#e65100;'>{rate_1997}%</div>
    </div>""", unsafe_allow_html=True)
    if rate_now > 0:
        ratio = rate_1997 / rate_now
        st.info(f"1997년은 현재보다 이자가 약 **{ratio:.1f}배** 높았어요!")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>3. 복리의 마술 — 72의 법칙</div>", unsafe_allow_html=True)
    interest = st.slider("수익률(이자율)을 선택하세요 (%)", 1, 30,
                          value=int(act.get("interest", 6)), step=1)
    double_time = 72 / interest
    st.markdown(f"""
    <div style='background:#e8f5e9;border-radius:12px;padding:18px;margin-top:10px;text-align:center;'>
        <div style='font-size:14px;color:#2e7d32;'>100만원 → 200만원이 되는 시간</div>
        <div style='font-size:36px;font-weight:700;color:#1b5e20;'>{double_time:.1f}년</div>
        <div style='font-size:13px;color:#388e3c;'>72 ÷ {interest}% = {double_time:.1f}년</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>4. 오늘 배운 점</div>", unsafe_allow_html=True)
    feeling = st.text_area("저축과 투자에 대해 새롭게 알게 된 것을 적어보세요.",
                            value=act.get("feeling", ""), height=90)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 저장하기", key="save1", use_container_width=True):
        act.update({"reason": reason, "rate_now": rate_now, "rate_1997": rate_1997,
                    "interest": interest, "feeling": feeling})
        update_student(st.session_state.student_name, student)
        st.success("✅ 저장되었습니다!")

# ───────────────────────────────────────────────
# 활동지 2 — 투자의 기초
# ───────────────────────────────────────────────
def page_act2(student):
    st.title("활동(2) 투자의 기초")
    act = student["activities"]["2"]

    types = ["주식", "채권", "부동산", "펀드", "금", "암호화폐"]
    descs = {
        "주식":   "회사의 소유권 일부를 구매 — 수익 가능성 높지만 위험도 높음",
        "채권":   "국가·기업에 돈을 빌려줌 — 안정적, 수익 낮음",
        "부동산": "땅·건물에 투자 — 장기적 안정, 큰 돈 필요",
        "펀드":   "여러 사람이 모아 전문가가 투자 — 분산 효과",
        "금":     "귀금속에 투자 — 위기 때 강세",
        "암호화폐":"디지털 화폐 — 변동성 매우 큼",
    }

    st.markdown("<div class='card'><div class='card-title'>1. 투자의 종류</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, t in enumerate(types):
        cols[i % 3].markdown(f"""
        <div style='background:#f5f7ff;border-radius:10px;padding:12px;margin-bottom:8px;border-left:4px solid #3949ab;'>
            <b style='color:#1a237e;'>{t}</b><br>
            <small style='color:#555;'>{descs[t]}</small>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>2. 위험(리스크)와 수익의 관계</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#fff8e1;border-radius:10px;padding:14px;font-size:14px;color:#555;'>
        ⚠️ <b>높은 수익 기대 = 높은 위험 감수</b> (하이리스크 하이리턴)<br>
        안전한 투자일수록 수익이 낮고, 위험한 투자일수록 수익도 높을 수 있어요.
    </div>""", unsafe_allow_html=True)
    risk_ans = st.text_area("위험을 줄이기 위한 방법은 무엇이 있을까요?",
                             value=act.get("risk_ans", ""), height=90)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>3. 내가 관심 있는 투자 방법</div>", unsafe_allow_html=True)
    fav_type = st.selectbox("가장 관심 있는 투자 방법",
                             options=types,
                             index=types.index(act.get("fav_type", "주식")) if act.get("fav_type") in types else 0)
    fav_reason = st.text_area("선택 이유", value=act.get("fav_reason", ""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 저장하기", key="save2", use_container_width=True):
        act.update({"risk_ans": risk_ans, "fav_type": fav_type, "fav_reason": fav_reason})
        update_student(st.session_state.student_name, student)
        st.success("✅ 저장되었습니다!")

# ───────────────────────────────────────────────
# 활동지 3 — 주식시장 이해
# ───────────────────────────────────────────────
def page_act3(student):
    st.title("활동(3) 주식시장 이해")
    act = student["activities"]["3"]

    st.markdown("<div class='card'><div class='card-title'>1. 주식시장이란?</div>", unsafe_allow_html=True)
    market_def = st.text_area("주식시장을 내 말로 설명해 보세요.",
                               value=act.get("market_def", ""), height=90)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>2. 코스피 vs 코스닥</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.markdown("""
    <div style='background:#e3f2fd;border-radius:12px;padding:16px;'>
        <b style='color:#1565c0;font-size:16px;'>KOSPI (코스피)</b>
        <ul style='font-size:13px;color:#444;margin-top:8px;'>
            <li>대기업 중심</li>
            <li>삼성전자, 현대차 등</li>
            <li>비교적 안정적</li>
        </ul>
    </div>""", unsafe_allow_html=True)
    c2.markdown("""
    <div style='background:#fff3e0;border-radius:12px;padding:16px;'>
        <b style='color:#e65100;font-size:16px;'>KOSDAQ (코스닥)</b>
        <ul style='font-size:13px;color:#444;margin-top:8px;'>
            <li>중소·벤처기업 중심</li>
            <li>카카오게임즈, 셀트리온 등</li>
            <li>성장 가능성 높음</li>
        </ul>
    </div>""", unsafe_allow_html=True)
    market_diff = st.text_area("코스피와 코스닥의 차이점을 내 말로 적어보세요.",
                                value=act.get("market_diff", ""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>3. 주가에 영향을 주는 요소</div>", unsafe_allow_html=True)
    factors = st.text_area("주가가 오르고 내리는 이유에는 어떤 것들이 있을까요?",
                            value=act.get("factors", ""), height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>4. 내가 알고 있는 회사</div>", unsafe_allow_html=True)
    known_company = st.text_area("주식시장에 상장된 회사 중 내가 알고 있는 회사와 그 이유를 적어보세요.",
                                  value=act.get("known_company", ""), height=90)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 저장하기", key="save3", use_container_width=True):
        act.update({"market_def": market_def, "market_diff": market_diff,
                    "factors": factors, "known_company": known_company})
        update_student(st.session_state.student_name, student)
        st.success("✅ 저장되었습니다!")

# ───────────────────────────────────────────────
# 활동지 4 — 정보 찾기
# ───────────────────────────────────────────────
def page_act4(student):
    st.title("활동(4) 정보 찾기")
    act = student["activities"]["4"]

    st.markdown("<div class='card'><div class='card-title'>1. 투자 정보를 찾는 방법</div>", unsafe_allow_html=True)
    sources = ["뉴스·신문", "기업 공시(DART)", "애널리스트 리포트", "증권사 앱", "유튜브·SNS", "직접 관찰"]
    cols = st.columns(3)
    for i, s in enumerate(sources):
        cols[i % 3].markdown(f"""
        <div style='background:#f0f4ff;border-radius:8px;padding:10px 12px;margin-bottom:6px;font-size:13px;'>
            🔍 <b>{s}</b>
        </div>""", unsafe_allow_html=True)
    info_method = st.text_area("내가 정보를 찾을 때 주로 사용할 방법과 이유를 적어보세요.",
                                value=act.get("info_method", ""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>2. 관심 종목 조사</div>", unsafe_allow_html=True)
    company = st.text_input("조사할 회사 이름", value=act.get("company", ""),
                             placeholder="예: 하나투어, 삼성전자")
    c1, c2 = st.columns(2)
    biz     = c1.text_area("어떤 사업을 하나요?",    value=act.get("biz", ""),    height=100)
    news    = c2.text_area("최근 뉴스·소식은?",       value=act.get("news", ""),   height=100)
    reason4 = st.text_area("이 회사에 투자하고 싶은 이유와 근거",
                            value=act.get("reason4", ""), height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>3. 좋은 정보와 나쁜 정보</div>", unsafe_allow_html=True)
    good_bad = st.text_area("투자할 때 믿을 수 있는 정보와 조심해야 할 정보의 차이는?",
                             value=act.get("good_bad", ""), height=90)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 저장하기", key="save4", use_container_width=True):
        act.update({"info_method": info_method, "company": company,
                    "biz": biz, "news": news, "reason4": reason4, "good_bad": good_bad})
        update_student(st.session_state.student_name, student)
        st.success("✅ 저장되었습니다!")

# ───────────────────────────────────────────────
# 활동지 5 — 투자 설계 (포트폴리오 입력)
# ───────────────────────────────────────────────
def page_act5(student):
    st.title("활동(5) 투자 설계")
    act = student["activities"]["5"]

    st.info(f"💰 사용 가능한 금액: **{fmt(BUDGET)}**")

    # 포트폴리오 입력
    st.markdown("<div class='card'><div class='card-title'>나의 투자 포트폴리오 설계</div>", unsafe_allow_html=True)
    st.markdown("최대 6개 종목까지 입력할 수 있어요.")

    portfolio = student.get("portfolio_v1") or []
    # 최대 6행
    rows = []
    for i in range(6):
        existing = portfolio[i] if i < len(portfolio) else {}
        c1, c2, c3 = st.columns([3, 2, 2])
        name  = c1.text_input(f"종목명 {i+1}", value=existing.get("name", ""),
                               key=f"p5n{i}", placeholder="예: 하나투어")
        price = c2.number_input(f"주가(원) {i+1}", value=int(existing.get("price", 0)),
                                 key=f"p5p{i}", min_value=0, step=100)
        qty   = c3.number_input(f"매수량(주) {i+1}", value=int(existing.get("qty", 0)),
                                 key=f"p5q{i}", min_value=0, step=1)
        if name.strip():
            rows.append({"name": name.strip(), "price": price, "qty": qty})
    st.markdown("</div>", unsafe_allow_html=True)

    # 요약 테이블
    if rows:
        total_buy = sum(r["price"] * r["qty"] for r in rows)
        remain    = BUDGET - total_buy
        st.markdown("<div class='card'><div class='card-title'>📊 포트폴리오 요약</div>", unsafe_allow_html=True)
        st.markdown("""
        <table class='port-table'>
          <tr><th>종목명</th><th>주가</th><th>수량</th><th>투자금액</th><th>비중</th></tr>
        """ + "".join(
            f"<tr><td><b>{r['name']}</b></td><td>{fmt(r['price'])}</td>"
            f"<td>{r['qty']}주</td><td>{fmt(r['price']*r['qty'])}</td>"
            f"<td>{r['price']*r['qty']/total_buy*100:.1f}%</td></tr>"
            if total_buy else f"<tr><td><b>{r['name']}</b></td><td>—</td><td>—</td><td>—</td><td>—</td></tr>"
            for r in rows
        ) + "</table>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        cm1, cm2, cm3 = st.columns(3)
        cm1.metric("총 투자금액",  fmt(total_buy))
        cm2.metric("잔여 금액",    fmt(remain),
                   delta=f"{'초과!' if remain<0 else '남음'}", delta_color="inverse" if remain<0 else "normal")
        cm3.metric("투자 비중",    f"{total_buy/BUDGET*100:.1f}%")

        if remain < 0:
            st.error(f"⚠️ 투자금액이 {fmt(-remain)} 초과되었어요! 수량을 줄여보세요.")

    st.markdown("<div class='card'><div class='card-title'>투자 전략 및 이유</div>", unsafe_allow_html=True)
    strategy = st.text_area("이 포트폴리오를 선택한 이유와 투자 전략을 설명하세요.",
                             value=act.get("strategy", ""), height=120)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 포트폴리오 저장하기", key="save5", use_container_width=True):
        student["portfolio_v1"] = rows
        act["strategy"] = strategy
        update_student(st.session_state.student_name, student)
        st.success("✅ 포트폴리오가 저장되었습니다!")
        st.balloons()

# ───────────────────────────────────────────────
# 활동지 6 — 결과 분석 1
# ───────────────────────────────────────────────
def page_act6(student):
    st.title("활동(6) 결과 분석 ①")
    act = student["activities"]["6"]
    portfolio = student.get("portfolio_v1", [])

    if not portfolio:
        st.warning("⚠️ 먼저 활동(5)에서 포트폴리오를 설계해 주세요!")
        return

    st.markdown("<div class='card'><div class='card-title'>현재가 입력 — 지금 주가를 적어보세요</div>", unsafe_allow_html=True)
    prices = student.get("current_prices", {})

    rows = []
    for p in portfolio:
        cur_default = prices.get(p["name"], p["price"])
        col1, col2, col3 = st.columns([3, 2, 2])
        col1.markdown(f"<b style='font-size:15px;'>{p['name']}</b>  \n매수가: {fmt(p['price'])}", unsafe_allow_html=True)
        cur = col2.number_input(f"현재가(원)", value=int(cur_default),
                                 key=f"cur6_{p['name']}", min_value=0, step=100)
        gain = (cur - p["price"]) * p["qty"]
        rate = (cur - p["price"]) / p["price"] * 100 if p["price"] else 0
        col3.markdown(
            f"<div style='text-align:center;'>"
            f"<div class='{'profit' if rate>=0 else 'loss'}'>{rate:+.2f}%</div>"
            f"<small style='color:#888;'>{'+' if gain>=0 else ''}{fmt(gain)}</small></div>",
            unsafe_allow_html=True,
        )
        rows.append({**p, "cur": cur, "gain": gain, "rate": rate})
        prices[p["name"]] = cur
    st.markdown("</div>", unsafe_allow_html=True)

    # 전체 수익률
    total_buy = sum(r["price"] * r["qty"] for r in rows)
    total_cur = sum(r["cur"]   * r["qty"] for r in rows)
    total_gain= total_cur - total_buy
    total_rate= total_gain / total_buy * 100 if total_buy else 0

    st.markdown("<div class='card'><div class='card-title'>📈 1차 분석 결과</div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("총 매수금액",  fmt(total_buy))
    m2.metric("총 평가금액",  fmt(total_cur))
    m3.metric("전체 수익률",  f"{total_rate:+.2f}%",
              delta=f"{'+' if total_gain>=0 else ''}{fmt(total_gain)}")

    # 종목별 성과 막대
    st.markdown("**종목별 수익률**")
    for r in rows:
        bar_color = "#ef5350" if r["rate"] >= 0 else "#42a5f5"
        bar_width  = min(abs(r["rate"]) * 3, 100)
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:6px;'>
            <div style='width:80px;font-size:13px;font-weight:600;'>{r['name']}</div>
            <div style='flex:1;background:#f0f2ff;border-radius:6px;height:20px;overflow:hidden;'>
                <div style='width:{bar_width}%;background:{bar_color};height:100%;border-radius:6px;'></div>
            </div>
            <div style='width:70px;text-align:right;font-size:13px;color:{bar_color};font-weight:700;'>
                {r['rate']:+.2f}%
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>소감 및 분석</div>", unsafe_allow_html=True)
    review6 = st.text_area("1차 투자 결과에 대한 느낀 점과 원인 분석",
                            value=act.get("review6", ""), height=120)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 저장하기", key="save6", use_container_width=True):
        student["current_prices"] = prices
        act["review6"] = review6
        update_student(st.session_state.student_name, student)
        st.success("✅ 저장되었습니다!")

# ───────────────────────────────────────────────
# 활동지 7 — 포트폴리오 재작성
# ───────────────────────────────────────────────
def page_act7(student):
    st.title("활동(7) 포트폴리오 재작성")
    act = student["activities"]["7"]

    st.markdown("<div class='card'><div class='card-title'>1차 분석 결과 돌아보기</div>", unsafe_allow_html=True)
    v1 = student.get("portfolio_v1", [])
    prices = student.get("current_prices", {})
    if v1:
        st.markdown("<table class='port-table'><tr><th>종목</th><th>매수가</th><th>현재가</th><th>수익률</th></tr>" +
            "".join(f"<tr><td>{p['name']}</td><td>{fmt(p['price'])}</td>"
                    f"<td>{fmt(prices.get(p['name'], p['price']))}</td>"
                    f"<td class='{'profit' if prices.get(p['name'],p['price'])>=p['price'] else 'loss'}'>"
                    f"{(prices.get(p['name'],p['price'])-p['price'])/p['price']*100:+.2f}%</td></tr>"
                    for p in v1) + "</table>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>변경 이유</div>", unsafe_allow_html=True)
    change_reason = st.text_area("어떤 종목을 왜 바꾸려고 하나요?",
                                  value=act.get("change_reason", ""), height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>수정된 포트폴리오</div>", unsafe_allow_html=True)
    st.info(f"💰 사용 가능 금액: **{fmt(BUDGET)}**")
    v2 = student.get("portfolio_v2") or v1[:]
    rows = []
    for i in range(6):
        existing = v2[i] if i < len(v2) else {}
        c1, c2, c3 = st.columns([3, 2, 2])
        name  = c1.text_input(f"종목명 {i+1}", value=existing.get("name", ""), key=f"p7n{i}")
        price = c2.number_input(f"주가(원) {i+1}", value=int(existing.get("price", 0)),
                                 key=f"p7p{i}", min_value=0, step=100)
        qty   = c3.number_input(f"매수량(주) {i+1}", value=int(existing.get("qty", 0)),
                                 key=f"p7q{i}", min_value=0)
        if name.strip():
            rows.append({"name": name.strip(), "price": price, "qty": qty})
    if rows:
        total = sum(r["price"] * r["qty"] for r in rows)
        st.metric("수정 후 총 투자금액", fmt(total),
                  delta=f"잔여 {fmt(BUDGET-total)}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>수정 전략 설명</div>", unsafe_allow_html=True)
    new_strategy = st.text_area("새로운 전략을 설명하세요.",
                                 value=act.get("new_strategy", ""), height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 수정 포트폴리오 저장", key="save7", use_container_width=True):
        student["portfolio_v2"] = rows
        act.update({"change_reason": change_reason, "new_strategy": new_strategy})
        update_student(st.session_state.student_name, student)
        st.success("✅ 수정된 포트폴리오가 저장되었습니다!")
        st.balloons()

# ───────────────────────────────────────────────
# 활동지 8 — 결과 분석 2 (최종)
# ───────────────────────────────────────────────
def page_act8(student):
    st.title("활동(8) 결과 분석 ② — 최종")
    act = student["activities"]["8"]
    portfolio = student.get("portfolio_v2") or student.get("portfolio_v1", [])

    if not portfolio:
        st.warning("⚠️ 먼저 활동(5) 또는 (7)에서 포트폴리오를 설계해 주세요!")
        return

    st.markdown("<div class='card'><div class='card-title'>최종 현재가 입력</div>", unsafe_allow_html=True)
    prices = student.get("current_prices", {})
    rows = []
    for p in portfolio:
        cur_def = prices.get(p["name"], p["price"])
        c1, c2 = st.columns([3, 3])
        c1.markdown(f"**{p['name']}** — 매수가 {fmt(p['price'])}", unsafe_allow_html=True)
        cur = c2.number_input("최종 현재가(원)", value=int(cur_def),
                               key=f"cur8_{p['name']}", min_value=0, step=100)
        gain = (cur - p["price"]) * p["qty"]
        rate = (cur - p["price"]) / p["price"] * 100 if p["price"] else 0
        rows.append({**p, "cur": cur, "gain": gain, "rate": rate})
        prices[p["name"]] = cur
    st.markdown("</div>", unsafe_allow_html=True)

    total_buy  = sum(r["price"] * r["qty"] for r in rows)
    total_cur  = sum(r["cur"]   * r["qty"] for r in rows)
    total_gain = total_cur - total_buy
    total_rate = total_gain / total_buy * 100 if total_buy else 0

    st.markdown("<div class='card'><div class='card-title'>🏆 최종 투자 결과</div>", unsafe_allow_html=True)
    result_color = "#c62828" if total_rate >= 0 else "#1565c0"
    st.markdown(f"""
    <div style='text-align:center;padding:20px;background:{"#fff8e1" if total_rate>=0 else "#e3f2fd"};
         border-radius:16px;margin-bottom:16px;'>
        <div style='font-size:14px;color:#555;'>최종 수익률</div>
        <div style='font-size:48px;font-weight:700;color:{result_color};'>{total_rate:+.2f}%</div>
        <div style='font-size:16px;color:{result_color};'>{'+' if total_gain>=0 else ''}{fmt(total_gain)}</div>
    </div>""", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("총 매수금액", fmt(total_buy))
    m2.metric("최종 평가금액", fmt(total_cur))
    m3.metric("전체 순이익", f"{'+' if total_gain>=0 else ''}{fmt(total_gain)}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>종목별 최종 성과</div>", unsafe_allow_html=True)
    st.markdown("<table class='port-table'><tr><th>종목</th><th>매수가</th><th>최종가</th><th>수익률</th><th>손익</th></tr>" +
        "".join(f"<tr><td><b>{r['name']}</b></td><td>{fmt(r['price'])}</td><td>{fmt(r['cur'])}</td>"
                f"<td class='{'profit' if r['rate']>=0 else 'loss'}'>{r['rate']:+.2f}%</td>"
                f"<td class='{'profit' if r['gain']>=0 else 'loss'}'>{'+' if r['gain']>=0 else ''}{fmt(r['gain'])}</td></tr>"
                for r in rows) + "</table>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>최종 소감</div>", unsafe_allow_html=True)
    final_review = st.text_area("모의투자 최종 결과에 대한 분석과 느낀 점",
                                 value=act.get("final_review", ""), height=130)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 저장하기", key="save8", use_container_width=True):
        student["current_prices"] = prices
        act["final_review"] = final_review
        update_student(st.session_state.student_name, student)
        st.success("✅ 저장되었습니다!")

# ───────────────────────────────────────────────
# 활동지 9 — 차트 분석
# ───────────────────────────────────────────────
def page_act9(student):
    st.title("활동(9) 차트 분석")
    act = student["activities"]["9"]

    st.markdown("<div class='card'><div class='card-title'>1. 차트의 종류</div>", unsafe_allow_html=True)
    chart_types = {
        "선 차트": ("📉", "주가의 흐름을 선으로 연결 — 추세 파악에 유리"),
        "봉 차트 (캔들스틱)": ("🕯️", "시가·종가·고가·저가를 하나의 봉으로 표현"),
        "거래량 차트": ("📊", "얼마나 많이 사고팔았는지 막대로 표현"),
        "이동평균선": ("〰️", "일정 기간 평균 주가를 선으로 연결 — 추세 확인"),
    }
    for ct, (icon, desc) in chart_types.items():
        st.markdown(f"""
        <div style='display:flex;gap:12px;align-items:flex-start;
             background:#f5f7ff;border-radius:10px;padding:12px;margin-bottom:6px;'>
            <span style='font-size:22px;'>{icon}</span>
            <div><b style='color:#1a237e;'>{ct}</b><br>
            <small style='color:#555;'>{desc}</small></div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>2. 차트 분석 실습</div>", unsafe_allow_html=True)
    chart_stock  = st.text_input("분석할 종목", value=act.get("chart_stock", ""),
                                  placeholder="예: 삼성전자")
    chart_pattern= st.text_area("차트에서 발견한 패턴이나 특징",
                                 value=act.get("chart_pattern", ""), height=90)
    chart_predict= st.text_area("이 차트를 보고 예상되는 미래 주가와 근거",
                                 value=act.get("chart_predict", ""), height=90)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>3. 차트 분석의 한계</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#fff3e0;border-radius:10px;padding:14px;font-size:14px;'>
        ⚠️ 차트만으로 미래 주가를 완벽하게 예측하는 것은 불가능합니다.
        차트 분석은 <b>하나의 참고 도구</b>일 뿐이에요.
    </div>""", unsafe_allow_html=True)
    chart_limit = st.text_area("차트 분석의 한계점에 대한 내 생각",
                                value=act.get("chart_limit", ""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 저장하기", key="save9", use_container_width=True):
        act.update({"chart_stock": chart_stock, "chart_pattern": chart_pattern,
                    "chart_predict": chart_predict, "chart_limit": chart_limit})
        update_student(st.session_state.student_name, student)
        st.success("✅ 저장되었습니다!")

# ───────────────────────────────────────────────
# 활동지 10 — 재무제표
# ───────────────────────────────────────────────
def page_act10(student):
    st.title("활동(10) 재무제표")
    act = student["activities"]["10"]

    st.markdown("""
    <div class='card'>
        <div class='card-title'>재무제표란?</div>
        <div style='background:#e8f5e9;border-radius:10px;padding:12px;font-size:14px;'>
            📋 재무제표는 <b>회사의 성적표</b>예요.<br>
            돈을 얼마나 벌었는지, 가진 재산은 얼마인지, 빚은 얼마인지 알 수 있어요.
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>주요 재무제표 3가지</div>", unsafe_allow_html=True)
    items = [
        ("손익계산서", "매출 - 비용 = 이익", "#e3f2fd", "#1565c0",
         "회사가 일정 기간 동안 얼마를 벌고 얼마를 썼는지"),
        ("재무상태표", "자산 = 부채 + 자본", "#f3e5f5", "#6a1b9a",
         "일정 시점에 회사가 가진 것(자산)과 빌린 것(부채)"),
        ("현금흐름표", "현금 유입 - 현금 유출", "#e8f5e9", "#2e7d32",
         "실제 현금이 얼마나 들어오고 나갔는지"),
    ]
    for title, formula, bg, color, desc in items:
        st.markdown(f"""
        <div style='background:{bg};border-radius:12px;padding:14px;margin-bottom:8px;'>
            <b style='color:{color};font-size:15px;'>{title}</b>
            <div style='font-size:13px;color:#555;margin-top:4px;'>{desc}</div>
            <div style='font-size:13px;font-weight:700;color:{color};margin-top:6px;'>{formula}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>재무제표 분석 실습</div>", unsafe_allow_html=True)
    fin_company = st.text_input("분석할 회사", value=act.get("fin_company", ""))
    c1, c2 = st.columns(2)
    revenue = c1.number_input("매출액 (억원)", value=float(act.get("revenue", 0)),
                               min_value=0.0, step=10.0)
    op_profit = c2.number_input("영업이익 (억원)", value=float(act.get("op_profit", 0)),
                                 min_value=0.0, step=1.0)
    if revenue > 0:
        margin = op_profit / revenue * 100
        m_color = "#2e7d32" if margin >= 10 else ("#f57f17" if margin >= 5 else "#c62828")
        st.markdown(f"""
        <div style='background:{m_color}22;border-radius:10px;padding:12px;text-align:center;'>
            <div style='font-size:13px;color:#555;'>영업이익률</div>
            <div style='font-size:30px;font-weight:700;color:{m_color};'>{margin:.1f}%</div>
            <div style='font-size:12px;color:#555;'>
                {"👍 우수 (10% 이상)" if margin>=10 else ("보통 (5~10%)" if margin>=5 else "⚠️ 낮음 (5% 미만)")}
            </div>
        </div>""", unsafe_allow_html=True)
    fin_opinion = st.text_area("이 회사의 재무상태에 대한 내 의견",
                                value=act.get("fin_opinion", ""), height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 저장하기", key="save10", use_container_width=True):
        act.update({"fin_company": fin_company, "revenue": revenue,
                    "op_profit": op_profit, "fin_opinion": fin_opinion})
        update_student(st.session_state.student_name, student)
        st.success("✅ 저장되었습니다!")

# ───────────────────────────────────────────────
# 활동지 11 — 선생님 사주세요!
# ───────────────────────────────────────────────
def page_act11(student):
    st.title("활동(11) 선생님 사주세요! 📣")
    act = student["activities"]["11"]

    st.warning("⚠️ 근거 자료가 터무니없으면 매수가 진행되지 않습니다! 꼼꼼하게 작성하세요 😊")

    st.markdown("<div class='card'><div class='card-title'>매수 신청서</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    grp_name    = c1.text_input("우리 모둠 이름", value=st.session_state.group or act.get("grp_name", ""))
    stock_req   = c2.text_input("매수하고 싶은 종목", value=act.get("stock_req", ""),
                                 placeholder="예: 하나투어")
    c3, c4 = st.columns(2)
    req_price   = c3.number_input("희망 매수 가격(원)", value=int(act.get("req_price", 0)),
                                   min_value=0, step=100)
    req_qty     = c4.number_input("매수 수량(주)", value=int(act.get("req_qty", 0)),
                                   min_value=0, step=1)
    total_req   = req_price * req_qty
    if total_req > 0:
        st.info(f"💰 총 매수 요청 금액: **{fmt(total_req)}**")

    evidence    = st.text_area("이 주식을 사야 하는 이유와 근거 (뉴스·재무지표·시장동향 등)",
                                value=act.get("evidence", ""), height=140,
                                help="구체적인 근거를 작성할수록 선생님 승인 가능성이 높아요!")
    st.markdown("</div>", unsafe_allow_html=True)

    # 이전 신청 내역
    if student.get("teacher_requests"):
        st.markdown("<div class='card'><div class='card-title'>📋 신청 내역</div>", unsafe_allow_html=True)
        for req in student["teacher_requests"]:
            status_color = {"대기중": "#fff8e1", "승인": "#e8f5e9", "반려": "#ffebee"}
            status_badge = {"대기중": "badge-blue", "승인": "badge-green", "반려": "badge-red"}
            s = req.get("status", "대기중")
            st.markdown(f"""
            <div style='background:{status_color.get(s,"#f5f7ff")};border-radius:10px;padding:12px;margin-bottom:6px;'>
                <b>{req['stock']}</b> — {fmt(req['price'])} × {req['qty']}주
                <span class='badge {status_badge.get(s,"badge-blue")}' style='float:right;'>{s}</span><br>
                <small style='color:#888;'>{req.get('date','')}</small>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("📬 선생님께 제출하기!", key="save11", use_container_width=True):
        if not stock_req.strip() or not evidence.strip():
            st.error("종목명과 근거를 모두 작성해 주세요!")
        else:
            act.update({"grp_name": grp_name, "stock_req": stock_req,
                        "req_price": req_price, "req_qty": req_qty, "evidence": evidence})
            req_item = {
                "stock": stock_req, "price": req_price,
                "qty": req_qty, "evidence": evidence,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "대기중"
            }
            student.setdefault("teacher_requests", []).append(req_item)
            update_student(st.session_state.student_name, student)
            st.success(f"✅ {grp_name} 모둠의 **{stock_req}** 매수 신청이 완료되었습니다!")
            st.balloons()

# ───────────────────────────────────────────────
# 활동지 12 — 타임캡슐
# ───────────────────────────────────────────────
def page_act12(student):
    st.title("활동(12) 나만의 투자 타임캡슐 🕰️")
    act = student["activities"]["12"]

    if student.get("timecapsule_sealed"):
        st.markdown(f"""
        <div class='capsule-sealed'>
            🔒 타임캡슐이 봉인되었습니다!<br>
            <small style='opacity:0.7;'>{act.get('sealed_date','')}</small><br><br>
            훗날 꺼내 읽어보세요. 📬
        </div>""", unsafe_allow_html=True)
        if st.button("🔓 다시 열기", key="unseal"):
            student["timecapsule_sealed"] = False
            update_student(st.session_state.student_name, student)
            st.rerun()
        return

    st.markdown("""
    <div style='background:#fff8e1;border-radius:12px;padding:14px;margin-bottom:16px;font-size:14px;color:#555;'>
        ✉️ 이 활동지는 프로젝트가 끝난 후 <b>미래의 내가 읽게 될 편지</b>입니다.<br>
        솔직하게, 진심으로 작성해 보세요.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>📊 투자 결과 요약</div>", unsafe_allow_html=True)
    result_summary = st.text_area("이번 모의투자 결과를 요약해서 적어보세요.",
                                   value=act.get("result_summary", ""), height=90)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>✅ 잘한 점 & 아쉬운 점</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    good_dec = c1.text_area("가장 잘한 투자 결정",    value=act.get("good_dec", ""), height=100)
    bad_dec  = c2.text_area("가장 아쉬운 투자 결정", value=act.get("bad_dec",  ""), height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>💡 배운 점</div>", unsafe_allow_html=True)
    lesson = st.text_area("이번 프로젝트를 통해 배운 가장 중요한 교훈",
                           value=act.get("lesson", ""), height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>💌 10년 후 나에게</div>", unsafe_allow_html=True)
    letter = st.text_area("미래의 나에게 투자에 대한 조언을 남겨보세요.",
                           value=act.get("letter", ""), height=150,
                           placeholder="10년 후의 나에게...\n\n이번 모의투자를 통해...")
    st.markdown("</div>", unsafe_allow_html=True)

    c_save, c_seal = st.columns(2)
    if c_save.button("💾 임시 저장", key="save12", use_container_width=True):
        act.update({"result_summary": result_summary, "good_dec": good_dec,
                    "bad_dec": bad_dec, "lesson": lesson, "letter": letter})
        update_student(st.session_state.student_name, student)
        st.success("✅ 임시 저장되었습니다!")

    if c_seal.button("🔒 타임캡슐 봉인하기!", key="seal12", use_container_width=True):
        if not letter.strip():
            st.error("편지 내용을 먼저 작성해 주세요!")
        else:
            act.update({"result_summary": result_summary, "good_dec": good_dec,
                        "bad_dec": bad_dec, "lesson": lesson, "letter": letter,
                        "sealed_date": datetime.now().strftime("%Y년 %m월 %d일")})
            student["timecapsule_sealed"] = True
            update_student(st.session_state.student_name, student)
            st.success("🎉 타임캡슐이 봉인되었습니다!")
            st.balloons()
            st.rerun()

# ───────────────────────────────────────────────
# 메인 앱
# ───────────────────────────────────────────────
def main_app():
    student = get_student(st.session_state.student_name)

    # 사이드바
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:16px 0 8px;'>
            <div style='font-size:36px;'>📈</div>
            <div style='font-size:18px;font-weight:700;margin-top:4px;'>모의투자 프로젝트</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.15);border-radius:12px;padding:10px 14px;margin-bottom:12px;'>
            <div style='font-size:14px;opacity:0.8;'>학생</div>
            <div style='font-size:17px;font-weight:700;'>{st.session_state.student_name}</div>
            <div style='font-size:13px;opacity:0.7;'>{st.session_state.group}</div>
        </div>""", unsafe_allow_html=True)

        menu_items = [
            "활동(1) 저축과 투자",    "활동(2) 투자의 기초",
            "활동(3) 주식시장 이해",  "활동(4) 정보 찾기",
            "활동(5) 투자 설계",      "활동(6) 결과 분석 ①",
            "활동(7) 포트폴리오 재작성","활동(8) 결과 분석 ②",
            "활동(9) 차트 분석",      "활동(10) 재무제표",
            "활동(11) 선생님 사주세요!","활동(12) 타임캡슐",
        ]
        choice = st.selectbox("📚 활동지 선택", menu_items, label_visibility="collapsed")

        # 실시간 포트폴리오 위젯
        sidebar_portfolio(student)

        st.markdown("---")
        if st.button("🚪 로그아웃", use_container_width=True):
            st.session_state.logged_in   = False
            st.session_state.student_name = ""
            st.session_state.group       = ""
            st.rerun()

    # 각 활동지 렌더링
    pages = {
        "활동(1) 저축과 투자":      page_act1,
        "활동(2) 투자의 기초":      page_act2,
        "활동(3) 주식시장 이해":    page_act3,
        "활동(4) 정보 찾기":        page_act4,
        "활동(5) 투자 설계":        page_act5,
        "활동(6) 결과 분석 ①":     page_act6,
        "활동(7) 포트폴리오 재작성":page_act7,
        "활동(8) 결과 분석 ②":     page_act8,
        "활동(9) 차트 분석":        page_act9,
        "활동(10) 재무제표":        page_act10,
        "활동(11) 선생님 사주세요!":page_act11,
        "활동(12) 타임캡슐":        page_act12,
    }
    if choice in pages:
        pages[choice](student)

# ───────────────────────────────────────────────
# 진입점
# ───────────────────────────────────────────────
if st.session_state.logged_in:
    main_app()
else:
    show_login()
