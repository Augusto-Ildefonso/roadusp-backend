"""
Classe que representa uma disciplina da USP

Autores:
- Augusto Fernandes Ildefonso (15441810)
"""

from typing import List

class Disciplina():

    # Criando métodos

    '''
    Construtor: cria uma classe Disciplina

    @param codigo Código da disciplina
    @param nome Nome da disciplina
    @param cred_aula Crédito aula
    @param cred_trab Crédito trabalho
    @param carg_hor Carga horária
    @param carg_hor_est Carga horária de estágio
    @param carg_hor_prat  Carga horária de práticas como componentes curriculares
    @param ativ_teo Atividades teórico-práticas de aprofundamento
    '''
    def __init__(self, codigo : str, nome : str, cred_aula : int, cred_trab : int, carg_hor : int, carg_hor_est : int, carg_hor_prat : int, ativ_teo : int, requisitos : List):
        self._codigo : str = codigo
        self._nome : str = nome
        self._cred_aula : int = cred_aula
        self._cred_trab : int = cred_trab
        self._ch : int = carg_hor
        self._ce : int = carg_hor_est
        self._cp : int = carg_hor_prat
        self._atpa : int = ativ_teo
        self._requisitos : List = requisitos

    def to_dict(self):
        return {
            "codigo": self._codigo,
            "nome": self._nome,
            "credito_aula": self._cred_aula,
            "credito_trabalho": self._cred_trab,
            "carga_horaria": self._ch,
            "carga_horaria_estagio": self._ce,
            "carga_horaria_pratica": self._cp,
            "atividades_teo": self._atpa,
            "requisitos": self._requisitos
        }

    # Criando descritores para acessar os atributos da classe

    '''
    Descritor do atributo código
    '''
    @property
    def codigo(self):
        return self._codigo
    
    '''
    Descritor do atributo nome
    '''
    @property
    def nome(self):
        return self._nome
    
    '''
    Descritor do crédito aula
    '''
    @property
    def cred_aula(self):
        return self._cred_aula
    
    '''
    Descritor do crédito trabalho
    '''
    @property
    def cred_trab(self):
        return self._cred_trab
    
    '''
    Descritor da carga horária
    '''
    @property
    def carg_hor(self):
        return self._carg_hor
    
    '''
    Descritor da carga horária de estágio
    '''
    @property
    def carg_hor_est(self):
        return self._carg_hor_est
    
    '''
    Descritor da carga horária de práticas como componentes curriculares
    '''
    @property
    def carg_hor_prat(self):
        return self._carg_hor_prat
    
    '''
    Descritor atividades teórico-práticas de aprofundamento
    '''
    @property
    def ativ_teo(self):
        return self._ativ_teo
    
    '''
    Descritor dos requisistos
    '''
    def requisitos(self):
        return self._requisitos