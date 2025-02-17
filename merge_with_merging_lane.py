from flow.networks.base import Network
import numpy as np


ADDITIONAL_NET_PARAMS = {
    # length of the merge edge
    "merge_length": 100,
    # length of the highway leading to the merge
    "highway_pre_merge_length": 100,
    # length of the merging lane
    "merging_lane_length": 50,
    # length of the highway past the merge
    "highway_post_merge_length": 100,
    # number of lanes in the merge
    "merge_lanes": 1,
    # number of lanes in the highway
    "highway_lanes": 1,
    # max speed limit of the highway
    "highway_speed_limit": 30,
    # max speed limit of the merge
    "merge_speed_limit": 30,
}

class MergeWithMergingLaneNetwork(Network):
    def specify_nodes(self, net_params):

        highway_pre_merge_length = net_params.additional_params["highway_pre_merge_length"]
        highway_post_merge_length = net_params.additional_params["highway_post_merge_length"]
        merging_lane_length = net_params.additional_params["merging_lane_length"]
        merge_length = net_params.additional_params["merge_length"]

        nodes = [
            {"id": "highway_in", "x": -highway_pre_merge_length, "y": 0},
            {"id": "merge_in", "x": -merge_length / np.sqrt(2), "y": -merge_length / np.sqrt(2)},
            {"id": "merging_lane_in", "x": 0, "y": 0},
            {"id": "merging_lane_out", "x": merging_lane_length, "y": 0},
            {"id": "highway_out", "x": merging_lane_length + highway_post_merge_length, "y": 0}
        ]
        return nodes

    def specify_edges(self, net_params):

        highway_lanes = net_params.additional_params["highway_lanes"]
        merge_lanes = net_params.additional_params["merge_lanes"]
        highway_speed_limit = net_params.additional_params["highway_speed_limit"]
        merge_speed_limit = net_params.additional_params["merge_speed_limit"]
        highway_pre_merge_length = net_params.additional_params["highway_pre_merge_length"]
        highway_post_merge_length = net_params.additional_params["highway_post_merge_length"]
        merging_lane_length = net_params.additional_params["merging_lane_length"]
        merge_length = net_params.additional_params["merge_length"]

        edges = [
            {
                "id": "highway_in",
                "numLanes": highway_lanes,
                "speed": highway_speed_limit,
                "from": "highway_in",
                "to": "merging_lane_in",
                "length": highway_pre_merge_length,
            },
            {
                "id": "merge",
                "numLanes": merge_lanes,
                "speed": merge_speed_limit,
                "from": "merge_in",
                "to": "merging_lane_in",
                "length": merge_length,
            },
            {
                "id": "merging_lane",
                "numLanes": highway_lanes + 1,
                "speed": highway_speed_limit,
                "from": "merging_lane_in",
                "to": "merging_lane_out",
                "length": merging_lane_length,
            },
            {
                "id": "highway_out",
                "numLanes": highway_lanes,
                "speed": highway_speed_limit,
                "from": "merging_lane_out",
                "to": "highway_out",
                "length": highway_post_merge_length,
            }
        ]
        return edges

    def specify_routes(self, net_params):

        rts = { "highway": ["highway_in", "merging_lane", "highway_out"],
                "merge": ["merge", "merging_lane", "highway_out"]
               }
        return rts

    def specify_edge_starts(self):
        highway_pre_merge_length = self.net_params.additional_params["highway_pre_merge_length"]
        highway_post_merge_length = self.net_params.additional_params["highway_post_merge_length"]
        merging_lane_length = self.net_params.additional_params["merging_lane_length"]
        merge_length = self.net_params.additional_params["merge_length"]

        highway_in_start = 0
        merging_lane_start = highway_pre_merge_length
        highway_out_start = highway_pre_merge_length + merging_lane_length
        merge_start = highway_pre_merge_length + merging_lane_length + highway_post_merge_length

        edgestarts = [
            ("highway_in", highway_in_start),
            ("merging_lane", merging_lane_start),
            ("highway_out", highway_out_start),
            ("merge", merge_start)
        ]
        return edgestarts
