import os
import shutil
import temoatools as tt
from pathlib import Path
import sys

def test_directory(path):
    # check if directory exists, create the directory if it does not
    try:
        os.stat(path)
    except:
        os.mkdir(path)


# ===================================
# Inputs
# ===================================

# Baseline databases to use


dbs = ["Duke_CapEx_3stages_.sqlite"]
solver = 'gurobi'

cutoff = 0.05  # cutoff^n<1e-6, where n is # of model years excluding the first time step


# model years
years = [2017, 2020, 2025, 2030]

#Hurricane scenarios with corresponding probabilities and windspeeds
scenarios = ["H1", "H2", "H3"]
probabilities_hist = [0.52, 0.32, 0.16]  # sum must equal 1
probabilities_climate_change = [0.2, 0.32, 0.48]  # sum must equal 1
windspeeds = [22.0, 113.0, 154.0]  # mph

#scenarios = ["H1", "H2"]
#probabilities_hist = [0.52, 0.48]  # sum must equal 1
#probabilities_climate_change = [0.2, 0.8]  # sum must equal 1
#windspeeds = [22.0, 120.0]  # mph

# scenarios = ["H1"]
# probabilities_hist = [1]  # sum must equal 1
# probabilities_climate_change = [1]  # sum must equal 1
# windspeeds = [120.0]  # mph



# temoa model technologies and corresponding fragility curve groups
techs = {
'IMPELCNGAEA': "natgas_petrol",
'IMPELCDSLEA': "natgas_petrol",
'IMPURNA': "UGND",
'IMPELCBIGCCEA':"coal_biomass",
'IMPELCBIOSTM':"coal_biomass",
'IMPSOL':"solar",
'IMPWND':"wind",
'IMPELCHYD':"hydro",
'IMPLFGICEEA':"coal_biomass",
'IMPLFGGTREA':"coal_biomass",
'ENGACC05':"natgas_petrol",
'ENGACT05':"natgas_petrol",
'ENGAACC':"natgas_petrol",
'ENGAACT':"natgas_petrol",
'ENGACCCCS':"natgas_petrol" ,
'ECOALSTM':"coal_biomass",
'ECOALIGCC':"coal_biomass",
'ECOALIGCCS':"coal_biomass",
'EBIOIGCC':"coal_biomass",
'EGEOBCFS':"coal_biomass",
'ESOLPVCEN':"solar",
'ESOLPVDIS':"solar",
'ESOL':"solar",
'EWNDON':"wind",
'EWNDONS_59968':"wind",
'EWNDOFS':"wind",
'ETRANS':"trans",
'EDISTR':"dist_cond",
'EBIOSTMR_10378':"coal_biomass",
'EBIOSTMR_10379':"coal_biomass",
'EBIOSTMR_10382':"coal_biomass",
'EBIOSTMR_10525':"coal_biomass",
'EBIOSTMR_50188':"coal_biomass",
'EBIOSTMR_50254':"coal_biomass",
'EBIOSTMR_NC_25':"coal_biomass",
'EBIOSTMR_54656':"coal_biomass",
'ECOASTMR_2712':"coal_biomass",
'ECOASTMR_2718':"coal_biomass",
'ECOASTMR_2721':"coal_biomass",
'ECOASTMR_2727':"coal_biomass",
'ECOASTMR_6250':"coal_biomass",
'ECOASTMR_8042':"coal_biomass",
'ECOASTMR_10384':"coal_biomass",
'ECOASTMR_50244':"coal_biomass",
'EDSLCTR_2707':"natgas_petrol",
'ECOASTMR_54276':"coal_biomass",
'EDSLCTR_2716':"natgas_petrol",
'EDSLCTR_NC_25':"natgas_petrol",
'EDSLCTR_54276':"natgas_petrol",
'EDSLCTR_54823':"natgas_petrol",
'EHYDCONR_2707':"hydro",
'EHYDCONR_2714':"hydro",
'EHYDCONR_2715':"hydro",
'EHYDCONR_2719':"hydro",
'EHYDCONR_2722':"hydro",
'EHYDCONR_2726':"hydro",
'EHYDCONR_2728':"hydro",
'EHYDCONR_2729':"hydro",
'EHYDCONR_2730':"hydro",
'EHYDCONR_2747':"hydro",
'EHYDCONR_2756':"hydro",
'EHYDCONR_2758':"hydro",
'EHYDCONR_2779':"hydro",
'EHYDCONR_2780':"hydro",
'EHYDCONR_54894':"hydro",
'EHYDCONR_54895':"hydro",
'EHYDCONR_54896':"hydro",
'EHYDCONR_54897':"hydro",
'EHYDCONR_54898':"hydro",
'EHYDCONR_54899':"hydro",
'EHYDCONR_NC_25':"hydro",
'EHYDREVR_2780':"hydro",
'ELFGGTR_NC_25':"coal_biomass",
'ELFGICER_NC_25':"coal_biomass",
'ENGACCR_1016':"natgas_petrol",
'ENGACCR_2706':"natgas_petrol",
'ENGACCR_2720':"natgas_petrol",
'ENGACCR_2723':"natgas_petrol",
'ENGACCR_7805':"natgas_petrol",
'ENGACCR_7826':"natgas_petrol",
'ENGACCR_50555':"natgas_petrol",
'ENGACCR_58215':"natgas_petrol",
'ENGACCR_58697':"natgas_petrol",
'ENGACCR_59325':"natgas_petrol",
'ENGACTR_1016':"natgas_petrol",
'ENGACTR_2706':"natgas_petrol",
'ENGACTR_7277':"natgas_petrol",
'ENGACTR_7538':"natgas_petrol",
'ENGACTR_7805':"natgas_petrol",
'ENGACTR_7826':"natgas_petrol",
'ENGACTR_54316':"natgas_petrol",
'ENGACTR_55116':"natgas_petrol",
'ENGACTR_56249':"natgas_petrol",
'ENGACTR_56292':"natgas_petrol",
'ENGACTR_57029':"natgas_petrol",
'ENGACTR_58697':"natgas_petrol",
'ENGACTR_NC_25':"natgas_petrol",
'ESOLPVR_NC':"solar",
'ESOLPVR_SC':"solar",
'EHYDCONR_3255':"hydro",
'EHYDCONR_3256':"hydro",
'EHYDCONR_3257':"hydro",
'EHYDCONR_3266':"hydro",
'EHYDCONR_3270':"hydro",
'EHYDCONR_3271':"hydro",
'EHYDCONR_3323':"hydro",
'EHYDCONR_6517':"hydro",
'EHYDCONR_SC_25':"hydro",
'ECOASTMR_6249':"coal_biomass",
'ECOASTMR_57919':"coal_biomass",
'EHYDREVR_3262':"hydro",
'EHYDREVR_6126':"hydro",
'EHYDREVR_7125':"hydro",
'ELFGGTR_SC_25':"coal_biomass",
'ELFGICER_SC_25':"coal_biomass",
'ENGACTR_3250':"natgas_petrol",
'ENGACCR_7834':"natgas_petrol",
'ENGACCR_55043':"natgas_petrol",
'ENGACTR_3264':"natgas_petrol",
'ENGACTR_3291':"natgas_petrol",
'ENGACTR_7834':"natgas_petrol",
'ENGACTR_7981':"natgas_petrol",
'ENGACTR_55166':"natgas_petrol",
'ENGACTR_SC_25':"natgas_petrol",
'EDSLCTR_3250':"natgas_petrol",
'EDSLCTR_3320':"natgas_petrol",
'EDSLCTR_SC_25':"natgas_petrol",
'EBIOSTMR_50806':"coal_biomass",
'EBIOSTMR_54087':"coal_biomass",
'EBIOSTMR_57470':"coal_biomass",
'EBIOSTMR_SC_25':"coal_biomass",
'ESLION':"battery",
'GeneralOcean':"wind"

}

curves = {"inf_stiff": "inf_stiff",
          "trans": "trans_UK_base",
          "sub": "sub_HAZUS_severe_k3",
          "dist_cond": "dist_cond_TX",
          "dist_twr": "dist_60yr",
          "wind": "wind_nonyaw",
          "solar": "solar_utility",
          "coal_biomass": "secbh_severe",
          "natgas_petrol": "secbm_severe",
          "battery": "secbl_severe",
          "hydro": "cecbl_severe",
          "UGND": "secbm_severe"}

# ===================================
# Begin input file preparation
# ===================================

# Check for appropriate cutoff number
n_years = len(years) - 1
if cutoff ** n_years < 1e-6:
    print("Warning: cutoff^n<1e-6, where n is # of model years excluding the first time step")
else:
    print("Verified: Appropriate value for cutoff")

# --------------------
# directory management
# --------------------

# current working directory (assumed to be temoatools//projects/puerto_rich_stoch)
wrkdir = os.getcwd()

# Create directory to store stochastic shell scripts
stochdir = os.path.join(wrkdir, 'sbatch_files')
test_directory(stochdir)

# temoa_stochastic directory (already exists from temoatools package)
temoadir = os.path.abspath('..//..//temoa_stochastic')

# configuration file directory (create if necessary)
configdir = os.path.abspath('..//..//temoa_stochastic//configs')
test_directory(configdir)

# database directory (create if necessary)
datadir = os.path.abspath('..//..//temoa_stochastic//data_files')
test_directory(datadir)

# Create directory to store scenario tree scripts for stochastic simulations
treedir = os.path.abspath('..//..//temoa_stochastic//tools//options')

# --------------------
# begin creation of input files
# --------------------

# Create all input files
n_cases = 1
for case in range(n_cases):
    # historical probabilities
    if case == 0:
        probabilities = probabilities_hist

    # climate change probabilities
    else:  # case == 1:
        probabilities = probabilities_climate_change

    # Iterate through each database for each case
    for db in dbs:
        db_name = tt.remove_ext(db)

        # ====================================
        # Stochastic input file
        # ====================================
        os.chdir(treedir)

        # Write File
        filename = "stoch_" + db_name + "_" + str(case) + ".py"
        # Open File
        f = open(filename, "w")
        f.write(
            "# Automatically generated stochastic input file from temoatools github.com/EnergyModels/temoatools\n\n")
        f.write("verbose = True\n")
        f.write("force = True\n")
        f.write("\n")
        f.write("dirname = '" + db_name + "_" + str(case) + "'\n")
        f.write("modelpath = '" + "../temoa_model/temoa_model.py'\n")
        f.write("dotdatpath = '../data_files/" + db_name + "_" + str(case) + ".dat'\n")  # TODO
        f.write("stochasticset = 'time_optimize'\n")
        f.write("stochastic_points = (")
        for year in years:
            f.write(str(year) + ", ")
        f.write(")\n")
        f.write("stochastic_indices = {'CapReduction': 0}\n")
        f.write("types = (\n\t")
        for scenario in scenarios:
            f.write("'" + scenario + "', ")
        f.write("\n")
        f.write(")\n")
        f.write("conditional_probability = dict(\n")
        for scenario, prob in zip(scenarios, probabilities):
            f.write("\t" + scenario + "=" + str(prob) + ",\n")
        f.write(")\n")
        f.write("rates = {\n")
        f.write("\t'CapReduction': dict(\n")
        for scenario, prob, windspeed in zip(scenarios, probabilities, windspeeds):
            f.write("\t\t" + scenario + "=(\n")
            for tech in techs.keys():
                tech_cat = techs[tech]
                curve = curves[tech_cat]
                fragility = tt.fragility(windspeed, curve=curve)
                capReduction = round(1.0 - fragility, 3)
                # Check for unallowed values of capReduction
                if capReduction > 1.0:
                    capReduction = 1.0
                elif capReduction < cutoff:  # Zero values will crash
                    capReduction = cutoff
                f.write("\t\t\t('" + tech + "', " + str(capReduction) + "),\n")
            f.write("\t\t),\n\n")
        f.write("\t),\n")
        f.write("}\n")
        #
        # # Close File
        # f.close()

        # ====================================
        # Configuration file
        # ====================================
        os.chdir(configdir)
        filename = "config_stoch_" + db_name + "_" + str(case) + ".txt"
        input_path = os.path.join(temoadir, "tools", db_name + "_" + str(case),
                                  "ScenarioStructure.dat")
        output_path = os.path.join(datadir,  db_name + "_" + str(case) + ".sqlite")
        db_io_path = os.path.join(datadir, )

        f = open(filename, "w")
        # ---
        f.write(
            "#-----------------------------------------------------\n")
        f.write("# This is an automatically generated configuration file for Temoa using")
        f.write(" temoatools github.com/EnergyModels/temoatools\n")
        f.write("# It allows you to specify (and document) all run-time model options\n")
        f.write("# Legal chars in path: a-z A-Z 0-9 - _  / . :\n")
        f.write("# Comment out non-mandatory options to omit them\n")
        f.write("#----------------------------------------------------- \n")
        f.write("\n")
        f.write("# Input File (Mandatory)\n")
        f.write("# Input can be a .sqlite or .dat file\n")
        f.write("# Both relative path and absolute path are accepted\n")
        f.write("--input=" + input_path + "\n")
        f.write("\n")
        f.write("# Output File (Mandatory)\n")
        f.write("# The output file must be a existing .sqlite file\n")
        f.write("--output=" + output_path + "\n")
        f.write("\n")
        f.write("# Scenario Name (Mandatory)\n")
        f.write("# This scenario name is used to store results within the output .sqlite file\n")
        f.write("--scenario=" + db_name + "_" + str(case) + "\n")
        f.write("\n")
        f.write("# Path to the 'db_io' folder (Mandatory)\n")
        f.write("# This is the location where database files reside\n")
        f.write("--path_to_db_io=" + db_io_path + "\n")
        f.write("\n")
        f.write("# Spreadsheet Output (Optional)\n")
        f.write("# Direct model output to a spreadsheet\n")
        f.write("# Scenario name specified above is used to name the spreadsheet\n")
        f.write("#--saveEXCEL\n")
        f.write("\n")
        f.write("# Save the log file output (Optional)\n")
        f.write("# This is the same output provided to the shell\n")
        f.write("#--saveTEXTFILE\n")
        f.write("\n")
        f.write("# Solver-related arguments (Optional)\n")
        if len(solver) > 0:
            f.write("--solver=" + solver + "                    # Optional, indicate the solver\n")
        else:
            f.write("#--solver=cplex                    # Optional, indicate the solver\n")

        f.write("#--keep_pyomo_lp_file             # Optional, generate Pyomo-compatible LP file\n")
        f.write("\n")
        f.write("# Modeling-to-Generate Alternatives (Optional)\n")
        f.write(
            "# Run name will be automatically generated by appending '_mga_' and iteration number to scenario name\n")
        f.write("#--mga {\n")
        f.write("#	slack=0.1                     # Objective function slack value in MGA runs\n")
        f.write("#	iteration=4                   # Number of MGA iterations\n")
        f.write(
            "#	weight=integer                # MGA objective function weighting method, currently 'integer' or 'normalized'\n")
        f.write("#}\n")
        f.write("\n")
        f.close()

        # ====================================
        # Script file - Individual
        # ====================================
        os.chdir(stochdir)

        config_filename = "config_stoch_" + db_name + "_" + str(case) + ".txt"
        tree_filename = "stoch_" + db_name + "_" + str(case) + ".py"
        script_filename = "stoch_" + db_name + "_" + str(case) + ".sh"
        config_filepath = os.path.join(configdir, config_filename)

        f = open(script_filename, "w")
        f.write("#!/bin/bash\n")
        f.write("#SBATCH -N 1\n")
        f.write("#SBATCH --cpus-per-task=36\n")
        f.write("#SBATCH -t 16:00:00\n")
        f.write("#SBATCH -p standard\n\n")
        f.write("module purge\n")
        f.write("module load anaconda/2019.10-py2.7\n\n")
        f.write("# activate temoa environment\n")
        f.write("source activate temoa-stoch-py2\n\n")
        f.write("# if gurobi is available\n")
        f.write("export PYTHONPATH=$EBROOTGUROBI/lib/python2.7_utf32\n")
        f.write("module load gurobi/9.0.1\n\n")
        f.write("# set the NUM_PROCS env variable for the Python script\n")
        f.write("export NUM_PROCS =$SLURM_CPUS_PER_TASK\n\n")
        f.write("# run\n")
        f.write("cd " + temoadir + "\n")
        f.write("cd tools\n\n")
        f.write("python generate_scenario_tree_JB.py options/" + tree_filename + " --debug\n")
        f.write("python rewrite_tree_nodes.py options/" + tree_filename + " --debug\n\n")
        f.write("cd ..\n\n")
        f.write("python temoa_model/temoa_stochastic.py --config=" + config_filepath + "\n")
        f.close()

# ====================================
# Script file - batch
# ====================================
os.chdir(wrkdir)
f = open("run_all_simulations.sh", "w")
f.write("#!/bin/bash\n\n")
f.write('cd sbatch_files\n\n')
for case in range(n_cases):
    for db in dbs:
        db_name = tt.remove_ext(db)
        script_filename = "stoch_" + db_name + "_" + str(case) + ".sh"
        f.write("sbatch " + script_filename + " \n")
f.close()

# Copy baseline databases
for db in dbs:
    for case in range(n_cases):
        db_name = tt.remove_ext(db)
        # .sqlite
        src_dir = os.path.join(wrkdir, "databases", db_name + ".sqlite")
        dst_dir = os.path.join(datadir, db_name + "_" + str(case) + ".sqlite")
        shutil.copy(src_dir, dst_dir)
        # .dat
        src_dir = os.path.join(wrkdir, "databases", db_name + ".dat")
        dst_dir = os.path.join(datadir, db_name + "_" + str(case) + ".dat")
        shutil.copy(src_dir, dst_dir)

# Return to original working directory
os.chdir(wrkdir)
