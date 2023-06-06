import proj as Proj

def KATEC_to_wgs84(x, y):
    WGS84 = {'proj': 'latlong', 'datum': 'WGS84', 'ellps': 'WGS84'}
    KATEC = {'proj': 'tmerc', 'lat_0': '38N', 'lon_0': '128E', 
             'ellps': 'bessel', 'x_0': '400000', 'y_0': '600000',
             'k': '0.9999', 'units': 'm',
             'towgs84': '-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43'}

    inProj = Proj(**KATEC)
    outProj = Proj(**WGS84)
    return Proj.transform(inProj, outProj, x, y)

KATEC_to_wgs84(320469, 545820)