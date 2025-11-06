carbohidrato('arroz con verduras', 220, 'imagenes/Carbohidratos/arroz.png').
carbohidrato('pasta integral con tomate', 250, 'imagenes/Carbohidratos/pasta.png').
carbohidrato('puré de papas con mantequilla', 200, 'imagenes/Carbohidratos/pure.png').
carbohidrato('quinoa con frutos secos', 210, 'imagenes/Carbohidratos/quinoa.png').
carbohidrato('cuscús marroquí', 230, 'imagenes/Carbohidratos/cuscus.png').
carbohidrato('pan integral tostado', 180, 'imagenes/Carbohidratos/pan.png').
carbohidrato('tortilla de maíz', 150, 'imagenes/Carbohidratos/tortilla.png').
carbohidrato('papas al ajillo', 300, 'imagenes/Carbohidratos/papas.png').

carne('pollo en salsa de champiñones', 350, blanca, 'imagenes/Proteínas/pollo.png').
carne('res al horno con hierbas', 400, roja, 'imagenes/Proteínas/res.png').
carne('salmón a la plancha con limón', 300, blanca, 'imagenes/Proteínas/salmon.png').
carne('tofu al curry', 250, vegetariana, 'imagenes/Proteínas/tofu.png').
carne('pavo al ajillo', 280, blanca, 'imagenes/Proteínas/pavo.png').
carne('cerdo estofado', 380, roja, 'imagenes/Proteínas/cerdo.png').
carne('tempeh a la parrilla', 220, vegetariana, 'imagenes/Proteínas/tempeh.png').
carne('gambas al ajillo', 200, blanca, 'imagenes/Proteínas/gambas.png').

vegetal('ensalada César', 150, 'imagenes/Vegetales/cesar.png').
vegetal('brócoli al vapor', 80, 'imagenes/Vegetales/brocoli.png').
vegetal('vegetales salteados', 120, 'imagenes/Vegetales/vegetalesSalteados.png').
vegetal('col rizada con limón', 70, 'imagenes/Vegetales/col.png').
vegetal('espinacas a la crema', 100, 'imagenes/Vegetales/espinacas.png').
vegetal('berenjenas a la parmesana', 130, 'imagenes/Vegetales/berenjenas.png').
vegetal('calabacín al horno', 90, 'imagenes/Vegetales/calabacin.png').
vegetal('pimientos asados', 60, 'imagenes/Vegetales/pimientos.png').

% Postres
postre('tarta de chocolate', 450, 'imagenes/Postres/tarta.png').
postre('flan de vainilla', 250, 'imagenes/Postres/flan.png').
postre('helado de fresa', 200, 'imagenes/Postres/helado.png').
postre('mousse de chocolate negro', 300, 'imagenes/Postres/mousse.png').
postre('fruta fresca con miel', 150, 'imagenes/Postres/frutaMiel.png').
postre('pudín de pan', 350, 'imagenes/Postres/pudín.png').
postre('brownie de nueces', 400, 'imagenes/Postres/brownie.png').
postre('gelatina de frutas', 100, 'imagenes/Postres/gelatina.png').

% Entradas
entrada('bruschetta de tomate y albahaca', 120, vegetariana, 'imagenes/Entradas/buschetta.png').
entrada('sopa de verduras', 100, vegetariana, 'imagenes/Entradas/sopaVerduras.png').
entrada('ensalada caprese', 150, vegetariana, 'imagenes/Entradas/caprese.png').
entrada('rollitos de jamón y queso', 180, no_vegetariana, 'imagenes/Entradas/rollitos.png').
entrada('gazpacho', 90, vegetariana, 'imagenes/Entradas/gazpacho.png').
entrada('tartar de salmón', 200, no_vegetariana, 'imagenes/Entradas/tartar.png').
entrada('humus con pan de pita', 130, vegetariana, 'imagenes/Entradas/humus.png').
entrada('croquetas de pollo', 160, no_vegetariana, 'imagenes/Entradas/croquetas.png').

% :- dynamic carbohidrato/3.
% :- dynamic carne/4.
% :- dynamic vegetal/3.
% :- dynamic postre/3.
% :- dynamic entrada/4. 

