import streamlit as st
import random

# --- ページ設定 ---
st.set_page_config(page_title="Elemental Core Online", layout="centered")

# --- 1. 膨大なカードデータベース ---
CARD_POOL = {
    # 火属性 (攻撃)
    "🔥ファイア・ラビット": {"elem": "火", "atk": 3, "rar": "C", "eff": "なし"},
    "🔥紅蓮の騎士": {"elem": "火", "atk": 5, "rar": "U", "eff": "速攻"},
    "🔥フレイム・ドラゴン": {"elem": "火", "atk": 8, "rar": "R", "eff": "全体攻撃"},
    "🔥魔王サウロン": {"elem": "火", "atk": 12, "rar": "SR", "eff": "爆発"},
    "🔥不死鳥フェニックス": {"elem": "火", "atk": 10, "rar": "SEC", "eff": "再生"},
    
    # 水属性 (防御・ドロー)
    "💧アクア・タートル": {"elem": "水", "atk": 1, "rar": "C", "eff": "壁"},
    "💧ミスト・ウィザード": {"elem": "水", "atk": 3, "rar": "U", "eff": "1枚ドロー"},
    "💧氷結の女王": {"elem": "水", "atk": 6, "rar": "R", "eff": "凍結"},
    "💧深海のリヴァイアサン": {"elem": "水", "atk": 7, "rar": "SR", "eff": "2枚ドロー"},
    "💧ポセイドン": {"elem": "水", "atk": 11, "rar": "SEC", "eff": "大津波"},

    # 木属性 (回復・加速)
    "🌳リーフ・エルフ": {"elem": "木", "atk": 2, "rar": "C", "eff": "回復"},
    "🌳フォレスト・ゴーレム": {"elem": "木", "atk": 4, "rar": "U", "eff": "硬化"},
    "🌳大地の精霊": {"elem": "木", "atk": 5, "rar": "R", "eff": "MP加速"},
    "🌳エメラルド・レックス": {"elem": "木", "atk": 9, "rar": "SR", "eff": "回復大"},
    "🌳世界樹": {"elem": "木", "atk": 3, "rar": "SEC", "eff": "無限供給"},
    
    # 光・闇・無 (特殊)
    "✨ホーリー・ナイト": {"elem": "光", "atk": 7, "rar": "R", "eff": "聖域"},
    "💀ダーク・アサシン": {"elem": "闇", "atk": 8, "rar": "R", "eff": "急所攻撃"},
    "💎精霊王の審判": {"elem": "無", "atk": 15, "rar": "SEC", "eff": "全破壊"},
}

# 追加で15枚ほどバリエーション（名前違い・数値違い）を自動生成的に想定
# (ここでは代表的なものをリスト化)

# --- 2. セッション状態の初期化 ---
if "gold" not in st.session_state:
    st.session_state.gold = 1000
if "collection" not in st.session_state:
    st.session_state.collection = []
if "deck" not in st.session_state:
    st.session_state.deck = []

# --- 3. アプリケーション画面 ---
st.title("🎴 Elemental Core Online")
st.sidebar.metric("所持金", f"{st.session_state.gold} G")

tab1, tab2, tab3 = st.tabs(["🎁 パック開封", "🗃 デッキ編集", "⚔️ クエストバトル"])

# --- パック開封タブ ---
with tab1:
    st.header("ラッキーパック (300G)")
    if st.button("パックを購入する"):
        if st.session_state.gold >= 300:
            st.session_state.gold -= 300
            new_cards = random.sample(list(CARD_POOL.keys()), 3)
            st.session_state.collection.extend(new_cards)
            st.balloons()
            cols = st.columns(3)
            for idx, cname in enumerate(new_cards):
                card = CARD_POOL[cname]
                cols[idx].info(f"**{cname}**\n\n{card['rar']}\nATK:{card['atk']}")
        else:
            st.warning("ゴールドが足りません！")

# --- デッキ編集タブ ---
with tab2:
    st.header("あなたのコレクション")
    if st.session_state.collection:
        selected_cards = st.multiselect("対戦で使うカードを5枚選んでください", 
                                        options=list(set(st.session_state.collection)))
        st.session_state.deck = selected_cards
        st.write(f"現在のデッキ枚数: {len(st.session_state.deck)}/5")
    else:
        st.write("まずはパックを引こう！")

# --- バトルタブ ---
with tab3:
    st.header("対戦ステージ")
    if len(st.session_state.deck) < 1:
        st.error("デッキが空です！カードを選んでください。")
    else:
        stage = st.selectbox("ステージ選択", ["初級：草原の魔物", "中級：灼熱の洞窟", "上級：精霊の塔"])
        if st.button("デュエル開始！"):
            # 簡易対戦ロジック
            player_power = sum([CARD_POOL[c]["atk"] for c in st.session_state.deck])
            cpu_power = random.randint(10, 35 if stage == "初級：草原の魔物" else 60)
            
            st.write(f"あなたの総戦力: **{player_power}**")
            st.write(f"敵の総戦力: **{cpu_power}**")
            
            if player_power >= cpu_power:
                st.success("✨ 勝利！報酬 500G ゲット！")
                st.session_state.gold += 500
            else:
                st.error("💀 敗北... 修行して出直そう。")
