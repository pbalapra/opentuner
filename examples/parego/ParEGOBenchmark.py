#!/usr/bin/env python
#
# This is a simple testcase purely for testing the autotuner
#
# http://en.wikipedia.org/wiki/Rosenbrock_function
#
# Also supports some other test functions taken from:
# http://en.wikipedia.org/wiki/Test_functions_for_optimization
#

import adddeps  # fix sys.path

import argparse
import logging

import opentuner
from opentuner.measurement import MeasurementInterface
from opentuner.search.manipulator import ConfigurationManipulator
from opentuner.search.manipulator import FloatParameter


import math

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(parents=opentuner.argparsers())
parser.add_argument('--dimensions', type=int, default=2,
                    help='dimensions for the Rosenbrock function')
parser.add_argument('--domain', type=float, default=1000,
                    help='bound for variables in each dimension')
parser.add_argument('--function', default='f_dtlz1a',
                    choices=('f_dtlz1a', 'f_dtlz2a', 'f_dtlz7a','f_vlmop3','f_oka1','f_oka2','f_vlmop2','f_kno1'),
                    help='function to use')


class ParEGOBenchmark(MeasurementInterface):
  def run(self, desired_result, input, limit):
    cfg = desired_result.configuration.data
    val = 0.0
    if self.args.function == 'f_dtlz1a':
        assert self.args.dimensions == 6
        dim = self.args.dimensions
        x=list()
        x.append(-1)
        vals=list()

        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x
        g = 0.0;
        for i in xrange(2,self.args.dimensions+1):
            g+= (x[i]-0.5)*(x[i]-0.5) - math.cos(2*math.pi*(x[i]-0.5)) # Note this is 20*PI in Deb's DTLZ1

        g += dim-1
        g *= 100


        val1 = 0.5*x[1]*(1 + g)
        val2 = 0.5*(1-x[1])*(1 + g)
        vals.append(val1)
        vals.append(val2)

        val=vals[0]
    elif self.args.function == 'f_dtlz2a':
        assert self.args.dimensions == 8
        dim = self.args.dimensions
        x=list()
        x.append(-1)
        vals=list()

        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x
        g = 0.0;
        alph=1.0

        for i in xrange(3,self.args.dimensions+1):
            g+=(x[i]-0.5)*(x[i]-0.5);

        y1 = (1 + g)*math.cos(math.pow(x[1],alph)*math.pi/2)*math.cos(math.pow(x[2],alph)*math.pi/2);
        y2 = (1 + g)*math.cos(math.pow(x[1],alph)*math.pi/2)*math.sin(math.pow(x[2],alph)*math.pi/2);
        y3 = (1 + g)*math.sin(math.pow(x[1],alph)*math.pi/2);

        vals = [y1,y2,y3]
    elif self.args.function == 'f_dtlz4a':
        assert self.args.dimensions == 8
        dim = self.args.dimensions
        x=list()
        x.append(-1)
        vals=list()

        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x
        g = 0.0;
        alph=100.0

        for i in xrange(3,self.args.dimensions+1):
            g+=(x[i]-0.5)*(x[i]-0.5);

        y1 = (1 + g)*math.cos(math.pow(x[1],alph)*math.pi/2)*math.cos(math.pow(x[2],alph)*math.pi/2);
        y2 = (1 + g)*math.cos(math.pow(x[1],alph)*math.pi/2)*math.sin(math.pow(x[2],alph)*math.pi/2);
        y3 = (1 + g)*math.sin(math.pow(x[1],alph)*math.pi/2);

        vals = [y1,y2,y3]
    elif self.args.function == 'f_dtlz7a':
        assert self.args.dimensions == 8
        dim = self.args.dimensions
        nobjs = 3

        x=list()
        x.append(-1)
        vals=list()

        y=list()
        y.append(-1)

        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x

        y.append(x[1])
        y.append(x[2])

        g = 0.0;
        for i in xrange(3,self.args.dimensions+1):
            g+=x[i]
        g*=9.0/(dim-nobjs+1);
        g+=1.0;

        sumv=0.0;
        #for(int i=1;i<=nobjs-1;i++)
        for i in xrange(1,nobjs-1):
            sumv += ( y[i]/(1.0+g) * (1.0+math.sin(3*math.pi*y[i])) );
        h = nobjs - sumv;

        y.append((1 + g)*h)
        #print y
        y.pop(0)
        vals = y
    elif self.args.function == 'f_vlmop3':
        assert self.args.dimensions == 2
        dim = self.args.dimensions
        nobjs = 3
        x=list()
        x.append(-1)


        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x

        y=list()
        y1 = 0.5*(x[1]*x[1]+x[2]*x[2]) + math.sin(x[1]*x[1]+x[2]*x[2])
        y2 = math.pow(3*x[1]-2*x[2]+4.0, 2.0)/8.0 + math.pow(x[1]-x[2]+1, 2.0)/27.0 + 15.0
        y3 = 1.0 / (x[1]*x[1]+x[2]*x[2]+1.0) - 1.1*math.exp(-(x[1]*x[1]) - (x[2]*x[2]))

        y = [y1,y2,y3]

        vals = y
    elif self.args.function == 'f_oka1':
        assert self.args.dimensions == 2
        dim = self.args.dimensions
        nobjs = 2
        x=list()
        x.append(-1)


        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x

        x1p = math.cos(math.pi/12.0)*x[1] - math.sin(math.pi/12.0)*x[2];
        x2p = math.sin(math.pi/12.0)*x[1] + math.cos(math.pi/12.0)*x[2];

        y1 = x1p;
        y2 = math.sqrt(2*math.pi) - math.sqrt(math.abs(x1p)) + 2 * math.pow(math.abs(x2p-3*math.cos(x1p)-3) ,0.33333333);

        vals = [y1, y2]
    elif self.args.function == 'f_oka2':
        assert self.args.dimensions == 2
        dim = self.args.dimensions
        nobjs = 2
        x=list()
        x.append(-1)


        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x

        y1=x[1];
        y2=1 - (1/(4*math.pi*math.pi))*math.pow(x[1]+math.pi,2) + math.pow(math.abs(x[2]-5*math.cos(x[1])),0.333333333) + pow(math.abs(x[3] - 5*math.sin(x[1])),0.33333333);

        vals = [y1,y2]
    elif self.args.function == 'f_vlmop2':
        assert self.args.dimensions == 2
        dim = self.args.dimensions
        nobjs = 2
        x=list()
        x.append(-1)
        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x

        sum1=0;
        sum2=0;
        for i in xrange(1,2+1):
            sum1+=math.pow(x[i]-(1/math.sqrt(2.0)),2);
            sum2+=math.pow(x[i]+(1/math.sqrt(2.0)),2);

        y1 = 1 - exp(-sum1)
        y2 = 1 - exp(-sum2)

        vals = [y1,y2]
    elif self.args.function == 'f_kno1':
        assert self.args.dimensions == 2
        dim = self.args.dimensions
        nobjs = 2
        x=list()
        x.append(-1)
        for d in xrange(self.args.dimensions):
            x.append(cfg[d])
        print x

        c = x[1]+x[2];
        f = 20-( 11+3*math.sin((5*c)*(0.5*c)) + 3*math.sin(4*c) + 5 *math.sin(2*c+2));
        g = (math.pi/2.0)*(x[1]-x[2]+3.0)/6.0;
        y1= 20-(f*math.cos(g));
        y2= 20-(f*math.sin(g));
        vals = [y1,y2]


    return opentuner.resultsdb.models.Result(time=vals[0],extra=vals)


  def manipulator(self):
    manipulator = ConfigurationManipulator()
    for d in xrange(self.args.dimensions):
      manipulator.add_parameter(FloatParameter(d,
                                               -self.args.domain,
                                               self.args.domain))
    return manipulator

  def program_name(self):
    return self.args.function

  def program_version(self):
    return "%dx%d" % (self.args.dimensions, self.args.domain)

  def save_final_config(self, configuration):
    """
    called at the end of autotuning with the best resultsdb.models.Configuration
    """
    print "Final configuration", configuration.data


if __name__ == '__main__':
  args = parser.parse_args()
  if args.function == 'beale':
    # fixed for this function
    args.domain = 4.5
    args.dimensions = 2
  ParEGOBenchmark.main(args)
