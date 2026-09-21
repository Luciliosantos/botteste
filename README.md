# Bot Teste


INSTALAÇÃO SOMENTE PARA SCRIPT QUE TENHA BOT TESTE

wget -q https://raw.githubusercontent.com/Luciliosantos/botteste/main/iniciar.sh && chmod +x iniciar.sh && ./iniciar.sh


ATUALIZACAO INICIAR.SH

systemctl stop bot_ssh.service 2>/dev/null && \
wget -qO /root/iniciar.sh https://raw.githubusercontent.com/Luciliosantos/botteste/main/iniciar.sh && \
sed -i 's/\r$//' /root/iniciar.sh && \
bash /root/iniciar.sh


ATUALIZADO BOTSSH

systemctl stop bot_ssh.service 2>/dev/null && \
wget -qO /root/bot/botssh https://raw.githubusercontent.com/Luciliosantos/botteste/main/botssh && \
sed -i 's/\r$//' /root/bot/botssh && \
systemctl daemon-reload && \
systemctl restart bot_ssh.service

Telegrama @NETxx0