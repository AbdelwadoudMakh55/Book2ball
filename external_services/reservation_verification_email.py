from azure.communication.email import EmailClient
from models.user import User
import json

def send_email_for_reservation_verification(user: User, pitch_name: str, start_time: str, reservation_id: str):
    try:
        with open("local.setting.json", "r") as file:
            data = json.load()
        api_key = data["Values"]["API_KEY"] 
        endpoint = data["Values"]["ENDPOINT"]
        connection_string = f"endpoint={endpoint};accesskey={api_key}"
        verification_link = f"http://localhost:7071/api/verify-reservation?user_id={user.id}&reservation_id={reservation_id}"
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "DoNotReply@79f6f715-eb45-4f9a-a9c7-019d34148c88.azurecomm.net",
            "recipients": {
                "to": [{"address": user.email}]
            },
            "content": {
                "subject": "Verify your reservation",
                "plainText": f"Hello {user.name}, please verify your reservation on {start_time} for pitch {pitch_name}",
                "html": f"""
                <html>
                    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                            <h1 style="color: #333333;">Verify Your Reservation</h1>
                            <p style="color: #555555;">Hello {user.name},</p>
                            <p style="color: #555555;">Please verify your reservation on {start_time} for pitch {pitch_name} by clicking the button below:</p>
                            <a href="{verification_link}" style="display: inline-block; padding: 10px 20px; margin: 20px 0; font-size: 16px; color: #ffffff; background-color: #4CAF50; text-decoration: none; border-radius: 5px;">Verify Reservation</a>
                            <p style="color: #555555;">Thank you,<br />Book2ball Team</p>
                        </div>
                    </body>
                </html>
                """
            },
            
        }

        poller = client.begin_send(message)
        result = poller.result()
        print("Message sent: ", result)

    except Exception as ex:
        print(ex)