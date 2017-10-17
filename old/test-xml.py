#Este es el programa base de la App
#Empezaremos con algunos test basicos con la API de hattrick (o CHPP)

from  chpp import CHPPhelp
import hidden
import xml.etree.ElementTree as ET

#Iniciamos claves para acceder a los recursos CHPP de la API de Hatrick
helper = CHPPhelp()
secrets = hidden.keys_app()
user_key = secrets['token_key']
user_secret = secrets['token_secret']

#Example: get the list of youth players
#xmldoc = helper.request_resource_with_key(      user_key,
#                                                user_secret,
#                                                'youthplayerlist',
#                                                {
#                                                 'actionType' : 'details',
#                                                 'showScoutCall' : 'true',
#                                                 'showLastMatch' : 'true'
#                                                }
#                                               )

xmldoc = helper.request_resource_with_key(  user_key,
                                           user_secret,
                                           'leaguedetails',
                                           {
                                           'version' : 1.5,
                                           }
                                       )

# xmldoc = '''
# <HattrickData>
#   <FileName>leaguedetails.xml</FileName>
#   <Version>1.5</Version>
#   <UserID>10150426</UserID>
#   <FetchedDate>2017-10-11 16:36:20</FetchedDate>
#   <LeagueID>36</LeagueID>
#   <LeagueName>Espanya</LeagueName>
#   <LeagueLevel>3</LeagueLevel>
#   <MaxLevel>8</MaxLevel>
#   <LeagueLevelUnitID>3419</LeagueLevelUnitID>
#   <LeagueLevelUnitName>III.12</LeagueLevelUnitName>
#   <CurrentMatchRound>7</CurrentMatchRound>
#   <Team>
#     <UserId>8220844</UserId>
#     <TeamID>1593528</TeamID>
#     <TeamName>Olimpic de Burdeos</TeamName>
#     <Position>1</Position>
#     <PositionChange>0</PositionChange>
#     <Matches>6</Matches>
#     <GoalsFor>21</GoalsFor>
#     <GoalsAgainst>3</GoalsAgainst>
#     <Points>18</Points>
#     <Won>6</Won>
#     <Draws>0</Draws>
#     <Lost>0</Lost>
#   </Team>
#   <Team>
#     <UserId>8699180</UserId>
#     <TeamID>990216</TeamID>
#     <TeamName>Pueblica F.C.</TeamName>
#     <Position>2</Position>
#     <PositionChange>0</PositionChange>
#     <Matches>6</Matches>
#     <GoalsFor>19</GoalsFor>
#     <GoalsAgainst>12</GoalsAgainst>
#     <Points>10</Points>
#     <Won>3</Won>
#     <Draws>1</Draws>
#     <Lost>2</Lost>
#   </Team>
#   <Team>
#     <UserId>11726340</UserId>
#     <TeamID>989444</TeamID>
#     <TeamName>Racing de Zamora</TeamName>
#     <Position>3</Position>
#     <PositionChange>0</PositionChange>
#     <Matches>6</Matches>
#     <GoalsFor>15</GoalsFor>
#     <GoalsAgainst>16</GoalsAgainst>
#     <Points>10</Points>
#     <Won>3</Won>
#     <Draws>1</Draws>
#     <Lost>2</Lost>
#   </Team>
#   <Team>
#     <UserId>7322463</UserId>
#     <TeamID>1596538</TeamID>
#     <TeamName>Son Rapinya</TeamName>
#     <Position>4</Position>
#     <PositionChange>1</PositionChange>
#     <Matches>6</Matches>
#     <GoalsFor>10</GoalsFor>
#     <GoalsAgainst>10</GoalsAgainst>
#     <Points>8</Points>
#     <Won>2</Won>
#     <Draws>2</Draws>
#     <Lost>2</Lost>
#   </Team>
#   <Team>
#     <UserId>11107505</UserId>
#     <TeamID>125815</TeamID>
#     <TeamName>rayitus vallekanus</TeamName>
#     <Position>5</Position>
#     <PositionChange>2</PositionChange>
#     <Matches>6</Matches>
#     <GoalsFor>7</GoalsFor>
#     <GoalsAgainst>9</GoalsAgainst>
#     <Points>7</Points>
#     <Won>2</Won>
#     <Draws>1</Draws>
#     <Lost>3</Lost>
#   </Team>
#   <Team>
#     <UserId>10150426</UserId>
#     <TeamID>120994</TeamID>
#     <TeamName>V@der SC</TeamName>
#     <Position>6</Position>
#     <PositionChange>0</PositionChange>
#     <Matches>6</Matches>
#     <GoalsFor>10</GoalsFor>
#     <GoalsAgainst>11</GoalsAgainst>
#     <Points>5</Points>
#     <Won>0</Won>
#     <Draws>5</Draws>
#     <Lost>1</Lost>
#   </Team>
#   <Team>
#     <UserId>265688</UserId>
#     <TeamID>122543</TeamID>
#     <TeamName>Marmota Phil</TeamName>
#     <Position>7</Position>
#     <PositionChange>1</PositionChange>
#     <Matches>6</Matches>
#     <GoalsFor>6</GoalsFor>
#     <GoalsAgainst>15</GoalsAgainst>
#     <Points>4</Points>
#     <Won>1</Won>
#     <Draws>1</Draws>
#     <Lost>4</Lost>
#   </Team>
#   <Team>
#     <UserId>5399535</UserId>
#     <TeamID>990843</TeamID>
#     <TeamName>PACKARD</TeamName>
#     <Position>8</Position>
#     <PositionChange>2</PositionChange>
#     <Matches>6</Matches>
#     <GoalsFor>5</GoalsFor>
#     <GoalsAgainst>17</GoalsAgainst>
#     <Points>4</Points>
#     <Won>1</Won>
#     <Draws>1</Draws>
#     <Lost>4</Lost>
#   </Team>
# </HattrickData>'''

root = ET.fromstring(xmldoc)

for team in root.findall('Team'):
    equipo = team.find('TeamName').text
    print(equipo)
