import pandas as pd
import json

from pprint import pprint 
import matplotlib.pyplot as plt

import networkx as nx
from networkx.readwrite import json_graph

from read_sheet import read_sheet


def create_cytoscape_json():
    G = nx.DiGraph()

    # data_df = pd.read_csv("https://gist.github.com/minesh1291/b516a4aac90af07a00761d34c13eaa79/raw/81343e2e211064cacc310f7b756d3c41ac5373d8/edgelist.csv")
    # G.add_edges_from(data_df[["source","target"]].values)

    data_df = pd.read_csv("data_df.csv", index_col=0)

    data_df = data_df[["Skills","Domain"]].dropna()
    data_df["Domain"] = data_df["Domain"].str.split(", ")
    data_df = data_df.explode("Domain")

    # ignore comments
    data_df = data_df[~data_df["Skills"].str.contains("#")]

    data_df["Skills"] = data_df["Skills"].str.split(", ")
    data_df = data_df.explode("Skills")

    G.add_edges_from(data_df.values)
    print(data_df)

    nodes = pd.concat([data_df["Skills"], data_df["Domain"]])
    nodes_cnt = pd.DataFrame(nodes.value_counts().rename("node_size"))
    nodes_dict = nodes_cnt.to_dict(orient="index")

    nx.set_node_attributes(G,nodes_dict,"graphics")

    # subax1 = plt.subplot(121)
    # nx.draw(G, with_labels=True, font_weight='bold')

    # nx.draw_random(G)
    # nx.draw_circular(G)
    # nx.draw_spectral(G, with_labels=True)
    # nx.draw_shell(G, with_labels=True)
    # plt.show()

    # json_graph.adjacency_data(G)
    d = json_graph.cytoscape_data(G)
    # json_graph.tree_data(G,root=1)


    # pprint(d,indent=1)
    # d

    f = open("data.json","w")
    f.write("data = "+ json.dumps(d))
    f.close()


def main():
    read_sheet()
    create_cytoscape_json()


if __name__ == "__main__":
    main()
