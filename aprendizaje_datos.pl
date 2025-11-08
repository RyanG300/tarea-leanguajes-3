:- dynamic aceptado/2.

aceptado(pedro, menu('humus con pan de pita', ' pure de papas con mantequilla', ' gambas al ajillo', ' col rizada con limon', ' gelatina de frutas', 700)).
aceptado(luis, menu('sopa de verduras', ' arroz con verduras', ' tempeh a la parrilla', ' pimientos asados', none, 600)).
aceptado(daniel, menu('sopa de verduras', ' arroz con verduras', ' pollo en salsa de champinones', ' brocoli al vapor', ' flan de vainilla', 1000)).
aceptado(daniel, menu('ensalada caprese', ' pasta integral con tomate', ' salmon a la plancha con limon', ' col rizada con limon', ' gelatina de frutas', 870)).
aceptado(daniel, menu('sopa de verduras', ' pan integral tostado', ' res al horno con hierbas', ' brocoli al vapor', ' gelatina de frutas', 860)).
aceptado(daniel, menu('sopa de verduras', ' tortilla de maiz', ' tofu al curry', ' ensalada Cesar', none, 650)).
aceptado(daniel, menu('tartar de salmon', ' tortilla de maiz', ' tofu al curry', ' pimientos asados', none, 660)).
aceptado(daniel, menu('tartar de salmon', ' tortilla de maiz', ' tofu al curry', ' ensalada Cesar', none, 750)).
aceptado(daniel, menu('sopa de verduras', ' pure de papas con mantequilla', ' tofu al curry', ' ensalada Cesar', none, 700)).
aceptado(pablo, menu(gazpacho, ' tortilla de maiz', ' pollo en salsa de champinones', ' berenjenas a la parmesana', ' gelatina de frutas', 820)).
aceptado(pedito, menu('tartar de salmon', ' quinoa con frutos secos', ' salmon a la plancha con limon', ' espinacas a la crema', ' flan de vainilla', 1060)).
aceptado(juancitoe, menu(gazpacho, ' papas al ajillo', ' pollo en salsa de champinones', ' pimientos asados', ' fruta fresca con miel', 950)).
aceptado(jorgino, menu('sopa de verduras', ' papas al ajillo', ' pollo en salsa de champinones', ' pimientos asados', ' gelatina de frutas', 910)).
aceptado(estebancito, menu('rollitos de jamon y queso', ' tortilla de maiz', ' pollo en salsa de champinones', ' ensalada Cesar', ' fruta fresca con miel', 980)).
aceptado(jorgino, menu('sopa de verduras', 'pan integral tostado', 'pollo en salsa de champinones', 'pimientos asados', 'helado de fresa', 890)).
aceptado(jorgino, menu('sopa de verduras', 'tortilla de maiz', 'pollo en salsa de champinones', 'ensalada Cesar', 'pudin de pan', 1100)).

:- dynamic rechazado/2.


:- dynamic regla/2.

regla(daniel, preferencia(carne, vegetariana)).
regla(daniel, preferencia(postre, none)).
regla(daniel, preferencia(calorias_promedio, 731.4285714285714)).
regla(daniel, preferencia(entrada, 'sopa de verduras')).
regla(daniel, preferencia(vegetal, 'ensalada César')).
regla(daniel, preferencia(combinacion, ('', '(vegetariana, ensalada César)'))).
regla(daniel, preferencia_condicional(postre, vegetariana, '_')).
regla(daniel, preferencia(carne, vegetariana)).
regla(daniel, preferencia(postre, none)).
regla(daniel, preferencia(calorias, 742.0)).
regla(daniel, preferencia_condicional(postre, vegetariana, si)).
regla(pablo, preferencia(incluye, 'pollo en salsa de champinones')).
regla(juancitoe, preferencia(incluye, 'pollo en salsa de champinones')).
regla(jorgino, preferencia(incluye, 'pollo en salsa de champinones')).
regla(estebancito, preferencia(incluye, 'ensalada Cesar')).
regla(jorgino, preferencia(incluye, 'sopa de verduras')).
regla(jorgino, preferencia(incluye, 'pollo en salsa de champinones')).
regla(jorgino, preferencia(incluye, 'pimientos asados')).
regla(jorgino, preferencia(incluye, 'sopa de verduras')).
regla(jorgino, preferencia(incluye, 'pollo en salsa de champinones')).
regla(jorgino, preferencia(incluye, 'pimientos asados')).
regla(jorgino, preferencia(incluye, 'ensalada Cesar')).
regla(jorgino, preferencia(incluye, 'sopa de verduras')).
regla(jorgino, preferencia(incluye, 'pollo en salsa de champinones')).
regla(jorgino, preferencia(incluye, 'pimientos asados')).
regla(jorgino, preferencia(incluye, 'ensalada Cesar')).
regla(jorgino, evita('pimientos asados')).
regla(jorgino, preferencia(incluye, 'sopa de verduras')).
regla(jorgino, preferencia(incluye, 'pollo en salsa de champinones')).
regla(jorgino, preferencia(incluye, 'ensalada Cesar')).
regla(jorgino, preferencia(carne, blanca)).
regla(jorgino, preferencia(postre, 'pudin de pan')).
regla(jorgino, preferencia(calorias_promedio, 966.6666666666666)).
regla(jorgino, preferencia(entrada, 'sopa de verduras')).
regla(jorgino, preferencia(vegetal, 'pimientos asados')).
regla(jorgino, preferencia(combinacion, (blanca, 'pimientos asados'))).
regla(jorgino, preferencia_condicional(postre, blanca, 'pudin de pan')).

