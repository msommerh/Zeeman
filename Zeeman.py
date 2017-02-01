# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:22:09 2017

@author: stefho
"""


import numpy as np
import matplotlib.pyplot as plt
 

# Konstanten


h = 6.626*10**(-34)         #Planck Konstante
c = 2.9979*10**8            #Lichtgeschw.
mb = 9.2740*10**(-24)       #Bohrsches Magneton
sa = np.pi*0.01002**2       #Querschnittsfläche Spule
sn = 127                    #Windungen Spule 
n = [1.5147,1.5172]         #Brechungsindex Lummerplatte
lambda0 = [585.249*10**(-9),540.056*10**(-9)]    #Unverschobene Wellenlängen
d = 3.213*10**-3            #Dicke der Lummerplatte
V = 4.372                   #Durchschnittlich gemessene Voltzahl
S = 230.42*10**-3           #Durchschnittliche gemmessener Abstand Drehpunkt-Mikrometerschraube
#m=0                        #Ordnung von Maximum von innen nach aussen 
                      
                      
                      
                      
# Funktionen 

def read_from_file(filename):                   #Liest Daten ein
    return np.loadtxt(filename, skiprows=1)

def Mittelwerte(dat):                           #Gibt Liste mit gemittelten Daten aus
    dat0 = dat-np.mean(dat)
    dat0m = []
    for i in range(0,18):
        dat0m.append(np.abs(np.mean(dat0[:,i]*10**-3)))
    return dat0m

def Abstand(dat, i):                            #Gibt gemittelten Abstand zwischen Maxima auf beiden Seiten aus
    A = 0
    dat0m = Mittelwerte(dat)
    A= dat0m[i]+dat0m[-(i+1)]  
    return A 
        
def Theta(dat,S,i):                             #Gibt Winkel des Maximums aus
    A = Abstand(dat, i)
    theta = np.arctan(A/(2*S)) 
    return theta    
    
def Maximumsordnung(dat, d, n, S, m, lambda0): #Gibt tatsächliche Ordnung des Maximums aus
    i = 3*m+1
    theta = Theta(dat,S,i)
    M = (2*d/lambda0)*np.sqrt(n**2-1+np.sin(theta)**2)
    return M 
        
def Frequenzunterschied(dat, d, lambda0, n, S, m, c, dn): #gibt Frequenzunterschied von unverschobenem zu verschobenen Übergängen
    
    ip = 3*m
    im = 3*m+2
    
    M = Maximumsordnung(dat, d, n, S, m, lambda0)
    thetap = Theta(dat,S,ip)
    thetam = Theta(dat,S,im)
    deltaf = (-c/lambda0**2)*(np.sin(thetam)**2-np.sin(thetap)**2)/(lambda0*M**2/d**2-4*n*dn)
    return deltaf
    
def Magnetfeld(V, sa, sn):                      #Berechnet Magnetfeldstärke
    B = V/(314.16*sa*sn)
    return B 

def Landefaktor(dat, d, lambda0, n, S, m, c, dn, V, sa, sn, mb, h): #Berechnet Landéfaktor
    deltaf = Frequenzunterschied(dat, d, lambda0, n, S, m, c, dn)
    B = Magnetfeld(V,sa,sn)
    gj = h*deltaf/(mb*B)
    return gj



"Ab hier Fehlerrechnung"

#Konstanten und ihre Fehler

r = 10.02*10**-3
deltar = 0.03*10**-3
n = [1.5147,1.5172] 
deltan = 0.0002
lambda0 = [585.249*10**(-9),540.056*10**(-9)]
deltalambda0 = 0        #exakt
V = 4.372 
deltaV = 0.12
S = 230.42*10**-3
deltaS= 0.9*10**-3
d = 3.213*10**-3
deltad = 0.001*10**-3
dn = [-49000,-60500]
deltadn = [4500, 3500]



#Fehler, die fuer alle Linien gleich sind:

#Fehler auf Magnetfeld

sa = np.pi*r**2 
deltasa = np.sqrt((np.pi*2*r*deltar)**2)

B = Magnetfeld(V, sa, sn) 

def FehleraufMagnetfeld(V,sa,sn):    
    deltaB = np.sqrt((deltaV/(314.16*sa*sn))**2+(-V*deltasa/(314.16*sn*sa**2))**2)
    return deltaB


#Fehler die einzeln Berechnet werden muessen

#A = Abstand(dat, i)

def FehleraufA(dat,i):
    deltaa = []
    deltaA = []
    for j in range(0,18):
        deltaa.append(np.std(dat[:,j]*10**-3))
    deltaA = np.sqrt(deltaa[i]**2+deltaa[-(i+1)]**2)
    return deltaA

#theta = Theta(dat,S,i)

def Fehlerauftheta(dat,S,i):
    A = Abstand(dat, i)
    deltaA = FehleraufA(dat,i)
    
    deltatheta = np.sqrt((2*S*deltaA/(4*S**2+A**2))**2+(2*A*deltaS/(A**2+4*S**2))**2)
    return deltatheta
    
#M = Maximumsordnung(dat, d, n, S, m, lambda0)
    
def FehleraufM(dat, d, n, S, m, lambda0):
    i = 3*m+1
    
    theta = Theta(dat,S,i)
    deltatheta = Fehlerauftheta(dat,S,i)
    
    wurzel = np.sqrt(n**2-1+(np.sin(theta))**2)    
    deltaM = np.sqrt((2*deltad*wurzel/lambda0)**2 + (2*d*n*deltan/(lambda0*wurzel))**2 + (2*d*np.sin(2*theta)*deltatheta/(lambda0*wurzel))**2)
    return deltaM
    
#dealtaf = Frequenzunterschied(dat, d, lambda0, n, S, m, c, dn)
    
def FehleraufFrequenzunterschied(dat, d, lambda0, n, S, m, c, dn, deltadn):
    ip = 3*m
    im = 3*m+2
    
    M = Maximumsordnung(dat, d, n, S, m, lambda0)
    thetap = Theta(dat,S,ip)
    thetam = Theta(dat,S,im)
    
    deltaM = FehleraufM(dat, d, n, S, m, lambda0)
    deltathetap = Fehlerauftheta(dat,S,ip)
    deltathetam = Fehlerauftheta(dat,S,im)
    
    difthetam = -c*np.sin(2*thetam)/(lambda0**2*(lambda0*M**2/d**2-4*n*dn))
    difthetap = c*np.sin(2*thetap)/(lambda0**2*(lambda0*M**2/d**2-4*n*dn))
    difM = 2*c*M*d**2*(np.sin(thetam)**2-np.sin(thetap)**2)/(lambda0*(lambda0*M**2-4*d**2*n*dn)**2) 
    difd = c*M**2*d*(np.cos(2*thetam)-np.cos(2*thetap))/(lambda0*(lambda0*M**2-4*n*dn*d**2)**2)
    difn = -4*c*dn*(np.sin(thetam)**2-np.sin(thetap)**2)/(lambda0**2*(lambda0*M**2/d**2-4*n*dn)**2)
    difdn = -4*c*n*(np.sin(thetam)**2-np.sin(thetap)**2)/(lambda0**2*(lambda0*M**2/d**2-4*n*dn)**2)
    
    deltadeltaf = np.sqrt((difthetam*deltathetam)**2+(difthetap*deltathetap)**2+(difM*deltaM)**2+(difd*deltad)**2+(difn*deltan)**2+(difdn*deltadn)**2)
    return deltadeltaf 
    
#gj = Landefaktor(dat, d, lambda0, n, S, m, c, dn, V, sa, sn, mb, h)
    
def FehleraufLandefaktor(dat, d, lambda0, n, S, m, c, dn, V, sa, sn, mb, h, deltadn):
    deltaf = Frequenzunterschied(dat, d, lambda0, n, S, m, c, dn)
    deltadeltaf = FehleraufFrequenzunterschied(dat, d, lambda0, n, S, m, c, dn, deltadn)
    B = Magnetfeld(V, sa, sn)
    deltaB = FehleraufMagnetfeld(V,sa,sn)
    
    deltagj = np.sqrt((h*deltadeltaf/(mb*B))**2+(-h*deltaf*deltaB/(mb*B**2))**2)
    return deltagj




"Ab hier Testen der Funktionen"

daty = read_from_file('Gelb.txt')
datbg = read_from_file('BlauGruen.txt')
datstg = read_from_file('Steigungen.txt')

lfy0 = Landefaktor(daty, d, lambda0[0], n[0], S, 2, c, datstg[0,0], V, sa, sn, mb, h)    #lines wider than my screen make me a saaad panda
lfy1 = Landefaktor(daty, d, lambda0[0], n[0], S, 1, c, datstg[0,0], V, sa, sn, mb, h)
lfy2 = Landefaktor(daty, d, lambda0[0], n[0], S, 0, c, datstg[0,0], V, sa, sn, mb, h)

lfbg0 = Landefaktor(datbg, d, lambda0[1], n[1], S, 2, c, datstg[1,0], V, sa, sn, mb, h)
lfbg1 = Landefaktor(datbg, d, lambda0[1], n[1], S, 1, c, datstg[1,0], V, sa, sn, mb, h)
lfbg2 = Landefaktor(datbg, d, lambda0[1], n[1], S, 0, c, datstg[1,0], V, sa, sn, mb, h)

lfy = (lfy0 + lfy1 + lfy2)/3
lfbg = (lfbg0 + lfbg1 + lfbg2)/3


print "gelb, M0:",lfy0
print "gelb, M0+1:",lfy1
print "gelb, M0+2:",lfy2
#print lfy

print "blaugruen, M0:",lfbg0
print "blaugruen, M0+1:",lfbg1
print "blaugruen, M0+2:",lfbg2
#print lfbg

#print Maximumsordnung(daty, d, n[0], S, 2, lambda0[0])
#print FehleraufM(daty, d, n[0], S, 2, lambda0[0])
#print Maximumsordnung(daty, d, n[0], S, 1, lambda0[0])
#print FehleraufM(daty, d, n[0], S, 1, lambda0[0])
#print Maximumsordnung(daty, d, n[0], S, 0, lambda0[0])
#print FehleraufM(daty, d, n[0], S, 0, lambda0[0])

print Maximumsordnung(daty, d, n[0], S, 2, lambda0[0])
print FehleraufM(daty, d, n[0], S, 2, lambda0[0])
print Frequenzunterschied(daty, d, lambda0[0], n[0], S, 2, c, dn[0])
print FehleraufFrequenzunterschied(daty, d, lambda0[0], n[0], S, 2, c, dn[0], deltadn[0])
print Landefaktor(daty, d, lambda0[0], n[0], S, 2, c, dn[0], V, sa, sn, mb, h)
print FehleraufLandefaktor(daty, d, lambda0[0], n[0], S, 2, c, dn[0], V, sa, sn, mb, h, deltadn[0])
print Landefaktor(datbg, d, lambda0[1], n[1], S, 2, c, dn[1], V, sa, sn, mb, h)
print FehleraufLandefaktor(datbg, d, lambda0[1], n[1], S, 2, c, dn[1], V, sa, sn, mb, h, deltadn[1])
