:- dynamic(aceptado/2).
:- dynamic(rechazado/2).
:- dynamic(regla/2).


%  REGISTRO DE DATOS

registrar_aceptado(U, M) :- assertz(aceptado(U, M)).
registrar_rechazado(U, M) :- assertz(rechazado(U, M)).

min_ejemplos(3).

cantidad_aceptados(U, N) :- findall(X, aceptado(U,X), L), length(L,N).
cantidad_rechazados(U, N) :- findall(X, rechazado(U,X), L), length(L,N).

estado_aprendizaje(U, aprendizaje_activo) :-
    cantidad_aceptados(U,A), cantidad_rechazados(U,R),
    S is A+R, min_ejemplos(M), S >= M.


%  INDUCCIÓN DE PREFERENCIAS


inducir_preferencias(U) :-
    estado_aprendizaje(U, aprendizaje_activo), !,
    writeln('Aprendiendo preferencias avanzadas del usuario.'),

    inducir_basicas(U),
    inducir_combinaciones(U),
    inducir_evitaciones(U),
    inducir_condicionales(U),

    writeln('Aprendizaje completo y actualizado.').

inducir_preferencias(_) :-
    writeln('Pocos datos todavía, no se ha inducido aprendizaje.').



inducir_basicas(U) :-
    % Tipo de carne preferido
    findall(Tipo, (aceptado(U, menu(_,_,C,_,_,_)), carne(C,_,Tipo)), LCarne),
    (LCarne \= [] ->
        contar_frecuencias(LCarne, FCarne),
        max_member(_-TipoCarne, FCarne),
        retractall(regla(U, preferencia(carne,_))),
        assertz(regla(U, preferencia(carne, TipoCarne))),
        format('Prefiere carne de tipo: ~w~n', [TipoCarne])
    ; true),

    % Preferencia de postre
    findall(P, aceptado(U, menu(_,_,_,_,P,_)), LPostres),
    (LPostres \= [] ->
        contar_frecuencias(LPostres, FPostres),
        max_member(_-PostrePref, FPostres),
        retractall(regla(U, preferencia(postre,_))),
        assertz(regla(U, preferencia(postre, PostrePref))),
        format('Prefiere postre: ~w~n', [PostrePref])
    ; true),

    % Promedio de calorías
    findall(Cal, aceptado(U, menu(_,_,_,_,_,Cal)), LCal),
    (LCal \= [] ->
        sum_list(LCal, TotalCal), length(LCal, NCal), Prom is TotalCal / NCal,
        retractall(regla(U, preferencia(calorias_promedio,_))),
        assertz(regla(U, preferencia(calorias_promedio, Prom))),
        format('Promedio calórico preferido: ~0f~n', [Prom])
    ; true),

    % Entrada más frecuente
    findall(E, aceptado(U, menu(E,_,_,_,_,_)), LEntradas),
    (LEntradas \= [] ->
        contar_frecuencias(LEntradas, FEnt),
        max_member(_-EntradaPref, FEnt),
        retractall(regla(U, preferencia(entrada,_))),
        assertz(regla(U, preferencia(entrada, EntradaPref))),
        format('Entrada preferida: ~w~n', [EntradaPref])
    ; true),

    % Vegetal más frecuente
    findall(V, aceptado(U, menu(_,_,_,V,_,_)), LVegs),
    (LVegs \= [] ->
        contar_frecuencias(LVegs, FVegs),
        max_member(_-VegPref, FVegs),
        retractall(regla(U, preferencia(vegetal,_))),
        assertz(regla(U, preferencia(vegetal, VegPref))),
        format('Vegetal preferido: ~w~n', [VegPref])
    ; true).


% COMBINACIONES FRECUENTES

inducir_combinaciones(U) :-
    findall((Tipo,Veg), (
        aceptado(U, menu(_,_,C,_,_,_)),
        carne(C,_,Tipo),
        aceptado(U, menu(_,_,_,Veg,_,_))
    ), LComb),
    (LComb \= [] ->
        contar_frecuencias(LComb, FComb),
        max_member(_-(TipoPref, VegPref), FComb),
        retractall(regla(U, preferencia(combinacion,_))),
        assertz(regla(U, preferencia(combinacion, (TipoPref, VegPref)))),
        format('Prefiere combinación: (~w, ~w)~n', [TipoPref, VegPref])
    ; true).


% EVITACIONES


inducir_evitaciones(U) :-
    findall(C, rechazado(U, menu(_,_,C,_,_,_)), LCarneEv),
    (LCarneEv \= [] ->
        contar_frecuencias(LCarneEv, FCarneEv),
        max_member(_-CarneEv, FCarneEv),
        retractall(regla(U, evita(_))),
        assertz(regla(U, evita(CarneEv))),
        format('Evita carne: ~w~n', [CarneEv])
    ; true),

    findall((E,V), (
        rechazado(U, menu(E,_,_,V,_,_))
    ), LEvComb),
    (LEvComb \= [] ->
        contar_frecuencias(LEvComb, FEvComb),
        max_member(_-(E,V), FEvComb),
        retractall(regla(U, evita_combinacion(_,_))),
        assertz(regla(U, evita_combinacion(E,V))),
        format('Evita combinación: (~w, ~w)~n', [E,V])
    ; true).


% CONDICIONALES


inducir_condicionales(U) :-
    findall((Tipo,Postre), (
        aceptado(U, menu(_,_,C,_,Postre,_)),
        carne(C,_,Tipo)
    ), LCond),
    (LCond \= [] ->
        contar_frecuencias(LCond, FCond),
        max_member(_-(TipoPref, PostrePref), FCond),
        retractall(regla(U, preferencia_condicional(postre,_,_))),
        assertz(regla(U, preferencia_condicional(postre, TipoPref, PostrePref))),
        format('Condición aprendida: si carne ~w → postre ~w~n', [TipoPref, PostrePref])
    ; true).


%  UTILIDADES

contar_frecuencias(Lista, Frecs) :-
    sort(Lista, Unicos),
    findall(C-Item, (
        member(Item, Unicos),
        include(=(Item), Lista, Todos),
        length(Todos, C)
    ), Frecs).

guardar_datos :-
    tell('aprendizaje_datos.pl'),
    listing(aceptado/2),
    listing(rechazado/2),
    listing(regla/2),
    told,
    writeln('Datos de aprendizaje guardados en "aprendizaje_datos.pl".').

