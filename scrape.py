import requests
from bs4 import BeautifulSoup
import time

teams = ["16-1291", "16-9999","16-3442", "16-2397", "16-1414", "16-0715"]  # Add your team numbers here

teams_data = []
request_count = 0

# Loop through each team and make the requests
for team in teams:
    print(f"fetching: {team}")
    url = f"https://scoreboard.uscyberpatriot.org/team.php?team={team}"

    response = requests.get(url)
    request_count += 1
    if request_count % 3 == 0:
        time.sleep(2)

    team_data = {  # Initialize team_data outside the try block
        "team": team,
        "images": [],
        "total_score": 0  # Initialize total_score
    }

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')[1]
        rows = table.find_all('tr')[1:]  # Exclude header row

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            image_name = cols[0].split('_')[0]  # Shorten the image name to the first word
            image_score = cols[-1]  # Assuming the score is in the last column

            team_data["images"].append({
                "name": image_name,
                "score": image_score,
            })

            # Add to the total score
            team_data["total_score"] += int(image_score) if image_score.isdigit() else 0

    except IndexError as e:
        print(f"Data for team {team} is not available or the table structure is different than expected.")
        team_data["images"].append({
            "name": "",
            "score": "",
        })

    # Add a check if total score is 0, then it's likely the team was not found
    if team_data["total_score"] == 0:
        team_data["total_score"] = "Team Not Found"

    teams_data.append(team_data)

# Sort teams by total score, highest to lowest; handle non-integer scores gracefully
teams_data.sort(key=lambda x: x['total_score'] if isinstance(x['total_score'], int) else -1, reverse=True)

# Function to create an HTML table row for a team
def create_team_row(team_data):
    row = f"<tr><td>{team_data['team']}</td>"
    for image_data in team_data['images']:
        row += f"<td>{image_data['name']}</td><td>{image_data['score']}</td>"

    # Add total score in red font color
    total_score_str = str(team_data['total_score']) if team_data['total_score'] != "Team Not Found" else team_data['total_score']
    row += f"<td style='color: red;'>{total_score_str}</td></tr>"
    return row

# Generate table content based on teams data
table_content = ""
for team_data in teams_data:
    table_content += create_team_row(team_data)

# Construct the dynamic headers based on the number of images
headers = "<th>Team</th>"
for _ in teams_data[0]['images']:
    headers += "<th>Image</th><th>Score</th>"
headers += "<th>Total Score</th>"  # Add header for total score

# Construct the final HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <META HTTP-EQUIV="refresh" CONTENT="15">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Data</title>
    <style>
        body {{
            background-color: #f4f4f4;
            margin: 0;
            padding-top: 20px;
        }}
        .rounded-rectangle {{
            border: 2px solid #821477;
            background-color: white;
            border-radius: 20px;
            padding: 20px;
            overflow: auto;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <div class="rounded-rectangle">
        <table>
            <tr>
                {headers}
            </tr>
            {table_content}
        </table>
    </div>
</body>
</html>
"""

# Write the data into a new HTML file
with open("/var/www/html/team_data.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Data has been written to team_data.html")
