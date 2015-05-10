

from opentuner.search import technique
import random


from sklearn import ensemble
import numpy as np
import pandas as pd
import copy
import random
import json

class MlSearch(technique.SequentialSearchTechnique):
  def main_generator(self):

    objective   = self.objective
    driver      = self.driver
    manipulator = self.manipulator
    init_samp_size = 1000
    print manipulator.params

    # generate initial samples
    cfg_list=list()
    train_list = list()
    test_list = list()
    test_df = pd.DataFrame()
    print '==============================='
    for i in xrange(init_samp_size):
        cfg = driver.get_configuration(manipulator.random())
        cfg_list.append(cfg)
        test_list.append(cfg.data)
    print '==============================='
    test_df = pd.DataFrame(test_list)
    print test_df

    #sys.exit(0)

    cfg = cfg_list[0]
    params = manipulator.parameters(cfg.data)
    dimension = len(params)
    print dimension

    samp_size=min(30,dimension+1)
    if dimension+1 < 30:
        samp_size=30

    train_index = random.sample(range(init_samp_size), samp_size)
    test_index = list(set(range(init_samp_size)) - set(train_index))

    #evalaute training index points
    for i in train_index:
        cfg=cfg_list[i]
        self.yield_nonblocking(cfg)
    yield None

    results_vec=list()
    points_vec=list()
    for i in train_index:
        p=cfg_list[i]
        down_cfg = manipulator.copy(p.data)
        cfg = driver.get_configuration(down_cfg)
        result = driver.results_query(config=cfg).one()
        points_vec.append(cfg.data)
        results_vec.append(result.extra)

    print points_vec
    print results_vec

    x_train = pd.DataFrame(points_vec)
    y_train = pd.DataFrame(results_vec)
    n_objective=y_train.shape[1]

    print x_train
    print y_train


    #initialize model
    model_list = list()
    for i in range(n_objective):
        model = ensemble.ExtraTreesRegressor(n_estimators=1000,random_state=0)
        model_list.append(model)


    x_test = test_df.iloc[test_index,:]
    x_test_cfgs = map(lambda x: cfg_list[x], test_index)

    print x_test.shape
    print len(x_test_cfgs)


    while True:
        print '######################'
        # fit model for each objective
        pred_df=pd.DataFrame()
        for i in range(n_objective):
            model = model_list[i]
            response = y_train.iloc[:,i]
            model.fit(x_train, response)
            pred = model.predict(x_test)
            model_list[i] = model
            pred_df['obj'+str(i)]=pred

        pred_df_list=pred_df.values.tolist()
        #print pred_df_list
        pareto_points_index = objective.result_pareto_front(pred_df_list)
        #print pareto_points_index
        assert len(pareto_points_index) > 0

        batch_x_cfgs=map(lambda x: x_test_cfgs[x], pareto_points_index)

        #evalaute points
        for cfg in batch_x_cfgs:
            self.yield_nonblocking(cfg)
        yield None


        #print x_train.shape
        #print y_train.shape

        for p in batch_x_cfgs:
            down_cfg = manipulator.copy(p.data)
            cfg = driver.get_configuration(down_cfg)
            result = driver.results_query(config=cfg).one()
            points_vec.append(cfg.data)
            results_vec.append(result.extra)

        x_train = pd.DataFrame(points_vec)
        y_train = pd.DataFrame(results_vec)
        print pareto_points_index
        print len(pareto_points_index)
        print x_train.shape
        print y_train.shape

        #update x_test
        test_index = list(set(range(len(x_test))) - set(pareto_points_index))
        x_test = x_test.iloc[test_index,:]
        x_test_cfgs = map(lambda x: x_test_cfgs[x], test_index)



        y_train_list=y_train.values.tolist()
        #print pred_df_list
        res_points_index = objective.result_pareto_front(y_train_list)
        print y_train.iloc[res_points_index,:]
        
# register our new technique in global list
technique.register(MlSearch())
