import astropy
import pyfits
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt

for j in range(9,317):
	home="/Software/all_weeks"
	datafile="%s/lat_photon_weekly_w%03d_p203_v001.fits" %(home,j)
	filename="sun_photon_weekly_w%03d_p202_v001" %(j) #z more than 100 and less than 110



	f=pyfits.open(datafile)
	tbdata=f[1].data
	header=pyfits.getheader(datafile,1)
	header.keys()
	TFields=header['TFIELDS']
#print header['TSTART']
	times= header['DATE-OBS'] #start date of the observation in UTC e.g 2012-06-28T01:50:32.000
	t=Time(times,format='isot',scale='utc')

	julian= t.jd #change UTC to julian date



	RA=[]
	DEC=[]
	List=[]
	TIME=[]
	TIMEDIFF=[]
	JULIE=[] 
	l=[]
	aa=[]
	ZENITH_ANGLE=[]
	z=[]
	for i in range(TFields):
    		x=i+1
    		TTYPE=header['TTYPE%d' %x]
    
    		List.append(TTYPE)
    		if TTYPE=="RA":
    		    RA=tbdata.field("%s" %TTYPE)
    		if TTYPE=="DEC":
    		    DEC=tbdata.field("%s" %TTYPE)
    		if TTYPE=="TIME": #get the photon live time
    		    TIME=tbdata.field("%s" %TTYPE)
		if TTYPE=="ZENITH_ANGLE":
			ZENITH_ANGLE=tbdata.field("%s" %TTYPE)
			



	for i in range(len(TIME)):
    		if i==0:
        		print "boo"
    		else:
        		t=TIME[i]-TIME[0] #difference in time between ith photon and the first, this is to calculate the elapsed time since start time of observation
        		TIMEDIFF.append(t)
      


	DAYS=np.array(TIMEDIFF)/float(86400) #express time diff in days




	JULIE.append(julian) #the first day is julian day
	for i in range(len(DAYS)):
    		j=DAYS[i]+julian #add the time elasped to the start julian date
    		JULIE.append(j)
    
	n=np.array(JULIE)-2451545 #number of days since Greenwich noon

	L=280.460+0.9856003*np.array(n)  #mean longitude of the SUN, have to ensure that 0<L<360

	for i in range(len(L)):
   		while L[i]>360:
        
      			L[i]=L[i]-360
   

	for i in range(len(L)):
		while L[i]<0:
			L[i]=L[i]+360
	
			

      
	g=357.528+0.9856003*np.array(n) #mean anomaly of the SUN, have to ensure that 0<g<360

	for i in range(len(g)):
		while g[i]>360:
			g[i]=g[i]-360

	for i in range(len(g)):
		while g[i]<0:
			g[i]=g[i]+360
		


	l1=1.915*np.degrees(np.sin(np.radians(g)))
	l2=0.020*np.degrees(np.sin(np.radians(2*g)))
 
	lambsy=np.add(L,l1)
	lambs=np.radians(np.add(lambsy,l2)) #lambs is lambda: ecliptic latitude of the sun 

	obliquity=np.radians(23.439-0.0000004*np.array(n)) 
	c=np.cos(obliquity)
	s=np.sin(obliquity)
	tl=np.tan(lambs)
	sl=np.sin(lambs)
	SRA=np.degrees(np.arctan(np.multiply(c,tl)))
	SDEC=np.degrees(np.arcsin(np.multiply(s,sl)))
	
	b=np.pi-np.radians(DEC)
	c=np.pi-np.radians(SDEC)
	
	A=np.subtract(np.radians(SRA),np.radians(RA))
	
	cosa1=np.multiply(np.cos(b),np.cos(c))
	cosa2=np.multiply(np.sin(b),np.sin(c),np.cos(A))
	cosa=np.add(cosa1,cosa2)
	a=np.arccos(cosa)
	a=np.degrees(a)
	
	log10time=np.log10(TIME[9:]-TIME[:-9])


	log10time=np.append(log10time , np.zeros(9))



	for i in range(len(log10time)):

		if log10time[i]<0:
			z.append(ZENITH_ANGLE[i])
			aa.append(a[i])
	plt.figure()

	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')
	plt.scatter(aa,z,marker='.', edgecolors='none', s=8,label="sun")
	plt.xlabel('sun angle')
	plt.ylabel('zenith angle: log10time less than 0')
	#params = {'legend.fontsize': 12,'legend.linewidth': 2, 'legend.numpoints':1}
	#plt.rcParams.update(params)
	#plt.legend(bbox_to_anchor=(1,1), loc=1, borderaxespad=0.)
	#plt.grid(True)
	plt.savefig("graph_a_log10timelessthanzero_%s.png" %(filename))
	plt.close()
		



