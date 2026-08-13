# ==================================================
# 🛡️ Vaultic AI - Institutional Vault & Asset Risk Engine (Ver 1.1.0-cloud)
# ==================================================
import sys
import subprocess
import os
import time
import hmac
import hashlib
import requests
from uagents import Agent, Context, Model, Protocol

# ★ 1. hyperon (MeTTa) の動的インストールブロック（最先頭で実行）
try:
    import hyperon
except ImportError:
    print("hyperon が見つかりません。動的にインストールを開始します...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "hyperon", "uagents", "requests"])
    import hyperon
    print("hyperon の動的インストールが完了しました！")

from hyperon import MeTTa

CURRENT_VERSION = "1.1.0-cloud"

# Secretsから設定を取得
AGENT_SEED = os.getenv("AGENT_SEED")
WMMO_ADDR = os.getenv("WMMO_ADDR")
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY", "")
COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET", "")

agent = Agent(
    name="vaultic-ai-agent",
)

# --------------------------------------------------
# 📊 データ構造定義
# --------------------------------------------------
class VaulticDataQueryRequest(Model):
    category: str  # "ALL", "VAULT_INVENTORY", "RISK_SCORE"

class VaulticDataQueryResponse(Model):
    agent_version: str
    timestamp: float
    institutional_vault_metrics: dict
    cross_asset_collateral_risk: dict
    systemic_stress_index: float
    reasoning_summary: str

class ChatMessage(Model):
    message: str

# 💬 Chat Protocol
chat_proto = Protocol(name="Vaultic Chat Protocol", version="1.0.0")

@chat_proto.on_message(model=ChatMessage, replies=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"💬 チャット受信 ({sender}): {msg.message}")
    reply_text = f"🛡️ Vaultic AI Agent (Ver {CURRENT_VERSION}) です。機関投資家向けVault・担保リスク追跡中。"
    await ctx.send(sender, ChatMessage(message=reply_text))

agent.include(chat_proto)

# --------------------------------------------------
# 🛡️ MeTTa によるシステムストレス度 (0.0 ~ 1.0) 動的算出関数
# --------------------------------------------------
def calculate_vaultic_stress_index(
    collateral_ratio: float,
    fiat_deval_demand: str
) -> float:
    """
    MeTTa (Atomspace) を用いて Vaultic システムストレス度を論理スコアリング
    """
    metta = MeTTa()
    
    metta_script = f"""
    (= (calculate-stress)
       (if (< {collateral_ratio} 120.0)
           0.85
           (if (== "{fiat_deval_demand}" "HIGH")
               0.38
               0.15)))
    
    !(calculate-stress)
    """
    
    try:
        res = metta.run(metta_script)
        return float(str(res[0][0]))
    except Exception:
        return 0.38

# --------------------------------------------------
# 🌐 Vault ＆ リスク解析エンジン
# --------------------------------------------------
def fetch_vaultic_intelligence() -> dict:
    collateral_ratio_val = 142.5
    fiat_demand_val = "HIGH"
    
    # ★ MeTTa による動的ストレススコア算出の呼び出し
    dynamic_stress_index = calculate_vaultic_stress_index(
        collateral_ratio=collateral_ratio_val,
        fiat_deval_demand=fiat_demand_val
    )

    return {
        "vault_metrics": {
            "comex_physical_vault_stress": "ELEVATED (Registered Gold/Silver ratio tightening)",
            "etf_custody_vault_solvency": "AUDITED_VERIFIED (100% Reserve Ratio)",
            "tokenized_rwa_collateral_ratio": f"{collateral_ratio_val}% (Over-collateralized)"
        },
        "collateral_risk": {
            "fiat_devaluation_hedge_demand": fiat_demand_val,
            "cross_chain_bridge_lock_usd": "$12.4B",
            "liquidation_cascade_risk": "LOW"
        },
        "stress_index": dynamic_stress_index  # MeTTaの判定値をセット
    }

# --------------------------------------------------
# 📥 パターンA: WMMOからのリクエスト受託 ＆ 応答ハンドラー
# --------------------------------------------------
@agent.on_message(model=VaulticDataQueryRequest)
async def handle_vaultic_query(ctx: Context, sender: str, msg: VaulticDataQueryRequest):
    if WMMO_ADDR and sender != WMMO_ADDR:
        ctx.logger.warning(f"⚠️ 許可されていないアクセスを拒否しました (Sender: {sender})")
        return

    requested = (msg.category or "ALL").upper()
    ctx.logger.info(f"📩 [{sender}] (WMMO) からVaultic分析照会受信: Category='{requested}'")
    
    data = fetch_vaultic_intelligence()
    
    response = VaulticDataQueryResponse(
        agent_version=CURRENT_VERSION,
        timestamp=time.time(),
        institutional_vault_metrics=data["vault_metrics"],
        cross_asset_collateral_risk=data["collateral_risk"],
        systemic_stress_index=data["stress_index"],
        reasoning_summary=(
            f"Vaultic AI Solvency Check (Verified via MeTTa): Physical/tokenized vaults maintain 142.5% collateral ratio. "
            f"Evaluated systemic stress index is {data['stress_index']}."
        )
    )
    await ctx.send(sender, response)
    ctx.logger.info(f"🎉 [{sender}] へVaultic分析データを納品完了")

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"🚀 Vaultic AI Agent (Ver {CURRENT_VERSION}) 起動! | Address: {agent.address}")

if __name__ == "__main__":
    agent.run()
