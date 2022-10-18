from utilities import utilities as utils


def generate(
    minimum_number_of_spans: int, maximum_number_of_spans: int
) -> None:

    # Ensure Valid Inputs
    if minimum_number_of_spans < 1:
        return
    elif maximum_number_of_spans < minimum_number_of_spans:
        return

    # Itterate through spans
    for i in range(minimum_number_of_spans, maximum_number_of_spans):
        # Setup Bridge Variables
        elements = [utils.generate_ground_element("left-ground")]
        relationships = [{
            "name": "left-ground-deck-1",
            "type": "boundary",
            "elements": [
                {"name": "left-ground"},
                {"name": "deck-1"}
            ]
        }]
        # Generate Spans
        for j in range(0, i):
            # Generate Deck
            elements.append({
                "name": "deck-{0}".format(j + 1),
                "type": "regular",
                "contextual": {"type": "deck"}
            })
            if j > 0:
                relationships.append({
                    "name": "deck-{0}-deck-{1}".format(j, j + 1),
                    "type": "perfect",
                    "elements": [
                        {"name": "deck-{0}".format(j)},
                        {"name": "deck-{0}".format(j + 1)}
                    ]
                })
            relationships.append({
                "name": "deck-{0}-column-{0}".format(j + 1),
                "type": "joint",
                "nature": {"name": "static", "nature": {"name": "other"}},
                "elements": [
                    {"name": "deck-{0}".format(j + 1)},
                    {"name": "column-{0}".format(j + 1)}
                ]
            })
            # Generate Column
            elements.append({
                "name": "column-{0}".format(j + 1),
                "type": "regular",
                "contextual": {"type": "column"}
            })
            relationships.append({
                "name": "column-{0}-column-ground-{0}".format(j + 1),
                "type": "boundary",
                "elements": [
                    {"name": "column-{0}".format(j + 1)},
                    {"name": "column-ground-{0}".format(j + 1)}
                ]
            })
            # Generate Ground
            elements.append(utils.generate_ground_element("column-ground-{0}".format(j + 1)))

        # Generate Right Ground
        elements.append(utils.generate_ground_element("right-ground"))
        relationships.append({
            "name": "deck-{0}-right-ground".format(i),
            "type": "boundary",
            "elements": [
                {"name": "deck-{0}".format(i)},
                {"name": "right-ground"}
            ]
        })
        # Save Document
        utils.generate_document_and_save(
            "slab-bridge-canonical-form-{0}-span-1-column".format(i),
            "Slab Bridge Canonical Form - {0} span".format(i),
            elements,
            relationships
        )
        # Save Graph
        utils.generate_2d_graph_and_save(
            "slab-bridge-canonical-form-{0}-span-1-column".format(i),
            elements,
            relationships
        )