
# from datetime import datetime, timedelta
# import xml.etree.ElementTree as ET
# import sqlite3
# from  chpp import CHPPhelp
# import xml.etree.ElementTree as ET

from colorama import init, Fore, Back, Style

# print('\n')
# print(Fore.GREEN + Style.BRIGHT + 'SE-Bigdata ha sido autorizado con éxito!' + Style.RESET_ALL)
# print(Style.BRIGHT + 'Disfruta de tus estadisticas! xD')
# print(Style.RESET_ALL)
# print('\n')

countMatchNuevos = 10
print(Back.GREEN + Fore.WHITE + str(countMatchNuevos), Style.RESET_ALL + ' partidos nuevos han sido encontrados!')

listaPartidos= [ '1', '2']

print('Recuperando los datos de los ',Back.WHITE + Fore.BLACK + str(len(listaPartidos)), Style.RESET_ALL + ' partidos nuevos en www.hattrick.org... ')
print('Paciencia, puede tardar un poco..')






# t = ['611097585', '615085410', '611097589']
#
# for id in t:
#     print(id)

# xmldoc = '''
# <HattrickData>
#   <FileName>matchdetails.xml</FileName>
#   <Version>2.9</Version>
#   <UserID>10150426</UserID>
#   <FetchedDate>2017-10-14 19:01:15</FetchedDate>
#   <UserSupporterTier>platinum</UserSupporterTier>
#   <SourceSystem>Hattrick</SourceSystem>
#   <Match>
#     <MatchID>611097589</MatchID>
#     <MatchType>1</MatchType>
#     <MatchContextId>3419</MatchContextId>
#     <CupLevel>0</CupLevel>
#     <CupLevelIndex>0</CupLevelIndex>
#     <MatchDate>2017-10-14 14:00:00</MatchDate>
#     <FinishedDate>2017-10-14 15:45:00</FinishedDate>
#     <AddedMinutes>0</AddedMinutes>
#     <HomeTeam>
#       <HomeTeamID>120994</HomeTeamID>
#       <HomeTeamName>V@der SC</HomeTeamName>
#       <DressURI>//res.hattrick.org/kits/16/157/1569/1568416/matchKitSmall.png</DressURI>
#       <Formation>2-5-3</Formation>
#       <HomeGoals>1</HomeGoals>
#       <TacticType>0</TacticType>
#       <TacticSkill>0</TacticSkill>
#       <RatingMidfield>60</RatingMidfield>
#       <RatingRightDef>39</RatingRightDef>
#       <RatingMidDef>31</RatingMidDef>
#       <RatingLeftDef>36</RatingLeftDef>
#       <RatingRightAtt>62</RatingRightAtt>
#       <RatingMidAtt>62</RatingMidAtt>
#       <RatingLeftAtt>59</RatingLeftAtt>
#       <TeamAttitude>0</TeamAttitude>
#       <RatingIndirectSetPiecesDef>42</RatingIndirectSetPiecesDef>
#       <RatingIndirectSetPiecesAtt>38</RatingIndirectSetPiecesAtt>
#     </HomeTeam>
#     <AwayTeam>
#       <AwayTeamID>1593528</AwayTeamID>
#       <AwayTeamName>Olimpic de Burdeos</AwayTeamName>
#       <DressURI>//res.hattrick.org/kits/15/144/1434/1433803/matchKitSmall.png</DressURI>
#       <Formation>5-5-0</Formation>
#       <AwayGoals>2</AwayGoals>
#       <TacticType>8</TacticType>
#       <TacticSkill>21</TacticSkill>
#       <RatingMidfield>57</RatingMidfield>
#       <RatingRightDef>78</RatingRightDef>
#       <RatingMidDef>82</RatingMidDef>
#       <RatingLeftDef>77</RatingLeftDef>
#       <RatingRightAtt>6</RatingRightAtt>
#       <RatingMidAtt>9</RatingMidAtt>
#       <RatingLeftAtt>6</RatingLeftAtt>
#       <RatingIndirectSetPiecesDef>50</RatingIndirectSetPiecesDef>
#       <RatingIndirectSetPiecesAtt>48</RatingIndirectSetPiecesAtt>
#     </AwayTeam>
#     <Arena>
#       <ArenaID>120994</ArenaID>
#       <ArenaName>El Tártaro</ArenaName>
#       <WeatherID>2</WeatherID>
#       <SoldTotal>45120</SoldTotal>
#       <SoldTerraces>27587</SoldTerraces>
#       <SoldBasic>11635</SoldBasic>
#       <SoldRoof>4861</SoldRoof>
#       <SoldVIP>1037</SoldVIP>
#     </Arena>
#     <MatchOfficials>
#       <Referee>
#         <RefereeId>346427054</RefereeId>
#         <RefereeName>Edson Pinho Cruz</RefereeName>
#         <RefereeCountryId>16</RefereeCountryId>
#         <RefereeCountryName>Brasil</RefereeCountryName>
#         <RefereeTeamId>1087558</RefereeTeamId>
#         <RefereeTeamname>Modiin united f.c</RefereeTeamname>
#       </Referee>
#       <RefereeAssistant1>
#         <RefereeId>57377167</RefereeId>
#         <RefereeName>Erminio Merivot</RefereeName>
#         <RefereeCountryId>4</RefereeCountryId>
#         <RefereeCountryName>Italia</RefereeCountryName>
#         <RefereeTeamId>852845</RefereeTeamId>
#         <RefereeTeamname>NUTELLAEPANE</RefereeTeamname>
#       </RefereeAssistant1>
#       <RefereeAssistant2>
#         <RefereeId>341221167</RefereeId>
#         <RefereeName>Garin Landa</RefereeName>
#         <RefereeCountryId>36</RefereeCountryId>
#         <RefereeCountryName>España</RefereeCountryName>
#         <RefereeTeamId>221932</RefereeTeamId>
#         <RefereeTeamname>Bayview Soccer Club</RefereeTeamname>
#       </RefereeAssistant2>
#     </MatchOfficials>
#     <Scorers>
#       <Goal Index="0">
#         <ScorerPlayerID>388939943</ScorerPlayerID>
#         <ScorerPlayerName>Gianfranco Rezza</ScorerPlayerName>
#         <ScorerTeamID>120994</ScorerTeamID>
#         <ScorerHomeGoals>1</ScorerHomeGoals>
#         <ScorerAwayGoals>0</ScorerAwayGoals>
#         <ScorerMinute>30</ScorerMinute>
#         <MatchPart>1</MatchPart>
#       </Goal>
#       <Goal Index="1">
#         <ScorerPlayerID>401091244</ScorerPlayerID>
#         <ScorerPlayerName>Josef 'Del Bar' Ascher</ScorerPlayerName>
#         <ScorerTeamID>1593528</ScorerTeamID>
#         <ScorerHomeGoals>1</ScorerHomeGoals>
#         <ScorerAwayGoals>1</ScorerAwayGoals>
#         <ScorerMinute>54</ScorerMinute>
#         <MatchPart>2</MatchPart>
#       </Goal>
#       <Goal Index="2">
#         <ScorerPlayerID>398938762</ScorerPlayerID>
#         <ScorerPlayerName>Edgar 'Baragua' Céspedes</ScorerPlayerName>
#         <ScorerTeamID>1593528</ScorerTeamID>
#         <ScorerHomeGoals>1</ScorerHomeGoals>
#         <ScorerAwayGoals>2</ScorerAwayGoals>
#         <ScorerMinute>77</ScorerMinute>
#         <MatchPart>2</MatchPart>
#       </Goal>
#     </Scorers>
#     <Bookings>
#       <Booking Index="0">
#         <BookingPlayerID>394723751</BookingPlayerID>
#         <BookingPlayerName>Franck Mengal</BookingPlayerName>
#         <BookingTeamID>1593528</BookingTeamID>
#         <BookingType>1</BookingType>
#         <BookingMinute>31</BookingMinute>
#         <MatchPart>1</MatchPart>
#       </Booking>
#     </Bookings>
#     <Injuries />
#     <PossessionFirstHalfHome>51</PossessionFirstHalfHome>
#     <PossessionFirstHalfAway>49</PossessionFirstHalfAway>
#     <PossessionSecondHalfHome>51</PossessionSecondHalfHome>
#     <PossessionSecondHalfAway>49</PossessionSecondHalfAway>
#     <EventList>
#       <Event Index="0">
#         <Minute>0</Minute>
#         <SubjectPlayerID>120994</SubjectPlayerID>
#         <SubjectTeamID>60965</SubjectTeamID>
#         <ObjectPlayerID>45120</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>32</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText>Una bona jornada va fer que el &lt;a href="/Club/Arena/?ArenaID=120994"&gt;El Tártaro&lt;/a&gt; presentés una entrada de 45120 espectadors. Hi havia un petit grup d'aficionats de l'equip visitant que feia estona que rondaven per l'estadi, ja que s'havien desplaçat en moto des de la dispesa on s'allotjaven els jugadors, fins l'estadi on es jugava el partit. En &lt;a href="/Club/HallOfFame/Player.aspx?playerId=346427054"&gt;Edson Pinho Cruz&lt;/a&gt; va ser l'àrbitre assignat amb l'ajuda dels assistents &lt;a href="/Club/HallOfFame/Player.aspx?playerId=57377167"&gt;Erminio Merivot&lt;/a&gt; i &lt;a href="/Club/HallOfFame/Player.aspx?playerId=341221167"&gt;Garin Landa&lt;/a&gt;.</EventText>
#       </Event>
#       <Event Index="1">
#         <Minute>0</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>0</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>19</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText></EventText>
#       </Event>
#       <Event Index="2">
#         <Minute>0</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>21</EventTypeID>
#         <EventVariation>1</EventVariation>
#         <EventText>L'entrenador va seleccionar els següents jugadors: &lt;a href="/Club/Players/Player.aspx?playerId=389005502" title="Sala" class="homeplayer"&gt;Sala&lt;/a&gt; - &lt;a href="/Club/Players/Player.aspx?playerId=384131341" title="Omarini" class="homeplayer"&gt;Omarini&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=379629767" title="Mező" class="homeplayer"&gt;Mező&lt;/a&gt; - &lt;a href="/Club/Players/Player.aspx?playerId=380939148" title="Chaabo" class="homeplayer"&gt;Chaabo&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=388939943" title="Rezza" class="homeplayer"&gt;Rezza&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=381679648" title="Whitaker" class="homeplayer"&gt;Whitaker&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=386416781" title="Mochelato" class="homeplayer"&gt;Mochelato&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=373182450" title="Thomas" class="homeplayer"&gt;Thomas&lt;/a&gt; - &lt;a href="/Club/Players/Player.aspx?playerId=391954865" title="Pi&amp;#241;a" class="homeplayer"&gt;Piña&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=391014759" title="Moss" class="homeplayer"&gt;Moss&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=391880826" title="Da'na" class="homeplayer"&gt;Da'na&lt;/a&gt;.&lt;br /&gt;&lt;br /&gt;</EventText>
#       </Event>
#       <Event Index="3">
#         <Minute>0</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>21</EventTypeID>
#         <EventVariation>2</EventVariation>
#         <EventText>L'alineació inicial: &lt;a href="/Club/Players/Player.aspx?playerId=391701062" title="Astrup Hansen" class="awayplayer"&gt;Astrup Hansen&lt;/a&gt; - &lt;a href="/Club/Players/Player.aspx?playerId=399410204" title="Cappellato" class="awayplayer"&gt;Cappellato&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=393918577" title="Cazos" class="awayplayer"&gt;Cazos&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=397840985" title="Flenuţă" class="awayplayer"&gt;Flenuţă&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=391309285" title="Sepin" class="awayplayer"&gt;Sepin&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=388233817" title="Hamedani" class="awayplayer"&gt;Hamedani&lt;/a&gt; - &lt;a href="/Club/Players/Player.aspx?playerId=401091244" title="Ascher" class="awayplayer"&gt;Ascher&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=396995560" title="Gallart" class="awayplayer"&gt;Gallart&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=400955515" title="Pierrot" class="awayplayer"&gt;Pierrot&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=398938762" title="C&amp;#233;spedes" class="awayplayer"&gt;Céspedes&lt;/a&gt;, &lt;a href="/Club/Players/Player.aspx?playerId=394723751" title="Mengal" class="awayplayer"&gt;Mengal&lt;/a&gt; -.&lt;br /&gt;&lt;br /&gt;</EventText>
#       </Event>
#       <Event Index="4">
#         <Minute>0</Minute>
#         <SubjectPlayerID>1020503</SubjectPlayerID>
#         <SubjectTeamID>0</SubjectTeamID>
#         <ObjectPlayerID>1050500</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>24</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText>El &lt;span class="hometeam"&gt;V@der SC&lt;/span&gt; va entrar al camp i es va disposar en un 2-5-3. Els visitants, en canvi, van escollir un  5-5-0.</EventText>
#       </Event>
#       <Event Index="5">
#         <Minute>0</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>0</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>598</EventTypeID>
#         <EventVariation>1</EventVariation>
#         <EventText></EventText>
#       </Event>
#       <Event Index="6">
#         <Minute>0</Minute>
#         <SubjectPlayerID>290</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>336</EventTypeID>
#         <EventVariation>1</EventVariation>
#         <EventText>El &lt;span class="awayteam"&gt;Olimpic&lt;/span&gt; va preferir finalitzar les seves jugades des de la llarga distància.</EventText>
#       </Event>
#       <Event Index="10">
#         <Minute>30</Minute>
#         <SubjectPlayerID>388939943</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>391701062</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>123</EventTypeID>
#         <EventVariation>1</EventVariation>
#         <EventText>Corria el minut 30 quan els locals van prendre avantatge mitjançant un gol de &lt;a href="/Club/Players/Player.aspx?playerId=388939943" title="Gianfranco Rezza" class="homeplayer"&gt;Gianfranco Rezza&lt;/a&gt;, que va posar el 1 - 0 al marcador després d'una jugada d'equip per la banda dreta.</EventText>
#       </Event>
#       <Event Index="11">
#         <Minute>31</Minute>
#         <SubjectPlayerID>394723751</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>510</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText>Al minut 31, &lt;a href="/Club/Players/Player.aspx?playerId=394723751" title="Franck Mengal" class="awayplayer"&gt;Franck Mengal&lt;/a&gt; de &lt;span class="awayteam"&gt;Olimpic&lt;/span&gt; va rebre una targeta groga per una entrada molt lletja sense pilota.</EventText>
#       </Event>
#       <Event Index="12">
#         <Minute>38</Minute>
#         <SubjectPlayerID>51</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>471</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText></EventText>
#       </Event>
#       <Event Index="13">
#         <Minute>45</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>0</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>45</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText>1 - 0 era el resultat a la mitja part.</EventText>
#       </Event>
#       <Event Index="14">
#         <Minute>45</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>51</ObjectPlayerID>
#         <MatchPart>1</MatchPart>
#         <EventTypeID>40</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText>&lt;span class="hometeam"&gt;V@der&lt;/span&gt;, amb una possessió del 51 per cent, va dominar aquests 45 minuts.&lt;br /&gt;&lt;br /&gt;</EventText>
#       </Event>
#       <Event Index="15">
#         <Minute>46</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>0</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>597</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText></EventText>
#       </Event>
#       <Event Index="16">
#         <Minute>47</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>0</SubjectTeamID>
#         <ObjectPlayerID>45120</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>464</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText></EventText>
#       </Event>
#       <Event Index="17">
#         <Minute>50</Minute>
#         <SubjectPlayerID>391309285</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>360</EventTypeID>
#         <EventVariation>1</EventVariation>
#         <EventText>Al minut 50, els jugadors de &lt;span class="awayteam"&gt;Olimpic&lt;/span&gt; van rebre noves instruccions del seu entrenador que veia com res del que havien preparat durant la setmana sortia, aprofitant una petita aturada del partit.</EventText>
#       </Event>
#       <Event Index="18">
#         <Minute>54</Minute>
#         <SubjectPlayerID>401091244</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>394723751</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>116</EventTypeID>
#         <EventVariation>2</EventVariation>
#         <EventText>Un ràpid moviment de &lt;a href="/Club/Players/Player.aspx?playerId=394723751" title="Franck Mengal" class="awayplayer"&gt;Franck Mengal&lt;/a&gt; va acabar en una passada genial cap al jugador de &lt;span class="awayteam"&gt;Olimpic&lt;/span&gt; &lt;a href="/Club/Players/Player.aspx?playerId=401091244" title="Josef 'Del Bar' Ascher" class="awayplayer"&gt;Josef 'Del Bar' Ascher&lt;/a&gt;, que va marcar el 1 - 1.</EventText>
#       </Event>
#       <Event Index="20">
#         <Minute>67</Minute>
#         <SubjectPlayerID>400955515</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>389005502</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>287</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText>L'entrenador d'en &lt;a href="/Club/Players/Player.aspx?playerId=400955515" title="David 'Samy' Pierrot" class="awayplayer"&gt;David 'Samy' Pierrot&lt;/a&gt; ja els havia advertit que el porter contrari, en &lt;a href="/Club/Players/Player.aspx?playerId=389005502" title="Dami&amp;#225;n Sala" class="homeplayer"&gt;Damián Sala&lt;/a&gt;, acostumava a jugar molt avançat quan la pilota era a camp contrari. Així que quan va poder, va intentar un xut llunyà des del mig del camp que va marxar per sobre el travesser per ben poc.</EventText>
#       </Event>
#       <Event Index="21">
#         <Minute>70</Minute>
#         <SubjectPlayerID>389206860</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>70</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>459</EventTypeID>
#         <EventVariation>2</EventVariation>
#         <EventText></EventText>
#       </Event>
#       <Event Index="24">
#         <Minute>77</Minute>
#         <SubjectPlayerID>398938762</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>401091244</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>187</EventTypeID>
#         <EventVariation>2</EventVariation>
#         <EventText>Després de 77 minuts el &lt;span class="awayteam"&gt;Olimpic&lt;/span&gt;, amb una sèrie de passades al primer toc, va deixar a en &lt;a href="/Club/Players/Player.aspx?playerId=398938762" title="Edgar 'Baragua' C&amp;#233;spedes" class="awayplayer"&gt;Edgar 'Baragua' Céspedes&lt;/a&gt; sense cap marcador a prop, perfecte per poder xutar des de lluny. No s'ho va pensar dos cops, i la pilota va entrar ajustada al pal dret de la porteria. El 1 - 2 va pujar al marcador.</EventText>
#       </Event>
#       <Event Index="25">
#         <Minute>80</Minute>
#         <SubjectPlayerID>373182450</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>389206860</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>350</EventTypeID>
#         <EventVariation>1</EventVariation>
#         <EventText>Al minut 80, &lt;span class="hometeam"&gt;V@der&lt;/span&gt; va fer un canvi per intentar capgirar el marcador. &lt;a href="/Club/Players/Player.aspx?playerId=389206860" title="Cezary Pauch" class="homeplayer"&gt;Cezary Pauch&lt;/a&gt; va entrar al camp per substituir &lt;a href="/Club/Players/Player.aspx?playerId=373182450" title="Morgan Thomas" class="homeplayer"&gt;Morgan Thomas&lt;/a&gt;.</EventText>
#       </Event>
#       <Event Index="27">
#         <Minute>90</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>0</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>599</EventTypeID>
#         <EventVariation>1</EventVariation>
#         <EventText>Resultat final: 1 - 2.</EventText>
#       </Event>
#       <Event Index="28">
#         <Minute>90</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>601</EventTypeID>
#         <EventVariation>2</EventVariation>
#         <EventText></EventText>
#       </Event>
#       <Event Index="29">
#         <Minute>90</Minute>
#         <SubjectPlayerID>0</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>51</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>40</EventTypeID>
#         <EventVariation>2</EventVariation>
#         <EventText>&lt;span class="hometeam"&gt;V@der&lt;/span&gt; va controlar la pilota, amb un 51% de possessió.&lt;br /&gt;&lt;br /&gt;</EventText>
#       </Event>
#       <Event Index="30">
#         <Minute>90</Minute>
#         <SubjectPlayerID>391954865</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>41</EventTypeID>
#         <EventVariation>2</EventVariation>
#         <EventText>El jugador més determinant de &lt;span class="hometeam"&gt;V@der&lt;/span&gt; va ser sens dubte &lt;a href="/Club/Players/Player.aspx?playerId=391954865" title="Sa&amp;#250;l Pi&amp;#241;a" class="homeplayer"&gt;Saúl Piña&lt;/a&gt;.</EventText>
#       </Event>
#       <Event Index="31">
#         <Minute>90</Minute>
#         <SubjectPlayerID>389206860</SubjectPlayerID>
#         <SubjectTeamID>120994</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>42</EventTypeID>
#         <EventVariation>2</EventVariation>
#         <EventText>&lt;a href="/Club/Players/Player.aspx?playerId=389206860" title="Cezary Pauch" class="homeplayer"&gt;Cezary Pauch&lt;/a&gt;, en canvi, va destacar pel contrari, ja que va destorbar el joc dels companys amb els seus errors continuats.</EventText>
#       </Event>
#       <Event Index="32">
#         <Minute>90</Minute>
#         <SubjectPlayerID>391701062</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>41</EventTypeID>
#         <EventVariation>5</EventVariation>
#         <EventText>En &lt;a href="/Club/Players/Player.aspx?playerId=391701062" title="Thorleif 'El Sordo' Astrup Hansen" class="awayplayer"&gt;Thorleif 'El Sordo' Astrup Hansen&lt;/a&gt; va fer un partit admirable per a &lt;span class="awayteam"&gt;Olimpic&lt;/span&gt;.</EventText>
#       </Event>
#       <Event Index="33">
#         <Minute>90</Minute>
#         <SubjectPlayerID>394723751</SubjectPlayerID>
#         <SubjectTeamID>1593528</SubjectTeamID>
#         <ObjectPlayerID>0</ObjectPlayerID>
#         <MatchPart>2</MatchPart>
#         <EventTypeID>42</EventTypeID>
#         <EventVariation>3</EventVariation>
#         <EventText>Tanmateix, &lt;a href="/Club/Players/Player.aspx?playerId=394723751" title="Franck Mengal" class="awayplayer"&gt;Franck Mengal&lt;/a&gt; va fer baixar el nivell de l'equip.</EventText>
#       </Event>
#     </EventList>
#   </Match>
# </HattrickData>
# '''
#
# def recopilar_detail_partido(helper, user_key, user_secret, idpartido):
#
#     conn = sqlite3.connect('bigdata.sqlite')
#     cur = conn.cursor()
#
#     root = ET.fromstring(xmldoc)
#
#     for match in root.findall('Match'):
#         typetactichome = match.find('HomeTeam/TacticType').text
#         skilltactichome = match.find('HomeTeam/TacticSkill').text
#         typetacticaway = match.find('AwayTeam/TacticType').text
#         skilltacticaway = match.find('AwayTeam/TacticSkill').text
#         try:
#             test = match.find('Bookings/Booking/BookingPlayerID').text
#             tarjetas = 1
#         except:
#             tarjetas = 0
#         try:
#             test = match.find('Injuries/Injury/InjuryPlayerID').text
#             lesiones = 1
#         except:
#             lesiones = 0
#         homeFpos = match.find('PossessionFirstHalfHome').text
#         awayFpos = match.find('PossessionFirstHalfAway').text
#         homeSpos = match.find('PossessionSecondHalfHome').text
#         awaySpos = match.find('PossessionSecondHalfAway').text
#         ratIndDefhome = match.find('HomeTeam/RatingIndirectSetPiecesDef').text
#         ratIndAtthome = match.find('HomeTeam/RatingIndirectSetPiecesAtt').text
#         ratIndDefaway = match.find('AwayTeam/RatingIndirectSetPiecesDef').text
#         ratIndAttaway = match.find('AwayTeam/RatingIndirectSetPiecesAtt').text
#         cur.execute('''UPDATE partidos SET TacticTypeHome=?, TacticSkillHome=?, TacticTypeAway=?, TacticSkillAway=?,
#                     tarjetas=?, lesiones=?, PossessionFirstHalfHome=?, PossessionFirstHalfAway=?, PossessionSecondHalfHome=?,
#                     PossessionSecondHalfAway=?, RatingIndirectSetPiecesDefHome=?, RatingIndirectSetPiecesAttHome=?,
#                     RatingIndirectSetPiecesDefAway=?, RatingIndirectSetPiecesAttAway=? WHERE MatchID= ?''',
#                 (typetactichome, skilltactichome, typetacticaway, skilltacticaway, tarjetas, lesiones, homeFpos, awayFpos, homeSpos, awaySpos, ratIndDefhome, ratIndAtthome, ratIndDefaway, ratIndAttaway, idpartido))
#         conn.commit()
#
#     cur.execute('''
#                 CREATE TABLE IF NOT EXISTS eventos
#                 (MatchID INTEGER, IndexEv INTEGER, Minute INTEGER, EventTypeID INTEGER,
#                 SubjectTeamID INTEGER, SubjectPlayerID INTEGER, ObjectPlayerID INTEGER, SubPorteria INTEGER,
#                 SubDefensa INTEGER, SubJugadas INTEGER, SubLateral INTEGER, SubPases INTEGER,
#                 SubAnotacion INTEGER, SubXP INTEGER, SubFidelidad INTEGER, SubForma INTEGER,
#                 SubResistencia INTEGER, ObjPorteria INTEGER, ObjDefensa INTEGER,
#                 ObjJugadas INTEGER, ObjLateral INTEGER, ObjPases INTEGER,
#                 ObjAnotacion INTEGER, ObjXP INTEGER, ObjFidelidad INTEGER, ObjForma INTEGER, ObjResistencia INTEGER,
#                 UNIQUE(MatchID, IndexEv))
#                 ''')
#
#     for event in root.findall('Match/EventList/Event'):
#         indexevent = event.get("Index")
#         minute = event.find('Minute').text
#         idtypeevent = event.find('EventTypeID').text
#         subteam = event.find('SubjectTeamID').text
#         subplayer = event.find('SubjectPlayerID').text
#         objplayer = event.find('ObjectPlayerID').text
#         cur.execute('''INSERT INTO eventos (MatchID, IndexEv, Minute, EventTypeID, SubjectTeamID, SubjectPlayerID, ObjectPlayerID)
#                     VALUES (?, ?, ?, ?, ?, ?, ?)''', (idpartido, indexevent, minute, idtypeevent, subteam, subplayer, objplayer))
#         conn.commit()
#
#     cur.close()
#
# recopilar_detail_partido('helper', 'key', 'secret', 611097589)





# conn = sqlite3.connect('bigdata.sqlite')
# cur = conn.cursor()
#
# cur.execute( 'SELECT max(MatchDate) FROM partidos')
# fechamax = cur.fetchone()[0]
# print(fechamax)
#
# cur.execute( 'SELECT min(MatchDate) FROM partidos')
# fechamin = cur.fetchone()[0]
# print(fechamin)
#
# cur.close()



# fechalimite = datetime.today()
# dias28 = timedelta(days=15)
# fecha28 = fechalimite - dias28
# f2 = datetime.__str__(fecha28)
# print(fechalimite)
# print(fecha28)
# print(f2)
# print(type(fechalimite))
# print(type(fecha28))
# print(type(f2))


# xmldoc = '''
# <HattrickData>
#   <FileName>matchesArchive.xml</FileName>
#   <Version>1.3</Version>
#   <UserID>10150426</UserID>
#   <FetchedDate>2017-10-14 13:15:43</FetchedDate>
#   <IsYouth>False</IsYouth>
#   <Team>
#     <TeamID>120994</TeamID>
#     <TeamName>V@der SC</TeamName>
#     <MatchList>
#       <Match>
#         <MatchID>614891855</MatchID>
#         <HomeTeam>
#           <HomeTeamID>488289</HomeTeamID>
#           <HomeTeamName>Hueber</HomeTeamName>
#         </HomeTeam>
#         <AwayTeam>
#           <AwayTeamID>120994</AwayTeamID>
#           <AwayTeamName>V@der SC</AwayTeamName>
#         </AwayTeam>
#         <MatchDate>2017-09-27 12:00:00</MatchDate>
#         <MatchType>3</MatchType>
#         <MatchContextId>43</MatchContextId>
#         <CupLevel>1</CupLevel>
#         <CupLevelIndex>1</CupLevelIndex>
#         <HomeGoals>1</HomeGoals>
#         <AwayGoals>3</AwayGoals>
#       </Match>
#       <Match>
#         <MatchID>611097580</MatchID>
#         <HomeTeam>
#           <HomeTeamID>120994</HomeTeamID>
#           <HomeTeamName>V@der SC</HomeTeamName>
#         </HomeTeam>
#         <AwayTeam>
#           <AwayTeamID>125815</AwayTeamID>
#           <AwayTeamName>rayitus vallekanus</AwayTeamName>
#         </AwayTeam>
#         <MatchDate>2017-09-30 14:00:00</MatchDate>
#         <MatchType>1</MatchType>
#         <MatchContextId>3419</MatchContextId>
#         <CupLevel>0</CupLevel>
#         <CupLevelIndex>0</CupLevelIndex>
#         <HomeGoals>2</HomeGoals>
#         <AwayGoals>2</AwayGoals>
#       </Match>
#       <Match>
#         <MatchID>614992822</MatchID>
#         <HomeTeam>
#           <HomeTeamID>123771</HomeTeamID>
#           <HomeTeamName>sapa2408</HomeTeamName>
#         </HomeTeam>
#         <AwayTeam>
#           <AwayTeamID>120994</AwayTeamID>
#           <AwayTeamName>V@der SC</AwayTeamName>
#         </AwayTeam>
#         <MatchDate>2017-10-04 12:00:00</MatchDate>
#         <MatchType>3</MatchType>
#         <MatchContextId>43</MatchContextId>
#         <CupLevel>1</CupLevel>
#         <CupLevelIndex>1</CupLevelIndex>
#         <HomeGoals>0</HomeGoals>
#         <AwayGoals>5</AwayGoals>
#       </Match>
#       <Match>
#         <MatchID>611097585</MatchID>
#         <HomeTeam>
#           <HomeTeamID>990843</HomeTeamID>
#           <HomeTeamName>PACKARD</HomeTeamName>
#         </HomeTeam>
#         <AwayTeam>
#           <AwayTeamID>120994</AwayTeamID>
#           <AwayTeamName>V@der SC</AwayTeamName>
#         </AwayTeam>
#         <MatchDate>2017-10-07 14:00:00</MatchDate>
#         <MatchType>1</MatchType>
#         <MatchContextId>3419</MatchContextId>
#         <CupLevel>0</CupLevel>
#         <CupLevelIndex>0</CupLevelIndex>
#         <HomeGoals>1</HomeGoals>
#         <AwayGoals>1</AwayGoals>
#       </Match>
#       <Match>
#         <MatchID>615085410</MatchID>
#         <HomeTeam>
#           <HomeTeamID>796332</HomeTeamID>
#           <HomeTeamName>Los Peques Campeones</HomeTeamName>
#         </HomeTeam>
#         <AwayTeam>
#           <AwayTeamID>120994</AwayTeamID>
#           <AwayTeamName>V@der SC</AwayTeamName>
#         </AwayTeam>
#         <MatchDate>2017-10-11 12:00:00</MatchDate>
#         <MatchType>3</MatchType>
#         <MatchContextId>43</MatchContextId>
#         <CupLevel>1</CupLevel>
#         <CupLevelIndex>1</CupLevelIndex>
#         <HomeGoals>4</HomeGoals>
#         <AwayGoals>2</AwayGoals>
#       </Match>
#     </MatchList>
#   </Team>
# </HattrickData>'''
#
# conn = sqlite3.connect('bigdata.sqlite')
# cur = conn.cursor()
#
# cur.execute('''
#             CREATE TABLE IF NOT EXISTS partidos
#             (MatchID INTEGER PRIMARY KEY, MatchType INTEGER, MatchDate TEXT, HomeTeamID INTEGER,
#             HomeGoals INTEGER, AwayTeamID INTEGER, AwayGoals INTEGER, TacticTypeHome INTEGER,
#             TacticSkillHome INTEGER, TacticTypeAway INTEGER, TacticSkillAway INTEGER, tarjetas INTEGER
#             lesiones INTEGER, SUS_Home INTEGER, SUS_Away INTEGER, PossessionFirstHalfHome INTEGER,
#             PossessionFirstHalfAway INTEGER, PossessionSecondHalfHome INTEGER, PossessionSecondHalfAway INTEGER,
#             RatingIndirectSetPiecesDefHome INTEGER, RatingIndirectSetPiecesAttHome INTEGER, RatingIndirectSetPiecesDefAway INTEGER,
#             RatingIndirectSetPiecesAttAway INTEGER)
#             ''')
#
# root = ET.fromstring(xmldoc)
# for match in root.findall('Team/MatchList/Match'):
#     idmatch = match.find('MatchID').text
#     typematch = match.find('MatchType').text
#     datematch = match.find('MatchDate').text
#     goalshome = match.find('HomeGoals').text
#     goalsaway = match.find('AwayGoals').text
#     teamidHome= match.find('HomeTeam/HomeTeamID').text
#     teamidAway = match.find('AwayTeam/AwayTeamID').text
#     cur.execute('INSERT INTO partidos (MatchID, MatchType, MatchDate, HomeTeamID, HomeGoals, AwayTeamID, AwayGoals) VALUES (?, ?, ?, ?, ?, ?, ?)',
#     (idmatch, typematch, datematch, teamidHome, goalshome, teamidAway, goalsaway))
#
# conn.commit()
# cur.close()
