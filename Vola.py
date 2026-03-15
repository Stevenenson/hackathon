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
                      for o in oferte[:3]:
                          pret = o.get('score', {}).get('price')
                          rezumat.append(f"Zbor la {pret} EUR")
                      return " | ".join(rezumat)

          return "Căutarea a durat prea mult pentru un mesaj rapid."

      except Exception as e:
          print(f"[VOLA API EROARE] {e}")
          return f"Eroare la căutare: {str(e)[:100]}"
