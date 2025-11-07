:- dynamic aceptado/2.

aceptado(pablo, menu(gazpacho, 'arroz con verduras', 'tempeh a la parrilla', 'espinacas a la crema', 'fruta fresca con miel', 780)).

:- dynamic rechazado/2.


:- dynamic regla/2.

regla(pablo, evita('pollo en salsa de champiñones')).
regla(pablo, preferencia(incluye, 'arroz con verduras')).

