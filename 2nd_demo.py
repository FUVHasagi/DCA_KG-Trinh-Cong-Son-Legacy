import sys

sys.path.append("./nano-graphrag")

from nano_graphrag import GraphRAG, QueryParam
from nano_graphrag._storage import Neo4jStorage


# Api key handling
import importlib.util
import sys
import os
spec = importlib.util.spec_from_file_location("OPAI_api", "/home/comrade/bach/TCS_KG_LLM/data/creds.py")
key = importlib.util.module_from_spec(spec)


sys.modules["OPAI_api"] = key
spec.loader.exec_module(key)
os.environ['OPENAI_API_KEY']=key.OPAI_api


# GraphRAG here
sys.path.append("./")

neo4j_config = {
  "neo4j_url": os.environ.get("NEO4J_URL", "neo4j://localhost:7687"),
  "neo4j_auth": (
      os.environ.get("NEO4J_USER", "neo4j"),
      os.environ.get("NEO4J_PASSWORD", "Thaibach"),
  ),
   "neo4j_database_name": os.environ.get("NEO4J_DATABASE_NAME", "neo4j://localhost:7687")
}

graph_func = GraphRAG(working_dir="./KGs/demo_2", graph_storage_cls=Neo4jStorage, addon_params=neo4j_config)

for file in os.listdir('./data/txt_songs_sampled'):
    # print(file)
    with open("./data/txt_songs_sampled/" + file) as f:
        graph_func.insert(f.read())

param = QueryParam(mode="local")
# param =QueryParam()
# Perform global graphrag search
print(graph_func.query("Hãy viết một bài văn phân tích thật cụ thể bài hát Biển nghìn thu ở lại", param))