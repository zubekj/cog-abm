#!/bin/bash
# argument 1: suffix nazwy symulacji, np normal
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
	sh call_simulation_move_results.sh "../cog_abm/extras/wordanalysis/input_xmls/synthetic_cube_data/simulation_cube_"$1".xml" "cube_"$1""$i
done

