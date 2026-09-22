import asyncio
import requests
from datetime import datetime
from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync

# ================ PREENCHA TUDO AQUI ================
SSID = "COLA_SEU_SSID_AQUI"
TELEGRAM_TOKEN = "TOKEN_NOVO_DO_BOT_COPIADOR"
TELEGRAM_CHAT_ID = "SEU_NUMERO_DE_ID_TELEGRAM"

VALOR_POR_OPERACAO = 1.00
MIN_ACERTO = 65
MIN_DIAS_ATIVO = 7
MAX_PERDA_SEGUIDA = 3
IS_DEMO = True
# ======================================================

def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensagem,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        })
    except Exception as e:
        print(f"[ERRO TELEGRAM] {e}")

class CopiadorBot:
    def __init__(self):
        self.client = None
        self.trader_alvo = None
        self.ultima_op_id = None
        self.perdas_seguidas = 0
        self.ganhos = 0
        self.total_ops = 0
        self.rodando = True

    async def conectar(self):
        try:
            self.client = PocketOptionAsync(ssid=SSID, is_demo=IS_DEMO)
            await self.client.connect()
            saldo = await self.client.balance()
            tipo = "📊 CONTA DE TESTE" if IS_DEMO else "💰 CONTA REAL"
            enviar_telegram(
                f"✅ <b>CONECTADO COM SUCESSO</b>\n"
                f"{tipo}\n"
                f"💵 Saldo: ${saldo:.2f}\n"
                f"🔍 Buscando melhor trader..."
            )
            return True
        except Exception as e:
            enviar_telegram(f"❌ ERRO DE CONEXÃO:\n{str(e)}\n\nVerifique o SSID!")
            return False

    async def buscar_melhor_trader(self):
        try:
            ranking = await self.client.get_ranking(limit=50)
            if not ranking or 'list' not in ranking:
                return None

            aprovados = []
            for t in ranking['list']:
                acerto = t.get('win_rate', 0) * 100
                dias = t.get('days_active', 0)
                ops = t.get('trades_count', 0)

                if acerto >= MIN_ACERTO and dias >= MIN_DIAS_ATIVO and ops >= 30:
                    aprovados.append({
                        'id': t.get('user_id'),
                        'nome': t.get('name', 'Anônimo'),
                        'acerto': round(acerto, 1),
                        'dias': dias,
                        'operacoes': ops,
                        'lucro': t.get('profit', 0)
                    })

            if not aprovados:
                return None
            aprovados.sort(key=lambda x: x['acerto'], reverse=True)
            return aprovados[0]
        except Exception as e:
            print(f"[ERRO RANKING] {e}")
            return None

    async def monitorar(self, trader_id):
        try:
            async for op in self.client.subscribe_trader(trader_id):
                if not self.rodando:
                    break

                op_id = op.get('id')
                if op_id == self.ultima_op_id:
                    continue
                self.ultima_op_id = op_id

                ativo = op.get('asset')
                direcao = op.get('direction')
                tempo = op.get('duration', 60)

                if not ativo or not direcao:
                    continue

                if self.perdas_seguidas >= MAX_PERDA_SEGUIDA:
                    enviar_telegram(f"🛑 PAUSADO — {MAX_PERDA_SEGUIDA} perdas seguidas. Reiniciando em 5 min...")
                    await asyncio.sleep(300)
                    self.perdas_seguidas = 0
                    continue

                enviar_telegram(
                    f"📋 <b>OPERAÇÃO DETECTADA — COPIANDO</b>\n"
                    f"👤 Trader: {self.trader_alvo['nome']}\n"
                    f"📈 Acerto: {self.trader_alvo['acerto']}%\n"
                    f"────────────────────\n"
                    f"💹 Ativo: {ativo}\n"
                    f"📊 Direção: {'🟢 COMPRA (CALL)' if direcao=='call' else '🔴 VENDA (PUT)'}\n"
                    f"⏱️ Tempo: {tempo}s\n"
                    f"💵 Valor: ${VALOR_POR_OPERACAO:.2f}"
                )

                status, resp = await self.client.buy(
                    amount=VALOR_POR_OPERACAO,
                    asset=ativo,
                    direction=direcao,
                    duration=tempo
                )

                if not status:
                    enviar_telegram(f"❌ Falha ao copiar:\n{resp}")
                    continue

                await asyncio.sleep(tempo + 3)
                ganhou = await self.client.check_win(resp['id'])
                self.total_ops += 1

                if ganhou:
                    self.ganhos += 1
                    self.perdas_seguidas = 0
                    enviar_telegram(
                        f"✅ <b>OPERAÇÃO CONCLUÍDA — GANHOU</b>\n"
                        f"Lucro: +${VALOR_POR_OPERACAO * 0.85:.2f}\n"
                        f"────────────────────\n"
                        f"Total: {self.ganhos}/{self.total_ops}"
                    )
                else:
                    self.perdas_seguidas += 1
                    enviar_telegram(
                        f"🔴 <b>OPERAÇÃO CONCLUÍDA — PERDEU</b>\n"
                        f"Valor: -${VALOR_POR_OPERACAO:.2f}\n"
                        f"────────────────────\n"
                        f"Perdas seguidas: {self.perdas_seguidas}/{MAX_PERDA_SEGUIDA}"
                    )
        except Exception as e:
            enviar_telegram(f"⚠️ Erro no monitoramento:\n{str(e)}\nReconectando...")
            await asyncio.sleep(10)

    async def iniciar(self):
        if not await self.conectar():
            return

        while self.rodando:
            if not self.trader_alvo:
                self.trader_alvo = await self.buscar_melhor_trader()

                if self.trader_alvo:
                    enviar_telegram(
                        f"🏆 <b>TRADER SELECIONADO</b>\n"
                        f"Nome: {self.trader_alvo['nome']}\n"
                        f"✅ Acerto: {self.trader_alvo['acerto']}%\n"
                        f"📅 Dias: {self.trader_alvo['dias']}\n"
                        f"🔄 Copiando agora..."
                    )
                else:
                    enviar_telegram("⏳ Nenhum trader qualificado. Aguardando 60s...")
                    await asyncio.sleep(60)
                    continue

            await self.monitorar(self.trader_alvo['id'])
            self.trader_alvo = None
            await asyncio.sleep(5)

if __name__ == "__main__":
    bot = CopiadorBot()
    try:
        asyncio.run(bot.iniciar())
    except KeyboardInterrupt:
        enviar_telegram("🛑 Bot parado pelo usuário")
        print("Encerrado.")
