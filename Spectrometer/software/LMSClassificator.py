from Classificator import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.cbook import _string_to_bool
from sklearn import cross_validation

class LMSClassificator():

	bestA, bestB = None,None #model constants y=m*x+c
	 
	def __init__(self, SpecterXs, SpecterY):
		self.SpecterX = np.mean(SpecterXs, axis=0)
		self.SpecterY = SpecterY

	def spectersLMS(self, start=-10, stop=10, nElements=100):
		"Find the best fit for two specters and calculate the error"
		errors = np.zeros(shape=(nElements,nElements))
		smallestError, bestA, bestB = None, None, None

		rng = np.linspace(start,stop,nElements)
		for i,a in enumerate(rng ):
			for j,b in enumerate(rng ):
				errors[i][j] = np.sum(np.power(a*self.SpecterX+b-self.SpecterY,2))
				if(errors[i][j])<smallestError or smallestError is None:
					smallestError=errors[i][j]
					bestA = a
					bestB = b

		self.bestA = bestA
	 	self.bestB = bestB
	 	return errors,bestA,bestB,rng,smallestError

	def plotErrorSurface(self, rng,error):
		"Plots the error surface, where X = 1xn, Y = 1xn, and Error = nxn"
		fig = plt.figure()
		ax = fig.gca(projection='3d')

		surf = ax.plot_surface(rng, rng, error, rstride=1, cstride=1, cmap=cm.jet, linewidth=0.2)
		

		plt.show()

	def plotComparison(self):
		plt.plot(self.SpecterY, self.SpecterX, 'bo', label='Original data', markersize=10)
		plt.plot(self.SpecterY, self.bestA*self.SpecterX + self.bestB, 'go', label='Fitted line', markersize=10)
		plt.plot(self.SpecterY, self.SpecterY, 'r-')
		plt.xlabel("intensity - f(x|w)")
		plt.ylabel("intensity - y")
		plt.legend()
		plt.show()

	def plotComparison2(self):
		plt.plot(np.arange(400,400+len(self.SpecterX),1)[::-1], self.SpecterY, 'b-',label='Original data')
		plt.plot(np.arange(400,400+len(self.SpecterX),1)[::-1], self.SpecterX, 'r-', label='Target data')
		plt.plot(np.arange(400,400+len(self.SpecterX),1)[::-1], self.SpecterX*self.bestA+self.bestB, 'g-', label='Fitted line')
		
		plt.xlabel("wavelenght")
		plt.ylabel("intensity")
		plt.legend()
		plt.show()

	def plotCrossValidation(self, foldErrors):
		plt.title("Cross Validation")
		plt.xlabel("Training Set")
		plt.ylabel("Test Error")
		plt.semilogx(foldErrors, 'b-', label='Test error')
		plt.legend()
		plt.show()

	
	def crossValidate(self,data, n=5, k_folds=5):
		kf = cross_validation.KFold(n, n_folds=k_folds)
		foldErrors = np.zeros(n)

		for i,(train_index, test_index) in enumerate(kf):
			print("TRAIN:", train_index, "TEST:", test_index)
			self.SpecterX= np.mean(data[train_index], axis=0) #train
			self.SpecterY=data[test_index] #train
			errors,bestA,bestB,rng,smallestError = self.spectersLMS() #test
			foldErrors[i] = smallestError

		return foldErrors

	def compareWithUnknown(self, specterY):
		self.SpecterY=specterY
		return self.spectersLMS()


