import numpy as np
import sys
from tqdm import tqdm

sys.path.append("../../")

from ReacherSoft3D.MuscleTorquesWithBspline.set_environment import Environment


# User defined condition for exiting the simulation
def user_defined_condition_function(reward, systems, time):
    """
    This function will be defined by the user. Depending on
    the controller requirements and system states, with returning
    done=True boolean, simulation can be exited before reaching
    final simulation time. This function is thought for stopping the
    simulation if desired reward is reached.
    Parameters
    ----------
    reward: user defined reward
    systems: [shearable rod, rigid_rod] classes
    time: current simulation time

    Returns
    -------
    done: boolean
    """
    done = False
    # rod = systems[0]  # shearable rod or cyber-octopus
    # cylinder = systems[1]  # rigid body or target object
    if time > 20.0:
        done = True

    return done


def main():
    # Set simulation final time
    final_time = 3.0

    env = Environment(final_time, number_of_control_points=6, COLLECT_DATA_FOR_POSTPROCESSING=True,)

    # Do multiple simulations for learning, or control
    for i_episodes in range(1):

        # Reset the environment before the new episode and get total number of simulation steps
        total_steps, systems = env.reset()

        # Simulation loop starts
        time = np.float64(0.0)
        user_defined_condition = False
        # activation = [
        #     np.vstack(
        #         (
        #             np.linspace(0, 1.0, 8),
        #             np.array([0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0]),
        #         )
        #     )
        # ]
        activation = [ np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])]

        reward = 0.0

        for i_sim in tqdm(range(total_steps)):

            """ Learning loop """
            # Reward and activation does not have to be computed or updated every simulation step.
            # Simulation time step is chosen to satisfy numerical stability of Elastica simulation.
            # However, learning time step can be larger. For example in the below if loop,
            # we are updating activation every 200 step.
            if i_sim % 200:
                """ Use systems for observations """
                # Observations can be rod parameters and can be accessed after every time step.
                # shearable_rod.position_collection = position of the elements ( here octopus )
                # shearable_rod.velocity_collection = velocity of the elements ( here octopus )
                # rigid_body.position_collection = position of the rigid body (here target object)

                """Reward function should be here"""
                # User has to define his/her own reward function
                reward = 0.0
                """Reward function should be here"""

                """ Compute the activation signal and pass to environment """
                # Based on the observations and reward function, have the learning algorithm
                # update the muscle activations. Make sure that the activation arrays are packaged
                # properly. See the segment_activation_function function defined above for an
                # example of manual activations.
                # activation = [
                #     np.vstack(
                #         (
                #             np.linspace(0, 1.0, 8),
                #             np.array([0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0]),
                #         )
                #     )
                # ]
                activation = [np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])]

            if i_sim > 20000:
                # activation = [
                #     np.vstack(
                #         (
                #             np.linspace(0, 1.0, 8),
                #             10 * np.array([0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0]),
                #         )
                #     )
                # ]
                activation = [10*np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])]

            # Do one simulation step. This function returns the current simulation time,
            # systems which are shearable rod (octopus) and rigid body, and done condition.
            time, systems, done = env.step(activation, time)

            """ User defined condition to exit simulation loop """
            # Below function has to be defined by the user. If user wants to exit the simulation
            # after some condition is reached before simulation completed, user
            # has to return a True boolean.
            user_defined_condition = user_defined_condition_function(
                reward, systems, time
            )
            if user_defined_condition == True:
                print(" User defined condition satisfied, exit simulation")
                print(" Episode finished after {} ".format(time))
                break

            # If done=True, NaN detected in simulation.
            # Exit the simulation loop before, reaching final time
            if done:
                print(" Episode finished after {} ".format(time))
                break

        print("Final time of simulation is : ", time)
        # Simulation loop ends

        # Post-processing
        # Make a video of octopus for current simulation episode. Note that
        # in order to make a video, COLLECT_DATA_FOR_POSTPROCESSING=True
        env.post_processing(
            filename_video="arm_simulation_with_beta_spline_muscle_torques.mp4",
            # The following parameters are optional
            x_limits=(-1.0, 1.0),  # Set bounds on x-axis
            y_limits=(-1.0, 1.0),  # Set bounds on y-axis
            z_limits=(-0.05, 1.00),  # Set bounds on z-axis
            dpi=100,  # Set the quality of the image
            vis3D=True,  # Turn on 3D visualization
            vis2D=True,  # Turn on projected (2D) visualization
        )

    return env


if __name__ == "__main__":
    env = main()
