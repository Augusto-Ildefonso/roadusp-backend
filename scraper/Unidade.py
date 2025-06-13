"""
Classe que representa uma Unidade da USP

Autores:
- Augusto Fernandes Ildefonso (15441810)
"""
class Unidade():

    # Criando métodos

    '''
    Construtor: cria uma classe Unidade com um atributo nome e um atributo cursos

    @param nome Nome da unidade
    '''
    def __init__(self, nome):
        self._nome = nome
        self._cursos = []

    '''
    Esse método adiciona um curso na lista de cursos da unidade
    
    @param curso Objeto curso que será adicionado na lista
    '''
    def adicionar_cursos(self, curso):
        self.cursos.append(curso)

    def to_dict(self):
        return{
            "nome": self.nome,
            "cursos": [curso.to_dict() for curso in self.cursos]
        }
    
    #Criando descritores para acessar os atributos da classe   
 
    '''
    Descritor do atributo nome
    '''
    @property
    def nome(self):
        return self._nome

    '''
    Descritor do atributo curso
    '''
    @property
    def cursos(self):
        return self._cursos
    