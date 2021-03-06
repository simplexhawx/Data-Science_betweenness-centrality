# betweenness-centrality in the road network of the Canton of ZH
import networkx as nx
import geopandas as gpd

# general workspace settings
myworkspace = "/Users/Morris/Documents/2_Uni/2_Master/9_Data science, complex networks/5_PyCharm"

# input data: nodes and edges
nodesfile = myworkspace + "/zh_nodes.shp"
edgesfile = myworkspace + "/zh_roads.shp"

# input data: the roads file
nodesgdf = gpd.read_file(nodesfile)
edgesgdf = gpd.read_file(edgesfile)
floodednodesfile = myworkspace + "/zh_nodes_flooded.shp"
floodededgesfile = myworkspace + "/zh_roads_flooded.shp"

# input data: the flooded nodes and roads files
floodednodesgdf = gpd.read_file(floodednodesfile)
floodededgesgdf = gpd.read_file(floodededgesfile)

# output data: the nodes file
nodesbetweennesscentralityfile = open(myworkspace + "/betweennesscentrality_flooded.csv", "w")
nodesbetweennesscentralityfile.write("nodeid" + ";" + "betweennesscentrality" + "\n")

# output data: the nodes distances file
nodesdistancesfile = open(myworkspace + "/nodesdistancesflooding.csv", "w")
nodesdistancesfile.write("nodeid" + ";" + "distancetoZHsbbFLOOD" + "\n")

# plot the geodata
nodesgdf.plot()
edgesgdf.plot()

# create lists of flooded nodes and flooded edges
listoffloodednodes = floodednodesgdf["nodeid"].unique().tolist()
listoffloodededges = floodededgesgdf["ID_Road"].unique().tolist()
print(str(len(listoffloodednodes)) + " nodes are flooded")
print(str(len(listoffloodededges)) + " road segments are flooded")

# create the networkx graph
G = nx.Graph()
nodesidlist = []
edgesidlist = []

# loop through the road shapefile
counter = 0
for index, row in edgesgdf.iterrows():
    if row.ID_Road not in listoffloodededges:
        # print(counter)
        length = row.SHAPE_Leng
        nodeid1 = row.nodeid1
        nodeid2 = row.nodeid2
        if row.nodeid1 not in listoffloodednodes:
            xcoord = nodesgdf[nodesgdf["nodeid"] == row.nodeid1].x
            ycoord = nodesgdf[nodesgdf["nodeid"] == row.nodeid1].y
            if row.nodeid1 not in G:
                G.add_node(row.nodeid1, pos=(xcoord, ycoord))
                nodesidlist.append(row.nodeid1)
        if row.nodeid2 not in listoffloodednodes:
            xcoord = nodesgdf[nodesgdf["nodeid"] == row.nodeid2].x
            ycoord = nodesgdf[nodesgdf["nodeid"] == row.nodeid2].y
            if row.nodeid2 not in G:
                G.add_node(row.nodeid2, pos=(xcoord, ycoord))
                nodesidlist.append(row.nodeid2)
        edgesidlist.append(row.ID_Road)
        if row.nodeid1 not in listoffloodednodes and row.nodeid2 not in listoffloodednodes:
            G.add_edge(row.nodeid1, row.nodeid2, weight=length)
        counter += 1
print("network graph created ...")

betweennesscentrality = nx.betweenness_centrality(G, k=1000, normalized=True, endpoints=True)

for n in betweennesscentrality:
    nodesbetweennesscentralityfile.write(str(n) + ";" + str(betweennesscentrality[n]) + "\n")
nodesbetweennesscentralityfile.close()
print("betweenness centrality during flooding for nodes in ZH traffic network computed and exported to file ...")
