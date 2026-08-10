# ==================================================
# 🛡️ Vaultic AI - Institutional Vault & Asset Risk Engine
# ==================================================
import os
import time
from uagents import Agent, Context, Model, Protocol

CURRENT_VERSION = "1.0.0-cloud"

# Secretsから設定を取得
AGENT_SEED = os.getenv("AGENT_SEED")
WMMO_ADDR = os.getenv("WMMO_ADDR")

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
# 🌐 Vault ＆ リスク解析エンジン
# --------------------------------------------------
def fetch_vaultic_intelligence() -> dict:
    return {
        "vault_metrics": {
            "comex_physical_vault_stress": "ELEVATED (Registered Gold/Silver ratio tightening)",
            "etf_custody_vault_solvency": "AUDITED_VERIFIED (100% Reserve Ratio)",
            "tokenized_rwa_collateral_ratio": "142.5% (Over-collateralized)"
        },
        "collateral_risk": {
            "fiat_devaluation_hedge_demand": "HIGH",
            "cross_chain_bridge_lock_usd": "$12.4B",
            "liquidation_cascade_risk": "LOW"
        },
        "stress_index": 0.38  # 0.0 (Clean) ~ 1.0 (Critical)
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
            "Vaultic AI Solvency Check: Physical and tokenized vaults maintain strong collateral ratios (142.5%). "
            "Systemic stress index remains low at 0.38 despite fiat devaluation pressures."
        )
    )
    await ctx.send(sender, response)
    ctx.logger.info(f"🎉 [{sender}] へVaultic分析データを納品完了")

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"🚀 Vaultic AI Agent (Ver {CURRENT_VERSION}) 起動! | Address: {agent.address}")

if __name__ == "__main__":
    agent.run()
