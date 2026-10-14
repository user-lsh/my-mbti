import streamlit as st

# 기본 설정
st.set_page_config(
    page_title="MBTI로 포켓몬 찾기",
    page_icon="⚡",
    layout="wide",
)

# 디자인
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fffaf0 0%, #fff3cf 100%);
        color: #46351f;
    }
    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 {
        color: #65451f;
    }
    .hero {
        background: #fffdf7;
        border: 2px solid #f2d58a;
        border-radius: 24px;
        padding: 26px 22px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(140, 99, 26, 0.08);
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #8a5a13;
        margin-bottom: 8px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #7a6241;
    }
    .result-card {
        background: rgba(255, 255, 255, 0.88);
        border: 2px solid #f2d58a;
        border-radius: 24px;
        padding: 22px;
        margin-top: 18px;
    }
    .pill {
        display: inline-block;
        background: #ffedb3;
        color: #6b4a0b;
        border-radius: 999px;
        padding: 6px 12px;
        margin: 3px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    div.stButton > button {
        background: #fffdf7;
        color: #65451f;
        border: 2px solid #f0d28a;
        border-radius: 14px;
        min-height: 48px;
        font-weight: 700;
        transition: 0.15s ease-in-out;
    }
    div.stButton > button:hover {
        background: #ffe8a3;
        color: #52370d;
        border-color: #e7b947;
    }
    div.stButton > button:focus {
        border-color: #d99c19;
        color: #52370d;
    }
    .small-note {
        color: #806b4d;
        font-size: 0.9rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# MBTI별 포켓몬 데이터: 포켓몬은 16마리 모두 중복되지 않음
POKEMON = {
    "ISTJ": {
        "name_ko": "거북왕", "name_en": "Blastoise", "id": 9,
        "types": ["물"],
        "features": "책임감이 강하고 계획적으로 움직이며, 맡은 일을 끝까지 해내는 든든한 타입.",
        "reasons": [
            "차분하게 상황을 살피고 안정적인 방법을 선택해요.",
            "꾸준한 노력과 강한 책임감으로 팀을 지켜 줘요."
        ],
        "match": "ESFP",
        "match_reason": "신중한 ISTJ와 활기찬 ESFP가 서로에게 새로운 관점을 더해 줘요."
    },
    "ISFJ": {
        "name_ko": "해피너스", "name_en": "Blissey", "id": 242,
        "types": ["노말"],
        "features": "다정하고 세심하며, 주변 사람을 살뜰하게 챙기는 따뜻한 타입.",
        "reasons": [
            "다른 사람의 감정과 필요를 잘 알아차려요.",
            "조용하지만 꾸준한 배려로 주변에 안정감을 줘요."
        ],
        "match": "ENTP",
        "match_reason": "배려 깊은 ISFJ와 아이디어가 넘치는 ENTP가 서로의 부족한 부분을 채워 줘요."
    },
    "INFJ": {
        "name_ko": "가디안", "name_en": "Gardevoir", "id": 282,
        "types": ["에스퍼", "페어리"],
        "features": "직관적이고 공감 능력이 뛰어나며, 자신만의 가치와 이상을 소중히 여기는 타입.",
        "reasons": [
            "말하지 않은 마음도 섬세하게 헤아리려 해요.",
            "소중한 사람을 지키기 위해 깊이 고민하고 행동해요."
        ],
        "match": "ESTP",
        "match_reason": "깊이 생각하는 INFJ와 행동력이 좋은 ESTP가 균형을 이룰 수 있어요."
    },
    "INTJ": {
        "name_ko": "뮤츠", "name_en": "Mewtwo", "id": 150,
        "types": ["에스퍼"],
        "features": "전략적이고 독립적이며, 복잡한 문제를 분석해 큰 그림을 그리는 타입.",
        "reasons": [
            "목표를 정하면 논리적으로 계획을 세워요.",
            "혼자 깊이 생각하며 더 나은 해결책을 찾아요."
        ],
        "match": "ENFP",
        "match_reason": "전략적인 INTJ와 창의적인 ENFP가 만나면 새로운 가능성을 발견할 수 있어요."
    },
    "ISTP": {
        "name_ko": "메타그로스", "name_en": "Metagross", "id": 376,
        "types": ["강철", "에스퍼"],
        "features": "침착하고 분석적이며, 실제로 작동하는 해결책을 빠르게 찾아내는 타입.",
        "reasons": [
            "문제가 생기면 원인과 해결 방법을 살펴봐요.",
            "도구와 기술을 활용해 효율적으로 문제를 해결해요."
        ],
        "match": "ENFJ",
        "match_reason": "실용적인 ISTP와 사람을 이끄는 ENFJ가 서로 다른 강점을 발휘해요."
    },
    "ISFP": {
        "name_ko": "이브이", "name_en": "Eevee", "id": 133,
        "types": ["노말"],
        "features": "감각적이고 다정하며, 자신만의 취향과 자유로운 가능성을 소중히 여기는 타입.",
        "reasons": [
            "주변의 작은 아름다움과 즐거움을 잘 발견해요.",
            "상황에 맞게 자신만의 방식으로 성장할 수 있어요."
        ],
        "match": "ESTJ",
        "match_reason": "유연한 ISFP와 체계적인 ESTJ가 함께하면 아이디어를 실제 결과로 이어 갈 수 있어요."
    },
    "INFP": {
        "name_ko": "무나", "name_en": "Munna", "id": 517,
        "types": ["에스퍼"],
        "features": "상상력이 풍부하고 이상을 중요하게 여기며, 마음속의 의미를 깊이 생각하는 타입.",
        "reasons": [
            "풍부한 상상력으로 다양한 가능성을 떠올려요.",
            "자신과 다른 사람의 감정을 소중하게 여겨요."
        ],
        "match": "ENTJ",
        "match_reason": "이상과 가치를 중시하는 INFP와 실행력 있는 ENTJ가 서로의 꿈을 구체화해요."
    },
    "INTP": {
        "name_ko": "후딘", "name_en": "Alakazam", "id": 65,
        "types": ["에스퍼"],
        "features": "호기심이 많고 논리적이며, 원리와 개념을 깊이 탐구하는 타입.",
        "reasons": [
            "궁금한 것이 생기면 이유와 원리를 파고들어요.",
            "정해진 답보다 새로운 관점과 가능성을 탐색해요."
        ],
        "match": "ESFJ",
        "match_reason": "분석적인 INTP와 관계를 잘 돌보는 ESFJ가 생각과 실천을 연결해요."
    },
    "ESTP": {
        "name_ko": "루카리오", "name_en": "Lucario", "id": 448,
        "types": ["격투", "강철"],
        "features": "대담하고 현실 감각이 뛰어나며, 기회가 오면 빠르게 행동하는 타입.",
        "reasons": [
            "눈앞의 상황을 빠르게 파악하고 대응해요.",
            "도전을 두려워하지 않고 직접 부딪쳐 배워요."
        ],
        "match": "INFJ",
        "match_reason": "즉각 행동하는 ESTP와 깊이 통찰하는 INFJ가 서로의 시야를 넓혀 줘요."
    },
    "ESFP": {
        "name_ko": "피카츄", "name_en": "Pikachu", "id": 25,
        "types": ["전기"],
        "features": "밝고 사교적이며, 주변 사람과 순간의 즐거움을 나누는 것을 좋아하는 타입.",
        "reasons": [
            "에너지가 넘치고 사람들과 어울리는 데서 즐거움을 느껴요.",
            "현재의 순간을 즐기며 주변 분위기를 밝게 만들어요."
        ],
        "match": "ISTJ",
        "match_reason": "활기찬 ESFP와 차분한 ISTJ가 서로에게 즐거움과 안정감을 줄 수 있어요."
    },
    "ENFP": {
        "name_ko": "나옹", "name_en": "Meowth", "id": 52,
        "types": ["노말"],
        "features": "호기심이 많고 재치 있으며, 새로운 사람과 아이디어를 만나는 것을 좋아하는 타입.",
        "reasons": [
            "새로운 경험과 가능성을 발견하는 데 신나요.",
            "재치 있는 표현으로 사람들과 쉽게 친해져요."
        ],
        "match": "INTJ",
        "match_reason": "아이디어가 풍부한 ENFP와 전략적인 INTJ가 상상력을 계획으로 발전시켜요."
    },
    "ENTP": {
        "name_ko": "팬텀", "name_en": "Gengar", "id": 94,
        "types": ["고스트", "독"],
        "features": "재치 있고 도전적이며, 익숙한 생각을 뒤집어 새로운 가능성을 찾는 타입.",
        "reasons": [
            "색다른 관점으로 문제를 바라보는 것을 즐겨요.",
            "재미있는 토론과 기발한 아이디어에 강해요."
        ],
        "match": "ISFJ",
        "match_reason": "새로움을 추구하는 ENTP와 세심한 ISFJ가 서로에게 신선함과 편안함을 더해요."
    },
    "ESTJ": {
        "name_ko": "괴력몬", "name_en": "Machamp", "id": 68,
        "types": ["격투"],
        "features": "체계적이고 추진력이 있으며, 목표를 정하면 팀을 이끌어 결과를 만드는 타입.",
        "reasons": [
            "해야 할 일을 정리하고 계획대로 진행해요.",
            "결정을 내린 뒤 책임감 있게 실행하는 편이에요."
        ],
        "match": "ISFP",
        "match_reason": "체계적인 ESTJ와 유연한 ISFP가 계획과 감각을 조화롭게 활용해요."
    },
    "ESFJ": {
        "name_ko": "푸린", "name_en": "Jigglypuff", "id": 39,
        "types": ["노말", "페어리"],
        "features": "친근하고 협조적이며, 모두가 편안하게 어울리는 분위기를 만드는 타입.",
        "reasons": [
            "사람들을 챙기고 함께하는 활동을 즐겨요.",
            "갈등을 줄이고 서로 잘 지낼 수 있도록 노력해요."
        ],
        "match": "INTP",
        "match_reason": "사람을 챙기는 ESFJ와 분석적인 INTP가 관계와 아이디어 양쪽에서 배울 수 있어요."
    },
    "ENFJ": {
        "name_ko": "라프라스", "name_en": "Lapras", "id": 131,
        "types": ["물", "얼음"],
        "features": "공감 능력이 뛰어나고 격려를 잘하며, 사람들과 함께 성장하는 것을 중요하게 여기는 타입.",
        "reasons": [
            "다른 사람의 장점을 발견하고 응원해요.",
            "공동의 목표를 위해 사람들을 따뜻하게 이끌어요."
        ],
        "match": "ISTP",
        "match_reason": "사람 중심의 ENFJ와 실용적인 ISTP가 서로 다른 관점으로 문제를 해결해요."
    },
    "ENTJ": {
        "name_ko": "망나뇽", "name_en": "Dragonite", "id": 149,
        "types": ["드래곤", "비행"],
        "features": "결단력과 추진력이 강하며, 큰 목표를 세우고 실행하는 것을 좋아하는 타입.",
        "reasons": [
            "목표를 명확하게 정하고 효율적인 길을 찾아요.",
            "어려운 과제도 주도적으로 해결하려고 해요."
        ],
        "match": "INFP",
        "match_reason": "실행력 있는 ENTJ와 가치 중심의 INFP가 서로의 목표에 의미와 추진력을 더해요."
    },
}

# 상단 소개
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">⚡ MBTI로 포켓몬 찾기 ⚡</div>
        <div class="hero-subtitle">
            나의 성격과 닮은 포켓몬은 누구일까요?<br>
            MBTI를 선택하고 나만의 포켓몬을 만나 보세요!
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 🌟 나의 MBTI를 선택해 주세요")
st.write("아래 버튼 중 하나를 누르면 어울리는 포켓몬을 확인할 수 있어요.")

# 선택 상태 관리
if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None

mbti_list = list(POKEMON.keys())

# MBTI 버튼 4개씩 표시
for start in range(0, len(mbti_list), 4):
    cols = st.columns(4)
    for offset, mbti in enumerate(mbti_list[start:start + 4]):
        with cols[offset]:
            if st.button(mbti, key=f"mbti_{mbti}", use_container_width=True):
                st.session_state.selected_mbti = mbti
                st.session_state[f"celebrate_{mbti}"] = True

# 결과 화면
selected = st.session_state.selected_mbti

if selected:
    data = POKEMON[selected]

    if st.session_state.get(f"celebrate_{selected}", False):
        st.balloons()
        st.session_state[f"celebrate_{selected}"] = False

    st.markdown("---")
    st.markdown(f"## 🎉 당신의 포켓몬은 {data['name_ko']}!")

    left, right = st.columns([1, 1.25], gap="large")

    with left:
        image_url = (
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
            f"sprites/pokemon/other/official-artwork/{data['id']}.png"
        )
        st.image(
            image_url,
            caption=f"{data['name_ko']} · {data['name_en']}",
            width=300,
        )

    with right:
        type_pills = "".join(
            f'<span class="pill">{pokemon_type}</span>'
            for pokemon_type in data["types"]
        )

        st.markdown(
            f"""
            <div class="result-card">
                <h2>{data['name_ko']} <span style="font-size: 1rem;">({data['name_en']})</span></h2>
                <p><b>나의 MBTI:</b> {selected}</p>
                <p><b>포켓몬 번호:</b> #{data['id']}</p>
                <p><b>타입:</b> {type_pills}</p>
                <p><b>특징</b><br>{data['features']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 💛 왜 나와 닮았을까요?")
    for reason in data["reasons"]:
        st.markdown(f"- {reason}")

    st.markdown("### 🤝 나와 잘 맞을 수 있는 MBTI")
    st.markdown(f"**{data['match']}** — {data['match_reason']}")

    st.caption(
        "재미를 위한 성격 유형 콘텐츠이며, 실제 성격이나 궁합을 "
        "과학적으로 판정하는 검사는 아니에요."
    )

    if st.button("🔄 다른 MBTI 다시 선택하기", use_container_width=True):
        st.session_state.selected_mbti = None
        st.rerun()
else:
    st.info("👆 MBTI 버튼을 눌러 포켓몬을 확인해 보세요!")

st.markdown("---")
st.markdown(
    '<p class="small-note">Made with 💛 · MBTI × Pokémon</p>',
    unsafe_allow_html=True,
)
