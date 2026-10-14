```python
import streamlit as st

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="MBTI로 포켓몬 찾기",
    page_icon="🌼",
    layout="centered",
)

# ==========================================
# 2. 디자인
# ==========================================
st.markdown("""
<style>
.stApp {
    background-color: #FFF9E9;
    color: #55432E;
}

.block-container {
    max-width: 800px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #FFF0B8, #FFE1A0);
    border: 2px solid #F1D17C;
    border-radius: 25px;
    padding: 28px 16px;
    text-align: center;
    margin-bottom: 25px;
}

.hero h1 {
    color: #55432E;
    font-size: clamp(30px, 6vw, 44px);
    margin: 8px 0;
}

.hero p {
    color: #6D5739;
    font-size: 18px;
    line-height: 1.8;
}

.stButton > button {
    background-color: #FFF2CB;
    color: #55432E;
    border: 2px solid #EBD8A6;
    border-radius: 14px;
    min-height: 48px;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #FFDE83;
    border-color: #DDB54A;
    color: #55432E;
}

.result-card {
    background-color: #FFF4D5;
    border: 2px solid #F0DCA7;
    border-radius: 24px;
    padding: 20px;
    margin-top: 20px;
    text-align: center;
}

.info-card {
    background-color: #FFFEF8;
    border: 1px solid #EFDFB9;
    border-radius: 18px;
    padding: 18px;
    margin: 14px 0;
    line-height: 1.9;
    font-size: 17px;
}

.match-card {
    background-color: #FFE9E0;
    border: 2px solid #F3D0C2;
    border-radius: 18px;
    padding: 18px;
    margin-top: 16px;
    text-align: center;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #927D60;
    font-size: 13px;
    line-height: 1.8;
    margin-top: 30px;
}

div[data-testid="stImage"] img {
    border-radius: 20px;
}

@media (max-width: 600px) {
    .hero {
        padding: 22px 10px;
    }

    .hero p {
        font-size: 16px;
    }

    .info-card {
        font-size: 16px;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MBTI별 포켓몬 데이터
# 형식: 한글 이름, 영어 이름, 도감 번호,
#       타입, 특징, 이유 2개, 궁합, 궁합 설명
# ==========================================
POKEMON = {
    "ISTJ": {
        "name": "거북왕", "english": "Blastoise", "id": 9,
        "type": "물",
        "feature": "책임감 · 신중함 · 끈기",
        "reason": [
            "계획을 세우고 맡은 일을 끝까지 해내는 모습이 닮았어.",
            "어려운 상황에서도 침착하게 자신의 역할을 다하는 든든한 단짝이야."
        ],
        "match": "ESFP",
        "match_reason": "ESFP의 밝은 에너지가 일상에 즐거움을 더하고, 너의 신중함은 상대에게 안정감을 줄 수 있어."
    },
    "ISFJ": {
        "name": "해피너스", "english": "Blissey", "id": 242,
        "type": "노말",
        "feature": "배려 · 다정함 · 헌신",
        "reason": [
            "주변 사람을 세심하게 챙기고 도움이 필요한 사람을 돕는 모습이 닮았어.",
            "따뜻한 마음으로 친구에게 편안함과 안정감을 주는 단짝이야."
        ],
        "match": "ESFP",
        "match_reason": "ESFP의 활발함은 너에게 즐거움을 주고, 너의 다정함은 상대에게 따뜻함을 줄 수 있어."
    },
    "INFJ": {
        "name": "가디안", "english": "Gardevoir", "id": 282,
        "type": "에스퍼 / 페어리",
        "feature": "통찰력 · 공감 · 신념",
        "reason": [
            "다른 사람의 감정을 깊이 이해하고 소중한 사람을 지키려는 모습이 닮았어.",
            "조용하지만 깊은 생각과 강한 신념을 지닌 점도 잘 어울려."
        ],
        "match": "ENFP",
        "match_reason": "ENFP의 상상력은 너의 생각을 넓혀 주고, 너는 상대가 자신의 가능성을 발견하도록 도와줄 수 있어."
    },
    "INTJ": {
        "name": "뮤츠", "english": "Mewtwo", "id": 150,
        "type": "에스퍼",
        "feature": "전략 · 독립성 · 지성",
        "reason": [
            "복잡한 문제를 분석하고 효율적인 해결책을 찾는 모습이 닮았어.",
            "독립적으로 생각하며 장기적인 목표를 세우는 점도 잘 어울려."
        ],
        "match": "ENFP",
        "match_reason": "ENFP의 창의적인 발상과 너의 전략적인 사고가 만나면 새로운 가능성을 발견할 수 있어."
    },
    "ISTP": {
        "name": "메타그로스", "english": "Metagross", "id": 376,
        "type": "강철 / 에스퍼",
        "feature": "논리 · 분석력 · 실용성",
        "reason": [
            "정보를 분석하고 문제의 원리를 파악하는 모습이 닮았어.",
            "복잡한 상황에서도 침착하게 해결 방법을 찾아내는 단짝이야."
        ],
        "match": "ESFJ",
        "match_reason": "ESFJ의 따뜻한 소통과 너의 실용적인 사고가 서로를 보완해 줄 수 있어."
    },
    "ISFP": {
        "name": "이브이", "english": "Eevee", "id": 133,
        "type": "노말",
        "feature": "감성 · 자유로움 · 가능성",
        "reason": [
            "자신만의 취향과 감성을 소중히 여기는 모습이 닮았어.",
            "다양한 가능성을 품고 자기만의 방식으로 성장하는 점도 어울려."
        ],
        "match": "ENFJ",
        "match_reason": "ENFJ의 응원은 너의 가능성을 펼치도록 도와주고, 너는 상대에게 편안함을 줄 수 있어."
    },
    "INFP": {
        "name": "몽나", "english": "Munna", "id": 517,
        "type": "에스퍼",
        "feature": "상상력 · 섬세함 · 이상",
        "reason": [
            "풍부한 상상력과 자신만의 세계를 소중히 여기는 모습이 닮았어.",
            "부드러운 감성과 자신이 중요하게 생각하는 가치를 지키는 점이 어울려."
        ],
        "match": "ENFJ",
        "match_reason": "ENFJ의 따뜻한 격려가 너의 꿈을 응원하고, 너의 진솔한 마음은 상대에게 새로운 시각을 줄 수 있어."
    },
    "INTP": {
        "name": "후딘", "english": "Alakazam", "id": 65,
        "type": "에스퍼",
        "feature": "호기심 · 논리 · 독창성",
        "reason": [
            "궁금한 것이 생기면 원리를 이해할 때까지 깊이 생각하는 모습이 닮았어.",
            "독창적인 아이디어와 논리적인 사고를 즐기는 점도 잘 어울려."
        ],
        "match": "ENTJ",
        "match_reason": "ENTJ의 실행력과 너의 분석력이 만나면 아이디어를 실제 결과로 발전시킬 수 있어."
    },
    "ESTP": {
        "name": "루카리오", "english": "Lucario", "id": 448,
        "type": "격투 / 강철",
        "feature": "행동력 · 용기 · 집중력",
        "reason": [
            "상황을 빠르게 파악하고 망설이기보다 직접 행동하는 모습이 닮았어.",
            "도전을 두려워하지 않고 눈앞의 문제를 해결하는 멋진 단짝이야."
        ],
        "match": "ISFJ",
        "match_reason": "ISFJ의 세심함이 너의 빠른 행동을 보완하고, 너는 상대에게 새로운 경험을 선물할 수 있어."
    },
    "ESFP": {
        "name": "피카츄", "english": "Pikachu", "id": 25,
        "type": "전기",
        "feature": "활발함 · 친화력 · 에너지",
        "reason": [
            "주변 분위기를 밝게 만들고 사람들과 함께 즐기는 모습이 닮았어.",
            "순간의 즐거움을 소중히 여기고 활기찬 에너지를 나누는 단짝이야."
        ],
        "match": "ISTJ",
        "match_reason": "ISTJ의 차분함은 너에게 안정감을 주고, 너의 활기는 상대의 일상에 즐거움을 더할 수 있어."
    },
    "ENFP": {
        "name": "나옹", "english": "Meowth", "id": 52,
        "type": "노말",
        "feature": "호기심 · 재치 · 자유로움",
        "reason": [
            "새로운 사람과 아이디어에 관심이 많고 다양한 가능성을 탐색하는 모습이 닮았어.",
            "재치 있는 발상과 자유로운 에너지로 주변에 활기를 더하는 단짝이야."
        ],
        "match": "INFJ",
        "match_reason": "INFJ의 통찰은 너의 아이디어를 발전시키고, 너의 활기는 상대에게 새로운 시각을 열어 줄 수 있어."
    },
    "ENTP": {
        "name": "팬텀", "english": "Gengar", "id": 94,
        "type": "고스트 / 독",
        "feature": "재치 · 장난기 · 창의성",
        "reason": [
            "남들이 생각하지 못한 방식으로 문제를 바라보는 모습이 닮았어.",
            "기발한 아이디어와 유쾌한 장난으로 일상을 특별하게 만드는 단짝이야."
        ],
        "match": "INTJ",
        "match_reason": "INTJ의 전략적인 사고와 너의 기발한 발상이 만나면 독창적인 아이디어를 구체화할 수 있어."
    },
    "ESTJ": {
        "name": "괴력몬", "english": "Machamp", "id": 68,
        "type": "격투",
        "feature": "추진력 · 책임감 · 리더십",
        "reason": [
            "목표를 향해 체계적으로 움직이고 맡은 일을 확실하게 처리하는 모습이 닮았어.",
            "강한 책임감과 실행력으로 주변을 이끄는 든든한 단짝이야."
        ],
        "match": "ISFP",
        "match_reason": "ISFP의 유연함과 감성이 너에게 새로운 관점을 더하고, 너는 상대가 목표를 이루도록 도와줄 수 있어."
    },
    "ESFJ": {
        "name": "푸린", "english": "Jigglypuff", "id": 39,
        "type": "노말 / 페어리",
        "feature": "사교성 · 배려 · 친근함",
        "reason": [
            "사람들과 어울리는 것을 좋아하고 모두가 즐겁기를 바라는 모습이 닮았어.",
            "노래와 밝은 분위기로 주변 사람들에게 행복을 전하는 단짝이야."
        ],
        "match": "ISTP",
        "match_reason": "ISTP의 침착함은 너를 도와주고, 너의 따뜻한 소통은 상대에게 활력을 줄 수 있어."
    },
    "ENFJ": {
        "name": "라프라스", "english": "Lapras", "id": 131,
        "type": "물 / 얼음",
        "feature": "공감 · 배려 · 협동",
        "reason": [
            "다른 사람의 마음을 이해하고 함께 성장하는 것을 중요하게 생각하는 모습이 닮았어.",
            "주변 사람들을 돕고 따뜻한 분위기를 만들어 가는 점이 잘 어울려."
        ],
        "match": "INFP",
        "match_reason": "INFP의 진솔한 감성과 너의 따뜻한 배려가 만나면 서로의 마음을 깊이 이해할 수 있어."
    },
    "ENTJ": {
        "name": "망나뇽", "english": "Dragonite", "id": 149,
        "type": "드래곤 / 비행",
        "feature": "결단력 · 목표 의식 · 추진력",
        "reason": [
            "큰 목표를 세우고 자신 있게 앞으로 나아가는 모습이 닮았어.",
            "강한 추진력과 결단력으로 어려운 상황을 돌파하는 단짝이야."
        ],
        "match": "INTP",
        "match_reason": "INTP의 논리적인 분석이 너의 계획을 탄탄하게 만들고, 너는 아이디어가 실현되도록 추진력을 더해 줄 수 있어."
    },
}

# ==========================================
# 4. 제목과 소개
# ==========================================
st.markdown("""
<div class="hero">
    <div style="font-size:48px;">🌼 ⚡ 🌼</div>
    <h1>MBTI로 포켓몬 찾기</h1>
    <p>
        내 성격과 꼭 닮은 단짝 포켓몬은 누구일까?<br>
        MBTI를 선택하고 특별한 만남을 시작해 봐!
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align:center;'>💛 나의 MBTI를 골라 줘!</h3>"
    "<p style='text-align:center;'>16가지 유형 중 하나를 선택해 봐.</p>",
    unsafe_allow_html=True,
)

# ==========================================
# 5. 선택 상태 초기화
# ==========================================
if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None

if "celebrate" not in st.session_state:
    st.session_state.celebrate = False

# ==========================================
# 6. MBTI 버튼 16개
# ==========================================
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
]

for start in range(0, len(mbti_list), 4):
    cols = st.columns(4)

    for offset, mbti in enumerate(mbti_list[start:start + 4]):
        with cols[offset]:
            if st.button(
                mbti,
                key="btn_" + mbti,
                use_container_width=True,
            ):
                st.session_state.selected_mbti = mbti
                st.session_state.celebrate = True

# ==========================================
# 7. 결과 표시
# ==========================================
selected = st.session_state.selected_mbti

if selected in POKEMON:
    data = POKEMON[selected]

    # 새로 선택했을 때만 축하 효과 실행
    if st.session_state.celebrate:
        st.balloons()
        st.session_state.celebrate = False

    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:20px;">🎉 단짝 포켓몬 발견!</div>
        <h2 style="font-size:32px; margin:12px 0;">
            {selected}의 단짝은 {data["name"]}!
        </h2>
        <p style="font-size:17px;">
            너와 잘 어울리는 포켓몬을 찾았어!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 공식 일러스트 이미지 주소
    image_url = (
        "https://raw.githubusercontent.com/PokeAPI/sprites/"
        "master/sprites/pokemon/other/official-artwork/"
        + str(data["id"])
        + ".png"
    )

    # 이미지가 표시되지 않아도 나머지 결과는 계속 보여 줌
    try:
        st.image(
            image_url,
            width=300,
            caption=data["name"] + " (" + data["english"] + ")",
        )
    except Exception:
        st.info(
            "포켓몬 이미지를 불러오지 못했어. "
            "인터넷 연결을 확인해 줘."
        )

    st.markdown(
        "<div style='text-align:center;'>"
        f"<h2 style='font-size:34px;'>{data['name']}</h2>"
        f"<p style='font-size:20px;'>{data['english']}</p>"
        f"<p style='font-size:19px;'>타입: {data['type']}</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='info-card'>"
        "<h3>🌟 포켓몬의 특징</h3>"
        f"<p>{data['feature']}</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='info-card'>"
        "<h3>💛 너와 어울리는 이유</h3>"
        f"<p>① {data['reason'][0]}</p>"
        f"<p>② {data['reason'][1]}</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='match-card'>"
        "<h3>💗 잘 맞을 것 같은 MBTI</h3>"
        f"<div style='font-size:30px;'>{data['match']}</div>"
        f"<p>{data['match_reason']}</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "🔄 다른 MBTI로 다시 찾기",
        key="reset_button",
        use_container_width=True,
    ):
        st.session_state.selected_mbti = None
        st.session_state.celebrate = False
        st.rerun()

else:
    st.markdown("""
    <div class="result-card">
        <div style="font-size:48px;">🎁</div>
        <h3>나만의 단짝 포켓몬을 찾아봐!</h3>
        <p style="font-size:17px; line-height:1.8;">
            위에서 MBTI 버튼을 누르면<br>
            포켓몬 이미지와 특징을 확인할 수 있어.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. 안내
# ==========================================
st.markdown("""
<div class="footer">
    🌼 MBTI와 포켓몬을 재미있게 연결한 콘텐츠야.<br>
    궁합은 공식 설정이나 과학적 판정이 아닌 재미를 위한 해석이야.<br>
    포켓몬 이미지는 외부 이미지 저장소에서 불러와.
</div>
""", unsafe_allow_html=True)
```
