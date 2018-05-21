# Space Queen

### Trajectory simulation and parameter fitting for Space Queen design phase.

Space Queen was the winner of [UCLA 2017 Aerospace Engineering Capstone competition](https://www.mae.ucla.edu/space-queen-wins-the-mae-157a-design-build-launch-competition/).

The main.py file is the entry point for all usage. Use `--mode <mode>`with one of the following strings to specify program behavior:
* trajectory
* mass-curve
* validation
* angle-compare
* stat-table

#### Trajectory analysis with plotting

`python main.py --mode "trajectory" -p`


#### Mass curve fitting

`python main.py --mode "mass-curve"`


#### Getting help

`python main.py -h`
