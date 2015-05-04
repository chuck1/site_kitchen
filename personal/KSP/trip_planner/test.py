
import networkx as nx

G=nx.DiGraph()

def add_edge(g, a, b, w):
    g.add_edge(a, b, weight=w)

def add_edge_bi(g, a, b, w):
    add_edge(g, a, b, w)
    add_edge(g, b, a, w)

G.add_edge("Kerbin",           "Low Kerbin Orbit", weight=4550)
G.add_edge("Low Kerbin Orbit", "Kerbin SOI Edge",  weight=950)

G.add_edge("Low Kerbin Orbit", "Minmus intercept", weight=930+340)

add_edge_bi(G, "Minmus intercept", "Low Minmus Orbit", 160)

G.add_edge("Low Minmus Orbit", "Minmus",           weight=180)
G.add_edge("Minmus",           "Low Minmus Orbit", weight=180)

G.add_edge("Minmus intercept", "Kerbin SOI Edge",  weight= 20)



G.add_edge("Low Kerbin Orbit", "Mun intercept",    weight=860)
G.add_edge("Mun intercept",    "Low Mun Orbit",    weight=310)
G.add_edge("Low Mun Orbit",    "Mun",              weight=580)

G.add_edge("Kerbin SOI Edge",       "Duna intercept",        weight=130+10)
G.add_edge("Duna intercept",        "Elliptical Duna Orbit", weight=250)
G.add_edge("Elliptical Duna Orbit", "Low Duna Orbit",        weight=360)
G.add_edge("Low Duna Orbit",         "Duna",                  weight=0)

G.add_edge("Duna",                  "Low Duna Orbit",                weight=1400)
G.add_edge("Low Duna Orbit",        "Elliptical Duna Orbit",        weight= 360)
G.add_edge("Elliptical Duna Orbit", "Ike Intercept",                weight=  30)
G.add_edge("Ike Intercept",         "Low Ike Orbit",                weight= 180)
G.add_edge("Low Ike Orbit",         "Ike",                          weight= 390)


l = ["Kerbin", "Low Kerbin Orbit", "Minmus", "Duna", "Ike"]

for i in range(0,len(l)-1):
    print nx.dijkstra_path_length(G, l[i], l[i+1])








