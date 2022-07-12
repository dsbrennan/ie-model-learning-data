import json
import os
import os.path
import random as rnd
import networkx as nx
import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import pytz as tz
from datetime import datetime as dt


class utilities:
    """Graph based utilities"""

    # Class Color Variables
    color_dictionary = {}
    available_colors = [name for name in mcolors.TABLEAU_COLORS]
    available_colors.remove("tab:red")
    # Graphics Variables
    fig = None
    # Population Variables
    population = "toylearning"

    @classmethod
    def _generate_graph(cls: type, elements: list, relationships: list) -> nx.graph:
        """Generate a networkx graph from an element and relatioship lists

        elements: a list of IE model elements
        relationships: a list of IE model relationships

        returns: a networkx graph
        """

        # Add Nodes
        graph = nx.Graph()
        for node in elements:
            if(node["type"] == "ground"):
                graph.add_node(node["name"], color="red")
            else:
                node_type = node["contextual"]["type"]
                if node_type not in cls.color_dictionary:
                    if len(cls.available_colors) == 0:
                        cls.available_colors = [name for name in mcolors.CSS4_COLORS]
                    cls.color_dictionary[node_type] = rnd.choice(cls.available_colors)
                    cls.available_colors.remove(cls.color_dictionary[node_type])
                graph.add_node(node["name"], color=cls.color_dictionary[node_type])
        # Add Edges
        for edge in relationships:
            graph.add_edge(
                edge["elements"][0]["name"],
                edge["elements"][1]["name"]
            )
        return graph

    @classmethod
    def generate_2d_graph_and_save(cls: type, name: str, elements: list, relationships: list) -> None:
        """Generate a 2D image representation of the Graph

        name: the name of the IE model
        elements: a list of IE model elements
        relationships: a list of IE model relationships

        """

        # Use NetworkX to generate graph
        graph = utilities._generate_graph(elements, relationships)
        positions = nx.fruchterman_reingold_layout(graph, dim=2)
        colors = nx.get_node_attributes(graph, "color")
        # Use Matplotlib for the Graphics
        # if cls.fig is None:
        cls.fig = plt.figure()
        ax = cls.fig.add_subplot(111)
        for node in graph.nodes:
            ax.scatter(*positions[node].T, s=100, ec="w", color=colors[node])
        for (u, v) in graph.edges:
            ax.plot(*np.transpose((positions[u], positions[v])), color="tab:gray", alpha=0.6)
        node_types = [node["contextual"]["type"] for node in elements if node["type"] == "regular"]
        ax.legend(
            handles=[
                mlines.Line2D([0], [0], marker="o", markersize=12, color="w", markerfacecolor="tab:red", label="ground"),
                *[mlines.Line2D([0], [0], marker="o", markersize=12, color="w", markerfacecolor=cls.color_dictionary[name], label=name) for name in cls.color_dictionary if name in node_types]
            ]
        )
        ax.grid(False)
        ax.axis("off")
        for dim in (ax.xaxis, ax.yaxis):
            dim.set_ticks([])
        cls.fig.tight_layout()
        # Save & Clear
        plt.savefig(f"data/{cls.population}/{name}-2d-graph.jpg", dpi=300)
        cls.fig.clear()

    @classmethod
    def generate_3d_graph_and_save(cls: type, name: str, elements: list, relationships: list) -> None:
        """Generate a 3D image representation of the Graph

        name: the name of the IE model
        elements: a list of IE model elements
        relationships: a list of IE model relationships

        """

        # Use NetworkX to generate positional data
        graph = utilities._generate_graph(elements, relationships)
        positions = nx.spring_layout(graph, dim=3)
        colors = nx.get_node_attributes(graph, "color")
        # Use Matplotlib for the Graphics
        if cls.fig is None:
            cls.fig = plt.figure()
        ax = cls.fig.add_subplot(111, projection="3d")
        for node in graph.nodes:
            ax.scatter(*positions[node].T, s=100, ec="w", color=colors[node])
        for (u, v) in graph.edges:
            ax.plot(*np.transpose((positions[u], positions[v])), color="tab:gray", alpha=0.6)
        node_types = [node["contextual"]["type"] for node in elements if node["type"] == "regular"]
        ax.legend(
            handles=[
                mlines.Line2D([0], [0], marker="o", markersize=12, color="w", markerfacecolor="tab:red", label="ground"),
                *[mlines.Line2D([0], [0], marker="o", markersize=12, color="w", markerfacecolor=cls.color_dictionary[name], label=name) for name in cls.color_dictionary if name in node_types]
            ]
        )
        ax.grid(False)
        ax.axis("off")
        for dim in (ax.xaxis, ax.yaxis, ax.zaxis):
            dim.set_ticks([])
        cls.fig.tight_layout()
        # Save & Clear
        plt.savefig(f"data/{cls.population}/{name}-3d-graph.jpg", dpi=300)
        cls.fig.clear()

    @classmethod
    def generate_document_and_save(cls: type, name: str, description: str, elements: list, relationships: list) -> None:
        """Generate PBSHM Schema Document and Save to file system

        name: the name of the IE model
        description: the description of the IE model
        elements: a list of IE model elements
        relationships: a list of IE model relationships

        """

        # Create Document
        document = {
            "version": "1.1.0",
            "name": name,
            "description": description,
            "population": cls.population,
            "timestamp": utilities.datetime_to_nanoseconds_since_epoch(dt.now()),
            "models": {
                "irreducibleElement": {
                    "type": "grounded",
                    "elements": elements,
                    "relationships": relationships
                }
            }
        }
        # Save Document
        if not os.path.isdir(f"data/{cls.population}"):
            os.mkdir(f"data/{cls.population}")
        with open(f"data/{cls.population}/{name}.json", "w", encoding="utf-8") as fs:
            json.dump(document, fs, indent=4)

    @staticmethod
    def generate_ground_element(name: str) -> dict:
        """Generate a named ground element

        returns: JSON Object
        """

        return {"name": name, "type": "ground"}

    @staticmethod
    def datetime_to_nanoseconds_since_epoch(timestamp: dt) -> int:
        """Convert datetime to nanoseconds since unix epoch

        returns: int
        """

        delta = timestamp.astimezone(tz.utc) - dt.fromtimestamp(0, tz.utc)
        return ((((delta.days * 24 * 60 * 60) + delta.seconds) * 1000000) + delta.microseconds) * 1000
