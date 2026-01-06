import cv2
import numpy as np

class Preprocessador_img:

    @staticmethod
    def open_img(img):
        try:
            file_bytes = img.read()
            np_array = np.frombuffer(file_bytes, np.uint8)
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            if image is None:
                raise TypeError("O arquivo não é uma imagem válida ou formato não suportado.")
            
            return image
        
        except AttributeError:
            print("Erro: O objeto passado não possui o método .read(). Verifique se você enviou o arquivo corretamente.")
            raise TypeError("Erro: O objeto passado não possui o método .read(). Verifique se você enviou o arquivo corretamente.")
        except ValueError as e:
            print(f"Erro de Valor: {e}")
            raise TypeError(f"Erro de Valor: {e}")
        except TypeError as e:
            print(f"Erro de Tipo: {e}")
            raise TypeError(f"Erro de Tipo: {e}")
        except Exception as e:
            # Captura qualquer outro erro inesperado (rede, memória, etc)
            print(f"Erro inesperado ao processar a imagem: {e}")
            raise TypeError(f"Erro inesperado ao processar a imagem: {e}")


    @staticmethod
    def preprocess(img):
        try:
            #img = cv2.imread(image_path)

            if img is None:
                raise ValueError("Imagem não encontrada ou invalida")
            
            
            # 1. Converter para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          
            cv2.imwrite("etapa_um.jpg", gray)

            

           # 2. Aqui é o ponto principal, aqui vamos decidir, de forma inteligente, o que vai virar preto e o que vai virar branco
            thresh = cv2.adaptiveThreshold(
            gray,
                255, # Brilho maximo que um pixel pode receber
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,# O cerebro que vai decidir o limiar, para definir o que vira branco e o que vira preto
                cv2.THRESH_BINARY,# Aqui, binarizamos a imagem
                31, # Tamanho da lupa (31x31)
                10 # a subtração de acordo com a media para tratar ruidos
            )
            cv2.imwrite("etapa_dois.jpg", thresh)

            # 5. Sharpen leve
            kernel = np.array([
                [-0, -1, -0],
                [-1, 5, -1],
                [-0, -1, -0]
            ])
            sharpened = cv2.filter2D(thresh, -1, kernel)
            cv2.imwrite("etapa_tres.jpg", sharpened)

            return sharpened

        except Exception as e:

            raise RuntimeError(f"Erro no pré-processamento da imagem: {e}")
        
