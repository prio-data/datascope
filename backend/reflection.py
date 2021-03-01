import networkx as nx

def join_graph(tables):
    """
    Returns the join-graph for a database
    """
    g = nx.DiGraph()
    for t in tables.values():
        for fk in t.foreign_keys:
            references_table = [t for t in tables.values() if fk.references(t)][-1]
            g.add_edge(t.name,
                    references_table.name,
                    reference=fk.parent.name,
                    referent=fk.column.name
                )
    return g
