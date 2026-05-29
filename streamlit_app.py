import streamlit as st

# 1. 웹페이지 설정
st.set_page_config(page_title="🤖 초간단 디지털 자판기", layout="centered")
st.title("🥤 디지털 자판기")
st.write("돈을 넣고 원하는 음료를 선택하세요!")

# 2. session_state를 이용한 데이터 초기화 (재고 및 투입 금액 유지)
if "balance" not in st.session_state:
    st.session_state.balance = 0

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "콜라 🥤": {"price": 1200, "stock": 5},
        "사이다 🍏": {"price": 1100, "stock": 3},
        "캔커피 ☕": {"price": 900, "stock": 8},
        "생수 💧": {"price": 600, "stock": 10},
    }

# --- 사이드바: 금액 투입 및 잔돈 반환 ---
st.sidebar.header("💰 금액 투입구")
money_input = st.sidebar.selectbox("투입할 금액을 선택하세요", [500, 1000, 5000])

if st.sidebar.button("돈 넣기 🪙"):
    st.session_state.balance += money_input
    st.sidebar.success(f"{money_input}원이 투입되었습니다!")

st.sidebar.markdown("---")
st.sidebar.metric(label="현재 투입 금액", value=f"{st.session_state.balance} 원")

if st.sidebar.button("잔돈 반환 💸"):
    if st.session_state.balance > 0:
        st.sidebar.info(f"잔돈 {st.session_state.balance}원이 반환되었습니다. 감사합니다!")
        st.session_state.balance = 0
    else:
        st.sidebar.warning("반환할 잔돈이 없습니다.")


# --- 메인 화면: 상품 목록 및 구매 ---
st.subheader("🛒 판매 상품 목록")

# 상품들을 보기 좋게 컬럼으로 배치
cols = st.columns(2)

for i, (item_name, info) in enumerate(st.session_state.inventory.items()):
    # 0, 1번 컬럼에 번갈아가며 배치
    with cols[i % 2]:
        st.markdown(f"### {item_name}")
        st.write(f"**가격:** {info['price']}원")
        st.write(f"**재고:** {info['stock']}개")
        
        # 구매 버튼 활성화/비활성화 조건 체크
        if info['stock'] == 0:
            st.button(f"{item_name} 품절", key=item_name, disabled=True)
        else:
            if st.button(f"{item_name} 구매하기", key=item_name):
                # 잔액 확인
                if st.session_state.balance >= info['price']:
                    st.session_state.balance -= info['price']  # 잔액 차감
                    st.session_state.inventory[item_name]['stock'] -= 1  # 재고 차감
                    st.success(f"🎉 {item_name} 나왔습니다! 맛있게 드세요.")
                    st.rerun() # 화면 갱신해서 잔액과 재고 바로 반영
                else:
                    st.error("❌ 금액이 부족합니다. 돈을 더 넣어주세요!")
        st.write("") # 간격 띄우기