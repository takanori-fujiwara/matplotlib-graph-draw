# Drawing a graph/network with matplotlib

<img src="images/example.png">

About
-----
* Function for drawing a graph with matplotlib.
  * Using matplotlib's LineCollection to draw edges relatively fast.
  * Various visual encodings for graph vertices (e.g., colored by numerical and categorical values)
  * Other custom settings, including vertex filtering, saving files, etc.
  * Graph examples made with this function can be found in: Fujiwara et al., [Network Comparison with Interpretable Contrastive Network Representation Learning](https://jdssv.org/index.php/jdssv/%20article/view/56), JDSSV, 2022

Requirements
-----
* Python 3
* Numpy and matplotlib

Usage
-----
* See the documentation of 'plot_nw' in 'graph_draw.py'
* Also, you can find examples using graph-tool and NetworkX in 'graph_draw.py'.

  `python3 graph_draw.py`

  * graph-tool: https://graph-tool.skewed.de/

    * With HomeBrew, you can install with `brew install graph-tool`

  * NetworkX: https://networkx.org/

    * With pip, you can install with `pip3 install networkx`
