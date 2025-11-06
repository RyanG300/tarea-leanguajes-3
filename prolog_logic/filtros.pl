:- consult('combinaciones.pl').


en_rango(Min, Max, Cal) :-
    (var(Min) ; Cal >= Min),
    (var(Max) ; Cal =< Max).

menu_segun_postre(si, E,C,X,Y,P,Cal) :- menu_con_postre(E,C,X,Y,P,Cal).
menu_segun_postre(no, E,C,X,Y,none,Cal) :- menu_sin_postre(E,C,X,Y,none,Cal).

menu_vegetariano_segun_postre(si, E,C,X,Y,P,Cal) :-
    entrada(E, CalE, vegetariana, _),
    plato_fuerte_vegetariano(C,X,Y,CalPF),
    postre(P, CalPo, _),
    Cal is CalE + CalPF + CalPo.

menu_vegetariano_segun_postre(no, E,C,X,Y,none,Cal) :-
    entrada(E, CalE, vegetariana, _),
    plato_fuerte_vegetariano(C,X,Y,CalPF),
    Cal is CalE + CalPF.

cumple_tipo_carne(Carne, TipoDeseado) :-
    carne(Carne, _, TipoC, _),
    (TipoDeseado = any ; TipoC = TipoDeseado).

ingrediente_en_menu(I,E,C,X,Y,P) :- member(I,[E,C,X,Y,P]), I \= none.
