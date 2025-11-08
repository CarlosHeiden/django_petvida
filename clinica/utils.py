# clinica/utils.py
from firebase_admin import messaging
from clinica.firebase_init import initialize_firebase

def send_push_notification(fcm_token: str, title: str, body: str, data=None):
    """
    Envia uma notificação push real via Firebase Cloud Messaging.
    Usa o Firebase Admin SDK inicializado no projeto.
    """
    if not fcm_token:
        print("⚠️ Token FCM não encontrado. Notificação não enviada.")
        return

    # Garante que o Firebase esteja inicializado
    initialize_firebase()

    try:
        # Cria o corpo da mensagem
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=fcm_token,
            data=data or {"click_action": "FLUTTER_NOTIFICATION_CLICK"},
            android=messaging.AndroidConfig(
                priority="high",
                notification=messaging.AndroidNotification(
                    sound="default",
                    color="#4CAF50",
                ),
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(sound="default")
                ),
            ),
        )

        # Envia a mensagem
        response = messaging.send(message)
        print(f"✅ Notificação FCM enviada com sucesso! ID: {response}")

    except messaging.UnregisteredError:
        print(f"⚠️ Token FCM inválido ou expirado: {fcm_token[:10]}...")
    except Exception as e:
        print(f"❌ Erro ao enviar notificação FCM: {e}")