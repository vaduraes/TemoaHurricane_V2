#!/usr/bin/env python

"""
Tools for Energy Model Optimization and Analysis (Temoa): 
An open source framework for energy systems optimization modeling

Copyright (C) 2015,  NC State University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A complete copy of the GNU General Public License v2 (GPLv2) is available 
in LICENSE.txt.  Users uncompressing this from an archive may not have 
received this license file.  If not, see <http://www.gnu.org/licenses/>.
"""

from temoa_initialize import Var, Objective, Constraint, NonNegativeReals, minimize
from temoa_model import temoa_create_model
from temoa_rules import PeriodCost_rule
from temoa_run import parse_args
from pyomo.environ import *
import pyomo.environ as pyo
from pformat_results import pformat_results
from pyomo.opt import SolverFactory
from time import time
import os, sys
from mpisppy.utils.pysp_model import PySPModel
from mpisppy.opt.ph import PH
import mpisppy.utils.sputils as sputils


def return_CP_and_path(p_data):
    # return_CP_and_path(p_data) -> dict(), dict()
    # This function reads the path to the instance directory (p_data) and 
    # returns conditional two dictionaries, the first one is the conditional 
    # probability of a scenario, the second one is the path to all files of a
    # scenario.
    from collections import deque, defaultdict
    # from pyomo.pysp.util.scenariomodels import scenario_tree_model
    from pyomo.pysp.scenariotree.tree_structure_model import \
    CreateAbstractScenarioTreeModel

    pwd = os.getcwd()
    os.chdir(p_data)

    s2fp_dict = defaultdict(deque) # Scenario to 'file path' dictionary, .dat not included
    s2cd_dict = defaultdict(float) # Scenario to conditonal density mapping
    # sStructure = scenario_tree_model.create_instance( filename='ScenarioStructure.dat' )
    sStructure = CreateAbstractScenarioTreeModel().create_instance( filename='ScenarioStructure.dat' )

    # The following code is borrowed from Kevin's temoa_lib.py
    ###########################################################################
    # Step 1: find the root node.  PySP doesn't make this very easy ...
    
    # a child -> parent mapping, because every child has only one parent, but
    # not vice-versa
    ctpTree = dict() # Child to parent dict, one to one mapping
    
    to_process = deque()
    to_process.extend( sStructure.Children.keys() )
    while to_process:
        node = to_process.pop()
        if node in sStructure.Children:
            # it's a parent!
            new_nodes = set( sStructure.Children[ node ] )
            to_process.extend( new_nodes )
            ctpTree.update({n : node for n in new_nodes })
    
    #                  parents           -     children
    root_node = (set( ctpTree.values() ) - set( ctpTree.keys() )).pop()
    
    # ptcTree = defaultdict( list ) # Parent to child node, one to multiple mapping
    # for c, p in ctpTree.iteritems():
    #         ptcTree[ p ].append( c )
    # ptcTree = dict( ptcTree )   # be slightly defensive; catch any additions
    
    # leaf_nodes = set(ctpTree.keys()) - set(ctpTree.values())
    # leaf_nodes = set(sStructure.ScenarioLeafNode.values()) # Try to hack Kevin's code
    leaf_nodes = sStructure.ScenarioLeafNode.values() # Try to hack Kevin's code
    leaf_nodes_names = list()
    for n in leaf_nodes:
        leaf_nodes_names.append(n.value)
    leaf_nodes_names = set(leaf_nodes_names)
    
    scenario_nodes = dict() # Map from leafnode to 'node path'
    for node in leaf_nodes_names: # e.g.: {Rs0s0: [R, Rs0, Rs0s0]}
        s = deque()
        scenario_nodes[ node ] = s
        while node in ctpTree:
            s.append( node )
            node = ctpTree[ node ]
        s.append( node )
        s.reverse()
    ###########################################################################

    for s in sStructure.Scenarios:
        cp = 1.0 # Starting probability
        for n in scenario_nodes[value( sStructure.ScenarioLeafNode[s]) ]:
            cp = cp*value( sStructure.ConditionalProbability[n] )
            if not sStructure.ScenarioBasedData.value:
                s2fp_dict[s].append(n + '.dat')
        s2cd_dict[s] = cp
    
    from pyomo.core import Objective
    if sStructure.ScenarioBasedData.value:
        for s in sStructure.Scenarios:
            s2fp_dict[s].append(s + '.dat')
    os.chdir(pwd)
    return (s2cd_dict, s2fp_dict)


import argparse, sys
import os, re
from os.path import dirname, abspath

def solve_ef(model, p_dot_dat, data_dir, temoa_options):


    
    Instance = PySPModel(model=model, scenario_tree=p_dot_dat, data_dir=data_dir)   
    
    ef = sputils.create_EF(Instance.all_scenario_names, Instance.scenario_creator)
    
    solver = pyo.SolverFactory(temoa_options.solver)
    ef_result=solver.solve(ef, tee=True, symbolic_solver_labels=True)
        
        
    # Write to database
    if hasattr(temoa_options, 'output'):
        sys.path.append(data_dir)
    
        ef_result.solution.Status = 'feasible' # Assume it is feasible
        
        s2cd_dict, s2fp_dict = return_CP_and_path(os.path.dirname(p_dot_dat))
        stochastic_run = temoa_options.scenario # Name of stochastic run
        

        ScenarioName=list(ef.component_map())[3:-2]

        for sname in ScenarioName:
            s=ef.component(sname)

            
            temoa_options.scenario = '.'.join( [stochastic_run, s.name] )
            
            temoa_options.dot_dat = list()
            
            
            for fname in s2fp_dict[s.name]:
                
                temoa_options.dot_dat.append(os.path.join(data_dir, fname))
    
            msg = '\nStoring results from scenario {} to database.\n'.format(s.name)
            sys.stderr.write(msg)

            formatted_results = pformat_results( s, ef_result, temoa_options )

    return ef.EF_Obj()

def StochasticPointObjective_rule ( M, p ):
    expr = ( M.StochasticPointCost[ p ] == PeriodCost_rule( M, p ) )
    return expr

def Objective_rule ( M ):
    return sum( M.StochasticPointCost[ pp ] for pp in M.time_optimize )

M = model = temoa_create_model( 'TEMOA Stochastic' )

M.StochasticPointCost = Var( M.time_optimize, within=NonNegativeReals )
M.StochasticPointCostConstraint = Constraint( M.time_optimize, rule=StochasticPointObjective_rule )

del M.TotalCost
M.TotalCost = Objective( rule=Objective_rule, sense=minimize )
model=M

if __name__ == "__main__":
    
    temoa_options, config_flag = parse_args()
    p_dot_dat = temoa_options.dot_dat[0] # must be ScenarioStructure.dat
    data_dir  = os.path.normpath(p_dot_dat + os.sep + os.pardir) #folder where the scenarios are
    

    print(p_dot_dat, data_dir)
    print(solve_ef(model, p_dot_dat, data_dir, temoa_options))
    
