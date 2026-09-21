# Bot Teste


INSTALAÇÃO SOMENTE PARA SCRIPT QUE TENHA BOT TESTE

✅ COMANDO DE INSTALAÇÃO COMPLETA (VPS NOVA)
 
Copia tudo de uma vez, cola e dá Enter — faz TUDO sozinho:

apt update -y && apt upgrade -y && \
apt install -y php wget curl ca-certificates && \
mkdir -p /root/bot && cd /root/bot && \
wget -qO botssh https://raw.githubusercontent.com/Luciliosantos/botteste/main/botteste/botssh && \
chmod +x botssh && sed -i 's/\r$//' botssh && \
echo "✅ Arquivos baixados!"


⚠️ Depois disso, você PRECISA criar os arquivos de configuração:
 
1. Cria o  dadosBot.ini  — coloca seus dados reais:

nano /root/bot/dadosBot.ini

Cola dentro:  ip=SEU_IP_DO_SERVIDOR
token=SEU_TOKEN_DO_TELEGRAM
limite=10


Salva:  Ctrl+O  →  Enter  →  Ctrl+X 
 
2. Cria o  textos.json  (mensagens personalizadas):

Cola dentro:  
{
  "start": "🤖 Bem-vindo ao Gerenciador SSH!"
}

Salva igual acima.
 
3. Cria o serviço pra iniciar sozinho:

cat << 'EOF' > /etc/systemd/system/bot_ssh.service
[Unit]
Description=Bot Telegram SSH
After=network.target

[Service]
User=root
WorkingDirectory=/root/bot
ExecStart=/usr/bin/php /root/bot/botssh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload && \
systemctl enable bot_ssh.service && \
systemctl start bot_ssh.service && \
systemctl status bot_ssh.service


📌 RESUMO — O que fazer em VPS NOVA:
 
Tabela   
Passo O que faz 
1 Roda o comando de instalação no topo ⬆️ 
2 Edita  dadosBot.ini  com IP e Token 
3 Cria o serviço com o último comando 
4 Pronto! Bot rodando e inicia sozinho ✅ 
 
 
 
🔄 Para ATUALIZAR depois (em qualquer VPS):
 
Sempre que alterar no GitHub, cola:

ATUALIZAR 1
systemctl stop bot_ssh.service && \
wget -qO /root/bot/botssh https://raw.githubusercontent.com/Luciliosantos/botteste/main/botteste/botssh && \
chmod +x /root/bot/botssh && sed -i 's/\r$//' /root/bot/botssh && \
systemctl daemon-reload && systemctl restart bot_ssh.service && \
echo "✅ ATUALIZADO!"





COMANDO DE ATUALIZACAO

systemctl stop bot_ssh.service && \
wget -qO /root/bot/botssh https://raw.githubusercontent.com/Luciliosantos/botteste/main/botteste/botssh && \
chmod +x /root/bot/botssh && \
sed -i 's/\r$//' /root/bot/botssh && \
systemctl daemon-reload && \
systemctl restart bot_ssh.service && \
systemctl status bot_ssh.service




Telegrama @NETxx0