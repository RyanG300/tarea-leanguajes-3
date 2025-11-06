:- consult('base_alimentos.pl').


plato_fuerte(Carb, Carne, Veg, CalPF) :-
    carbohidrato(Carb, CalC, _),
    carne(Carne, CalM, _, _),
    vegetal(Veg, CalV, _),
    CalPF is CalC + CalM + CalV.

plato_fuerte_vegetariano(Carb, ProtVeg, Veg, CalPF) :-
    carbohidrato(Carb, CalC, _),
    carne(ProtVeg, CalP, vegetariana, _),
    vegetal(Veg, CalV, _),
    CalPF is CalC + CalP + CalV.

plato_fuerte_vegetariano(C1, C2, Veg, CalPF) :-
    carbohidrato(C1, Cal1, _),
    carbohidrato(C2, Cal2, _),
    vegetal(Veg, CalV, _),
    CalPF is Cal1 + Cal2 + CalV.

plato_fuerte_vegetariano(C, V1, V2, CalPF) :-
    carbohidrato(C, CalC, _),
    vegetal(V1, Cal1, _),
    vegetal(V2, Cal2, _),
    CalPF is CalC + Cal1 + Cal2.

menu_con_postre(E, C, X, Y, P, Cal) :-
    entrada(E, CalE, _, _),
    (plato_fuerte(C, X, Y, CalPF); plato_fuerte_vegetariano(C, X, Y, CalPF)),
    postre(P, CalPo, _),
    Cal is CalE + CalPF + CalPo.

menu_sin_postre(E, C, X, Y, none, Cal) :-
    entrada(E, CalE, _, _),
    (plato_fuerte(C, X, Y, CalPF); plato_fuerte_vegetariano(C, X, Y, CalPF)),
    Cal is CalE + CalPF.