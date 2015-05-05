from PIL import Image
from pylab import *
from matplotlib.widgets import Button
import numpy as np
import PIL

class Spectrometer:
	"""The Core Spectrometer Class"""
	
	#Image Processing Parameters
	image = None
	#Set the target size of the spectral image 300 x 100
	width = 300
	heigth = 100

	########### Calibration Parameters ###########
	left = 400
	right = 700
	# fourescentRed = 435
	# fourescentBlue = 615
	# we want to estimate where on the image spectra defined above starts
	pxLeft = None
	pxRight = None
	samplingRow = None # px of the brightest row
	windowSize = None
	# pxFlourescentBlue = None
	# pxFlourescentRed = None
	###########

	def __init__(self, imageName):
		self.image = Image.open(imageName)
		return

	#Methods
	def selectImage(self, imageName):
		self.image = Image.open(imageName)

	def processImage(self):
		'This is the core method of spectrometer that does all the processing'
		brighestRow = self.find_brightest_row()
		spectra = self.get_spectra(brighestRow)
		#need to normalise it
		spectra = self.normalise(spectra)
		self.plot_spectra(spectra)

	def getAverageSpectra(self):
		brighestRow = self.find_brightest_row()
		sp = self.get_spectra(brighestRow)
		averageSpecter = self.normalise(sp)[3]
		return averageSpecter

	def find_brightest_row(self):
		"returns intex of brigtest row"
		brightness = brigtest = 0
		brigtest_row = 0 # index

		for i in range(self.image.size[1]):    # for every pixel:
			brightness=0
			pixels = self.image.load()

			for j in range(self.image.size[0]):
		    	 r = pixels[j,i][0]
		    	 g = pixels[j,i][1]
	    		 b = pixels[j,i][2]
	    		 brightness += abs(r-g)+ abs(g-b)+abs(b-r) #add up the absolute differences
	    		 brightness += r+g+b #overall brightness
	
			if brightness > brigtest:
			 	brigtest_row=i
			 	brigtest = brightness

		self.samplingRow=brigtest_row
		return brigtest_row

	def get_spectra(self, row):
		"Extracts spectral values for RGB based on information in 1*width pixels row"
		width = self.image.size[0]
		red = [0]*width
		green = [0]*width
		blue = [0]*width
		average = [0]*width

		pixels = self.image.load() # pixels[column, row]

		for j in range(width): 
			red[j] = pixels[j,row][0]
			green[j] = pixels[j,row][1]
			blue[j]= pixels[j,row][2]
			average[j] = (red[j] + green[j] + blue[j])/3

		return np.array([red, green, blue, average])

	def normalise(self,specter):
		R, G, B = 0, 1, 2
		allValues = specter[R]+specter[G]+specter[B]

		std = np.std(allValues)
		mean = np.mean(allValues)

		normalisedSpecter = (specter-mean)/std

		return normalisedSpecter

	def plot_spectra(self, specter):
		'requires pylab from matplotlib'
		size = len(specter[0])
		figure(1)
		plt.subplot(212)
		plot(np.linspace(self.left,self.right,size), specter[0], 'r-',label='red')
		plot(np.linspace(self.left,self.right,size), specter[1], 'g-',label='green')
		plot(np.linspace(self.left,self.right,size), specter[2], 'b-',label='blue')
		plot(np.linspace(self.left,self.right,size), specter[3], 'k-',label='average')
		xlabel('Wavelength nm')
		ylabel('Magnitude %')
		title('Spactral Analysis')
		legend()
		subplot(211)
		imshow(self.image)
		plot(np.linspace(0, self.image.size[0],self.image.size[0]),[self.samplingRow]*self.image.size[0], 'y-') #draw a sampling row
		axis([0, self.image.size[0], 0, self.image.size[1]])
		# axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
		# bnext = Button(axnext, 'Calibrate')
		#plot([1,2,3,4], [1,4,9,16])

		show()
		return

	def calibrate(flourescentImage):
		return

	def calibrateImage(self):
		"Crops and scales image according to calibration parameters"
		w, h = self.image.size 
		# crop(left, upper, right, and lower pixel)
		self.image = self.image.crop((169, 140, 380, h-180))
		self.image = self.image.resize((self.width,self.heigth), PIL.Image.ANTIALIAS)
		self.image.save("burek.png")
		self.image = Image.open("burek.png")
		# canvas.draw() 
		return
