import numpy as np

def rain_attenuation(freqHz:float, rainrate:float, polarization, elevation):
    """
    rainrate: [mm/hour]
    """
    
    a,k = _rain_coeff(freqHz, polarization,elevation)
    
    rain_atten_dBkm = k*rainrate**a
    
    return rain_atten_dBkm
    

def _rain_coeff(freqHz:float, polarization:float, elevation):
    """
    ITU-R P.838-3  Revision 2005 March
    https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.838-3-200503-I!!PDF-E.pdf
    
    Attenuation due to rain at specified rate in mm/hour
    freqHz: Frequency [Hz]
    polarization: "v" or "h" or float for elliptical (45 degrees for circular) 
    elevation angle: Degrees above horizon of path
    """
    freqHz = np.asarray(freqHz)
    assert ((1e9 <= freqHz) &  (freqHz < 1e16)).all(),'Model validity bounds: 1-1000 GHz'
    
    if polarization == 'v':
        polarization = 90.
    elif polarization == 'h':
        polarization = 0
    else:
        assert isinstance(polarization,(int,float)) and 0. <= polarization <=90.
        elevation = np.radians(elevation)
        polarization = np.radians(elevation)
         
    if np.isclose(polarization,0.):
        # Table 1
        ak = (-5.33980, -0.35351, -0.23789, -0.94158)
        bk = (-0.10008, 1.26970, 0.86036, 0.64552)
        ck = (1.13098, 0.45400, 0.15354, 0.16817)
        mk = -0.18961
        Ck = 0.71147
    
        # Table 3
        aa = (-0.14318, 0.29591, 0.32177, -5.37610, 16.1721)
        ba = (1.82442, 0.77564, 0.63773, -0.96230, -3.29980)
        ca= (-0.55187, 0.19822, 0.13164, 1.47828, 3.43990)
        ma = 0.67849
        Ca = -1.95537
    elif np.isclose(polarization,90.):    
        # Table 2
        ak = (-3.80595, -3.44965, -0.39902, 0.50167)
        bk = (0.56934, -0.22911, 0.73042, 1.07319)
        ck = (0.81061, 0.51059, 0.11899, 0.27195)
        mk = -0.16398
        Ck = 0.63297
        
        # Table 4
        aa = (-0.07771, 0.56727, -0.20238, -48.2991, 48.5833)
        ba = (2.33840, 0.95545, 1.14520, 0.791669, 0.791459)
        ca = (-0.76284, 0.54039, 0.26809, 0.116226, 0.116479)
        ma = -0.053739
        Ca = 0.83433
    else:
#%% elliptical polarization
        av,kv = _rain_coeff(freqHz,'v',elevation)
        ah,kh = _rain_coeff(freqHz,'h',elevation)
        
        # Equation 4
        k = (kh + kv + (kh-kv)*np.cos(elevation)**2 * np.cos(2.*polarization)) / 2.
        # Equation 5
        a = (kh*ah + kv*av + (kh*ah-kv*av)*np.cos(elevation)**2 * np.cos(2*polarization)) / (2.*k)
        
        return a,k
#%%      
    logF = np.log10(freqHz/1e9)
#%% compute k (Equation 2)
    logk = 0.
    for j in range(4):
        logk += ak[j] * np.exp(-((logF-bk[j])/ck[j])**2) 
        
    logk += mk * logF + Ck    
    k = 10**logk
#%% compute alpha==a (Equation 3)
    a = 0.
    for j in range(5):
        a += aa[j] * np.exp(-((logF - ba[j])/ca[j])**2) 
        
    a += ma * logF + Ca

    return a,k
