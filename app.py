import streamlit as st # 小文字のimportに修正
import random
import time

# --- ページ設定 ---
st.set_page_config(page_title="Elemental Core: Master Edition", layout="centered")

# --- 1. カードデータベース (省略なし) ---
CARD_POOL = {
    "🔥ファイア・ラビット": {"elem": "火", "atk": 3, "rar": "C", "eff_type": "none", "val": 0, "desc": "能力なし"},
    "🔥紅蓮の騎士": {"elem": "火", "atk": 5, "rar": "U", "eff_type": "damage", "val": 2, "desc": "登場時:敵に2点ダメージ"},
    "🔥フレイム・ドラゴン": {"elem": "火", "atk": 8, "rar": "R", "eff_type": "damage", "val": 4, "desc": "登場時:敵に4点ダメージ"},
    "🔥爆炎の魔導師": {"elem": "火", "atk": 6, "rar": "SR", "eff_type": "damage", "val": 6, "desc": "登場時:敵に6点の大ダメージ"},
    "🔥不死鳥フェニックス": {"elem": "火", "atk": 10, "rar": "SEC", "eff_type": "heal", "val": 10, "desc": "登場時:自分のHPを10回復"},
    "💧アクア・タートル": {"elem": "水", "atk": 1, "rar": "C", "eff_type": "none", "val": 0, "desc": "高い防御力を持つ"},
    "💧ミスト・ウィザード": {"elem": "水", "atk": 3, "rar": "U", "eff_type": "draw", "val": 1, "desc": "登場時:カードを1枚引く(ATK+1)"},
    "💧氷結の女王": {"elem": "水", "atk": 6, "rar": "R", "eff_type": "debuff", "val": 3, "desc": "登場時:敵の攻撃力を3下げる"},
    "💧深海のリヴァイアサン": {"elem": "水", "atk": 7, "rar": "SR", "eff_type": "draw", "val": 2, "desc": "登場時:カードを2枚引く(ATK+2)"},
    "💧ポセイドン": {"elem": "水", "atk": 11, "rar": "SEC", "eff_type": "draw", "val": 3, "desc": "登場時:カードを3枚引く(ATK+3)"},
    "🌳リーフ・エルフ": {"elem": "木", "atk": 2, "rar": "C", "eff_type": "heal", "val": 3, "desc": "登場時:自分のHPを3回復"},
    "🌳フォレスト・ゴーレム": {"elem": "木", "atk": 4, "rar": "U", "eff_type": "none", "val": 0, "desc": "どっしりと構えている"},
    "🌳大地の精霊": {"elem": "木", "atk": 5, "rar": "R", "eff_type": "mp_boost", "val": 4, "desc": "登場時:次の攻撃力が+4"},
    "🌳エメラルド・レックス": {"elem": "木", "atk": 9, "rar": "SR", "eff_type": "heal", "val": 8, "desc": "登場時:自分のHPを8回復"},
    "🌳世界樹": {"elem": "木", "atk": 3, "rar": "SEC", "eff_type": "heal", "val": 20, "desc": "登場時:自分のHPを20回復"},
    "💎精霊王の審判": {"elem": "無", "atk": 15, "rar": "SEC", "eff_type": "damage", "val": 10, "desc": "登場時:敵に10点ダメージ"},
}

# --- 2. セッション状態の初期化 (★pack_opened_countを追加) ---
if "gold" not in st.session_state:
    st.session_state.gold = 1000 # 2回引けるように少し増やしました
if "collection" not in st.session_state:
    st.session_state.collection = []
if "deck" not in st.session_state:
    st.session_state.deck = []
if "tut_step" not in st.session_state:
    st.session_state.tut_step = 0
if "pack_opened_count" not in st.session_state: # ★これが必要！
    st.session_state.pack_opened_count = 0

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

# --- 4. メインレイアウト ---
st.title("🔥💧🌳 Elemental Core")
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
    st.header("🗃 デッキ構築")
    
    # チュートリアルのロック機能
    if st.session_state.pack_opened_count < 2:
        st.warning("⚠️ まだ戦力が足りません！パックを合計2回引いてからデッキを組みましょう。")
    elif not st.session_state.collection:
        st.warning("カードを1枚も持っていません。")
    else:
        st.write("手持ちのカードから、バトルに出す5枚を選んでください。")
        
        # 重複を除去して選択肢を表示
        options = list(set(st.session_state.collection))
        selected = st.multiselect(
            f"カードを選択 (現在: {len(st.session_state.deck)}枚登録中)", 
            options=options,
            default=st.session_state.deck if all(c in options for c in st.session_state.deck) else []
        )
        
        if st.button("このデッキを保存する"):
            if len(selected) > 0:
                st.session_state.deck = selected
                st.success(f"✅ {len(selected)}枚のカードをデッキに登録しました！")
                # チュートリアルを進める
                if st.session_state.tut_step == 1:
                    st.session_state.tut_step = 2
                time.sleep(1)
                st.rerun()
            else:
                st.error("最低でも1枚はカードを選んでください。")

# --- タブ3: バトルシステム ---
with tab3:
    st.header("⚔️ タクティカル・バトル")
    
    if len(st.session_state.deck) < 1:
        st.error("❌ デッキが設定されていません。『デッキ編集』タブでカードを選んでください。")
    elif st.session_state.tut_step < 2:
        st.warning("⚠️ 先にデッキを保存してチュートリアルを進めましょう！")
    else:
        st.subheader("対戦相手：シャドウ・マスター")
        if st.button("💥 バトル開始！！"):
            player_hp, cpu_hp = 30, 30
            st.write("--- 🛡️ デュエル開始 🛡️ ---")
            
            # ログ表示用のエリア
            battle_log = st.empty()
            log_text = ""
            
            # デッキから最大5枚でターン進行
            battle_cards = st.session_state.deck[:5]
            
            for i, cname in enumerate(battle_cards):
                card = CARD_POOL[cname]
                log_text += f"\n**【ターン {i+1}】 {cname} を召喚！**\n"
                
                # --- 特殊効果の発動ロジック ---
                current_atk = card["atk"]
                
                if card["eff_type"] == "damage":
                    cpu_hp -= card["val"]
                    log_text += f"✨ 特殊能力：敵に {card['val']} の直接ダメージ！\n"
                elif card["eff_type"] == "heal":
                    player_hp += card["val"]
                    log_text += f"✨ 特殊能力：自分のHPを {card['val']} 回復！\n"
                elif card["eff_type"] == "draw":
                    current_atk += card["val"]
                    log_text += f"✨ 特殊能力：魔力充填！今回の攻撃力が {current_atk} に上昇！\n"
                elif card["eff_type"] == "mp_boost":
                    current_atk += card["val"]
                    log_text += f"✨ 特殊能力：大地の咆哮！攻撃力が {current_atk} に上昇！\n"
                elif card["eff_type"] == "debuff":
                    log_text += f"✨ 特殊能力：敵を弱体化させた！（※簡易版のためログのみ）\n"

                # --- 通常攻撃 ---
                cpu_hp -= current_atk
                log_text += f"⚔️ 物理攻撃：敵に {current_atk} ダメージ！ (敵残りHP: {max(0, cpu_hp)})\n"
                
                if cpu_hp <= 0:
                    break # 勝利
                
                # --- CPUの反撃 ---
                cpu_dmg = random.randint(4, 9)
                player_hp -= cpu_dmg
                log_text += f"👾 敵の反撃：{cpu_dmg} ダメージを受けた！ (自分残りHP: {max(0, player_hp)})\n"
                
                if player_hp <= 0:
                    break # 敗北
                
                # 1ターンごとにログを更新して表示（アニメーション効果）
                battle_log.markdown(log_text)
                time.sleep(1.0)

            # 最終結果
            battle_log.markdown(log_text)
            
            if cpu_hp <= 0:
                st.balloons()
                st.success("🏆 VICTORY! 敵を倒しました！ (報酬: 500G)")
                st.session_state.gold += 500
                if st.session_state.tut_step == 2:
                    st.session_state.tut_step = 3
                    st.session_state.gold += 1000 # チュートリアル完了ボーナス
                    st.toast("🌟 チュートリアル完全制覇！ 1000G獲得！")
            elif player_hp <= 0:
                st.error("💀 DEFEAT... 敗北しました。もっと強いカードを引きましょう。")
            else:
                st.warning("⌛ TIME UP! 引き分けです。 (報酬: 100G)")
                st.session_state.gold += 100
            
            # バトル終了後に画面を保持
            st.button("戦績を確認して戻る")
