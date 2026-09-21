#!/bin/bash
 clear
 echo "==============================================="
 echo "   INSTALADOR AUTOMÁTICO - REPOSITÓRIO TURBO   "
 echo "==============================================="
 echo ""
 # Garante que a VPS tem o php-curl instalado para o bot rodar
 apt update -y && apt install php-curl wget screen -y 2>/dev/null
 # Acessa a pasta do bot e limpa resquícios antigos
 mkdir -p /root/bot
 cd /root/bot
 # Baixa os novos arquivos direto do seu GitHub correto
 wget -qO botssh https://raw.githubusercontent.com/Luciliosantos/botteste/main/botssh
 wget -qO textos.json https://raw.githubusercontent.com/Luciliosantos/botteste/main/textos.json
 # Cria o arquivo de mensagens local de contingência caso falhe
 cat << 'EOF' > /root/bot/textos.json
 {
   "start": "😊 Para comprar sua SSH/EHI de 30 dias entre para nosso grupo de vendas @NETxx0 , você também pode ganhar uma renda extra com o nosso Painel de Revenda",
   "sshgratis": {
     "nao_criado": "🙃 Você já criou uma conta SSH hoje volte amanhã :)",
     "limite": "👽 Atingimos o limite de contas por hoje volte amanhã :)"
   }
 }
 EOF
 # Pergunta os dados na tela para o usuário configurar a máquina nova
 read -p "Digite o Token do seu Bot Telegram: " token_user
 read -p "Digite o IP da sua VPS: " ip_user
 read -p "Digite o Limite diário de contas grátis (Padrão 100): " limite_user
 if [ -z "$limite_user" ]; then limite_user="100"; fi
 # Grava automaticamente o arquivo de configurações
 cat << EOF > /root/bot/dadosBot.ini
 ip="$ip_user"
 token="$token_user"
 limite="$limite_user"
 EOF
 # Cria o arquivo gerarusuario.sh acoplado ao painel SSHPlus
 cat << 'EOF' > /root/bot/gerarusuario.sh
 #!/bin/bash
 usuario=$1
 senha=$2
 dias=$3
 limite=$4
 if [ -f /etc/SSHPlus/openssh.sh ]; then
     /etc/SSHPlus/openssh.sh --criar "$usuario" "$senha" "$dias" "$limite"
 else
     useradd -M -s /bin/false "$usuario"
     echo "$usuario:$senha" | chpasswd
 fi
 EOF
 chmod +x /root/bot/gerarusuario.sh
 # Limpa o cache pendente do Telegram usando os dados coletados
 php -r '$i=parse_ini_file("dadosBot.ini"); $link="https://api.telegram.org/bot".$i["token"]."/deleteWebhook?drop_pending_updates=true"; file_get_contents($link);' 2>/dev/null
 # Desliga processos velhos e inicia o bot limpo em segundo plano
 pkill -f php
 screen -dmS bot_ssh php /root/bot/botssh
 echo ""
 echo "==============================================="
 echo " ✅ INSTALAÇÃO COMPLETA E BOT ATIVO NO SCREEN! "
 echo "==============================================="