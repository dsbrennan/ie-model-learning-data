import random as rnd
import math as m
from utilities import utilities as utils


def generate(
        minimum_number_of_spans: int, maximum_number_of_spans: int,
        minimum_number_of_columns: int, maximum_number_of_columns: int,
        minimum_number_of_nodes_per_span: int, maximum_number_of_nodes_per_span: int,
        maximum_deck_width: float, maximum_column_height: float, maximum_span_width: float,
        quantity: int) -> None:
    ''' Generate Slab Bridges in the format of:
    G - S - S - G
          |
          C      
          |
          G

    minimum_number_of_spans: Minimum number of Spans within the bridge, the minimum value must be greater than 0
    maximum_number_of_spans: Maximum number of Spans within the bridge, the maximum value must be greater or equal to the minimum number of spans
    minimum_number_of_columns: Minimum number of Columns within each span, the minimum value must be greater than 0
    maximum_number_of_columns: Maximum number of Columns within each span, the maximum value must be greater or equal to the minimum number of columns
    minimum_number_of_nodes_per_span: Minimum number of Perfectly Relationed Nodes within a Span, the minimum value must be greater than 0
    maximum_number_of_nodes_per_span: Maximum number of Perfectly Relationed Nodes within a Span, the maxium value must be greater or equal to the minimum number of Perfectly Relationed Nodes
    maximum_deck_width: Maximum width of the deck, the minimum value must be greater then 0
    maximum_column_height: Maximum height of the Column, the minimum value must be greater than 0
    maximum_span_width: Maximum Span width, the minium value must be greater than 4
    quantity: Number of bridges to generate
    '''
    # Ensure Valid Inputs
    if minimum_number_of_spans < 1:
        return
    elif maximum_number_of_spans < minimum_number_of_spans:
        return
    if minimum_number_of_columns < 1:
        return
    elif maximum_number_of_columns < minimum_number_of_columns:
        return
    if minimum_number_of_nodes_per_span < 1:
        return
    elif maximum_number_of_nodes_per_span < minimum_number_of_nodes_per_span:
        return
    if maximum_deck_width < 1:
        return
    if maximum_column_height < 1:
        return
    if maximum_span_width < 4:
        return
    # Beam and Slab Types
    material_types = [
        ["metal", "ferrousAlloy"],
        ["metal", "aluminiumAlloy"],
        ["metal", "nickelAlloy"],
        ["metal", "copperAlloy"],
        ["metal", "titaniumAlloy"],
        ["ceramic", "cement"],
        ["composite", "fibre-reinforced"]
    ]
    # Itterate through Quantity
    for i in range(0, quantity):
        # Setup Bridge Variables
        spans = rnd.randint(minimum_number_of_spans, maximum_number_of_spans)
        columns = rnd.randint(minimum_number_of_columns, maximum_number_of_columns)
        height = rnd.randint(1, maximum_column_height)
        width = rnd.randint(1, maximum_deck_width)
        deck_material_index = rnd.randint(0, len(material_types) - 1)
        column_material_index = rnd.randint(0, len(material_types) - 1)
        elements = [utils.generate_ground_element("left-ground")]
        relationships = [{
            "name": "left-ground-deck-1",
            "type": "boundary",
            "elements": [
                {"name": "left-ground"},
                {"name": "deck-1-1"}
            ]
        }]
        total_width = 0
        # Itterate through Spans
        previous_span_sub_sections = 0
        for j in range(0, spans + 1):
            # Setup Span Variables
            span_sub_sections = rnd.randint(minimum_number_of_nodes_per_span, maximum_number_of_nodes_per_span)
            span_width = rnd.randint(4, maximum_span_width)
            maximum_span_column_width = m.floor(span_width / 4 if span_width / 4 < width / (columns + 1) else width / (columns + 1))
            column_width = 1 if maximum_span_column_width < 1 else rnd.randint(1, maximum_span_column_width)
            #Generate Inter Deck Relationship
            if j > 0:
                relationships.append({
                    "name": "deck-{0}-{2}-deck-{1}-1".format(j, j + 1, previous_span_sub_sections),
                    "type": "perfect",
                    "elements": [
                        {"name": "deck-{0}-{1}".format(j, previous_span_sub_sections)},
                        {"name": "deck-{0}-1".format(j + 1)}
                    ],
                    "coordinates": {
                        "global": {
                            "translational": {
                                "x": {"unit": "other", "value": total_width},
                                "y": {"unit": "other", "value": height},
                                "z": {"unit": "other", "value": width / 2}
                            }
                        }
                    }
                })
            # Generate Span Deck Sections
            sub_span_left_over_width = span_width
            for k in range(0, span_sub_sections):
                sub_span_width = rnd.randint(1, sub_span_left_over_width - span_sub_sections + k) if k < span_sub_sections - 1 else sub_span_left_over_width
                # Create Span Deck
                elements.append({
                    "name": "deck-{0}-{1}".format(j + 1, k + 1),
                    "type": "regular",
                    "contextual": {"type": "deck"},
                    "material": {
                        "type": {
                            "name": material_types[deck_material_index][0],
                            "type": {
                                "name": material_types[deck_material_index][1]
                            }
                        }
                    },
                    "coordinates": {
                        "global": {
                            "translational": {
                                "x": {"unit": "other", "value": total_width + span_width - sub_span_left_over_width},
                                "y": {"unit": "other", "value": height},
                                "z": {"unit": "other", "value": 0}
                            }
                        }
                    },
                    "geometry": {
                        "type": {"name": "solid", "type": {"name": "translate", "type": {"name": "cuboid"}}},
                        "dimensions": {
                            "length": {"axis": "x", "source": "nominal", "unit": "other", "value": sub_span_width},
                            "width": {"axis": "z", "source": "nominal", "unit": "other", "value": width},
                            "height": {"axis": "y", "source": "nominal", "unit": "other", "value": 1}
                        }
                    }
                })
                if k > 0:
                    relationships.append({
                        "name": "deck-{0}-{1}-deck-{0}-{2}".format(j + 1, k, k + 1),
                        "type": "perfect",
                        "elements": [
                            {"name": "deck-{0}-{1}".format(j + 1, k)},
                            {"name": "deck-{0}-{1}".format(j + 1, k + 1)}
                        ],
                        "coordinates": {
                            "global": {
                                "translational": {
                                    "x": {"unit": "other", "value": total_width + span_width - sub_span_left_over_width},
                                    "y": {"unit": "other", "value": height},
                                    "z": {"unit": "other", "value": width / 2}
                                }
                            }
                        }
                    })
                sub_span_left_over_width -= sub_span_width
            # Setup Beam & Column Variables
            column_z_offset = (width - (columns * column_width)) / (columns + 1)
            # 0:Aligned to Current Deck, 1: Between Both Decks, 2: Aligned to Next Deck
            column_position = rnd.randint(0, 2)
            # Itterate through Columns
            for k in range(0, columns):
                if j >= spans:
                    break
                # Create Column
                elements.append({
                    "name": "column-{0}-{1}".format(j + 1, k + 1),
                    "type": "regular",
                    "contextual": {"type": "column"},
                    "material": {
                        "type": {
                            "name": material_types[column_material_index][0],
                            "type": {
                                "name": material_types[column_material_index][1]
                            }
                        }
                    },
                    "coordinates": {
                        "global": {
                            "translational": {
                                "x": {"unit": "other", "value": total_width + span_width - (column_width if column_position == 0 else (column_width / 2 if column_position == 1 else 0))},
                                "y": {"unit": "other", "value": 0},
                                "z": {"unit": "other", "value": ((k + 1) * column_z_offset) + (k * column_width)}
                            }
                        }
                    },
                    "geometry": {
                        "type": {"name": "solid", "type": {"name": "translate", "type": {"name": "cuboid"}}},
                        "dimensions": {
                            "length": {"axis": "x", "source": "nominal", "unit": "other", "value": column_width},
                            "width": {"axis": "z", "source": "nominal", "unit": "other", "value": column_width},
                            "height": {"axis": "y", "source": "nominal", "unit": "other", "value":  height}
                        }
                    }
                })
                if column_position <= 1:
                    relationships.append({
                        "name": "deck-{0}-{1}-column-{0}-{2}".format(j + 1, span_sub_sections, k + 1),
                        "type": "joint",
                        "nature": {"name": "static", "nature": {"name": "other"}},
                        "elements": [
                            {
                                "name": "deck-{0}-{1}".format(j + 1, span_sub_sections),
                                "coordinates": {
                                    "global": {
                                        "translational": {
                                            "x": {"unit": "other", "value": total_width + span_width - (column_width / 2 if column_position == 0 else 0)},
                                            "y": {"unit": "other", "value": height},
                                            "z": {"unit": "other", "value": ((k + 1) * column_z_offset) + (k * column_width) + (column_width / 2)}
                                        }
                                    }
                                }
                            },
                            {
                                "name": "column-{0}-{1}".format(j + 1, k + 1),
                                "coordinates": {
                                    "global": {
                                        "translational": {
                                            "x": {"unit": "other", "value": total_width + span_width - (column_width / 2 if column_position == 0 else 0)},
                                            "y": {"unit": "other", "value": height},
                                            "z": {"unit": "other", "value": ((k + 1) * column_z_offset) + (k * column_width) + (column_width / 2)}
                                        }
                                    }
                                }
                            }
                        ]
                    })
                if column_position >= 1:
                    relationships.append({
                        "name": "column-{1}-{2}-deck-{0}-1".format(j + 2, j + 1, k + 1),
                        "type": "joint",
                        "nature": {"name": "static", "nature": {"name": "other"}},
                        "elements": [
                            {
                                "name": "column-{0}-{1}".format(j + 1, k + 1),
                                "coordinates": {
                                    "global": {
                                        "translational": {
                                            "x": {"unit": "other", "value": total_width + span_width + (column_width / 2 if column_position == 2 else 0)},
                                            "y": {"unit": "other", "value": height},
                                            "z": {"unit": "other", "value": ((k + 1) * column_z_offset) + (k * column_width) + (column_width / 2)}
                                        }
                                    }
                                }
                            },
                            {
                                "name": "deck-{0}-1".format(j + 2),
                                "coordinates": {
                                    "global": {
                                        "translational": {
                                            "x": {"unit": "other", "value": total_width + span_width + (column_width / 2 if column_position == 2 else 0)},
                                            "y": {"unit": "other", "value": height},
                                            "z": {"unit": "other", "value": ((k + 1) * column_z_offset) + (k * column_width) + (column_width / 2)}
                                        }
                                    }
                                }
                            }
                        ]
                    })
                # Create Ground
                elements.append(utils.generate_ground_element("column-ground-{0}-{1}".format(j + 1, k + 1)))
                relationships.append({
                    "name": "column-{0}-{1}-column-ground-{0}-{1}".format(j + 1, k + 1),
                    "type": "boundary",
                    "elements": [
                        {"name": "column-{0}-{1}".format(j + 1, k + 1)},
                        {"name": "column-ground-{0}-{1}".format(j + 1, k + 1)}
                    ]
                })
            total_width += span_width
            previous_span_sub_sections = span_sub_sections
        # Create Right Ground
        elements.append(utils.generate_ground_element("right-ground"))
        relationships.append({
            "name": "deck-{0}-{1}-right-ground".format(spans + 1, previous_span_sub_sections),
            "type": "boundary",
            "elements": [
                {"name": "deck-{0}-{1}".format(spans + 1, previous_span_sub_sections)},
                {"name": "right-ground"}
            ]
        })
        # Save Document
        utils.generate_document_and_save(
            "slab-bridge-{0}-{1}-span-{2}-columns".format(i + 1, spans, columns),
            "{0} Spans, {1} Columns, {2} Width, {3} Height\r\nDeck Material: {4} -> {5}\r\nColumn Material: {6} -> {7}".format(
                spans, columns, width, height,
                material_types[deck_material_index][0], material_types[deck_material_index][1],
                material_types[column_material_index][0], material_types[column_material_index][1]
            ),
            elements,
            relationships
        )
        # Save Graph
        utils.generate_2d_graph_and_save(
            "slab-bridge-{0}-{1}-span-{2}-columns".format(i + 1, spans, columns),
            elements,
            relationships
        )
