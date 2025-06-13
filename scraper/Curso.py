"""
Classe que representa um curso da USP

Autores:
- Augusto Fernandes Ildefonso (15441810)
"""

# Importando bibliotecas
from typing import List

class Curso():

    # Criando métodos

    '''
    Construtor: cria uma classe Curso

    @param nome Nome do curso
    @param unidade Nome da unidade do curso
    @param duracao_ideal Duração ideal do curso
    @param duracao_min Duração mínima do curso
    @param duracao_max Duração máxima do curso
    @param disciplinas_obrigatorias Lista das disciplinas obrigatórias
    @param disciplinas_livres Lista das disciplinas livres
    @param disciplinas_eletivas Lista das disciplinas eletivas
    '''
    def __init__(self, nome : str, unidade : str, duracao_ideal : int, duracao_min : int, duracao_max : int, disciplinas_obrigatorias : List, disciplinas_livres : List, disciplinas_eletivas : List):
        self._nome : str = nome
        self._unidade : str = unidade
        self._duracao_ideal : int = duracao_ideal
        self._duracao_minima : int = duracao_min
        self._duracao_maxima : int = duracao_max
        self._disciplinas_obrigatorias : List = disciplinas_obrigatorias
        self._disciplinas_livres : List = disciplinas_livres
        self._disciplinas_eletivas : List = disciplinas_eletivas

    def __str__(self):
        return (
            f"- nome: {self.nome}\n"
            f"- unidade: {self.unidade}\n"
            f"- duração ideal: {self.duracao_ideal} semestres\n"
            f"- duração mínima: {self.duracao_minima} semestres\n"
            f"- duração máxima: {self.duracao_maxima} semestres\n"
            f"- disciplinas obrigatórias: {[disciplina.nome for disciplina in self.disciplinas_obrigatorias]}\n"
            f"- disciplinas eletivas: {[disciplina.nome for disciplina in self.disciplinas_eletivas]}\n"
            f"- disciplinas livres: {[disciplina.nome for disciplina in self.disciplinas_livres]}"
        )
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "unidade": self.unidade,
            "duracao_ideal": self.duracao_ideal,
            "duracao_min": self.duracao_minima,
            "duracao_max": self.duracao_maxima,
            "disciplinas_obrigatorias": [d.to_dict() for d in self.disciplinas_obrigatorias],
            "disciplinas_optativas_eletivas": [d.to_dict() for d in self.disciplinas_eletivas],
            "disciplinas_optativas_livres": [d.to_dict() for d in self.disciplinas_livres],
        }
        
    # Criando descritores para acessar os atributos da classe

    '''
    Descritor do atributo nome
    '''
    @property
    def nome(self):
        return self._nome
    
    '''
    Descritor do atributo unidade
    '''
    @property
    def unidade(self):
        return self._unidade

    '''
    Descritor do atributo duração ideal
    '''
    @property
    def duracao_ideal(self):
        return self._duracao_ideal
    
    '''
    Descritor do atributo duração mínima
    '''
    @property
    def duracao_minima(self):
        return self._duracao_minima
    
    '''
    Descritor do atributo duração máxima
    '''
    @property
    def duracao_maxima(self):
        return self._duracao_maxima
    
    '''
    Descritor do atributo disciplinas obrigatórias
    '''
    @property
    def disciplinas_obrigatorias(self):
        return self._disciplinas_obrigatorias

    '''
    Descritor do atributo disciplinas livres
    '''
    @property
    def disciplinas_livres(self):
        return self._disciplinas_livres

    '''
    Descritor do atributo disciplinas eletivas
    '''
    @property
    def disciplinas_eletivas(self):
        return self._disciplinas_eletivas