def somme_ligne(A):
    n,p=array(A).shape
    B=zeros((n,1))
    for k in range(0,n):
        for j in range(0,p):
            B[k][0]+=A[k][j]
    return B

def mat_S(L):
    n,p=array(L).shape
    M=somme_ligne(L)
    for k in range(0,n):
        if M[k][0]!=0:
            for j in range(0,p):
                L[k][j]=L[k][j]/M[k][0]
        else:
            for j in range(0,p):
                L[k][j]=1/p
    return L

def mat_G(S,a):
    n,p=array(S).shape
    E=ones((n,p))
    return array(S)*a+array(E)*(1-a)

def normalisation(L):
    n,p=array(L).shape
    M=somme_ligne(L)
    for k in range(0,n):
        for j in range(0,p):
            L[k][j]=L[k][j]/M[k][0]
    return L
    
def lisible(L):
    n,p=array(L).shape
    for k in range(0,n):
        for j in range(0,p):
            L[k][j]=1000*L[k][j]
            L[k][j]=int(L[k][j])
            L[k][j]=L[k][j]/1000
    return L

A=[[0,0,1,0,1,0,0,0,0,0],
[0,0,0,0,1,0,1,0,0,0],
[1,0,0,0,0,0,0,1,1,0],
[0,0,0,0,0,1,0,1,0,0],
[0,1,0,0,0,0,1,0,0,0],
[0,0,0,0,0,0,0,0,1,1],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,1,0,0,1,0,0,0],
[0,0,0,1,0,0,0,0,0,1],
[0,0,1,0,0,0,0,0,0,0]
]
>>> matrix_power(normalisation(mat_G(mat_S(A),0.001)),4)[0][0]-matrix_power(normalisation(mat_G(mat_S(A),0.001)),3)[0][0]
3.90e-14
>>> matrix_power(normalisation(mat_G(mat_S(A),0.5)),9)[0][0]-matrix_power(normalisation(mat_G(mat_S(A),0.5)),8)[0][0]
6.20e-12
>>> matrix_power(normalisation(mat_G(mat_S(A),0.85)),16)[0][0]-matrix_power(normalisation(mat_G(mat_S(A),0.85)),15)[0][0]
-6.35e-11
>>> matrix_power(normalisation(mat_G(mat_S(A),0.999)),50)[0][0]-matrix_power(normalisation(mat_G(mat_S(A),0.999)),49)[0][0]
-6.57e-11