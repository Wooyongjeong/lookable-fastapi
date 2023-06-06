from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.feed import feed_router
from domain.user import user_router
from domain.comment import comment_router

app = FastAPI()

# origins = [
#
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(feed_router.router)
app.include_router(user_router.router)
app.include_router(comment_router.router)
