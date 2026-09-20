#!/bin/bash
clear
echo "==============================================="
echo "     INTEGRADOR DO BOT (MERCADO PAGO AUTOMÁTICO) "
echo "==============================================="
echo ""

# 1. Verifica se o painel SSHPlus está realmente instalado na máquina
if [ ! -d "/etc/SSHPlus" ]; then
    echo "❌ Erro: O painel de gerenciamento SSHPlus não foi encontrado!"
    echo "Instale o painel na VPS antes de executar este integrador do bot."
    exit 1
fi

# 2. Instala pacotes do PHP essenciais para o bot rodar no PHP 8
echo "⏳ Verificando e instalando pacotes necessários..."
apt update -y && apt install php-curl php-redis redis-server screen wget -y 2>/dev/null
systemctl start redis-server 2>/dev/null

# 3. Cria e limpa o diretório oficial do bot gerenciado pelo painel
mkdir -p /etc/SSHPlus/bot
cd /etc/SSHPlus/bot

# 4. Baixa os arquivos atualizados direto do seu repositório do GitHub
echo "⏳ Baixando arquivos do seu GitHub..."
wget -qO bot.php https://githubusercontent.com
wget -qO Telegram.php https://githubusercontent.com
wget -qO textos.json https://githubusercontent.com

# 5. Solicita as credenciais para criar a comunicação correta
read -p "Digite o Token do seu Bot Telegram: " token_user
read -p "Digite o IP da sua VPS: " ip_user
read -p "Digite o Limite diário de contas grátis (Padrão 100): " limite_user

if [ -z "$limite_user" ]; then limite_user="100"; fi

# 6. Grava as credenciais no arquivo dadosBot.ini dentro da pasta correta
cat << EOF > /etc/SSHPlus/bot/dadosBot.ini
ip="$ip_user"
token="$token_user"
limite="$limite_user"
EOF

# 7. Cria o script de ponte para chamar o comando de criação oficial do painel SSHPlus
cat << 'EOF' > /etc/SSHPlus/bot/gerarusuario.sh
#!/bin/bash
usuario=$1
senha=$2
dias=$3
limite=$4

# Chama o script nativo do SSHPlus responsável por criar contas válidas no sistema
if [ -f /etc/SSHPlus/openssh.sh ]; then
    /etc/SSHPlus/openssh.sh --criar "$usuario" "$senha" "$dias" "$limite"
else
    # Segurança de contingência caso o caminho mude
    useradd -M -s /bin/false "$usuario"
    echo "$usuario:$senha" | chpasswd
fi
EOF
chmod +x /etc/SSHPlus/bot/gerarusuario.sh

# 8. Derruba processos antigos do bot do terminal e inicia a versão atualizada
pkill -f php
screen -dmS bot_ssh php /etc/SSHPlus/bot/bot.php

echo ""
echo "==============================================="
echo " ✅ BOT INTEGRADO AO PAINEL COM SUCESSO!      "
echo "==============================================="
