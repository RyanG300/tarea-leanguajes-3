:- dynamic aceptado/2.

aceptado(daniel, menu('sopa de verduras', 'arroz con verduras', 'pollo en salsa de champi帽ones', 'br贸coli al vapor', 'flan de vainilla', 820)).
aceptado(daniel, menu('ensalada caprese', 'pasta integral con tomate', 'salm贸n a la plancha con lim贸n', 'col rizada con lim贸n', 'gelatina de frutas', 780)).
aceptado(pedro, menu('humus con pan de pita', 'pur茅 de papas con mantequilla', 'gambas al ajillo', 'col rizada con lim贸n', 'gelatina de frutas', 700)).
aceptado(daniel, menu('sopa de verduras', 'pan integral tostado', 'res al horno con hierbas', 'br贸coli al vapor', 'gelatina de frutas', 860)).
aceptado(daniel, menu('sopa de verduras', 'tortilla de ma肻u00ADz', 'tofu al curry', 'ensalada C茅sar', none, 550)).
aceptado(daniel, menu('tartar de salm贸n', 'tortilla de ma肻u00ADz', 'tofu al curry', 'pimientos asados', none, 660)).
aceptado(daniel, menu('tartar de salm贸n', 'tortilla de ma肻u00ADz', 'tofu al curry', 'ensalada C茅sar', none, 750)).
aceptado(daniel, menu('sopa de verduras', 'pur茅 de papas con mantequilla', 'tofu al curry', 'ensalada C茅sar', none, 700)).
aceptado(luis, menu('sopa de verduras', 'arroz con verduras', 'tempeh a la parrilla', 'pimientos asados', none, 600)).
aceptado(daniel, menu('sopa de verduras', 'tortilla de maiz', 'pollo en salsa de champinones', 'vegetales salteados', 'gelatina de frutas', 820)).

:- dynamic rechazado/2.


:- dynamic regla/2.

regla(daniel, evita('tarta de chocolate')).
regla(daniel, preferencia(incluye, 'pollo en salsa de champinones')).
regla(daniel, preferencia(carne, vegetariana)).
regla(daniel, preferencia(postre, none)).
regla(daniel, preferencia(calorias_promedio, 742.5)).
regla(daniel, preferencia(entrada, 'sopa de verduras')).
regla(daniel, preferencia(vegetal, 'ensalada C茅sar')).
regla(daniel, preferencia(combinacion, (vegetariana, 'ensalada C茅sar'))).
regla(daniel, preferencia_condicional(postre, vegetariana, none)).

