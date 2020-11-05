# Cellular Automata Pandemic
## Project for ACIT4610 - Evolutionary Artificial Intelligence and Robotics

#### This model is based on Heterogeneous Cellular Automata
The project was to create a evolutionary model for the current covid-19 pandemic. And to see if the model can be realistic and evolve strategies can be used as recommendations or policies for a realistic scenario. 

To run the evolutionary model, just run the 'main.py' file. This will run the evolutionary model, and finish up with running the last values one time to plot results graphs. The constants in const.py is for changing initial values for running the model. 

To run the model just once, run the 'one_run.py' file. The constants in this file is set as the last values we got in our evolutionary algorithm. These can be changed to see how the model works. 

While running 'one_run.py', the model will plot the grid from 'GroupsOfPeople.py' to visualize how the virus spreads. At the end, it will plot the the states for all the people as time steps. 

To just plot the results, use the datafiles in final data, or 'data.json' from your run. Read this file with-save_data.read_from_csv' and use the methods in 'generate_graphs.py'.

Created by Marit Øye Gresdal, Pål Anders Owren and Shayan Yazdanmehr
