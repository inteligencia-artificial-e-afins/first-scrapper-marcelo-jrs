import requests
from email.message import EmailMessage
import ssl
import smtplib
from bs4 import BeautifulSoup

url = 'https://lol.fandom.com/wiki/CBLOL/2024_Season/Split_1_Playoffs/Player_Statistics'
page = requests.get(url)
soup = BeautifulSoup(page.text, features="html.parser")

table_kda = soup.find('table', class_='spstats')
tbody = table_kda.find('tbody')

players = tbody.find_all('tr')

new_players = players[5:]

players_stats = []

for player in new_players:
    team_img = player.find('td', class_='spstats-team').find('img')['src']
    player_name = player.find('td', class_='spstats-player').find('a').text
    td_tags = player.find_all('td')
    kda_text = td_tags[9].text
    kda = float(kda_text)
    players_stats.append({'img': team_img, 'name': player_name, 'kda': kda})

sorted_players = sorted(players_stats, key=lambda x: x['kda'], reverse=True)

top_5_kdas = sorted_players[:5]

table_html = """
<h2>Top 5 jogadores por KDA no playoff do CBLOL</h2>
<p>Esses foram os principais jogadorres dos playoffs, com maiores porcentagens de Kills e Assistências, e menos Mortes (Deaths)</p>
<table>
  <tr>
    <th>Time</th>
    <th>Nome</th>
    <th>KDA</th>
  </tr>
"""

for player in top_5_kdas:
    table_html += f"""
  <tr>
    <td><img src="{player['img']}" alt="{player['name']} logo" width="50"></td>
    <td>{player['name']}</td>
    <td>{player['kda']}</td>
  </tr>
"""


table_html += """
</table>
"""

import os
from dotenv import load_dotenv

load_dotenv()

email_sender = "fmarcelocarlos@edu.unifil.br"
password = os.environ.get('EMAIL_PASSWORD')
# email_receiver = "fmarcelocarlos@gmail.com"
email_receiver = "mario.adaniya@unifil.br"

subject = "[DS101] Marcelo Júnior"
body = table_html

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body, subtype='html')

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
