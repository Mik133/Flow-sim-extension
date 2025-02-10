from flow.networks.base import Network

ADDITIONAL_NET_PARAMS = {
    "edges_length": 100,
    "num_lanes": 1,
    "speed_limit": 30,
}

class SimpleIntersectionNetwork(Network):

    def specify_nodes(self, net_params):

        length = net_params.additional_params["edges_length"]

        nodes = [
            {"id": "center", "x": 0, "y": 0}, #, "type": "priority"},
            {"id": "top", "x": 0, "y": length}, #, "type": "priority"},
            {"id": "bottom", "x": 0, "y": -1 * length}, #, "type": "priority"},
            {"id": "left", "x": -1 * length, "y": 0}, #, "type": "priority"},
            {"id": "right", "x": length, "y": 0} #, "type": "priority"},
        ]
        return nodes

    def specify_edges(self, net_params):

        edgelen = net_params.additional_params["edges_length"]
        # this will let us control the number of lanes in the network
        lanes = net_params.additional_params["num_lanes"]
        # speed limit of vehicles in the network
        speed_limit = net_params.additional_params["speed_limit"]

        edges = [
            {
                "id": "left_in",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "left",
                "to": "center",
                "length": edgelen,
            },
            {
                "id": "left_out",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "center",
                "to": "left",
                "length": edgelen,
            },
            {
                "id": "right_out",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "center",
                "to": "right",
                "length": edgelen,
            },
            {
                "id": "right_in",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "right",
                "to": "center",
                "length": edgelen,
            },
            {
                "id": "top_out",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "center",
                "to": "top",
                "length": edgelen,
            },
            {
                "id": "top_in",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "top",
                "to": "center",
                "length": edgelen,
            },
            {
                "id": "bottom_out",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "center",
                "to": "bottom",
                "length": edgelen,
            },
            {
                "id": "bottom_in",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "bottom",
                "to": "center",
                "length": edgelen,
            }
        ]
        return edges

    def specify_routes(self, net_params):

        rts = { "bottom_in": [(["bottom_in", "right_out"], 1 / 3),
                              (["bottom_in", "top_out"], 1 / 3),
                              (["bottom_in", "left_out"], 1 / 3)],
                "top_in": [(["top_in", "right_out"], 1 / 3),
                           (["top_in", "bottom_out"], 1 / 3),
                           (["top_in", "left_out"], 1 / 3)],
                "left_in": [(["left_in", "right_out"], 1 / 3),
                            (["left_in", "top_out"], 1 / 3),
                            (["left_in", "bottom_out"], 1 / 3)],
                "right_in": [(["right_in", "left_out"], 1 / 3),
                             (["right_in", "top_out"], 1 / 3),
                             (["right_in", "bottom_out"], 1 / 3)]
               }
        return rts

    def specify_edge_starts(self):
        length = self.net_params.additional_params["edges_length"]

        edgestarts = [
            ("left_in", 0), ("left_out", length),
            ("right_in", 2 * length), ("right_out", 3 * length),
            ("top_in", 4 * length), ("top_out", 5 * length),
            ("bottom_in", 6 * length), ("bottom_out", 7 * length)
        ]
        return edgestarts
