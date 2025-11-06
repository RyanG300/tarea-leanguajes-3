:- consult('base_alimentos.pl').
:- consult('combinaciones.pl').
:- consult('filtros.pl').
:- consult('aprendizaje.pl').
:- consult('recomendador.pl').

:- (exists_file('aprendizaje_datos.pl') -> consult('aprendizaje_datos.pl'); true).
