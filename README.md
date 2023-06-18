# Vps  Deploy Method

<code>
sudo apt update
sudo apt upgrade -y
sudo apt install git -y
git clone https://github.com/JinnSulthan/QalbaanuFathima.git
cd QalbaanuFathima
sudo apt install python3-pip ffmpeg -y
curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm i -g npm
pip3 install --upgrade pip
pip3 install -U -r requirements.txt
python3 main.py
sudo npm install -g pm2
pm2 start main.py --interpreter=python3 --name=myapp
</code>
