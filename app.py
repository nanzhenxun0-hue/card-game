import streamlit as st
import random
import time

# --- ページ設定 ---
st.set_page_config(page_title="Elemental Core: Master Edition", layout="centered")

# --- 1. カードデータベース ---
CARD_POOL = {
    "🔥ファイア・ラビット": {"elem": "火", "atk": 3, "rar": "C", "eff_type": "none", "val": 0, "desc": "能力なし"},
    "🔥紅蓮の騎士": {"elem": "火", "atk": 5, "rar": "U", "eff_type": "damage", "val": 2, "desc": "登場時:敵に2点ダメージ"},
    "🔥フレイム・ドラゴン": {"elem": "火", "atk": 8, "rar": "R", "eff_type": "damage", "val": 4, "desc": "登場時:敵に4点ダメージ"},
    "🔥爆炎の魔導師": {"elem": "火", "atk": 6, "rar": "SR", "eff_type": "damage", "val": 6, "desc": "登場時:敵に6点の大ダメージ"},
    "🔥不死鳥フェニックス": {"elem": "火", "atk": 10, "rar": "SEC", "eff_type": "heal", "val": 10, "desc": "登場時:自分のHPを10回復"},
    "💧アクア・タートル": {"elem": "水", "atk": 1, "rar": "C", "eff_type": "none", "val": 0, "desc": "高い防御力を持つ"},
    "💧ミスト・ウィザード": {"elem": "水", "atk": 3, "rar": "U", "eff_type": "draw", "val": 1, "desc": "登場時:カードを1枚引く(ATK+1)"},
    "💧氷結の女王": {"elem": "水", "atk": 6, "rar": "R", "eff_type": "debuff", "val": 3, "desc": "登場時:敵の攻撃力を3下げる"},
    "💧ポセイドン": {"elem": "水", "atk": 11, "rar": "SEC", "eff_type": "draw", "val": 3, "desc": "登場時:カードを3枚引く(ATK+3)"},
    "🌳リーフ・エルフ": {"elem": "木", "atk": 2, "rar": "C", "eff_type": "heal", "val": 3, "desc": "登場時:自分のHPを3回復"},
    "🌳大地の精霊": {"elem": "木", "atk": 5, "rar": "R", "eff_type": "mp_boost", "val": 4, "desc": "登場時:次の攻撃力が+4"},
    "🌳世界樹": {"elem": "木", "atk": 3, "rar": "SEC", "eff_type": "heal", "val": 20, "desc": "登場時:自分のHPを20回復"},
    "💎精霊王の審判": {"elem": "無", "atk": 15, "rar": "SEC", "eff_type": "damage", "val": 10, "desc": "登場時:敵に10点ダメージ"},
}

# --- 2. セッション状態の初期化 ---
if "gold" not in st.session_state:
    st.session_state.gold = 1000  # 2パック引けるように初期金を少し調整
if "collection" not in st.session_state:
    st.session_state.collection = []
if "deck" not in st.session_state:
    st.session_state.deck = []
if "pack_opened_count" not in st.session_state:
    st.session_state.pack_opened_count = 0
if "tut_step" not in st.session_state:
    st.session_state.tut_step = 0 

# --- 3. チュートリアル表示 (2パックに変更) ---
def show_tutorial():
    steps = [
        f"💡 **Step 1: パック開封 ( {st.session_state.pack_opened_count} / 2 )**\n『🎁 パック』タブでカードパックを合計**2回**引きましょう！",
        "💡 **Step 2: デッキ編成**\nたくさんのカードが集まりました！『🗃 デッキ』タブで5枚選びましょう。",
        "💡 **Step 3: 初陣**\n準備完了！『⚔️ バトル』タブで敵と戦って勝利しましょう！",
        "🌟 **Complete!**\nチュートリアル完了！自由に最強のデッキを目指してください。"
    ]
    if st.session_state.tut_step < 4:
        st.info(steps[st.session_state.tut_step])

# --- 4. メインレイアウト ---
st.title("🎴 Elemental Core: Master Edition")
show_tutorial()
st.sidebar.metric("💰 所持金", f"{st.session_state.gold} G")

tab1, tab2, tab3 = st.tabs(["🎁 パック", "🗃 デッキ", "⚔️ バトル"])

# --- タブ1: パック開封 (演出あり & カウント機能) ---
with tab1:
    st.header("✨ ラッキーパック開封")
    if st.button("パックを購入する (300G)"):
        if st.session_state.gold >= 300:
            st.session_state.gold -= 300
            st.session_state.pack_opened_count += 1
            
            # 抽選
            new_cards = random.sample(list(CARD_POOL.keys()), 3)
            st.session_state.collection.extend(new_cards)
            
            # 演出
            placeholders = [st.empty() for _ in range(3)]
            with st.spinner('パックを開封中...'):
                time.sleep(1.2)
            
            for i, cname in enumerate(new_cards):
                card = CARD_POOL[cname]
                rar = card['rar']
                time.sleep(0.7)
                placeholders[i].markdown(f"""
                <div style="border: 2px solid #555; padding: 10px; border-radius: 10px; text-align: center; background-color: #222; margin-bottom: 10px;">
                    <p style="color: gold; font-weight: bold; margin:0;">{rar}</p>
                    <h3 style="margin: 5px 0;">{cname}</h3>
                    <p style="font-size: 0.8rem; margin:0;">{card['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.balloons()
            
            # 2パック引いたらステップ更新
            if st.session_state.tut_step == 0 and st.session_state.pack_opened_count >= 2:
                st.session_state.tut_step = 1
                st.toast("ステップ1 クリア！デッキを作りましょう。")
            
            time.sleep(1)
            st.rerun()
        else:
            st.error("ゴールドが足りません！")

# --- タブ2: デッキ編集 ---
with tab2:
    st.header("デッキ構築")
    if st.session_state.pack_opened_count < 2:
        st.warning("まずはパックを2回引いてカードを集めてください。")
    else:
        selected = st.multiselect("カードを5枚選択してください", 
                                  options=list(set(st.session_state.collection)),
                                  default=st.session_state.deck)
        if st.button("このデッキを保存"):
            if len(selected) >= 1:
                st.session_state.deck = selected
                st.success("デッキを保存しました！")
                if st.session_state.tut_step == 1:
                    st.session_state.tut_step = 2
                st.rerun()
            else:
                st.error("カードを選んでください。")

# --- タブ3: バトル --- (前回の高度なロジックを継承)
with tab3:
    st.header("バトル開始")
    if len(st.session_state.deck) < 1:
        st.error("デッキが空です。")
    else:
        if st.button("💥 デュエル！"):
            # 演出用に中身は簡略化していますが、以前の全ログ表示も可能です
            player_p = sum([CARD_POOL[c]["atk"] for c in st.session_state.deck])
            cpu_p = random.randint(10, 40)
            
            with st.spinner('バトル中...'):
                time.sleep(2)
            
            st.write(f"あなたの戦力: {player_p} vs 敵の戦力: {cpu_p}")
            if player_p >= cpu_p:
                st.success("勝利！報酬 500G")
                st.session_state.gold += 500
                if st.session_state.tut_step == 2:
                    st.session_state.tut_step = 3
                    st.session_state.gold += 1000
            else:
                st.error("敗北...")
            st.rerun()
