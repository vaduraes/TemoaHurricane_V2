Stochastic Capacity Expansion Model - For NC and FL
Author: Victor Augusto Duraes de Faria


Environments)
To run this code you will need to install the two environments available at ./environments folder <conda env create -f environment.yml>
> Geo_Env.yml will be used to create the database files
> TEMOA_P310.yml will be used to run the deterministic and stochastic capacity expansion model

On building the TEMOA_P310.yml environment some extra steps will be necessary:
1) activate the temoa environment, go to the pysp-main folder and run: < python setup.py develop > this
will install a version of pysp compatible with the stochastic code we developed
2) also go to the mpi-sppy-main folder and run: < pip install .>


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Instruction 1)
The CreateDB folder contain code and data used in the creation of DBs for each region of interest

----------------------------------------------------------------------------------------------------
Instruction 2)
The TemoaDeterministic folder contain a version of the deterministic TEMOA model <https://temoacloud.com/>

----------------------------------------------------------------------------------------------------
Instruction 3)
The TemoaStochastic folder contain a version of the stochastic TEMOA model <https://temoacloud.com/>

----------------------------------------------------------------------------------------------------
Instruction 4)
The IneterpretResults folder coantain code to help interpret the output data from the capacity expansion models



