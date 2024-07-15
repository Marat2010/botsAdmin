#wget https://raw.githubusercontent.com/Marat2010/botsAdmin/master/Prodamus/deployVPS.sh && chmod +x deployVPS.sh && ./deployVPS.sh


echo
echo "=== Клонирование проекта ==="
git clone https://github.com/Marat2010/botsAdmin.git
wait

cd botsAdmin/
echo "=== Установка пакетов из requirements ==="
python3.10 -m pip install --upgrade pip
python3.10 -m pip install -r requirements.txt



echo
echo "=== Подготовка самоподписанных SSL сертификатов для домена или IP  ===" 
mkdir /etc/ssl/nginx

echo
read -p "=== Введите имя домена или IP адрес сервера VPS: " domain_ip
echo "=== Установка переменных окружения ==="
echo "DOMAIN_IP='$domain_ip'" | sudo tee -a /etc/environment

openssl req -newkey rsa:2048 -sha256 -nodes -keyout $domain_ip.key -x509 -days 365 -out $domain_ip.crt -subj "/C=RU/ST=RT/L=KAZAN/O=Home/CN=$domain_ip"

#=== Копируем сертификаты в папку для Nginx (/etc/ssl/nginx) ===
sudo mv $domain_ip.key /etc/ssl/nginx/
sudo mv $domain_ip.crt /etc/ssl/nginx/

echo
echo "=== Запуск сервиса, службы (SYSTEMD) Prodamus-а ==="
echo
sudo cp Prodamus/payment_verification.service /lib/systemd/system/payment_verification.service
sudo systemctl daemon-reload
sudo systemctl enable payment_verification.service
sudo systemctl start payment_verification.service


echo "=== Добавьте настройки в конфигурацию Nginx: ==="
echo "listen 443 ssl; "
echo "ssl_certificate       /etc/ssl/nginx/$domain_ip.crt; "
echo "ssl_certificate_key   /etc/ssl/nginx/$domain_ip.key; "
echo
echo "location /Prodamus { "
echo "    proxy_pass http://127.0.0.1:9090 "
echo "}"
echo
echo "=== Перезапустите Nginx: ==="
echo "sudo systemctl daemon-reload"
echo "sudo systemctl restart nginx.service"
echo





