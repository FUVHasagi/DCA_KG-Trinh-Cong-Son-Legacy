import sys

sys.path.append("./nano-graphrag")

from nano_graphrag import GraphRAG, QueryParam

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

graph_func = GraphRAG(working_dir="./KGs/all_song_version1")

# for file in os.listdir('./data/txt_songs'):
#     with open("./data/txt_songs/" + file) as f:
#         graph_func.insert(f.read())
    

# graph_func.update_cluster()


param = QueryParam(mode="local")
# param =QueryParam()
# Perform global graphrag search
# print(graph_func.query("Hãy viết một bài văn phân tích thật cụ thể hình ảnh mẹ trong nhạc của Trịnh Công Sơn", param))

print(graph_func.query("Hãy liệt kê các bài hát có bối cảnh sáng tác vào sự kiện Tết Mậu Thân 1968", param))