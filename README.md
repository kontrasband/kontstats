# Kontstats
Gathering, displaying and keeping track of stats for <a href='https://www.instagram.com/kontrasband/'>Kontras</a>.


## Getting started

### 1. Clone the repo

```
git clone //github.com/kontrasband/stats.git
```

### 2. Create virtual environment

```
virtualenv -p /usr/local/bin/python3 venv
```

### 3. Activate virtual environment

```
source venv/bin/activate
```

### 4. Install `requirements.txt`

```
pip install -r requirements.txt
```

### 5. Setup `config.ini`

Paste `config.ini` in `src/` directory

## Config.ini

```
[SPOTIFY]
CLIENT_ID = 
CLIENT_SECRET = 
KONTRAS_URI = spotify:artist:13mo5g6PR09u3Rq8bEstY2

[INSTAGRAM]
KONT_USERNAME = 
KONT_PASSWORD = 

[GOOGLE]
KEY_FILE = 
API_KEY = 
```

## Watch out for

+ ffmpeg needs to be installed
+ only tested on MacOS Mojave

## API Config

ToDo

### Spotify

### Instagram
Using the the <a href='https://github.com/LevPasha/Instagram-API-python.git`'>InstagramAPI</a> package to interact with Instagram. Required `ffmpeg` to be install. On MacOS you can install `ffmpeg` by running:

```bash
brew install ffmpeg
```

For the first time logging in you'll have to generate some cookies. Instructions <a href='https://github.com/LevPasha/Instagram-API-python/issues/718#issuecomment-569419605'>here</a>. 

### Facebook

### Apple Music

### Youtube

