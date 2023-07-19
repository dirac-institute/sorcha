from abc import ABC, abstractmethod
import numpy as np 

timeColumn = 'FieldMJD'

class baseLightCurve(ABC):
	'''
	Base method for lightcurves, returning no shift independently of the time variable - should never be used!
	'''
	def __init__(self, colnames = []):
		'''
		Initialization function. Doesn't do anything
		'''
		self.colnames = colnames #column names for the light curve parameters - code should check if these exist in the input files
		pass

	def _compute(self, padain):
		'''
		Dataframe provided by SurveySimPP with the time information as well as the other light curve parameters

		Argument:
		- times: array of times
		'''
		return np.zeros_like(padain[timeColumn])

	def __call__(self, x):
		return self._compute(x)

	@staticmethod
	def name_id(self):
		return 'None'

class sinusoidalLightCurve(baseLightCurve):
	'''
	Note: assuming sinusoidal in magnitude instead of flux. Maybe not call LCA?
	'''
	def __init__(self):
		self.colnames = ['LCA', 'Period', 'Time0']


	def _compute(self, padain):
		'''
		Computes a sinusoidal light curve given the input dataframe 
		'''
		modtime = np.mod(padain[timeColumn]/padain['Period'] + padain['Time0'], 2 * np.pi)
		return padain['LCA'] * np.sin(modtime)
	
	@staticmethod
	def name_id(self):
		return 'Sinusoidal'


lightcurve_models = {'None' : baseLightCurve, 'Sinusoidal' : sinusoidalLightCurve} # add more ? 


@staticmethod
@abstractmethod
def name_id():
		"""This method will return the unique name of the Light Curve Model
		"""
		raise (NotImplementedError, "Must be implemented as a static method by the child class")

