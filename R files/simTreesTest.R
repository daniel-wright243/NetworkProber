library(TreeSimGM)
library(ape)

sim_function <- function(sim_numsim, sim_n, sim_m, filepath) {
	mytree <- sim.taxa(numbsim=sim_numsim, n=sim_n, m=sim_m, waitsp="rweibull(0.1,1)", waitext="rexp(0.5)", symmetric=FALSE, complete = FALSE)

	sim_tree_arr <- mytree

	for (x in 1:sim_numsim) {
		sim_tree_arr[[x]]$edge.length <- NULL
		file_name = paste(x, "simTree.nex", sep="")
		full_file_path = paste(filepath, file_name, sep="")
		write.nexus(sim_tree_arr[[x]], file=full_file_path)
	}
}

generate_trees <- function(leaf_set_array, subset_size, path) {
	for(x in leaf_set_array){
		folder_name = paste(x, "Leaves")
		dir.create(file.path(path, folder_name))
		filepath = file.path(path, folder_name)
		filepath_concat = paste(filepath, "/", sep = "")
		sim_function(subset_size, x/4, x, filepath_concat)
	}
}

leaf_set_array <- c(10,15,20,25,30,35)
subset_size = 100
path = "C:/Users/danwr/OneDrive - University of East Anglia/Documents/PhD Files/Reformatted BlueSky Tool/R files/"

generate_trees(leaf_set_array, subset_size, path)


#sim_function(100,10,40, "C:/Users/danwr/OneDrive - University of East Anglia/Documents/PhD Files/Reformatted BlueSky Tool/R files/10 Leaves/")
sim_function(subset_size, x/4, x, filepath)

