# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 11:11:10 2022

@author: GMET_PORTABLE
"""

import numpy as np




#########################
# DOMMAGES TYPES P OU M #
#########################

#-----------------------------#
# Composantes des contraintes #
#-----------------------------#

def calculate_sigma_N(Nb, d3) :
    sigma_N = 4*abs(Nb)/(np.pi*d3**2)
    return sigma_N

def calculate_sigma_M(Mb, d3) :
    sigma_M = 32*Mb/(np.pi*d3**3)
    return sigma_M

def calculate_tau_th_N(Nb, d2, L_prime) :
    tau_th_N = 2*abs(Nb)/(np.pi*d2*L_prime)
    return tau_th_N

def calculate_tau_th_M(Mb, d2, L_prime) :
    tau_th_M = 8*Mb/(np.pi*L_prime*d2**2)
    return tau_th_M

def calculate_tau_T(T, d3) :
    tau_T = 4*T/(np.pi*d3**2)
    return tau_T

def calculate_tau_Cr(Cr, d3) :
    tau_Cr = 16*Cr/(np.pi*d3**3)
    return tau_Cr

def calculate_tau_h_N(Nb, d1, H) :
    tau_h_N = abs(Nb)/(np.pi*d1*H)
    return tau_h_N

def calculate_tau_h_M(Mb, dl, H) :
    tau_h_M = Mb/(np.pi*H*dl**2)
    return tau_h_M

def calculate_tau_Ct(Ct, d1) :
    tau_Ct = 16*Ct/(np.pi*d1**3)
    return tau_Ct

def calculate_p_th_N(Nb, p, d, D, Le) :
    p_th_N = 4*abs(Nb)*p/(np.pi*(d**2 - D**2)*Le)
    return p_th_N

def calculate_p_th_M(Mb, p, d, D, Le) :
    p_th_M = 96*Mb*p/(np.pi*(d - D)*((d + D)**2 + 2*d**2)*Le)
    return p_th_M

def calculate_p_h_N(Nb, a, Dp) :
    p_h_N = 4*abs(Nb)/(np.pi*(a**2 - Dp**2))
    return p_h_N

def calculate_p_h_M(Mb, a, Dp) :
    p_h_M = 96*Mb/(np.pi*(a - Dp)*((a + Dp)**2 + 2*a**2))
    return p_h_M


#--------------------------#
# Contraintes équivalentes #
#--------------------------#

#Sigma_m
def calculate_sigma_m(Nb, T, d3) :
    sigma_N = calculate_sigma_N(Nb, d3)
    tau_T = calculate_tau_T(T, d3)
    sigma_m = (sigma_N**2 + 3*tau_T**2)**0.5
    return sigma_m

#Sigma_m_plus_b
def calculate_sigma_m_plus_b(Nb, Mb, T, Cr, d3) :
    sigma_N = calculate_sigma_N(Nb, d3)
    sigma_M = calculate_sigma_M(Mb, d3)
    tau_T = calculate_tau_T(T, d3)
    tau_Cr = calculate_tau_Cr(Cr, d3)
    sigma_m_plus_b = ((sigma_N + sigma_M)**2 + 3*(tau_Cr + tau_T)**2)**0.5
    return sigma_m_plus_b

#Tau_th
def calculate_tau_th(Nb, Mb, d2, L_prime) :
    tau_th_N = calculate_tau_th_N(Nb, d2, L_prime)
    tau_th_M = calculate_tau_th_M(Mb, d2, L_prime)
    tau_th = tau_th_N + tau_th_M
    return tau_th

#Tau_h
def calculate_tau_h(Nb, Mb, Ct, d1, H) :
    tau_h_N = calculate_tau_h_N(Nb, d1, H)
    tau_h_M = calculate_tau_h_M(Mb, d1, H)
    tau_Ct = calculate_tau_Ct(Ct, d1)
    tau_h = ((tau_h_N + tau_h_M)**2 + tau_Ct**2)**0.5
    return tau_h

#P_th
def calculate_p_th(Nb, Mb, p, d, D, Le) :
    p_th_N = calculate_p_th_N(Nb, p, d, D, Le)
    p_th_M = calculate_p_th_M(Mb, p, d, D, Le)
    p_th = p_th_N + p_th_M
    return p_th

#P_h
def calculate_p_h(Nb, Mb, a, Dp) :
    p_h_N = calculate_p_h_N(Nb, a, Dp)
    p_h_M = calculate_p_h_M(Mb, a, Dp)
    p_h = p_h_N + p_h_M
    return p_h





###########
# FATIGUE #
###########


def calculate_Delta_Sigma(L_Donnees) :
    d = L_Donnees[0][1]
    p = L_Donnees[1][1]
    Ne = L_Donnees[2][1]
    Te = L_Donnees[3][1]
    Me = L_Donnees[4][1]
    Cr = 0
    
    d3 = d - 1.2268*p
    
    sigma_N = calculate_sigma_N(Ne, d3)
    sigma_M = calculate_sigma_M(Me, d3)
    tau_T = calculate_tau_T(Te, d3)
    tau_Cr = calculate_tau_Cr(Cr, d3)

    Delta_Sigma = ((sigma_N + sigma_M)**2 + 3*(tau_Cr + tau_T)**2)**0.5
    
    return Delta_Sigma



def calculate_Delta_Epsilon(Delta_Sigma, E_T) :
    return (Delta_Sigma/E_T)*100



def calculate_Delta_Sigma_Barre(NbAL, d, p, Delta_Sigma, K_F, Symin_T, Sumin_T) :
    """


    Parameters
    ----------
    NbPL : TYPE
        DESCRIPTION.
    d : TYPE
        DESCRIPTION.
    p : TYPE
        DESCRIPTION.
    Delta_Sigma : TYPE
        DESCRIPTION.
    K_F : TYPE
        DESCRIPTION.
    Symin_T : TYPE
        DESCRIPTION.
    Sumin_T : TYPE
        DESCRIPTION.

    Returns
    -------
    Delta_Sigma_Barre : TYPE
        DESCRIPTION.

    """
    
    d3 = d - 1.2268*p
    sigma_N = calculate_sigma_N(NbAL, d3)
    
    print("Sigma_N = ", sigma_N)
    
    sigma_m = min(Symin_T, K_F*sigma_N)
    
    print("Sigma_m = ", sigma_m)
    
    Delta_Sigma_Barre = Delta_Sigma/(1 - sigma_m/Sumin_T)
    
    return Delta_Sigma_Barre

