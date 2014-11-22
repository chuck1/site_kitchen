import networkx as nx

import kitchen.models




def create():

    G = nx.Graph()
    
    for rec in kitchen.models.Recipe.objects.all():
        G.add_node(rec)

    for itm in kitchen.models.Recipe.objects.all():
        G.add_node(itm)

    for ing in kitchen.models.Ingredient.objects.all():
        G.add_edge(ing.recipe, ing.item, object=ing)

    print(G.number_of_nodes())
    print(G.number_of_edges())


