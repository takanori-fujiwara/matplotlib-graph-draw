import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection

# prepare categorical colormap with tableau color 10
# https://www.tableau.com/about/blog/2016/7/colors-upgrade-tableau-10-56782
tableau10 = {
    'blue': '#507AA6',
    'orange': '#F08E39',
    'red': '#DF585C',
    'teal': '#78B7B2',
    'green': '#5BA053',
    'yellow': '#ECC854',
    'purple': '#AF7BA1',
    'pink': '#FD9EA9',
    'brown': '#9A7460',
    'gray': '#BAB0AC'
}
cate_colors = plt.cm.tab10((np.arange(10)).astype(int))
cate_cmp = ListedColormap(cate_colors)

cmap = {'default': None, 'numeric': 'plasma', 'cate': cate_cmp}


# add edges as line collection in fig
def _draw_edges(fig,
                vertex_positions,
                edges,
                color='#BAB0AC',
                alpha=0.5,
                linewidth=1,
                vertex_filter=None):
    edge_pos = []
    related_vertices = np.copy(vertex_filter)
    if vertex_filter is None:
        edge_pos = np.asarray([(vertex_positions[e[0]], vertex_positions[e[1]])
                               for e in edges])
    else:
        for e in edges:
            related_vertices[e[0]] = vertex_filter[e[0]]
            related_vertices[e[1]] = vertex_filter[e[1]]
            if vertex_filter[e[0]] and vertex_filter[e[1]]:
                edge_pos.append(
                    (vertex_positions[e[0]], vertex_positions[e[1]]))

    edge_collection = LineCollection(edge_pos,
                                     colors=color,
                                     linewidths=linewidth,
                                     antialiaseds=(1, ),
                                     alpha=alpha)
    edge_collection.set_zorder(1)
    ax = fig.add_subplot(1, 1, 1)
    ax.add_collection(edge_collection)

    return related_vertices


def plot_nw(vertex_positions,
            edges,
            marker='o',
            c=tableau10['green'],
            cmap_type='default',
            vertex_size=80,
            vertex_linewidth=None,
            edge_linewidth=1,
            edge_color='#666666',
            vertex_filter=None,
            xlim=None,
            ylim=None,
            out_file_name=None,
            out_dir='./images/'):
    '''
    vertex_positions: 2D vertex positions. shape(number of vertices, 2)
    edges: a pair of source and target node indices. shape(number of edges, 2)
    marker: vertex shape (e.g., 'o': circle, '^': triangle)
    c: default vertex color
    cmap_type: type of color map
        default: vertex is colored with default color or color map
        numeric: vertex is colored by its numeric value
        cate: vertex is colored by its category/class
    vertex_size: vertex size
    vertex_linewidth: vertex line width
    edge_linewidth: edge line width
    edge_color: edge color
    vertex_filter: vertex filter created with graph-tool
    xlim: x-axis range
    ylim: y-axis range
    out_file_name:
        If None, not saving the result. Otherwise, use this as output file name
    out_dir: Output file dir.
    '''
    fig = plt.figure(figsize=(4, 4))

    if vertex_filter is None:
        vertex_filter = np.ones((vertex_positions.shape[0]), dtype=bool)

    vertex_filter = _draw_edges(fig,
                                vertex_positions,
                                edges,
                                linewidth=edge_linewidth,
                                vertex_filter=vertex_filter)

    plt.scatter(vertex_positions[vertex_filter, 0],
                vertex_positions[vertex_filter, 1],
                edgecolors=edge_color,
                linewidths=vertex_linewidth,
                marker=marker,
                c=c if type(c) is str else c[vertex_filter],
                cmap=cmap[cmap_type],
                zorder=2,
                s=vertex_size)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    if out_file_name:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        plt.savefig(out_dir + out_file_name)


if __name__ == '__main__':
    import importlib
    gt_spec = importlib.util.find_spec('graph_tool')
    nx_spec = importlib.util.find_spec('networkx')
    gt_found = gt_spec is not None
    nx_found = nx_spec is not None

    if (not gt_found) and (not nx_found):
        print('to see examples, you need to install graph-tool or NetworkX')

    # 1. Example with graph-tool
    # graph-tool: https://graph-tool.skewed.de/static/doc/quickstart.html
    if gt_found:
        import graph_tool.all as gt
        g = gt.collection.data['polbooks']

        v_pos = gt.sfdp_layout(g)
        # convert graph-tool's pos to 2d numpy array
        v_pos = np.array(list(v_pos))

        # Example 1: default plot
        plot_nw(v_pos, g.get_edges())

        # Example 2: color by PageRank
        centrality = gt.pagerank(g).a
        plot_nw(v_pos, g.get_edges(), c=centrality, cmap_type='numeric')

        # Example 3: color by community
        blocks = gt.minimize_blockmodel_dl(g).get_blocks().a
        plot_nw(v_pos, g.get_edges(), c=blocks, cmap_type='cate')

        # Example 4: with vertex filter
        vertex_filter = centrality > np.median(centrality)
        plot_nw(v_pos,
                g.get_edges(),
                c=centrality,
                cmap_type='numeric',
                vertex_filter=vertex_filter)

    # 2. Example with NetworkX
    # https://networkx.org/
    if nx_found:
        import networkx as nx
        import urllib.request as urllib
        import io
        import zipfile

        url = 'http://www-personal.umich.edu/~mejn/netdata/polbooks.zip'
        s = None
        with urllib.urlopen(url) as sock:
            s = io.BytesIO(sock.read())
        zf = zipfile.ZipFile(s)
        gml = zf.read('polbooks.gml').decode().split('\n')[1:]
        G = nx.parse_gml(gml)
        # use index to indicate nodes and edges
        G = nx.convert_node_labels_to_integers(G)

        v_pos = nx.spring_layout(G)
        # convert networkx's pos to 2d numpy array
        v_pos = np.array(list(v_pos.values()))

        # Example 1: default plot
        plot_nw(v_pos, G.edges())

        # Example 2: color by PageRank
        centrality = nx.pagerank(G)
        # dictionary to numpy array
        centrality = np.array(list(centrality.values()))
        plot_nw(v_pos, G.edges(), c=centrality, cmap_type='numeric')

        # Example 3: color by category
        blocks = np.array([0] * v_pos.shape[0])
        blocks[int(v_pos.shape[0] / 3):] = 1
        blocks[-int(v_pos.shape[0] / 3):] = 2
        plot_nw(v_pos, G.edges(), c=blocks, cmap_type='cate')

        # Example 4: with vertex filter
        vertex_filter = centrality > np.median(centrality)
        plot_nw(v_pos,
                G.edges(),
                c=centrality,
                cmap_type='numeric',
                vertex_filter=vertex_filter)
