import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg
import random
import math

def makeMatrix1(f,n):
    return makeMatrix2(f, range(n), range(n))
    
def makeMatrix2(f,rows, cols):
    return np.array([[f(i,j) for j in cols] for i in rows])
    
def resample_chain(numpoints, theta1, givendict):
    def kernel(x1,x2):
        return math.exp(-(theta1/2)*(x1-x2)**2)

    xs = [n+1 for n in range(numpoints)]
    Xgiven = givendict['xs']
    Ygiven = givendict['ys']
    if len(Xgiven) > 0:

        mu11 = np.array([0]*len(Ygiven))
        mu2 = [0]*len(xs)
        sig11 = makeMatrix2(kernel,Xgiven,Xgiven)
        sig12 = makeMatrix2(kernel,Xgiven, xs)
        sig21 = np.transpose(sig12)
        sig22 = makeMatrix2(kernel, xs, xs )

        inv11 = np.linalg.inv(sig11)
        temp = np.dot(inv11,(Ygiven-mu11))
        mu2_1 = mu2 + np.dot(sig21,temp)

        temp = np.dot( inv11,sig12)
        sig2_1 = sig22 - np.dot(sig21,temp)

        ys = np.random.multivariate_normal(mu2_1, sig2_1)
        std = np.diagonal(sig2_1)
        colors = ['blue']*numpoints
        for x in Xgiven:
            colors[x-1] = 'red'
    else:
        mu = [0]*numpoints
        sigma = makeMatrix1(kernel, numpoints)
        ys = np.random.multivariate_normal(mu, sigma)
        std=np.diagonal(sigma)
        colors =['blue']*numpoints
    
    return dict(xs=xs, ys=ys, std=std, color=colors)


def resample(numpoints, covar, given = None):
    s12 = s21 = covar;
    s11 = s22 = 1;
    sigma = [[ s11, s12],
             [ s21, s22]]

    L = scipy.linalg.cholesky(sigma, lower =True)
    mu1 = mu2 = 0
    mu = np.array([mu1,mu2]);
    x = np.array([mu1,mu2]);
    for i in range(numpoints):
        xnew = [random.gauss(0,1) for i in range(2)]
        x = np.vstack([x,mu + np.dot(L,xnew)])
    if numpoints == 1:
        return dict(x1=[x[1,0]],x2=[x[1,1]])
    else:
        return dict(x1=x[1:,0],x2=x[1:,1])

def resample_givenX1(numpoints, covar, x1):
    s12 = s21 = covar
    s11 = s22 = 1;
    sigma = [[ s11, s12],
             [ s21, s22]]
        
    mu1 = 0
    mu21 = mu1 + (s21/s11)*(x1-mu1)
    sig21 = s22 - (s21/s11)*s12

    x = np.array([x1,mu21]);
    for _ in range(numpoints):
        x = np.vstack([x,[x1, random.gauss(mu21,sig21)]])
    
    if numpoints == 1:
        return dict(x1=[x[1,0]],x2=[x[1,1]])
    else:
        return dict(x1=x[1:,0],x2=x[1:,1])
    
def update_normal(covar, x1):
    s12 = s21 = covar
    s11 = s22 = 1;
    sigma = [[ s11, s12],
             [ s21, s22]]
    mu1 = 0
    mu21 = mu1 + (s21/s11)*(x1-mu1)
    sig21 = s22 - (s21/s11)*s12
    
    yd = np.array([mu21]);
    xs = np.linspace(-3,3,100)
    norm_const=1/(math.sqrt(2*math.pi*sig21))
    for x in xs:
        x2 = x1 + (norm_const*math.exp(-(1/(2*sig21))*(x-mu21)**2))
        yd = np.vstack([yd,x2])
    return dict(xs=yd[1:], ys=xs)
    
def get_contour_data(X, Y, Z):
    cs = plt.contour(X, Y, Z, levels=[.05,.2], colors='b')
    xs = []
    ys = []
    col = []
    isolevelid = 0
    for isolevel in cs.collections:
        isocol = isolevel.get_color()[0]
        thecol = 3 * [None]
        theiso = str(cs.get_array()[isolevelid])
        isolevelid += 1
        for i in range(3):
            thecol[i] = int(255 * isocol[i])
        thecol = '#%02x%02x%02x' % (thecol[0], thecol[1], thecol[2])

        for path in isolevel.get_paths():
            v = path.vertices
            x = v[:, 0]
            y = v[:, 1]
            xs.append(x.tolist())
            ys.append(y.tolist())
            col.append(thecol)
    return dict(xs=xs, ys=ys, line_color=col)

def drawContour(covar):
    delta = 0.1
    xs = np.arange(-3.0, 3.0, delta)
    ys = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(xs, ys)
    
    s12 = s21 = covar
    s11 = s22 = 1;
    sigma = [[ s11, s12],
             [ s21, s22]]
    L = scipy.linalg.cholesky(sigma, lower =True)
    
    sigma = np.dot(L,np.transpose(L))
    I = [[1,0],[0,1]]
    sigmainv = np.linalg.solve(np.transpose(L),np.linalg.solve(L,I))
    
    normal_const = 1/(math.sqrt(2*math.pi* np.linalg.det(sigma)))
    zs = np.array([])
    for v in zip(X.flatten(),Y.flatten()):
        temp2 = np.dot(sigmainv, v)
        temp3 = np.dot(np.transpose(v), temp2)
        z = normal_const* np.exp((-1/2)*temp3)
        zs = np.concatenate((zs,[z]))
    return get_contour_data(X,Y,zs.reshape(X.shape))