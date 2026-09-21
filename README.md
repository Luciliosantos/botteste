# Bot Teste


INSTALAÇÃO SOMENTE PARA SCRIPT QUE TENHA BOT TESTE


systemctl stop bot_ssh.service && \
wget -qO /root/bot/botssh https://raw.githubusercontent.com/Luciliosantos/botteste/main/botteste/botssh && \
chmod +x /root/bot/botssh && \
sed -i 's/\r$//' /root/bot/botssh && \
systemctl daemon-reload && \
systemctl restart bot_ssh.service && \
systemctl status bot_ssh.service




Telegrama @NETxx0