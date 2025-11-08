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
aceptado(estebancito, menu('rollitos de jamon y queso', ' tortilla de maiz', ' pollo en salsa de champinones', ' ensalada Cesar', ' fruta fresca con miel', 980)).
aceptado(jorgino, menu('sopa de verduras', ' papas al ajillo', ' pollo en salsa de champinones', ' pimientos asados', ' gelatina de frutas', 910)).
aceptado(jorgino, menu('sopa de verduras', ' pan integral tostado', ' pollo en salsa de champinones', ' pimientos asados', ' helado de fresa', 890)).
aceptado(jorgino, menu('sopa de verduras', ' tortilla de maiz', ' pollo en salsa de champinones', ' ensalada Cesar', ' pudin de pan', 1100)).
aceptado(ryan, menu(gazpacho, ' cuscus marroqui', ' pollo en salsa de champinones', ' pimientos asados', ' mousse de chocolate negro', 1030)).
aceptado(ryan, menu('humus con pan de pita', ' pan integral tostado', ' pollo en salsa de champinones', ' pimientos asados', ' mousse de chocolate negro', 1020)).
aceptado(ryan, menu('humus con pan de pita', ' pan integral tostado', ' pollo en salsa de champinones', ' pimientos asados', ' mousse de chocolate negro', 1020)).
aceptado(ryan, menu('humus con pan de pita', ' tortilla de maiz', ' pollo en salsa de champinones', ' pimientos asados', ' mousse de chocolate negro', 990)).
aceptado(ryan, menu('humus con pan de pita', ' pan integral tostado', ' pollo en salsa de champinones', ' pimientos asados', ' mousse de chocolate negro', 1020)).
aceptado(ryanSegundo, menu('tartar de salmon', ' pure de papas con mantequilla', ' pollo en salsa de champinones', ' espinacas a la crema', ' brownie de nueces', 1250)).
aceptado(ryanSegundo, menu('ensalada caprese', ' pan integral tostado', ' pollo en salsa de champinones', ' ensalada Cesar', ' flan de vainilla', 1080)).
aceptado(ryanSegundo, menu('tartar de salmon', ' pure de papas con mantequilla', ' pollo en salsa de champinones', ' ensalada Cesar', ' tarta de chocolate', 1350)).
aceptado('Jose', menu('sopa de verduras', ' tortilla de maiz', ' pollo en salsa de champinones', ' pimientos asados', ' pudin de pan', 1010)).
aceptado('Eduardo', menu('sopa de verduras', ' tortilla de maiz', ' pollo en salsa de champinones', ' pimientos asados', ' pudin de pan', 1010)).
aceptado('Eduardo', menu('sopa de verduras', ' arroz con verduras', ' salmon a la plancha con limon', ' vegetales salteados', ' gelatina de frutas', 840)).
aceptado(_, menu('bruschetta de tomate y albahaca', 'pasta integral con tomate', 'pollo en salsa de champinones', 'pimientos asados', none, 780)).

:- dynamic rechazado/2.


:- dynamic regla/2.

regla(daniel, preferencia(calorias, 742.0)).
regla(pablo, preferencia(incluye, 'pollo en salsa de champinones')).
regla(juancitoe, preferencia(incluye, 'pollo en salsa de champinones')).
regla(estebancito, preferencia(incluye, 'ensalada Cesar')).
regla(jorgino, preferencia(incluye, 'pollo en salsa de champinones')).
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
regla(jorgino, preferencia(incluye, 'sopa de verduras')).
regla(jorgino, preferencia(incluye, 'pollo en salsa de champinones')).
regla(jorgino, preferencia(incluye, 'ensalada Cesar')).
regla(ryan, preferencia(incluye, 'pollo en salsa de champinones')).
regla(ryan, preferencia(incluye, 'pollo en salsa de champinones')).
regla(ryan, preferencia(incluye, 'pimientos asados')).
regla(ryan, preferencia(incluye, 'mousse de chocolate negro')).
regla(ryan, preferencia(incluye, 'pollo en salsa de champinones')).
regla(ryan, preferencia(incluye, 'pimientos asados')).
regla(ryan, preferencia(incluye, 'mousse de chocolate negro')).
regla(ryan, preferencia(incluye, 'pollo en salsa de champinones')).
regla(ryan, preferencia(incluye, 'pimientos asados')).
regla(ryan, preferencia(incluye, 'mousse de chocolate negro')).
regla(ryan, preferencia(incluye, 'pollo en salsa de champinones')).
regla(ryan, preferencia(incluye, 'pimientos asados')).
regla(ryan, preferencia(incluye, 'mousse de chocolate negro')).
regla(ryanSegundo, preferencia(incluye, 'pollo en salsa de champinones')).
regla(ryanSegundo, preferencia(incluye, 'pollo en salsa de champinones')).
regla(ryanSegundo, preferencia(incluye, 'ensalada Cesar')).
regla(ryanSegundo, preferencia(incluye, 'pollo en salsa de champinones')).
regla(ryanSegundo, preferencia(incluye, 'ensalada Cesar')).
regla(ryanSegundo, preferencia(incluye, 'tarta de chocolate')).
regla('Jose', preferencia(incluye, 'pollo en salsa de champinones')).
regla('Eduardo', preferencia(incluye, 'pollo en salsa de champinones')).
regla('Eduardo', preferencia(incluye, 'arroz con verduras')).
regla(_, evita('brocoli al vapor')).
regla(_, evita('tarta de chocolate')).
regla(_, evita('flan de vainilla')).
regla(_, evita('helado de fresa')).
regla(_, evita('mousse de chocolate negro')).
regla(_, evita('fruta fresca con miel')).
regla(_, evita('pudin de pan')).
regla(_, evita('brownie de nueces')).
regla(_, evita('gelatina de frutas')).
regla(_, preferencia(incluye, 'bruschetta de tomate y albahaca')).
regla(_, preferencia(carne, blanca)).
regla(_, preferencia(postre, none)).
regla(_, preferencia(calorias_promedio, 925)).
regla(_, preferencia(entrada, 'sopa de verduras')).
regla(_, preferencia(vegetal, ' pimientos asados')).
regla(_, preferencia(combinacion, (blanca, ' pimientos asados'))).
regla(_, preferencia_condicional(postre, blanca, none)).

