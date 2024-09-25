from PIL import Image

   # Função para ler os valores de uma linha específica da imagem
def ler_valores_pixel(imagem_path, linha):
       # Abre a imagem
       imagem = Image.open(imagem_path)
       
       # Converte a imagem em uma lista de pixels
       pixels = list(imagem.getdata())
       
       # Obtém a largura da imagem
       largura = imagem.width
       altura = imagem.height
       
       # Calcula o início e o fim da linha
       inicio = linha * largura
       fim = inicio + largura
       
       # Extrai os pixels da linha
       linha_pixels = pixels[inicio:fim]
       
       return linha_pixels

def valores_unicos(lista):
    # Converte a lista para um conjunto para remover duplicatas
    return list(set(lista))

caminho_imagem = "C:/Users/User/Projetos/OpenCV/lego_detector/barras.png"  # Substitua pelo caminho da sua imagem
imagem2 = Image.open(caminho_imagem)
altura = int(imagem2.height/2)
print(altura)
linha_desejada =  altura # Defina a linha que deseja ler
valores_pixels = ler_valores_pixel(caminho_imagem, linha_desejada)
print("Valores dos pixels na linha", linha_desejada, ":", valores_pixels)

print(valores_unicos(valores_pixels))
