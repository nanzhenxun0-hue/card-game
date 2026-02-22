import streamlit as st
import random
import time

# --- ページ設定 ---
st.set_page_config(page_title="Elemental Core: Master Edition", layout="centered")

# --- 1. 究極のカードデータベース (全カード効果付き) ---
CARD_POOL = {
    # 火属性 (攻撃特化)
    "🔥ファイア・ラビット": {"elem": "火", "atk": 3, "rar": "C", "eff_type": "none", "val": 0, "desc": "能力なし"},
    "🔥紅蓮の騎士": {"elem": "火", "atk": 5, "rar": "U", "eff_type": "damage", "val": 2, "desc": "登場時:敵に2点ダメージ"},
    "🔥フレイム・ドラゴン": {"elem": "火", "atk": 8, "rar": "R", "eff_type": "damage", "val": 4, "desc": "登場時:敵に4点ダメージ"},
    "🔥爆炎の魔導師": {"elem": "火", "atk": 6, "rar": "SR", "eff_type": "damage", "val": 6, "desc": "登場時:敵に6点の大ダメージ"},
    "🔥不死鳥フェニックス": {"elem": "火", "atk": 10, "rar": "SEC", "eff_type": "heal", "val": 10, "desc": "登場時:自分のHPを10回復"},
    
    # 水属性 (ドロー・妨害)
    "💧アクア・タートル": {"elem": "水", "atk": 1, "rar": "C", "eff_type": "none", "val": 0, "desc": "高い防御力を持つ"},
    "💧ミスト・ウィザード": {"elem": "水", "atk": 3, "rar": "U", "eff_type": "draw", "val": 1, "desc": "登場時:カードを1枚引く(ATK+1)"},
    "💧氷結の女王": {"elem": "水", "atk": 6, "rar": "R", "eff_type": "debuff", "val": 3, "desc": "登場時:敵の攻撃力を3下げる"},
    "💧深海のリヴァイアサン": {"elem": "水", "atk": 7, "rar": "SR", "eff_type": "draw", "val": 2, "desc": "登場時:カードを2枚引く(ATK+2)"},
    "💧ポセイドン": {"elem": "水", "atk": 11, "rar": "SEC", "eff_type": "draw", "val": 3, "desc": "登場時:カードを3枚引く(ATK+3)"},

    # 木属性 (回復・MP加速)
    "🌳リーフ・エルフ": {"elem": "木", "atk": 2, "rar": "C", "eff_type": "heal", "val": 3, "desc": "登場時:自分のHPを3回復"},
    "🌳フォレスト・ゴーレム": {"elem": "木", "atk": 4, "rar": "U", "eff_type": "none", "val": 0, "desc": "どっしりと構えている"},
    "🌳大地の精霊": {"elem": "木", "atk": 5, "rar": "R", "eff_type": "mp_boost", "val": 4, "desc": "登場時:次の攻撃力が+4"},
    "🌳エメラルド・レックス": {"elem": "木", "atk": 9, "rar": "SR", "eff_type": "heal", "val": 8, "desc": "登場時:自分のHPを8回復"},
    "🌳世界樹": {"elem": "木", "atk": 3, "rar": "SEC", "eff_type": "heal", "val": 20, "desc": "登場時:自分のHPを20回復"},
    
    # 特殊
    "💎精霊王の審判": {"elem": "無", "atk": 15, "rar": "SEC", "eff_type": "damage", "val": 10, "desc": "登場時:敵に10点ダメージ"},
}

# --- 2. セッション状態の初期化 ---
if "gold" not in st.session_state:
    st.session_state.gold = 500
if "collection" not in st.session_state:
    st.session_state.collection = []
if "deck" not in st.session_state:
    st.session_state.deck = []
if "tut_step" not in st.session_state:
    st.session_state.tut_step = 0 

# --- 3. チュートリアル表示 ---
def show_tutorial():
    steps = [
    　　 f"💡 **Step 1: パック開封 ( {st.session_state.pack_opened_count} / 2 )**\nまずは『🎁 パック』タブで、パックを**合計2回**引いて戦力を整えましょう！",
        "💡 **Step 2: デッキ編成**\n次は『🗃 デッキ』タブで、手に入れたカードを5枚選びましょう。",
        "💡 **Step 3: 初陣**\n準備完了！『⚔️ バトル』タブで敵と戦って勝利しましょう！",
        "🌟 **Complete!**\nチュートリアル完了！自由に最強のデッキを目指してください。"
    ]
    if st.session_state.tut_step < 4:
        st.info(steps[st.session_state.tut_step])

# --- 4. メイン画面レイアウト ---
st.title("🔥💧🌳 Elemental Core: Master Edition")
show_tutorial()
st.sidebar.metric("💰 所持金", f"{st.session_state.gold} G")

tab1, tab2, tab3 = st.tabs(["🎁 パック", "🗃 デッキ", "⚔️ バトル"])
# --- タブ1: パック開封 (演出強化版) ---
with tab1:
    st.header("✨ ラッキーパック購入")
    st.write("300Gで3枚のカードをゲット！SRやSECを狙おう！")
    
    if st.button("パックを開封する！！", key="gacha_btn"):
        if st.session_state.gold >= 300:
            st.session_state.gold -= 300
            
            # 1. 抽選 (裏側で行う)
            new_cards = random.sample(list(CARD_POOL.keys()), 3)
            st.session_state.collection.extend(new_cards)
            
            # 2. 演出開始
            st.write("---")
            placeholders = [st.empty() for _ in range(3)] # カード表示用の空枠を3つ作成
            
            # ドラムロール的な待機
            with st.spinner('パックを開封中...'):
                time.sleep(1.5)
            
            # 1枚ずつ時間差で公開！
            for i, cname in enumerate(new_cards):
                card = CARD_POOL[cname]
                rarity = card['rar']
                
                # レアリティによって色と演出を変える
                if rarity == "SEC":
                    color = "inverse"
                    prefix = "🌟🌟 [SECRET] 🌟🌟"
                elif rarity == "SR":
                    color = "primary"
                    prefix = "🔥 [SUPER RARE] 🔥"
                elif rarity == "R":
                    color = "success"
                    prefix = "✨ [RARE] ✨"
                else:
                    color = "secondary"
                    prefix = f"[{rarity}]"

                # じわっと表示される演出
                time.sleep(0.8)
                placeholders[i].markdown(f"""
                <div style="border: 2px solid #ccc; padding: 10px; border_radius: 10px; text-align: center; background-color: rgba(255,255,255,0.1);">
                    <p style="font-size: 0.8rem; color: #aaa;">Card {i+1}</p>
                    <h3 style="margin: 0;">{cname}</h3>
                    <strong style="color: gold;">{prefix}</strong>
                    <p style="font-size: 0.9rem;">ATK: {card['atk']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # レアカードが出た時の追加エフェクト
                if rarity in ["SR", "SEC"]:
                    st.toast(f"すごい！ {cname} が出たぞ！", icon="🎊")

            st.balloons() # 最後に紙吹雪！
            
            # チュートリアル進行
            if st.session_state.tut_step == 0:
                st.session_state.tut_step = 1
            
            time.sleep(0.5)
            st.rerun() # 状態を確定させる
        else:
            st.error("ゴールドが足りません！バトルで勝利して稼ぎましょう。")

# --- タブ2: デッキ編集 ---
with tab2:
    st.header("デッキ構築")
    if not st.session_state.collection:
        st.warning("カードを1枚も持っていません。")
    else:
        selected = st.multiselect("デッキに入れるカードを5枚選択 (現在: " + str(len(st.session_state.deck)) + "枚)", 
                                  options=list(set(st.session_state.collection)),
                                  default=st.session_state.deck if all(c in st.session_state.collection for c in st.session_state.deck) else [])
        if st.button("このデッキを保存する"):
            if len(selected) > 0:
                st.session_state.deck = selected
                st.success(f"{len(selected)}枚のカードをデッキに登録しました！")
                if st.session_state.tut_step == 1:
                    st.session_state.tut_step = 2
                st.rerun()
            else:
                st.error("カードを選んでください。")

# --- タブ3: バトルシステム ---
with tab3:
    st.header("タクティカル・バトル")
    if len(st.session_state.deck) < 1:
        st.error("デッキが空です。デッキ編集でカードを選んでください。")
    else:
        if st.button("💥 バトル開始！"):
            player_hp, cpu_hp = 30, 30
            st.write("--- ⚔️ 戦闘開始 ⚔️ ---")
            
            battle_log = st.empty()
            log_text = ""
            
            # 自分のデッキからランダムにカードを繰り出す（最大5ターン）
            turns = st.session_state.deck[:5]
            for i, cname in enumerate(turns):
                card = CARD_POOL[cname]
                log_text += f"\n**ターン {i+1}: {cname} の攻撃！**\n"
                
                # 特殊効果発動
                if card["eff_type"] == "damage":
                    cpu_hp -= card["val"]
                    log_text += f"✨ 効果発動：敵に {card['val']} ダメージ！\n"
                elif card["eff_type"] == "heal":
                    player_hp += card["val"]
                    log_text += f"✨ 効果発動：自分のHPを {card['val']} 回復！\n"
                elif card["eff_type"] == "draw":
                    card_atk = card["atk"] + card["val"]
                    log_text += f"✨ 効果発動：攻撃力が {card_atk} に上昇！\n"
                elif card["eff_type"] == "mp_boost":
                    card_atk = card["atk"] + card["val"]
                    log_text += f"✨ 効果発動：大地の力で攻撃力が {card_atk} に！\n"
                else:
                    card_atk = card["atk"]

                # 通常ダメージ
                cpu_hp -= card["atk"]
                log_text += f"⚔️ 敵に {card['atk']} ダメージ！ (敵HP: {max(0, cpu_hp)})\n"
                
                if cpu_hp <= 0: break
                
                # CPUの反撃
                cpu_dmg = random.randint(3, 8)
                player_hp -= cpu_dmg
                log_text += f"👾 敵の反撃：{cpu_dmg} ダメージ！ (自HP: {max(0, player_hp)})\n"
                
                if player_hp <= 0: break
                
                battle_log.markdown(log_text)
                time.sleep(0.8)

            battle_log.markdown(log_text)
            if cpu_hp <= 0:
                st.success("🏆 YOU WIN! 500G を獲得しました。")
                st.session_state.gold += 500
                if st.session_state.tut_step == 2:
                    st.session_state.tut_step = 3
                    st.session_state.gold += 1000 # 初回ボーナス
            elif player_hp <= 0:
                st.error("💀 YOU LOSE... もっと強いカードを集めよう。")
            else:
                st.warning("⌛ 引き分け！ 100G 獲得。")
                st.session_state.gold += 100
