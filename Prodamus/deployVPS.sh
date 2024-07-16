#!/bin/bash
#wget https://raw.githubusercontent.com/Marat2010/botsAdmin/master/Prodamus/deployVPS.sh && chmod +x deployVPS.sh && ./deployVPS.sh

echo
echo "=== Клонирование проекта ==="
git clone https://github.com/Marat2010/botsAdmin.git
wait

cd botsAdmin/
echo "=== Установка пакетов apt==="
sudo apt update
sudo apt -y install python3-pip
sudo apt -y install mc lynx
#=========================
if [ -n "`dpkg -s nginx | grep 'Status' `" ]
then
   echo "=== Nginx установлен ==="
else
   echo " === Установка Nginx === "
   sudo apt -y install nginx
   sudo systemctl enable nginx
fi
#==========================
echo "=== Установка пакетов из requirements.txt ==="
python3.10 -m pip install --upgrade pip
python3.10 -m pip install -r requirements.txt

echo
echo "====================================================================="
echo "=== Подготовка самоподписанных SSL сертификатов для домена или IP  ===" 
mkdir /etc/ssl/nginx
echo
echo "=== Установка переменных окружения ==="
read -p "=== Введите имя домена или IP адрес сервера VPS: " domain_ip
echo "DOMAIN_IP='$domain_ip'" | sudo tee -a /etc/environment
touch '.env'
echo "DOMAIN_IP=$domain_ip" | sudo tee -a .env
echo "URL_BASE_DOMAIN=https://$domain_ip/prodamus" | sudo tee -a .env

read -p "=== Введите SECRET_KEY_PAYMENT Prodamus-а: " SECRET_KEY_PAYMENT
echo "SECRET_KEY_PAYMENT=$SECRET_KEY_PAYMENT" | sudo tee -a .env

echo "#URL_RETURN=https://a1f8-178-204-220-54.ngrok-free.app/return" | sudo tee -a .env
echo "#URL_SUCCESS=https://a1f8-178-204-220-54.ngrok-free.app/successful" | sudo tee -a .env
echo "#URL_NOTIFICATION=https://prodamus.z2024.site/notificatio" | sudo tee -a .env

echo "# ===== База данных =====" | sudo tee -a .env
echo "DB_SQLITE_NAME=payments.sqlite3" | sudo tee -a .env
echo "# ===== Logs =====" | sudo tee -a .env
echo "LOG_PRODAMUS=verif_pay.log" | sudo tee -a .env

echo
echo "=== Запуск сервиса, службы (SYSTEMD) Prodamus-а ==="
echo
sudo cp Prodamus/payment_verification.service /lib/systemd/system/payment_verification.service
sudo systemctl daemon-reload
sudo systemctl enable payment_verification.service
sudo systemctl start payment_verification.service

echo "#=== Создаем и Копируем сертификаты в папку для Nginx (/etc/ssl/nginx) ==="
openssl req -newkey rsa:2048 -sha256 -nodes -keyout $domain_ip.key -x509 -days 365 -out $domain_ip.crt -subj "/C=RU/ST=RT/L=KAZAN/O=Home/CN=$domain_ip"
sudo mv $domain_ip.key /etc/ssl/nginx/
sudo mv $domain_ip.crt /etc/ssl/nginx/


echo "=== Добавьте настройки в конфигурацию Nginx: ==="
echo "listen 443 ssl; "
echo "ssl_certificate       /etc/ssl/nginx/$domain_ip.crt; "
echo "ssl_certificate_key   /etc/ssl/nginx/$domain_ip.key; "
echo
echo "location /prodamus { "
echo "    proxy_pass http://127.0.0.1:9090; "
echo "}"
echo
echo "=== Перезапустите Nginx: ==="
echo "sudo systemctl daemon-reload"
echo "sudo systemctl restart nginx.service"
echo





