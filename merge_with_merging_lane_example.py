from flow.core.params import NetParams, SumoParams, EnvParams, InitialConfig, InFlows, SumoLaneChangeParams
from flow.core.params import VehicleParams
from flow.controllers import IDMController
from flow.controllers.lane_change_controllers import SimLaneChangeController
from flow.envs.ring.accel import AccelEnv, ADDITIONAL_ENV_PARAMS
from flow.core.experiment import Experiment
from flow.networks.merge_with_merging_lane import MergeWithMergingLaneNetwork, ADDITIONAL_NET_PARAMS


additional_net_params = ADDITIONAL_NET_PARAMS
# changing additional parameters of the network
# additional_net_params['merging_lane_length'] = 60

vehicles = VehicleParams()
vehicles.add(
    veh_id="human",
    acceleration_controller=(IDMController, {}),
    lane_change_controller=(SimLaneChangeController, {}),
    lane_change_params=SumoLaneChangeParams(lane_change_mode="sumo_default"),
)

# Inflows allow us to simulate open networks where vehicles may enter (and potentially exit)
# the network constantly, such as a section of a highway or of an intersection.
inflow = InFlows()

# inflow of vehicles from top edge
inflow.add(veh_type="human", # this must match one of the types set in the VehicleParams object
           edge="highway", # the name of the edge as it appears on the routes where the inflow will insert vehicles
           vehs_per_hour=1000, # the maximum number of vehicles entering from the edge per hour
           depart_lane="random", # the starting lane of the vehicles
           depart_speed="random") # the initial speed of the vehicles
# inflow of vehicles from bottom edge
inflow.add(veh_type="human",
           edge="merge",
           vehs_per_hour=500,
           depart_lane="random",
           depart_speed="random")

net_params = NetParams(inflows=inflow, additional_params=additional_net_params)

sim_params = SumoParams(render=True, sim_step=0.2)

env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

## specifies parameters that affect the positioning of vehicle in the network at the start of a simulation
initial_config = InitialConfig()

flow_params = dict(
    exp_tag='test_network',
    env_name=AccelEnv,
    network=MergeWithMergingLaneNetwork,
    simulator='traci',
    sim=sim_params,
    env=env_params,
    net=net_params,
    veh=vehicles,
    initial=initial_config,
)

# number of time steps
flow_params['env'].horizon = 10000
exp = Experiment(flow_params)

# run the sumo simulation
_ = exp.run(1)
