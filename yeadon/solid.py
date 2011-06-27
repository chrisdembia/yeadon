import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import mymath

class stadium:
    '''Stadium
    '''
    def __init__(self,inID,in1,in2, alignment = 'ML' ):
        '''Defines a 2D stadium shape and checks inputs for errors. A stadium, described in Yeadon 1989-ii, is defined by two parameters. Stadia can depracate to circles if their "thickness" is 0.
    
        Parameters
        ----------
        inID : str
            Identifies the type of information for the next two inputs. 'perimwidth' for perimeter and width input, 'depthwidth' for depth and width input, 'perim' for a circle, 'thickradius' for thickness and radius input.
        in1 : float
            Either perimeter, depth, or thickness, as determined by inID
        in2 : float
            Either width, or radius, as determined by inID
        First argument is the perimeter p, and the second is the total width w. If an optional third argument is specified as 1, then the first argument is the half length of the rectangle t, and the second argument is the radius of the semicircle ends. The third argument defaults to 0.
        alignment = 'ML' : str
            Identifies the long direction of the stadium. 'ML' stands for medio-lateral. Aleternatively, 'AP' (anterior-posterior) can be supplied. The only 'AP' stadiums should be at the heels.
        '''
        if inID == 'perimwidth':
            self.perim = in1
            self.width = in2
            self.thick = (np.pi*self.width- self.perim) /(2.0*np.pi-4.0)
            self.radius = (self.perim - 2.0*self.width)   /(2.0*np.pi-4.0)
        elif inID == 'depthwidth':
            self.width = in2
            self.perim = 2.0*in2 + (np.pi - 2.0)*in1
            self.thick = (np.pi*self.width - self.perim) /(2.0*np.pi-4.0)
            self.radius = (self.perim - 2.0*self.width)    /(2.0*np.pi-4.0)
        elif inID == 'perim':
            self.perim = in1
            self.width = self.perim/np.pi
            self.thick = 0.0
            self.radius = self.perim/(2.0*np.pi)
        elif inID == 'thickradius':
            self.thick = in1
            self.radius = in2
            self.perim = 4.0*self.thick + 2.0*np.pi*self.radius
            self.width = 2.0*self.thick + 2.0*self.radius
        else:
            print "Error: stadium not defined properly, must use inID pw, dw, or p"
        
        if self.radius <= 0 or self.thick < 0:
            print "Error: a stadium is defined incorrectly, r must be positive and t must be nonnegative. r = ", self.radius, " and t = ", self.thick, "."

        if alignment != 'AP' and alignment != 'ML':
            print "Error: stadium alignment is not valid, must be either AP or ML"
        else:
            self.alignment = alignment

    def plot(self,ax,c):
        '''Plots the 2D stadium on 3D axes.
        
        Parameters
        ----------
        ax : Axes3D object
            Axis object from the matplotlib library.
        c : str
            Color
        '''
        theta = [np.linspace(0.0,np.pi/2.0,5)]
        x = self.thick + self.radius * np.cos(theta);
        y = self.radius * np.sin(theta);
        xrev = x[:, ::-1]
        yrev = y[:, ::-1]
        X2 = np.concatenate( (x, -xrev, -x, xrev ), axis = 1 )
        Y2 = np.concatenate( (y, yrev, -y, -yrev ), axis = 1 )
        X3 = np.concatenate( (X2, np.nan*X2), axis = 0 )
        Y3 = np.concatenate( (Y2, np.nan*Y2), axis = 0 )
        ax.plot_surface(X3,Y3, np.zeros((2,20)), color=c, alpha = 0.5 )
        
class solid:
    '''Solid
    '''
    def __init__(self,label,density):
        '''Defines a solid. This is a base class. Sets the alpha value to be used for plotting with matplotlib.
        
        Parameters
        ----------
        label : str
            Name of the solid
        density : float
            In units (kg/m^3), used to calculate the solid's mass
        '''
        self.label = label
        self.density = density
        
        solid.alpha = 0.4

    def setOrientation(self,pos,RotMat):
        '''Sets the position, rotation matrix of the solid, and calculate the "absolute" properties (center of mass, and inertia tensor) of the solid.
        '''
        self.pos = pos
        self.RotMat = RotMat
        self.calcProperties()

    def calcProperties(self):
        '''Sets the center of mass and inertia of the solid, both with respect to the fixed human frame.
        '''
        self.COM = self.pos + self.RotMat * self.relCOM
        self.Inertia = mymath.RotateInertia(self.RotMat,self.relInertia)

    def printProperties(self):
        '''Prints the mass, center of mass (local and absolute), and inertia tensor (local and absolute) of the solid.
        '''
        print self.label,"properties:\n"
        print "Mass (kg):",self.Mass,"\n"
        print "COM in local solid's frame (m):\n",self.relCOM,"\n"
        print "COM in fixed human frame (m):\n",self.COM,"\n"
        print "Inertia tensor in solid's frame about local solid's COM (kg-m^2):\n",self.relInertia,"\n"
        print "Inertia tensor in fixed human frame about local solid's COM (kg-m^2):\n",self.Inertia,"\n"
    def draw(self,ax,c):
        print "cannot draw base class solid"

class stadiumsolid(solid):
    '''Stadium solid. Derived from the solid class.
    '''
    def __init__(self,label,density,stadium0,stadium1,height):
        '''Defines a stadium solid object. Creates its base object, and calculates relative/local inertia properties. 
        
        Parameters
        ----------
        label : str
            Name of the solid.
        density : float
            Density of the solid (kg/m^3).
        stadium0 : stadium object
            Lower stadium of the stadium solid.
        stadium1 : stadium object
            Upper stadium of the stadium solid.
        height : float
            Distance between the lower and upper stadia.
        '''
        solid.__init__(self,label,density)
        self.stads = [stadium0,stadium1]
        self.height = height
        
        self.alignment = 'ML'
        # if either stadium is oriented anterior-posterior, inertia must be rotated, and the plots must be modified
        if self.stads[0].alignment == 'AP' or self.stads[1].alignment == 'AP':
            self.alignment = 'AP'

        self.calcRelProperties()
        
    def calcRelProperties(self):
        '''Calculates mass, relative center of mass, and relative/local inertia, according to formulae in Appendix B of Yeadon 1989-ii. If the stadium solid is arranged anterior-posteriorly, the inertia is rotated by pi/2 about the z axis.
        '''
        D = self.density
        h = self.height
        r0 = self.stads[0].radius
        t0 = self.stads[0].thick
        r1 = self.stads[1].radius
        t1 = self.stads[1].thick
        a = (r1 - r0)/r0
        if ( t0 == 0 ):
            b = 1.0
        else:
            b = (t1 - t0)/t0 # DOES NOT WORK FOR CIRCLES!!! 
        self.Mass = D*h*r0*(4.0*t0*self.F1(a,b) + np.pi*r0*self.F1(a,a))
        zcom = D*(h**2.0)*(4.0*r0*t0*self.F2(a,b) + np.pi*(r0**2.0)*self.F2(a,a))/self.Mass
        self.relCOM = np.array([[0.0],[0.0],[zcom]])

        # moments of inertia
        Izcom = D*h*( 4.0*r0*(t0**3.0)*self.F4(a,b)/3.0 + np.pi*(r0**2.0)*(t0**2.0)*self.F5(a,b) + 4.0*(r0**3.0)*t0*self.F4(b,a) + np.pi*(r0**4.0)*self.F4(a,a)*0.5 )
        
        Iy = D*h*(4.0*r0*(t0**3.0)*self.F4(a,b)/3.0 + np.pi*(r0**2.0)*(t0**2.0)*self.F5(a,b) + 8.0*(r0**3.0)*t0*self.F4(b,a)/3.0 + np.pi*(r0**4.0)*self.F4(a,a)*0.25) + D*(h**3.0)*(4.0*r0*t0*self.F3(a,b) + np.pi*(r0**2.0)*self.F3(a,a))
        # CAUGHT AN (minor) ERROR IN YEADON'S PAPER HERE
        Iycom = Iy - self.Mass*(zcom**2.0)
        
        Ix = D*h*(4.0*r0*(t0**3.0)*self.F4(a,b)/3.0 + np.pi*(r0**4.0)*self.F4(a,a)*0.25) + D*(h**3.0)*(4.0*r0*t0*self.F3(a,b) + np.pi*(r0**2.0)*self.F3(a,a))
        
        Ixcom = Ix - self.Mass*(zcom**2.0)
    
        self.relInertia = np.mat([[Ixcom,0.0,0.0],
                                  [0.0,Iycom,0.0],
                                  [0.0,0.0,Izcom]])
                                  
        if self.alignment == 'AP':
            # rearrange to anterior-posterior orientation
            self.relInertia = mymath.RotateInertia(mymath.Rotate3([0,0,np.pi/2]),self.relInertia)

    def draw(self,ax,c):
        '''Draws stadium solid using matplotlib's mplot3d library. Plotted with a non-one value for alpha. Also places the solid's label near the center of mass of the solid. Adjusts the plot for solids oriented anterior-posteriorly. Plots coordinate axes of the solid at the base of the solid.
        '''    
        X0,Y0,Z0,X0toplot,Y0toplot,Z0toplot = self.makePos(0)
        X1,Y1,Z1,X1toplot,Y1toplot,Z1toplot = self.makePos(1)

        for idx in np.arange(X0.size-1):
            Xpts = np.array([[X0[0,idx],X0[0,idx+1]],[X1[0,idx],X1[0,idx+1]]])
            Ypts = np.array([[Y0[0,idx],Y0[0,idx+1]],[Y1[0,idx],Y1[0,idx+1]]])
            Zpts = np.array([[Z0[0,idx],Z0[0,idx+1]],[Z1[0,idx],Z1[0,idx+1]]])
            ax.plot_surface( Xpts, Ypts, Zpts, color = c, alpha = solid.alpha , edgecolor = '');
            if 0:
                if idx == 8:
                    print "IDX IS 8\n",Xpts,'\n',Ypts,'\n',Zpts
                if idx == 9:
                    print "IDX IS 9\n",Xpts,'\n',Ypts,'\n',Zpts
            

        # draw stad0
        ax.plot_surface( X0toplot, Y0toplot, Z0toplot, color=c, alpha = solid.alpha )
        
        # draw stad1
        ax.plot_surface( X1toplot, Y1toplot, Z1toplot, color=c, alpha = solid.alpha )
        
        # rotated unit vectors (unit x prime, etc)
        uxp = self.RotMat * np.array([[1],[0],[0]]) + self.pos
        uyp = self.RotMat * np.array([[0],[1],[0]]) + self.pos
        uzp = self.RotMat * np.array([[0],[0],[1]]) + self.pos

        if 0:
            ax.plot( np.array([self.pos[0,0],uxp[0]]) , np.array([self.pos[1,0],uxp[1]]), np.array([self.pos[2,0],uxp[2]]), color=(1,0,0,1), linewidth = 2)
            ax.plot( np.array([self.pos[0,0],uyp[0]]) , np.array([self.pos[1,0],uyp[1]]), np.array([self.pos[2,0],uyp[2]]), color=(0,1,0,1), linewidth = 2)
            ax.plot( np.array([self.pos[0,0],uzp[0]]) , np.array([self.pos[1,0],uzp[1]]), np.array([self.pos[2,0],uzp[2]]), color=(0,0,1,0), linewidth = 2)

        # place solid's text label on the plot
        (labelstring,b,c) = self.label.partition(':')
        ax.text(self.COM[0],self.COM[1],self.COM[2],labelstring)
        
    def makePos(self,i):
        '''Generates coordinates to be used for matplotlib purposes.
        '''
        theta = [np.linspace(0.0,np.pi/2.0,5)]
        
        x = self.stads[i].thick + self.stads[i].radius * np.cos(theta);
        y = self.stads[i].radius * np.sin(theta);
        
        if self.alignment == 'AP':
            temp = x
            x = y
            y = temp
            del temp

        xrev = x[:, ::-1]
        yrev = y[:, ::-1]

        X = np.concatenate( (x, -xrev, -x, xrev ), axis = 1 )
        Y = np.concatenate( (y, yrev, -y, -yrev ), axis = 1 )
        Z = i*self.height*np.ones( (1,20) )

        POSES = np.concatenate( (X, Y, Z), axis = 0 )
        POSES = self.RotMat * POSES
        X,Y,Z = np.vsplit(POSES,3)
        
        X = X + self.pos[0]
        Y = Y + self.pos[1]
        Z = Z + self.pos[2]
        
        Xtoplot = np.array(np.concatenate( (X, np.nan*X) ) )
        Ytoplot = np.array(np.concatenate( (Y, np.nan*Y) ) )
        Ztoplot = np.array(np.concatenate( (Z, np.nan*Z) ) )
        
        return X,Y,Z,Xtoplot,Ytoplot,Ztoplot

    def F1(self,a,b):
        '''Integration term. See Yeadon 1990-ii Appendix 2.'''
        return 1.0 + (a+b)*0.5 + a*b/3.0
    def F2(self,a,b):
        '''Integration term. See Yeadon 1990-ii Appendix 2.'''
        return 0.5 + (a+b)/3.0 + a*b*0.25
    def F3(self,a,b):
        '''Integration term. See Yeadon 1990-ii Appendix 2.'''
        return 1.0/3.0 + (a+b)/4.0 + a*b*0.2
    def F4(self,a,b):
        '''Integration term. See Yeadon 1990-ii Appendix 2.'''
        return 1.0 + (a+3.0*b)*0.5 + (a*b + b**2.0) + (3.0*a*b**2.0 + b**3.0)*0.25 + a*(b**3.0)*0.2
    def F5(self,a,b):
        '''Integration term. See Yeadon 1990-ii Appendix 2.'''
        return 1.0 + (a+b) + (a**2.0 + 4.0*a*b + b**2.0)/3.0 + a*b*(a+b)*0.5 + (a**2.0)*(b**2.0)*0.2
        
class semiellipsoid(solid):
    '''Semiellipsoid.
    '''
    def __init__(self,label,density,baseperim,height):
        '''Defines a semiellipsoid (solid) object. Creates its base object, and calculates relative/local inertia properties. The base is circular (its height axis is pointed upwards), so only 2 parameters are needed to define the semiellipsoid.
        
        Parameters
        ----------
        label : str
            Name of the solid.
        density : float
            Density of the solid (kg/m^3).
        baseperimeter : float
            The base is circular.
        radius : float
            Calculated for base perimeter.
        height : float
            The remaining minor axis.
        '''
        solid.__init__(self,label,density)
        self.baseperimeter = baseperim
        self.radius = self.baseperimeter/(2.0*np.pi)
        self.height = height

        self.calcRelProperties()

    def calcRelProperties(self):
        '''Calculates mass, relative center of mass, and relative/local inertia, according to formulae in Appendix B of Yeadon 1989-ii.
        '''
        D = self.density
        r = self.radius
        h = self.height
        self.Mass = D*2.0/3.0*np.pi*(r**2)*h
        self.relCOM = np.array([[0.0],[0.0],[3.0/8.0*h]])
        
        Izcom = D*4.0/15.0*np.pi*(r**4.0)*h
        Iycom = D*np.pi*( 2.0/15.0*(r**2.0)*h*(r**2.0+h**2.0) - 3.0/32.0*(r**2.0)*(h**3.0) )
        Ixcom = Iycom
        self.relInertia = np.mat([[Ixcom,0.0,0.0],
                                  [0.0,Iycom,0.0],
                                  [0.0,0.0,Izcom]])

    def draw(self,ax,c):
        '''Draws semiellipsoid using matplotlib's mplot3d library. Plotted with a non-one value for alpha. Also places the solid's label near the center of mass of the solid. Plots coordinate axes of the solid at the base of the solid. Code is modified from matplotlib documentation for mplot3d.
        '''
        N = 30
        u = np.linspace(0, 2.0 * np.pi, N)
        v = np.linspace(0, np.pi/2.0, N)

        x = self.radius * np.outer(np.cos(u), np.sin(v))
        y = self.radius * np.outer(np.sin(u), np.sin(v))
        z = self.height * np.outer(np.ones(np.size(u)), np.cos(v))
        
        for i in np.arange(N):
            for j in np.arange(N):
                POS = np.array([[x[i,j]],[y[i,j]],[z[i,j]]])
                POS = self.RotMat * POS
                x[i,j] = POS[0,0]
                y[i,j] = POS[1,0]
                z[i,j] = POS[2,0]
            
        x = self.pos[0,0] + x
        y = self.pos[1,0] + y
        z = self.pos[2,0] + z        

        # must rotate the x y and z
        ax.plot_surface(x, y, z, rstride=4, cstride=4, color=c, alpha = solid.alpha , edgecolor ='')
        
        (labelstring,b,c) = self.label.partition(':')
        ax.text(self.COM[0],self.COM[1],self.COM[2],labelstring)            

