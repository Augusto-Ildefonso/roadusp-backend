"""
Webscraper do JúpiterWeb

Autor:
- Augusto Fernandes Ildefonso
"""
# Importando bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
import json
import time

from Unidade import Unidade
from Curso import Curso
from Disciplina import Disciplina

# Definindo variáveis globais
URL : str = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
TIMEOUT : int = 10  # Timeout padrão em segundos

# Configurando para que o Chrome não imprima logs
options = Options()
options.add_argument("--log-level=3")  # Minimiza o log
options.add_argument("--disable-logging")
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Remove logs extra

# Definindo classe do scraper
class ScraperJupiterWeb():

    '''
    Construtor: ele vai inicializar o selenium para podermos manipular a página
    '''
    def __init__(self):
        # Acessando a página com o selenium
        self.jupiter_selenium = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.jupiter_selenium, TIMEOUT)
        self.jupiter_selenium.get(URL)
        
        # Aguardando o carregamento do select de unidades
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
        except TimeoutException:
            print("Timeout: Página não carregou completamente")
    
    '''
    Função auxiliar para aguardar que overlays de carregamento desapareçam
    '''
    def _aguardar_sem_overlay(self):
        try:
            # Aguarda que overlays blockUI desapareçam
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "blockUI")))
        except TimeoutException:
            # Se não houver overlay ou timeout, continua
            pass
        
        try:
            # Aguarda que overlays blockOverlay desapareçam
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "blockOverlay")))
        except TimeoutException:
            # Se não houver overlay ou timeout, continua
            pass

    '''
    Essa função retorna uma lista das unidades disponíveis no júpiterweb

    @return retorna uma lista das unidades
    '''
    def pegar_unidades(self) -> List:
        # Criando lista de unidades
        lista_unidades : List = []

        try:
            # Aguardando o select de unidades estar presente e com opções
            select = self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
            
            # Aguardando que as opções sejam carregadas (mais de 1 opção, considerando o placeholder)
            self.wait.until(lambda driver: len(select.find_elements(By.TAG_NAME, "option")) > 1)
            
            # Achando todas as unidades
            unidades = select.find_elements(By.TAG_NAME, "option")
            
            for unidade in unidades:
                if unidade.get_attribute("value"):
                    lista_unidades.append(unidade.get_attribute("text"))
                    
        except TimeoutException:
            print("Timeout: Não foi possível carregar as unidades.")

        return lista_unidades
    
    '''
    Essa função retorna uma lista dos cursos disponíveis para uma determinada unidade no júpiterweb

    @param unidade_target A unidade da qual os cursos serão buscados
    @return retorna uma lista dos cursos
    '''
    def pegar_cursos(self, unidade_target : str) -> List:
        # Criando lista de cursos
        lista_cursos : List = []

        try:
            # Aguardando o select de unidades estar presente
            select_unidade = self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
            
            # Achando todas as unidades
            unidades = select_unidade.find_elements(By.TAG_NAME, "option")
            
            # Iterando sobre as unidades
            for unidade in unidades:
                # Verificando se a unidade é igual a unidade selecionada
                if unidade.get_attribute("text") == unidade_target:
                    # Marcando no select a unidade desejada
                    unidade.click()
                    break
            
            # Aguardando o select de cursos estar presente e ser clicável
            select_curso = self.wait.until(EC.element_to_be_clickable((By.ID, "comboCurso")))
            
            # Aguardando que os cursos sejam carregados (mais de 1 opção)
            self.wait.until(lambda driver: len(select_curso.find_elements(By.TAG_NAME, "option")) > 1)

            # Achando todos os cursos
            cursos = select_curso.find_elements(By.TAG_NAME, "option")

            # Iterando sobre os cursos
            for curso in cursos:
                if curso.get_attribute("value"):
                    lista_cursos.append(curso.get_attribute("text"))
                    
        except TimeoutException:
            print("Timeout: Não foi possível carregar os cursos.")
        
        return lista_cursos
    
    '''
    Essa função retorna uma tupla das informações de um determinado curso de uma determinada unidade no júpiterweb

    @param unidade_target A unidade da qual as disciplinas serão buscadas
    @param curso_target O curso do qual as disciplinas serão buscadas
    @return retorna uma lista das disciplinas
    '''
    def pegar_informacoes_curso(self, unidade_target : str, curso_target : str) -> Tuple:
        try:
            # Aguardando o select de unidades estar presente
            select_unidade = self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
            
            # Achando todas as unidades
            unidades = select_unidade.find_elements(By.TAG_NAME, "option")
            
            # Iterando sobre as unidades
            for unidade in unidades:
                # Verificando se a unidade é igual a unidade selecionada
                if unidade.get_attribute("text") == unidade_target:
                    # Marcando no select a unidade desejada
                    unidade.click()
                    break
            
            # Aguardando o select de cursos estar presente e ser clicável
            select_curso = self.wait.until(EC.element_to_be_clickable((By.ID, "comboCurso")))
            
            # Aguardando que os cursos sejam carregados
            self.wait.until(lambda driver: len(select_curso.find_elements(By.TAG_NAME, "option")) > 1)

            # Achando todos os cursos
            cursos = select_curso.find_elements(By.TAG_NAME, "option")

            # Iterando sobre os cursos
            for curso in cursos:
                if curso.get_attribute("text") == curso_target:
                    curso.click()
                    break
            
            # Aguardando o botão de buscar estar clicável e clicando nele
            botao_buscar = self.wait.until(EC.element_to_be_clickable((By.ID, "enviar")))
            botao_buscar.click()
            
            # Aguardando que qualquer overlay de carregamento desapareça
            self._aguardar_sem_overlay()
            
            # Verificando se a aba de grade curricular existe antes de tentar clicar
            abas = self.jupiter_selenium.find_elements(By.ID, "step4-tab")
            if not abas:
                # Aba não encontrada, provavelmente curso sem grade curricular
                return None

            try:
                pagina_grade_curricular = self.wait.until(EC.element_to_be_clickable((By.ID, "step4-tab")))
                pagina_grade_curricular.click()
            except Exception:
                # Não conseguiu clicar (ex: sobreposição), então retorna silenciosamente
                return None

            # Aguardando que qualquer overlay desapareça após clicar na aba
            self._aguardar_sem_overlay()

            # Aguardando os elementos de duração carregarem
            duracao_ideal = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "duridlhab")))[1]
            duracao_min = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "durminhab")))
            duracao_max = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "durmaxhab")))

            infos_curso : Tuple = (duracao_ideal.text, duracao_min.text, duracao_max.text)

            return infos_curso
            
        except TimeoutException:
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None
    
    '''
    Essa auxiliar é interna à classe e serve para criar uma lista com os nomes das disciplinas

    @param lista_linhas_disciplinas É uma lista dos objetos do selenium q representam as disciplinas
    @return retorna uma lista dos nomes das disciplinas
    '''
    def _criando_lista_disciplinas(self, lista_linhas_disciplina : List) -> List:
        lista_disciplinas : List = []
        
        for linha in lista_linhas_disciplina:
            disciplina : List = []
            
            # Achando dados das disciplinas
            dados = linha.find_all("td")
            
            # Percorrendo os dados e adicionando na lista
            for dado in dados:
                link = dado.find("a")
                if link:
                    disciplina.append(link.get_text(strip=True))
                else:
                    disciplina.append(dado.get_text(strip=True))
            
            lista_disciplinas.append(disciplina)
        
        return lista_disciplinas

    '''
    Essa função retorna um dicionário das disciplinas disponíveis para um determinado curso de uma determinada unidade no júpiterweb, dividindo elas entre obrigatórias, livres e eletivas

    @param unidade_target A unidade da qual as disciplinas serão buscadas
    @param curso_target O curso do qual as disciplinas serão buscadas
    @return retorna um dicionário das disciplinas
    '''
    def pegar_disciplinas(self) -> Dict:
        try:
            # Aguardando a grade curricular estar presente
            self.wait.until(EC.presence_of_element_located((By.ID, "gradeCurricular")))
            
            # Criando lista de disciplinas do curso
            lista_disciplinas_obrigatorias : List = []
            lista_disciplinas_livres : List = []
            lista_disciplinas_eletivas : List = []

            # Pegando o HTML da página
            html = self.jupiter_selenium.page_source

            soup = BeautifulSoup(html, "html.parser")

            # Achando grade curricular
            grade_curricular = soup.find(id="gradeCurricular")
            linhas = grade_curricular.find_all("tr")

            # Criando lista das linhas que são de disciplinas
            tipo_disciplina : str = ""
            for linha in linhas:
                # Verificando se a linha é o tipo de disciplina ou a disciplina em si
                style = linha.get("style", "")
                # Verificando se a linha é o tipo de disciplina
                if "rgb(16, 148, 171)" in style and "white" in style:
                    dado_tipo_disciplina = linha.find_all("td")
                    if dado_tipo_disciplina:
                        tipo_disciplina = dado_tipo_disciplina[0].get_text(strip=True)

                # Verificando se a linha representa uma disciplina
                elif style == "height: 20px;":
                    if tipo_disciplina == "Disciplinas Obrigatórias":
                        lista_disciplinas_obrigatorias.append(linha)
                    elif tipo_disciplina == "Disciplinas Optativas Livres":
                        lista_disciplinas_livres.append(linha)
                    elif tipo_disciplina == "Disciplinas Optativas Eletivas":
                        lista_disciplinas_eletivas.append(linha)

            # Criando disciplina e adicionando ela na lista de disciplinas
            disciplinas : Dict = {}
            disciplinas["Disciplinas Obrigatórias"] = self._criando_lista_disciplinas(lista_disciplinas_obrigatorias)
            disciplinas["Disciplinas Optativas Livres"] = self._criando_lista_disciplinas(lista_disciplinas_livres)
            disciplinas["Disciplinas Optativas Eletivas"] = self._criando_lista_disciplinas(lista_disciplinas_eletivas)

            return disciplinas
            
        except TimeoutException:
            print("Timeout: Não foi possível carregar as disciplinas")
            return {}
    
    '''
    Essa função retorna um dicionário das disciplinas disponíveis para um determinado curso de uma determinada unidade no júpiterweb, dividindo elas entre obrigatórias, livres e eletivas

    @param unidade_target A unidade da qual as disciplinas serão buscadas
    @param curso_target O curso do qual as disciplinas serão buscadas
    @return retorna uma lista das disciplinas
    '''
    def voltar_inicio(self):
        try:
            # Aguardando que qualquer overlay de carregamento desapareça
            self._aguardar_sem_overlay()
            
            # Aguardando o botão estar clicável e clicando nele
            botao_voltar = self.wait.until(EC.element_to_be_clickable((By.ID, "step1-tab")))
            botao_voltar.click()
            
            # Aguardando que a página inicial seja carregada novamente
            self.wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
            
        except TimeoutException:
            print("Timeout: Não foi possível voltar ao início")

    '''
    Essa função navega para uma página especificada

    @param pagina Link da página para qual será navegada
    '''
    def ir_para(self, pagina : str):
        self.jupiter_selenium.get(pagina)
        
        # Aguardando a página carregar completamente
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except TimeoutException:
            print("Timeout: Não foi possível carregar a página")

    '''
    Essa função fecha a janela do scraper
    '''
    def fechar_scraper(self):
        self.jupiter_selenium.quit()  # Usando quit() ao invés de close() para fechar todas as janelas
    
    '''
    Essa função retorna uma lista dos requisitos de uma disciplina específica
    
    @param codigo_disciplina O código da disciplina para buscar requisitos (ex: "SCC0221")
    @return retorna uma lista dos códigos das disciplinas que são requisitos
    '''
    def pegar_requisitos_disciplina(self, codigo_disciplina: str) -> List[str]:
        try:
            # Aguardando a grade curricular estar presente
            self.wait.until(EC.presence_of_element_located((By.ID, "gradeCurricular")))
            
            # Pegando o HTML da página
            html = self.jupiter_selenium.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            # Achando grade curricular
            grade_curricular = soup.find(id="gradeCurricular")
            if not grade_curricular:
                return []
            
            linhas = grade_curricular.find_all("tr")
            
            # Lista para armazenar os requisitos encontrados
            requisitos = []
            
            # Flag para indicar se encontramos a disciplina alvo
            disciplina_encontrada = False
            
            for i, linha in enumerate(linhas):
                # Verificando se esta linha contém a disciplina que estamos procurando
                if not disciplina_encontrada:
                    # Procurando pela disciplina nas células da linha
                    celulas = linha.find_all("td")
                    for celula in celulas:
                        # Verificando se a célula contém o código da disciplina
                        texto_celula = celula.get_text(strip=True)
                        if codigo_disciplina in texto_celula:
                            disciplina_encontrada = True
                            break
                    
                    # Se encontrou a disciplina, continue para verificar as próximas linhas
                    if disciplina_encontrada:
                        continue
                
                else:
                    # Já encontramos a disciplina, agora procuramos pelos requisitos
                    style = linha.get("style", "")
                    
                    # Verificando se a linha tem altura de 20px (linha de disciplina normal)
                    if "height: 20px;" in style:
                        # Esta é uma nova disciplina, paramos de procurar requisitos
                        break
                    
                    # Verificando se a linha tem cor laranja (requisitos)
                    # Baseado na imagem, as linhas de requisito têm cor rgb(235, 143, 0)
                    if "rgb(235, 143, 0)" in style or "color: rgb(235, 143, 0)" in style:
                        # Esta linha contém requisitos
                        celulas = linha.find_all("td")
                        
                        # Procurando por códigos de disciplinas nas células
                        for celula in celulas:
                            texto_celula = celula.get_text(strip=True)
                            
                            # Se a célula contém "Requisito fraco" ou similar, pegar a próxima célula
                            if "Requisito" in texto_celula:
                                continue
                            
                            # Se a célula não está vazia e parece ser um código de disciplina
                            if texto_celula and len(texto_celula) > 3:
                                # Verificando se contém padrão de código de disciplina (letras + números)
                                import re
                                codigos_encontrados = re.findall(r'[A-Z]{3}\d{4}', texto_celula)
                                requisitos.extend(codigos_encontrados)
                    
                    # Verificando se chegamos a uma linha de tipo de disciplina (azul)
                    elif "rgb(16, 148, 171)" in style:
                        # Chegamos a uma nova seção, paramos de procurar
                        break
            
            # Removendo duplicatas e retornando
            return list(set(requisitos))
            
        except TimeoutException:
            print("Timeout: Não foi possível carregar a grade curricular")
            return []
        except Exception as e:
            print(f"Erro ao buscar requisitos da disciplina {codigo_disciplina}: {e}")
            return []

def criar_usp() -> List:
    # Definindo lista e objeto do scraper
    USP : List = []
    jupiterweb : ScraperJupiterWeb = ScraperJupiterWeb()

    # Buscando unidades
    lista_unidades : List = jupiterweb.pegar_unidades()

    numero_unidades = len(lista_unidades)

    print([unidade for unidade in lista_unidades])

    # Criando unidades
    print("Iniciando download dos dados...\n")

    # Marcando tempo de início
    tempo_inicio : float = time.time()

    for i in range(numero_unidades):
        elemento_unidade = lista_unidades[i]
        print(f"Baixando dados da unidade: {elemento_unidade}")
        # Instanciando objeto unidade
        unidade : Unidade = Unidade(elemento_unidade)
        lista_cursos : List = jupiterweb.pegar_cursos(elemento_unidade)

        # Criando cursos
        for elemento_curso in lista_cursos:
            informacoes_curso : Tuple = jupiterweb.pegar_informacoes_curso(elemento_unidade, elemento_curso)

            if informacoes_curso == None:
                jupiterweb.ir_para("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")
                continue

            dicionario_disciplinas : Dict = jupiterweb.pegar_disciplinas()
            
            # Criando lista de disciplinas obrigatórias
            lista_disciplinas_obrigatorias : List = []
            for elemento_disciplina in dicionario_disciplinas["Disciplinas Obrigatórias"]:
                # Instanciando objeto disciplina
                requisitos = jupiterweb.pegar_requisitos_disciplina(elemento_disciplina[0]);
                disciplina : Disciplina = Disciplina(elemento_disciplina[0], 
                                        elemento_disciplina[1],
                                        elemento_disciplina[2],
                                        elemento_disciplina[3],
                                        elemento_disciplina[4],
                                        elemento_disciplina[5],
                                        elemento_disciplina[6],
                                        elemento_disciplina[7],
                                        requisitos)
                lista_disciplinas_obrigatorias.append(disciplina)
            
            # Criando lista de disciplinas optativas livres
            lista_disciplinas_livre : List = []
            for elemento_disciplina in dicionario_disciplinas["Disciplinas Optativas Livres"]:
                # Instanciando objeto disciplina
                requisitos = jupiterweb.pegar_requisitos_disciplina(elemento_disciplina[0]);
                disciplina : Disciplina = Disciplina(elemento_disciplina[0], 
                                        elemento_disciplina[1],
                                        elemento_disciplina[2],
                                        elemento_disciplina[3],
                                        elemento_disciplina[4],
                                        elemento_disciplina[5],
                                        elemento_disciplina[6],
                                        elemento_disciplina[7],
                                        requisitos)
                lista_disciplinas_livre.append(disciplina)
            
            # Criando lista de disciplinas eletivas
            lista_disciplinas_eletiva : List = []
            for elemento_disciplina in dicionario_disciplinas["Disciplinas Optativas Eletivas"]:
                # Instanciando objeto disciplina
                requisitos = jupiterweb.pegar_requisitos_disciplina(elemento_disciplina[0]);
                disciplina : Disciplina = Disciplina(elemento_disciplina[0], 
                                        elemento_disciplina[1],
                                        elemento_disciplina[2],
                                        elemento_disciplina[3],
                                        elemento_disciplina[4],
                                        elemento_disciplina[5],
                                        elemento_disciplina[6],
                                        elemento_disciplina[7],
                                        requisitos)
                lista_disciplinas_eletiva.append(disciplina)

            # Instanciando objeto curso
            curso : Curso = Curso(elemento_curso, 
                          elemento_unidade, 
                          informacoes_curso[0], 
                          informacoes_curso[1], 
                          informacoes_curso[2], 
                          lista_disciplinas_obrigatorias, 
                          lista_disciplinas_livre, 
                          lista_disciplinas_eletiva)
            
            unidade.adicionar_cursos(curso)
            jupiterweb.voltar_inicio()
        USP.append(unidade)

    # Fechando janela do scraper
    jupiterweb.fechar_scraper()
    
    # Marcando tempo de fim
    tempo_fim : float = time.time()

    # Tempo de execução
    tempo_execução : float = tempo_fim - tempo_inicio
    unidade : str = 's'

    # Transformando para minutos se tiver mais que 1 min
    if tempo_execução > 60:
        tempo_execução /= 60
        unidade = 'min'

        # Transformando para horas se tiver mais que 1 hora
        if tempo_execução > 60:
            tempo_execução /= 60
            unidade = 'h'

    # Imprimindo tempo de execução
    print(f"Tempo necessário para baixar dados foi: {round(tempo_execução, 2)} {unidade}\n\n")

    return USP

def main():
    # Inicia o processo de scraping
    usp_data_objects = criar_usp()
    # Converte os objetos para o formato de dicionário desejado para JSON
    dados_json = {}
    for unidade_obj in usp_data_objects:
        dados_json[unidade_obj.nome] = unidade_obj.to_dict()

    # Escreve os dados no arquivo JSON
    nome_arquivo = "dados.json"
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_json, f, ensure_ascii=False, indent=4)

    print(f"Dados salvos em '{nome_arquivo}' com sucesso!")

if __name__ == "__main__":
    main()