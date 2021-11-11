from ..makeConfigOIF import makeConfig
import configparser
import pytest

class args:
   def __init__(self, o, pointing, no):
      self.o = o
      self.pointing = pointing
      self.no= no 
      self.ndays =-1
      self.day1 = 1
      self.prefix = ''
      self.camerafov = 'instrument_polygon.dat'
      self.cache = '_cache'
      self.mpcfile =  'obslist.dat'
      self.inputformat = 'whitespace'


def test_makeConfigOIF():

   # python makeConfigOIF.py ../data/test/testorb.des ../data/test/baseline_10yrs_10klines.db 

   argv=args('../../data/test/testorb.des','../../data/test/baseline_10yrs_10klines.db', -1)

   makeConfig(argv)

   config = configparser.ConfigParser()
   config.read('testorb-1-5.ini')


   config2 = configparser.ConfigParser()
   config2.read('data/test_oif_1.ini')

   assert (config==config2)


   #  python makeConfigOIF.py ../data/test/testorb.des ../data/test/baseline_10yrs_10klines.db -no 3
 
   argv=args('../../data/test/testorb.des','../../data/test/baseline_10yrs_10klines.db',3)

   makeConfig(argv)

   config = configparser.ConfigParser()
   config.read('testorb-1-3.ini')


   config1 = configparser.ConfigParser()
   config1.read('testorb-4-5.ini')

   config2 = configparser.ConfigParser()
   config2.read('data/test_oif_2.ini')

   config3 = configparser.ConfigParser()
   config3.read('data/test_oif_3.ini')

   assert (config==config2)
   assert (config1==config3)


   return
