# Autor: Zbigniew Szymanski
# E-mail: z.szymanski@szymanski-net.eu
# Wersja: 1.1
# Historia zmian:
# 		1.1 dodano przeksztalcenie odwrotne PUWG 1992 ->WGS84
# 		1.0 przeksztalcenie WGS84 -> PUWG 1992
# Data modyfikacji: 2012-11-27
# Uwagi: Oprogramowanie darmowe. Dozwolone jest wykorzystanie i modyfikacja
#        niniejszego oprogramowania do wlasnych celow pod warunkiem
#        pozostawienia wszystkich informacji z naglowka. W przypadku
#        wykorzystania niniejszego oprogramowania we wszelkich projektach
#        naukowo-badawczych, rozwojowych, wdrozeniowych i dydaktycznych prosze
#        o zacytowanie nastepujacego artykulu:
#
#        Zbigniew Szymanski, Stanislaw Jankowski, Jan Szczyrek,
#        "Reconstruction of environment model by using radar vector field histograms.",
#        Photonics Applications in Astronomy, Communications, Industry, and
#        High-Energy Physics Experiments 2012, Proc. of SPIE Vol. 8454, pp. 845422 - 1-8,
#        doi:10.1117/12.2001354
#
# Literatura:
#        Uriasz, J., Wybrane odwzorowania kartograficzne, Akademia Morska w Szczecinie,
#        http://uriasz.am.szczecin.pl/naw_bezp/odwzorowania.html


from math import sin, cos, radians, degrees, tan, atan, log, pi, exp, asin


def wgs84_to_puwg92(B_stopnie, L_stopnie):
    e = 0.0818191910428
    R0 = 6367449.14577
    Snorm = 2.0E-6
    xo = 5760000.0
    a0 = 5765181.11148097
    a1 = 499800.81713800
    a2 = -63.81145283
    a3 = 0.83537915
    a4 = 0.13046891
    a5 = -0.00111138
    a6 = -0.00010504
    L0_stopnie = 19.0
    m0 = 0.9993
    x0 = -5300000.0
    y0 = 500000.0
    Bmin = radians(48.0)
    Bmax = radians(56.0)
    dLmin = radians(-6.0)
    dLmax = radians(6.0)
    B = radians(B_stopnie)
    dL_stopnie = L_stopnie - L0_stopnie
    dL = radians(dL_stopnie)
    if B < Bmin or B > Bmax:
        return 1, 0, 0
    if dL < dLmin or dL > dLmax:
        return 2, 0, 0

    U = 1.0 - e * sin(B)
    V = 1.0 + e * sin(B)
    K = pow((U / V), (e / 2.0))
    C = K * tan(B / 2.0 + pi / 4.0)
    fi = 2.0 * atan(C) - pi / 2.0
    d_lambda = dL

    p = sin(fi)
    q = cos(fi) * cos(d_lambda)
    r = 1.0 + cos(fi) * sin(d_lambda)
    s = 1.0 - cos(fi) * sin(d_lambda)
    XMERC = R0 * atan(p / q)
    YMERC = 0.5 * R0 * log(r / s)

    Z = (XMERC - xo) * Snorm + (YMERC * Snorm) * 1j
    Zgk = a0 + Z * (a1 + Z * (a2 + Z * (a3 + Z * (a4 + Z * (a5 + Z * a6)))))
    Xgk = Zgk.real
    Ygk = Zgk.imag

    Xpuwg = m0 * Xgk + x0
    Ypuwg = m0 * Ygk + y0

    return 0, Xpuwg, Ypuwg


def puwg92_do_wgs84(Xpuwg, Ypuwg):
    L0_stopnie = 19.0
    m0 = 0.9993

    x0 = -5300000.0

    y0 = 500000.0

    R0 = 6367449.14577
    Snorm = 2.0E-6

    xo_prim = 5765181.11148097

    b0 = 5760000

    b1 = 500199.26224125

    b2 = 63.88777449

    b3 = -0.82039170

    b4 = -0.13125817

    b5 = 0.00101782

    b6 = 0.00010778

    c2 = 0.0033565514856

    c4 = 0.0000065718731

    c6 = 0.0000000176466

    c8 = 0.0000000000540

    Xgk = (Xpuwg - x0) / m0
    Ygk = (Ypuwg - y0) / m0

    Z = (Xgk - xo_prim) * Snorm + (Ygk * Snorm) * 1j

    Zmerc = b0 + Z * (b1 + Z * (b2 + Z * (b3 + Z * (b4 + Z * (b5 + Z * b6)))))

    Xmerc = Zmerc.real

    Ymerc = Zmerc.imag

    alfa = Xmerc / R0

    beta = Ymerc / R0

    w = 2.0 * atan(exp(beta)) - pi / 2.0

    fi = asin(cos(w) * sin(alfa))

    d_lambda = atan(tan(w) / cos(alfa))

    B = fi + c2 * sin(2.0 * fi) + c4 * sin(4.0 * fi) + c6 * sin(6.0 * fi) + c8 * sin(8.0 * fi)

    dL = d_lambda

    B_stopnie = degrees(B)

    dL_stopnie = degrees(dL)
    L_stopnie = dL_stopnie + L0_stopnie
    return B_stopnie, L_stopnie