 main.py
  import json
  from fastapi import FastAPI, Form, BackgroundTasks
  from fastapi.responses import Response
  from openai import OpenAI
  from twilio.rest import Client
  from vola_api import search_flights_real

  # -- SETĂRI --
  client = OpenAI(
      base_url='https://api.featherless.ai/v1',
      api_key='rc_ae8d23eb6b3e632d533677bd4e89e00b91b7a3a02c041ad9ad590cac7748eb87'
  )

  TWILIO_ACCOUNT_SID = 'ACebee6446c9f4f91f6ff961e26a82b4fd'
  TWILIO_AUTH_TOKEN = '7537e577e4350bfd66b114f3cdecfa46'
  TWILIO_PHONE_NUMBER = 'whatsapp:+14155238886'

  twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
  app = FastAPI()

  tools = [
      {
          "type": "function",
          "function": {
              "name": "search_vola_flights",
              "description": "Caută prețuri reale de zboruri pe vola.ro. Folosește-o când utilizatorul cere o rută sau
  prețuri.",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "origin_code": {"type": "string", "description": "Cod IATA al ORAȘULUI de plecare (ex: BUH pentru
  București)."},
                      "dest_code": {"type": "string", "description": "Cod IATA al ORAȘULUI destinație (ex: ROM, PAR,
  LON)."},
                      "departure_date": {"type": "string", "description": "Data plecării YYYY-MM-DD"},
                      "return_date": {"type": "string", "description": "Data întoarcerii YYYY-MM-DD"}
                  },
                  "required": ["origin_code", "dest_code", "departure_date", "return_date"]
              }
          }
      }
  ]


  def proceseaza_mesajul(body: str, sender_phone: str):
      print(f"\n[BOT] M-am apucat de treabă pentru: {body}")

      mesaje = [
          {"role": "system", "content": "Ești VolaBot, asistentul de călătorii Vola.ro. Ești prietenos și scurt. Extrage
   orașele în format IATA și apelează funcția de căutare. Data de azi: " +
  __import__('datetime').datetime.now().strftime('%Y-%m-%d')},
          {"role": "user", "content": body}
      ]

      try:
          response = client.chat.completions.create(
              model='Qwen/Qwen3-8B',
              messages=mesaje,
              tools=tools,
              tool_choice="auto"
          )

          mesaj_raspuns = response.choices[0].message

          if mesaj_raspuns.tool_calls:
              tool_call = mesaj_raspuns.tool_calls[0]
              argumente = json.loads(tool_call.function.arguments)

              rezultat_zboruri = search_flights_real(
                  origin_code=argumente.get("origin_code"),
                  dest_code=argumente.get("dest_code"),
                  departure_date=argumente.get("departure_date"),
                  return_date=argumente.get("return_date")
              )

              mesaje.append(mesaj_raspuns)
              mesaje.append({
                  "role": "tool",
                  "tool_call_id": tool_call.id,
                  "name": tool_call.function.name,
                  "content": str(rezultat_zboruri)
              })

              raspuns_final = client.chat.completions.create(
                  model='Qwen/Qwen3-8B',
                  messages=mesaje
              )
              text_de_trimis = raspuns_final.choices[0].message.content
          else:
              text_de_trimis = mesaj_raspuns.content

          if not text_de_trimis:
              text_de_trimis = "Scuze, nu am putut procesa mesajul. Încearcă din nou."

      except Exception as e:
          print(f"[EROARE] {e}")
          text_de_trimis = "Scuze, am întâmpinat o eroare. Încearcă din nou."

      text_de_trimis = text_de_trimis[:1600]

      print(f"[WHATSAPP] Trimit mesajul către {sender_phone}...")

      twilio_client.messages.create(
          from_=TWILIO_PHONE_NUMBER,
          body=text_de_trimis,
          to=sender_phone
      )
      print("[WHATSAPP] Mesaj trimis cu succes!")


  @app.post("/whatsapp")
  async def whatsapp_webhook(background_tasks: BackgroundTasks, Body: str = Form(...), From: str = Form(...)):
      print(f"\n[USER] a trimis: {Body}")

      background_tasks.add_task(proceseaza_mesajul, Body, From)

      return Response(content="<Response></Response>", media_type="application/xml")

  vola_api.py
  import requests
  import time


  def search_flights_real(origin_code, dest_code, departure_date, return_date):
      print(f"Caut zboruri reale: {origin_code} -> {dest_code} ({departure_date} / {return_date})")

      headers = {
          'accept': 'application/json',
          'accept-language': 'ro',
          'api-key': '7f6c921c-d7f8-4303-b9ad-b60878ca12ed',
          'content-type': 'application/json',
          'origin': 'https://www.vola.ro',
          'referer': 'https://www.vola.ro/',
          'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Brave";v="144"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Linux"',
          'slot': 'volaFW6142',
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0
  Safari/537.36',
          'x-ab-test-token':
  'eyJpdiI6IjhrV1ZWZVVBeFdGZk1pdy9ZVmdXTWc9PSIsInZhbHVlIjoiRE5MSUNHc2NRK1BqY1J1UEJ5bWxFMUtRUzRZT2xvaTBwZEU5S01jM0dYVnBUT
  05ZYVBGVXJKYXR0cGwvYkIwcDE2am1ud3hqdnFnR2tzeUpMczJiM1dUUmk2SHpTR3RDVXB3SXd1aHJTbzE5NGpacDluS3dDcUlidGdjY0g1VEZUc1hXZVE
  yMGQ0eVg2UkxYOGQzWWE4MmFnRjFNc1dBaWtvRENyMU1DN1Y4cTV0dlgydUlhOWRRalZHQ3l2OVp4ZHc3YS9BRUZsMnpOdlo2N2dUcXQ0SjZXM25iNVRtW
  kxmMkR1Slo0aVFJdnhJdnQ5VTlITGFPV2JobmZPdGtCK1RQaC9kR1Q0NDBuUTNUQ05ZV1hGeEE2K2xOR0gxNndJMFltRUpMakhXWm41UFVxYVZ5enpqY0d
  4RGlzNFhtbXBRbk1Yd081T1JnVFJnMFVtOFJzTnpSWmdXaFZFK3FvYnNZOGNpeSt0bThlSHRZa1B3M2xZQWJJb0FXVFF5amlaV2FsbEk4MVZoWEVPYTlOa
  EtmaEtxWHRWdUQ1OE9PNFd5dGI0YmpRNkFYdGtHNEd4Nm5rNUljUFk2ZnZmUkxDVGltc2Z1QjI1dy9BWkpGZjd3d0JzSHpvVHJsV0YxYUY3enZ0eGUyTE5
  UZE00TUJJN2p5RXdDWDJjcFNsTWdzWW1iMlY1UDBqVlJUTXl4M1laVVVWYWZzblZsTjVMQlRNWWY1eW1kZE9rSkpWT0tsVHg5cUxwcXhlNkhJREk2eWdUI
  iwibWFjIjoiYWFmMmY5OGFhZWU5NjU2NGRjMzYwZDViNTUwNzI2ZTBmMWYzMzNiOTJjYzJjZTkyZjhmN2VlNzVkY2YzMzVhNCIsInRhZyI6IiJ9',
          'x-affiliate': 'vola',
          'x-app-origin': 'new-front-end',
      }

      payload = {
          'dates': {
              'departureFrom': departure_date,
              'departureTo': departure_date,
              'returnFrom': return_date,
              'returnTo': return_date
          },
          'passengers': {'adults': 1, 'children': 0, 'infants': 0, 'youth': 0},
          'locations': {
              'origins': [{'code': origin_code, 'type': 'CITY'}],
              'destinations': [{'code': dest_code, 'type': 'CITY'}]
          },
          'luggageOptions': {'personalItemCount': 1, 'cabinTrolleyCount': 0, 'checkedBaggageCount': 0}
      }

      try:
          resp = requests.post('https://api.ith.toys/gateway/discover', headers=headers, json=payload, timeout=10)
          if resp.status_code != 200:
              return f"Eroare la conectarea cu Vola. Status: {resp.status_code}"

          discovery_id = resp.json().get('discoveryId')
          if not discovery_id:
              return "Nu am primit un ID de căutare de la Vola."

          fetch_url = f"https://api.ith.toys/gateway/discover/fetch/{discovery_id}"

          for _ in range(5):
              time.sleep(1.5)
              fetch_resp = requests.get(fetch_url, headers=headers, timeout=10)

              if fetch_resp.status_code == 200:
                  rezultate = fetch_resp.json()
                  oferte = rezultate.get('offersResult', {}).get('offers', [])

                  if len(oferte) > 0:
                      rezumat = []
                      for o in oferte[:5]:
                          pret = o.get('score', {}).get('price')
                          rezumat.append(f"Zbor la {pret} EUR")
                      return " | ".join(rezumat)

          return "Căutarea a durat prea mult. Încearcă din nou."

      except Exception as e:
          print(f"[VOLA API EROARE] {e}")
          return f"Eroare la căutare: {str(e)[:100]}"
