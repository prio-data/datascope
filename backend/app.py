
import networkx as nx
import fastapi as fa
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests

from decorators import cache_to_file
from reflection import join_graph
import db
import settings

app = fa.FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"]
)

@app.get("/graph")
@cache_to_file("cache/graph.json")
def return_join_graph():
    return nx.json_graph.node_link_data(join_graph(db.Meta.tables))

if settings.PRODUCTION:
    app.mount("/static",StaticFiles(directory="static"),name="static")
else:
    @app.get("/static/{file:path}")
    def proxy_dev_server(r:fa.Request, file:str):
        rsp=requests.get(settings.DEVSERVER+file)
        return fa.Response(
                content=rsp.content,
                media_type=rsp.headers["Content-Type"],
                status_code=rsp.status_code
                )

