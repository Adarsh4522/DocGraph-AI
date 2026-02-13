import networkx as nx

def build_mindmap(chunks):
    G = nx.Graph()

    for chunk in chunks:
        words = chunk.split()
        if len(words) > 3:
            G.add_edge(words[0], words[1])

    return G
