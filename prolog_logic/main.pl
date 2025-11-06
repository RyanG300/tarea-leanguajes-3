:- dynamic carbohidrato/3.
:- dynamic carne/4.
:- dynamic vegetal/3.
:- dynamic postre/3.
:- dynamic entrada/4. 

:- consult('combinaciones.pl').
:- consult('filtros.pl').
:- consult('aprendizaje.pl').
:- consult('recomendador.pl').

:- (exists_file('aprendizaje_datos.pl') -> consult('aprendizaje_datos.pl'); true).
