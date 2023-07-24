from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

if __name__ == '__main__':
    print("Hello")

origins = ["http://localhost:7777"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_lyrics")
async def get_lyrics(song_title: str):
    song_id = search_song_id(song_title)

    if song_id:
        print(f"The song ID for '{song_title}' is: {song_id}")
    else:
        print("The song ID could not be found.")

    lyrics = get_lyrics_by_song_id(song_id)
    if lyrics:
        print(lyrics)
    else:
        print("가사를 찾을 수 없습니다.")

    return lyrics


def get_lyrics_by_song_id(song_id):
    url = f"https://www.melon.com/song/detail.htm?songId={song_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    lyrics = soup.find("div", class_="lyric")

    if lyrics:
        for br in lyrics.find_all("br"):
            br.replace_with("<br>")
        return lyrics.get_text().strip()

    return None


def search_song_id(title):
    base_url = f"https://www.melon.com/search/song/index.htm?q={title}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&ipath=srch_form"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    song_id_tag = soup.select_one('.btn_icon_detail')

    if song_id_tag is not None:
        song_id = song_id_tag.get('href').split('\'')[9]
        return song_id

    return None