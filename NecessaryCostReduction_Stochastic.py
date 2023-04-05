import os


# CondaEnv="TemoaPY2"
CondaEnv= "Temoa"
Case="Duke_CapEx"
dbs = "Duke_CapEx.sqlite"

Case="Duke_CapEx_3stages_"
dbs = "Duke_CapEx_3stages_.sqlite"

#def RunStochasticModel(CondaEnv, Case):
Origin=os.getcwd()
os.chdir("./temoatools/projects/nc_stoch")
os.system('conda run -n '+ CondaEnv +' python stochastics_write_input_files.py')
os.chdir("../../temoa_stochastic/tools")
os.system('conda run -n '+ CondaEnv +' python generate_scenario_tree_JB.py options/stoch_'+Case+'_0.py --debug')
os.system('conda run -n '+ CondaEnv +' python rewrite_tree_nodes.py options/stoch_'+Case+'_0.py --debug')
os.chdir("..")
os.system('conda run -n '+ CondaEnv +' python temoa_model/temoa_stochastic.py --config=configs/config_stoch_'+Case+'_0.txt')
os.chdir(Origin)          
            
#retrun 0
            
            
            