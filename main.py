import pygame
import random
import os
from colorama import init, Fore

# Inicializando o Pygame
pygame.init()

# Definindo as dimensões da janela
tamanho_janela = 1500
tamanho_carta = 100
tamanho_borda = 10

janela = pygame.display.set_mode((tamanho_janela, tamanho_janela))
pygame.display.set_caption("Jogo da Memória - Melhores Gráficos para Analisar Dados")

# Carregar fonte para o texto
fonte = pygame.font.SysFont(None, 35)  # Fonte padrão do Pygame com tamanho 35

# Carregar imagens
def carrega_imagens():
    imagens = []
    pasta_imagens = "imagens"  # Certifique-se de que esta pasta exista e contenha as imagens
    for file_name in os.listdir(pasta_imagens):
        if file_name.endswith(".png"):
            imagem = pygame.image.load(os.path.join(pasta_imagens, file_name))
            imagem = pygame.transform.scale(imagem, (tamanho_carta, tamanho_carta))
            imagens.append(imagem)
    return imagens
def quebra_texto(texto, fonte, largura_max):
    """Divide o texto em várias linhas para caber dentro da largura máxima."""
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        # Testa o comprimento da linha atual com a nova palavra
        if '\n' in palavra:
            # Se encontrar um '\n' no meio da palavra, quebra a linha
            sub_palavras = palavra.split('\n')
            for sub_palavra in sub_palavras[:-1]:
                linha_atual += sub_palavra
                linhas.append(linha_atual)  # Adiciona a linha atual e reinicia
                linha_atual = ""  # Reinicia após o \n
            palavra = sub_palavras[-1]

        if fonte.size(linha_atual + palavra)[0] <= largura_max:
            linha_atual += palavra + " "
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "

    linhas.append(linha_atual)  # Adiciona a última linha
    return linhas

# função usada só para saber o índice de cada imagem
'''def carrega_imagens():
    imagens = []
    pasta_imagens = "imagens"  
    for index, file_name in enumerate(os.listdir(pasta_imagens)):
        if file_name.endswith(".png"):
            imagem = pygame.image.load(os.path.join(pasta_imagens, file_name))
            imagem = pygame.transform.scale(imagem, (tamanho_carta, tamanho_carta))
            imagens.append(imagem)
            # Exibe o índice e o nome da imagem
            print(f"Imagem {index}: {file_name}")
    return imagens'''

def cria_tabuleiro(tamanho, imagens):
    pares = imagens[:tamanho**2 // 2] * 2
    random.shuffle(pares)
    return [pares[i:i+tamanho] for i in range(0, len(pares), tamanho)]

def desenha_tabuleiro(tabuleiro, visivel):
    for i, linha in enumerate(tabuleiro):
        for j, imagem in enumerate(linha):
            x = j * (tamanho_carta + tamanho_borda) + tamanho_borda
            y = i * (tamanho_carta + tamanho_borda) + tamanho_borda
            if visivel[i][j]:
                janela.blit(imagem, (x, y))
            else:
                pygame.draw.rect(janela, (100, 100, 100), (x, y, tamanho_carta, tamanho_carta))

def desenha_texto(janela, texto, pos):
    """Função para desenhar texto com várias linhas na janela do Pygame."""
    largura_max = 600  # Defina a largura máxima para o texto
    linhas = quebra_texto(texto, fonte, largura_max)
    for i, linha in enumerate(linhas):
        superficie_texto = fonte.render(linha.strip(), True, (255, 255, 255))
        janela.blit(superficie_texto, (pos[0], pos[1] + i * 30))  # Ajusta a altura de cada linha


def solicita_jogada(pos):
    x, y = pos
    coluna = x // (tamanho_carta + tamanho_borda)
    linha = y // (tamanho_carta + tamanho_borda)
    return linha, coluna

def jogo_da_memoria():
    tamanho = 5
    imagens = carrega_imagens()
    tabuleiro = cria_tabuleiro(tamanho, imagens)
    visivel = [[False] * tamanho for _ in range(tamanho)]
    pares_encontrados = 0
    tentativas = 0
    mensagem_atual = ""  # Mensagem a ser exibida na tela
    mensagens = {
        0: "Você encontrou o GRÁFICO DE LINHAS!\nO gráfico de linhas é utilizado principalmente para mostrar a evolução de uma variável ao longo do tempo. Ele é eficaz para dados contínuos e sequenciais, facilitando a visualização de mudanças, padrões e flutuações em intervalos regulares. Este tipo de gráfico conecta pontos de dados com linhas, o que ajuda a identificar tendências ou padrões de comportamento, como picos, quedas ou ciclos. É UMA DAS MELHORES OPÇÕES PARA DEMONSTRAR TENDÊNCIAS.\n",
        1: "Você encontrou o GRÁFICO DE DISPERSÃO!\nO gráfico de dispersão (ou scatter plot) é utilizado para visualizar a relação entre duas variáveis contínuas e identificar padrões de correlação, como a direção e a intensidade dessa relação. Ele exibe pontos no plano cartesiano, onde cada ponto representa o valor de duas variáveis. O gráfico de dispersão é eficaz para mostrar como uma variável influencia ou se relaciona com outra, facilitando a identificação de tendências, anomalias e grupos dentro dos dados.\n",
        2: "Você encontrou o GRAFICO DE BARRAS! \nO gráfico de barras é ideal para comparar diferentes categorias ou grupos de dados discretos. Ele é amplamente utilizado quando você deseja visualizar as diferenças entre essas categorias de maneira clara e objetiva. MELHOR OPÇÃO PARA RANKINGS.\n",
        3: "Você encontrou o GRÁFICO DE PIZZA!\n O gráfico de pizza é ideal para representar proporções ou percentuais de um todo, ou seja, quando você deseja visualizar como uma variável se divide em partes que somam 100%. Ele é útil para mostrar a participação relativa de cada categoria dentro de um conjunto total.\n",
        4: "Você encontrou o GRÁFICO DE HISTOGRAMA!\n O histograma é utilizado quando você deseja visualizar a distribuição de uma variável contínua, ou seja, para entender como os dados se distribuem ao longo de um intervalo de valores. Ele organiza os dados em intervalos (ou bins) e mostra a frequência com que os dados caem em cada intervalo. Esse tipo de gráfico é especialmente útil para identificar padrões como distribuição normal, assimetria, moda, e outliers.\n",
        5: "Você encontrou o GRÁFICO DE ÁREA!\n O gráfico de área é utilizado para mostrar como um valor se acumula ao longo de uma sequência contínua, normalmente ao longo do tempo, e é ideal para representar a evolução acumulada ou o comportamento de variáveis ao longo do tempo. Ele é semelhante ao gráfico de linhas, mas a área abaixo da linha é preenchida, o que o torna útil para destacar o volume total ou a contribuição acumulada de diferentes partes de um conjunto de dados. UMA DAS MELHORES OPÇÕES PARA DEMONSTRAR TENDÊNCIAS.\n",
        6: "Você encontrou o GRÁFICO DE RADAR!\nO gráfico de radar, também conhecido como gráfico de aranha ou gráfico de teia, é utilizado para comparar múltiplas variáveis de maneira simultânea, mostrando como diferentes categorias se comportam em relação a um ponto central. Esse tipo de gráfico é útil para avaliar desempenho multidimensional ou comparações de perfil entre várias entidades ou itens.\n",
        7: "Você encontrou o GRÁFICO DE BOXPLOT!\nO boxplot, ou gráfico de caixa, é uma ferramenta estatística usada para visualizar a distribuição de um conjunto de dados e destacar suas características principais, como a mediana, os quartis e os possíveis outliers. Ele é particularmente útil para comparar distribuições entre diferentes grupos e identificar a dispersão, assimetria e valores atípicos nos dados.\n",
        8: "Você encontrou o GRÁFICO DE COLUNA!\nO gráfico de coluna é utilizado para comparar valores de categorias distintas de maneira visual, sendo ideal para mostrar diferenças entre grupos ou categorias em um período específico. Cada categoria é representada por uma coluna vertical, facilitando a comparação de dados quantitativos. Ele é similar ao gráfico de barras, mas as colunas são dispostas verticalmente, o que pode ser útil quando se tem um grande número de categorias ou dados temporais. É UMA DAS MELHORES OPÇÕES PARA DEMONSTRAR TENDÊNCIAS.\n",
        9: "Você encontrou o GRÁFICO DE MAPA DE CALOR!\nO mapa de calor (heatmap) é uma ferramenta visual que utiliza cores para representar valores de dados, facilitando a interpretação de padrões e tendências em grandes volumes de dados. Ele é usado para visualizar a intensidade de valores em uma matriz ou em diferentes regiões geográficas, dependendo da aplicação. A intensidade ou densidade dos valores é indicada pela variação de cores, geralmente de mais claro (valores baixos) para mais escuro (valores altos).\n"

    }
    primeira_jogada = None

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                linha, coluna = solicita_jogada(evento.pos)

                # Ignora se a carta já estiver visível
                if visivel[linha][coluna]:
                    continue

                # Revela a carta clicada
                visivel[linha][coluna] = True
                desenha_tabuleiro(tabuleiro, visivel)
                pygame.display.update()

                if not primeira_jogada:
                    primeira_jogada = (linha, coluna)
                else:
                    segunda_jogada = (linha, coluna)

                    # Espera para que o jogador veja a segunda carta
                    pygame.time.wait(1000)

                    # Verifica se as cartas são iguais
                    if tabuleiro[primeira_jogada[0]][primeira_jogada[1]] == tabuleiro[segunda_jogada[0]][segunda_jogada[1]]:
                        par_encontrado = imagens.index(tabuleiro[primeira_jogada[0]][primeira_jogada[1]])
                        mensagem_atual = mensagens.get(par_encontrado, "Par encontrado!")
                        print(Fore.GREEN + mensagem_atual)
                        pares_encontrados += 1
                    else:
                        visivel[primeira_jogada[0]][primeira_jogada[1]] = False
                        visivel[segunda_jogada[0]][segunda_jogada[1]] = False
                        mensagem_atual = "Não combinam. Tente novamente."
                        print(Fore.RED + mensagem_atual)

                    primeira_jogada = None
                    tentativas += 1

        janela.fill((0, 0, 0))
        desenha_tabuleiro(tabuleiro, visivel)
        desenha_texto(janela, mensagem_atual, (570, 10))  # Exibe a mensagem na tela
        pygame.display.update()

        if pares_encontrados == (tamanho**2 // 2):
            mensagem_atual = f"Parabéns! Você encontrou todos os pares em {tentativas} tentativas."
            desenha_texto(janela, mensagem_atual, (410, 10))
            pygame.display.update()
            pygame.time.wait(3000)  # Espera 3 segundos antes de fechar
            rodando = False

    pygame.quit()

if __name__ == "__main__":
    jogo_da_memoria()