:- consult('filtros.pl').
:- consult('aprendizaje.pl').
:- use_module(library(random)).


% RECOMENDADOR PRINCIPAL


% Caso 1
recomendar(User, SiPostre, Veg, TipoC, Min, Max, Incluye, Evita, N, Menus) :-
    \+ estado_aprendizaje(User, aprendizaje_activo),
    findall(menu(E,C,X,Y,P,Cal),
        ( (Veg == si ->
              menu_vegetariano_segun_postre(SiPostre, E,C,X,Y,P,Cal)
          ;   menu_segun_postre(SiPostre, E,C,X,Y,P,Cal)
          ),
          en_rango(Min, Max, Cal),
          cumple_tipo_carne(X, TipoC),
          incluye_ok(Incluye, E,C,X,Y,P),
          evita_ok(Evita, E,C,X,Y,P)
        ),
    MenusRaw),
    random_permutation(MenusRaw, Barajados),
    take_first_n(Barajados, N, Menus),
    !,  % ← asegura UNA sola solución del predicado completo
    format('Usuario ~w sin aprendizaje suficiente, mostrando menús básicos.~n', [User]).

% Caso 2
recomendar(User, SiPostre, Veg, TipoC, Min, Max, Incluye, Evita, N, TopMenus) :-
    estado_aprendizaje(User, aprendizaje_activo),
    findall(menu(E,C,X,Y,P,Cal),
        ( (Veg == si ->
              menu_vegetariano_segun_postre(SiPostre, E,C,X,Y,P,Cal)
          ;   menu_segun_postre(SiPostre, E,C,X,Y,P,Cal)
          ),
          en_rango(Min, Max, Cal),
          cumple_tipo_carne(X, TipoC),
          incluye_ok(Incluye, E,C,X,Y,P),
          evita_ok(Evita, E,C,X,Y,P)
        ),
    MenusRaw),
    maplist(menu_score_pair(User), MenusRaw, Pairs),
    sort(0, @>=, Pairs, Sorted),
    pairs_values(Sorted, SortedMenus),
    take_first_n(SortedMenus, N, TopMenus),
    !,  % ← corta elección adicional
    format('Usuario ~w con aprendizaje activo, mostrando menús personalizados.~n', [User]).



% UTILIDADES

menu_score_pair(User, Menu, Score-Menu) :-
    score_menu(User, Menu, Score).

pairs_values([], []).
pairs_values([_-V|T],[V|T2]) :- pairs_values(T,T2).

take_first_n(List, N, FirstN) :-
    length(FirstN, N),
    append(FirstN, _, List), !.


% PUNTUACIÓN (aprendizaje simbólico)

score_menu(User, menu(E,C,X,Y,P,Cal), Score) :-
    base_score(User, menu(E,C,X,Y,P,Cal), 0, Score).

base_score(User, M, Acc, Score) :-

    % 1. Preferencia de tipo de carne

    ( regla(User, preferencia(carne, TipoP)),
      M = menu(_,_,C,_,_,_),
      carne(C,_,TipoP,_)
    -> Acc1 is Acc + 3
    ;  Acc1 = Acc ),

    % 2. Preferencia de postre

    ( regla(User, preferencia(postre, PrefP)),
      M = menu(_,_,_,_,P,_),
      (PrefP == none, P \= none -> Acc2 is Acc1 - 2 ;
       PrefP \= none, P \= none -> Acc2 is Acc1 + 1 ;
       Acc2 = Acc1)
    ; Acc2 = Acc1 ),

    % 3. Preferencia calórica (cercanía al promedio aprendido)

    ( regla(User, preferencia(calorias_promedio, Prom)),
      M = menu(_,_,_,_,_,Cal),
      Diff is abs(Cal - Prom),
      ( Diff =< 100 -> Acc3 is Acc2 + 2
      ; Diff =< 200 -> Acc3 is Acc2 + 1
      ; Acc3 = Acc2 )
    ; Acc3 = Acc2 ),


    % 4. Entrada y vegetal favoritos

    ( regla(User, preferencia(entrada, EntFav)),
      M = menu(E,_,_,_,_,_),
      E == EntFav
    -> Acc4 is Acc3 + 2
    ;  Acc4 = Acc3 ),

    ( regla(User, preferencia(vegetal, VegFav)),
      M = menu(_,_,_,V,_,_),
      V == VegFav
    -> Acc5 is Acc4 + 2
    ;  Acc5 = Acc4 ),


    % Combinaciones frecuentes (carne + vegetal)

    ( regla(User, preferencia(combinacion, (TipoFav, VegFav))),
      M = menu(_,_,C,_,_,_),
      carne(C,_,TipoFav,_),
      M = menu(_,_,_,VegFav,_,_)
    -> Acc6 is Acc5 + 3
    ;  Acc6 = Acc5 ),

    % Evitaciones simples y combinadas

    ( regla(User, evita(IngEv)),
      M = menu(E,C,X,Y,P,_),
      member(IngEv, [E,C,X,Y,P])
    -> Acc7 is Acc6 - 3
    ;  Acc7 = Acc6 ),

    ( regla(User, evita_combinacion(Ev1,Ev2)),
      M = menu(E,C,X,Y,P,_),
      member(Ev1, [E,C,X,Y,P]),
      member(Ev2, [E,C,X,Y,P])
    -> Acc8 is Acc7 - 4
    ;  Acc8 = Acc7 ),

    % Reglas condicionales (contexto)

    ( regla(User, preferencia_condicional(postre, Tipo, Pref)),
      M = menu(_,_,C,_,P,_),
      carne(C,_,Tipo,_),
      (Pref == si, P \= none -> Acc9 is Acc8 + 2 ;
       Pref == no, P == none -> Acc9 is Acc8 + 2 ;
       Acc9 is Acc8 - 1)
    ;  Acc9 = Acc8 ),


    % Bonificación general si el menú cumple muchas reglas

    (Acc9 >= 10 -> Score is Acc9 + 1 ; Score = Acc9).


% INCLUIR / EVITAR INGREDIENTES MANUALMENTE

incluye_ok([], _,_,_,_,_).
incluye_ok([I|T], E,C,X,Y,P) :-
    ingrediente_en_menu(I, E,C,X,Y,P),
    incluye_ok(T, E,C,X,Y,P).

evita_ok([], _,_,_,_,_).
evita_ok([I|T], E,C,X,Y,P) :-
    \+ ingrediente_en_menu(I, E,C,X,Y,P),
    evita_ok(T, E,C,X,Y,P).
