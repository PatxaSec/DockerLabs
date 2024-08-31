echo "Instalando..."

curl -L https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz -o geckodriver.tar.gz > /dev/null 2>&1
tar -xzf geckodriver.tar.gz > /dev/null 2>&1
chmod +x geckodriver
sudo mv geckodriver /usr/bin
echo "export PATH=\$PATH:/usr/bin/geckodriver" >> ~/.profile
source ~/.profile

echo "Instalado con exito! reinicia el sistema."
