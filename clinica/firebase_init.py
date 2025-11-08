# clinica/firebase_init.py

import firebase_admin
from firebase_admin import credentials
from django.conf import settings
import os

# Caminho para o arquivo de credenciais que você baixou
# AJUSTE ESTE CAMINHO CONFORME ONDE VOCÊ SALVOU O JSON!
# É uma boa prática usar caminhos absolutos e variáveis de ambiente.
# Exemplo: O arquivo está na raiz do projeto (não recomendado para produção)
PATH_TO_CREDENTIALS = os.path.join(settings.BASE_DIR, 'E:\carlos\python\django_petvida\petvida\petvida-app-firebase-adminsdk-fbsvc-a7920e3362.json') 

# Caso você use uma variável de ambiente para o caminho:
# PATH_TO_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS_PATH', None)


def initialize_firebase():
    """
    Inicializa o Firebase Admin SDK se ele ainda não tiver sido inicializado.
    """
    if not firebase_admin._apps:
        try:
            # 1. Carrega as credenciais
            cred = credentials.Certificate(PATH_TO_CREDENTIALS)
            
            # 2. Inicializa o aplicativo Firebase
            firebase_admin.initialize_app(cred)
            
            print("INFO: Firebase Admin SDK inicializado com sucesso.")
        except FileNotFoundError:
            print(f"ERRO CRÍTICO: Arquivo de credenciais do Firebase não encontrado em: {PATH_TO_CREDENTIALS}")
        except Exception as e:
            print(f"ERRO CRÍTICO: Falha na inicialização do Firebase Admin SDK: {e}")