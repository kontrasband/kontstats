export PATH=/bin:/usr/bin:/usr/local/bin;
cd ~/Documents/gitProjects/stats;
source ./kont_venv/bin/activate;
cd src/;
python kontstats.py -c config.ini;