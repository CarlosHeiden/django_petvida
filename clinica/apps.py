from django.apps import AppConfig


class ClinicaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinica'

    def ready(self):
        """
        Garante que o Firebase seja inicializado quando o Django iniciar.
        """
        # Importe e chame a função de inicialização
        try:
            from .firebase_init import initialize_firebase
            initialize_firebase()
        except ImportError:
            print("AVISO: Não foi possível importar o módulo firebase_init.py. Verifique o arquivo.")