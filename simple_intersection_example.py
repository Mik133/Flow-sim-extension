from flow.networks.simple_intersection import SimpleIntersectionNetwork, ADDITIONAL_NET_PARAMS
from flow.core.params import NetParams, SumoParams, EnvParams, InitialConfig, InFlows
from flow.core.params import VehicleParams, SumoLaneChangeParams
from flow.controllers import IDMController, SimLaneChangeController
from flow.envs.ring.accel import AccelEnv, ADDITIONAL_ENV_PARAMS
from flow.core.experiment import Experiment


additional_net_params = ADDITIONAL_NET_PARAMS
# changing additional parameters of the network
# additional_net_params['edges_length'] = 60

vehicles = VehicleParams()
vehicles.add(
    veh_id="human",
    acceleration_controller=(IDMController, {}),
    lane_change_controller=(SimLaneChangeController, {}),
    lane_change_params=SumoLaneChangeParams(lane_change_mode="sumo_default") # execute all changes unless in conflict with TraCI
)

# Inflows allow us to simulate open networks where vehicles may enter and potentially exit
inflow = InFlows()

# inflow of vehicles from top edge
inflow.add(veh_type="human", # this must match one of the types set in the VehicleParams object
           edge="top_in", # the name of the edge as it appears on the routes where the inflow will insert vehicles
           vehs_per_hour=200, # the maximum number of vehicles entering from the edge per hour
           depart_lane="random", # the starting lane of the vehicles
           depart_speed="random") # the initial speed of the vehicles
# inflow of vehicles from bottom edge
inflow.add(veh_type="human",
           edge="bottom_in",
           vehs_per_hour=300,
           depart_lane="random",
           depart_speed="random")
# inflow of vehicles from right edge
inflow.add(veh_type="human",
           edge="right_in",
           vehs_per_hour=400,
           depart_lane="random",
           depart_speed="random")
# inflow of vehicles from left edge
inflow.add(veh_type="human",
           edge="left_in",
           vehs_per_hour=100,
           depart_lane="random",
           depart_speed="random")

net_params = NetParams(inflows=inflow, additional_params=additional_net_params) # using the default of ADDITIONAL_NET_PARAMS

sim_params = SumoParams(render=True, sim_step=0.2) # define 'render=True' to open sumo-gui and see the simulation

env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

# specifies parameters that affect the positioning of vehicle in the network at the start of a simulation
initial_config = InitialConfig()

flow_params = dict(
    exp_tag='test_network',
    env_name=AccelEnv,
    network=SimpleIntersectionNetwork,
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
