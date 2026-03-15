import json
from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import Response
from openai import OpenAI
from twilio.rest import Client
from vola_api import search_flights_real

# -- SETĂRI --
client = OpenAI(
    base_url='httpsapi.featherless.aiv1',
    api_key='rc_ae8d23eb6b3e632d533677bd4e89e00b91b7a3a02c041ad9ad590cac7748eb87'
)

# Pune aici datele tale din contul Twilio
TWILIO_ACCOUNT_SID = 'AICI_PUI_SID_UL_TAU'
TWILIO_AUTH_TOKEN = 'AICI_PUI_TOKEN_UL_TAU'
TWILIO_PHONE_NUMBER = 'whatsapp+14155238886' # Ăsta e numărul Sandbox-ului Twilio. Dacă e altul la tine, modifică-l.

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
app = FastAPI()

tools = [
    {
        type function,
        function {
            name search_vola_flights,
            description Caută prețuri reale. Folosește-o când utilizatorul cere o rută.,
            parameters {
                type object,
                properties {
                    origin_code {type string, description Cod IATA al ORAȘULUI de plecare (ex BUH pentru București).},
                    dest_code {type string, description Cod IATA al ORAȘULUI destinație (ex ROM, PAR, LON).},
                    departure_date {type string, description Data plecării YYYY-MM-DD},
                    return_date {type string, description Data întoarcerii YYYY-MM-DD}
                },
                required [origin_code, dest_code, departure_date, return_date]
            }
        }
    }
]

# Asta e funcția care rulează în fundal, fără să o mai streseze Twilio cu timpul
def proceseaza_mesajul(body str, sender_phone str)
    print(fn[BOT] M-am apucat de treabă pentru {body})
    
    mesaje = [
        {role system, content Ești VolaBot. Ești prietenos și scurt. Extrage orașele în format IATA și apelează funcția de căutare.},
        {role user, content body}
    ]

    response = client.chat.completions.create(
        model='QwenQwen3-8B',
        messages=mesaje,
        tools=tools,
        tool_choice=auto
    )
    
    mesaj_raspuns = response.choices[0].message

    if mesaj_raspuns.tool_calls
        tool_call = mesaj_raspuns.tool_calls[0]
        argumente = json.loads(tool_call.function.arguments)
        
        rezultat_zboruri = search_flights_real(
            origin_code=argumente.get(origin_code),
            dest_code=argumente.get(dest_code),
            departure_date=argumente.get(departure_date),
            return_date=argumente.get(return_date)
        )
        
        mesaje.append(mesaj_raspuns)
        mesaje.append({
            role tool,
            tool_call_id tool_call.id,
            name tool_call.function.name,
            content str(rezultat_zboruri)
        })
        
        raspuns_final = client.chat.completions.create(
            model='QwenQwen3-8B',
            messages=mesaje
        )
        text_de_trimis = raspuns_final.choices[0].message.content
    else
        text_de_trimis = mesaj_raspuns.content

    print(f[WHATSAPP] Trimit mesajul asincron către {sender_phone}...)
    
    # Aici e magia. Trimitem mesajul proactiv către WhatsApp
    twilio_client.messages.create(
        from_=TWILIO_PHONE_NUMBER,
        body=text_de_trimis,
        to=sender_phone
    )
    print([WHATSAPP] Mesaj trimis cu succes!)


@app.post(whatsapp)
async def whatsapp_webhook(background_tasks BackgroundTasks, Body str = Form(...), From str = Form(...))
    print(fn[USER] a trimis {Body})
    
    # Trimitem funcția mare să ruleze în fundal
    background_tasks.add_task(proceseaza_mesajul, Body, From)
    
    # Răspundem INSTANT cu 200 OK și un XML gol, ca Twilio să nu ne dea timeout
    return Response(content=ResponseResponse, media_type=applicationxml)
