from fastapi import FastAPI

from cafe.crawl_blog_router import crawl_blog_router
app = FastAPI()

if __name__ == '__main__':
    print('PyCharm')

origins = ["https://coffeeground.site"]
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # *별 찍으면 안됨! 전부다 허용하겠다는 이야기라
    allow_credentials=True,
    allow_methods=["*"],  # *은 전부다
    allow_headers=["*"],
)
app.include_router(crawl_blog_router)

