import requests
from email.message import EmailMessage
import ssl
import smtplib
from bs4 import BeautifulSoup

# Get content from website

url = 'https://lol.fandom.com/wiki/CBLOL/2024_Season/Split_1'
page = requests.get(url)
soup = BeautifulSoup(page.text, features="html.parser")

standings = soup.find(class_='standings')

teams = standings.find_all(class_="teamhighlight")

teams_info = []

# Get info from each team individually

for team in teams:
  place = team.find(class_="standings-place").text.strip()
  team_name = team.find(class_="teamname").text.strip()
  img_tag = team.find('img')
  team_img = img_tag['src']
  team_points = team.find_all('td')[2].text.strip()

  team_dict = {"name": team_name, "place": place, "image": team_img, "points": team_points}
  teams_info.append(team_dict)

# Make html table
  
table_html = """
<table>
  <tr>
    <th>Colocação</th>
    <th>Logo</th>
    <th>Nome</th>
    <th>Pontos</th>
  </tr>
"""

for team in teams_info:
    table_html += f"""
  <tr>
    <td>{team['place']}</td>
    <td><img src="{team['image']}" alt="{team['name']} logo" width="50"></td>
    <td>{team['name']}</td>
    <td>{team['points']}</td>
  </tr>
"""

table_html += """
</table>
"""
   

email_sender = "fmarcelocarlos@edu.unifil.br"
password = "mcf01234"
email_receiver = "fmarcelocarlos@gmail.com"

subject = "TESTE"
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
