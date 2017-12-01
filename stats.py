
from datetime import datetime, timedelta
import sqlite3
from colorama import init, Fore, Back, Style

init(autoreset=True)

#Iniciamos base de datos de SE-Bigdata
basedatos = 'bigdata.sqlite'

# Buscamos si la App tiene la autorizacion CHPP del usuario
conn = sqlite3.connect(basedatos)
cur = conn.cursor()

# Ev. ID=15: Rápido + Anotación - Extremos y Delanteros
cur.execute('SELECT count(MatchID) as Partidos_e15 from (select distinct MatchID from alineacion_all where Specialty = 2 and (Pos = 106 or Pos > 109))')
Partidos_e15 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from alineacion_all where Specialty = 2 and (Pos = 106 or Pos > 109)) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e15 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 115')
Gols15 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 215')
Fallos15 = cur.fetchone()[0]

if Partidos_e15 == 0:
    App = 0.0
else:
    App = ((Gols15+Fallos15) / (Partidos_e15*Jug_partido_e15)) * 100
if Gols15+Fallos15 == 0:
    Con = 0.0
else:
    Con = ((Gols15) / (Gols15+Fallos15)) * 100

print(Fore.CYAN + Style.BRIGHT + '\nEv ID=15: Rápido + Anotación - Extremos y Delanteros')
print(Fore.CYAN +str(Partidos_e15), 'partidos, con una media de',Fore.CYAN + str("%.3f" % Jug_partido_e15),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.CYAN + str(Gols15+Fallos15),'eventos. Con', Fore.CYAN + str(Gols15),'goles.')
print('Es decir un',Fore.CYAN + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.CYAN + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=16: Rápido + Pase - Extremos y Delanteros
cur.execute('SELECT count(MatchID) as Partidos_e16 from (select distinct MatchID from alineacion_all where Specialty = 2 and (Pos = 106 or Pos > 109))')
Partidos_e16 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from alineacion_all where Specialty = 2 and (Pos = 106 or Pos > 109)) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e16 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 116')
Gols16 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 216')
Fallos16 = cur.fetchone()[0]

if Partidos_e16 == 0:
    App = 0.0
else:
    App = ((Gols16+Fallos16) / (Partidos_e16*Jug_partido_e16)) * 100
if Gols16+Fallos16 == 0:
    Con = 0.0
else:
    Con = ((Gols16) / (Gols16+Fallos16)) * 100

print(Fore.CYAN + Style.BRIGHT + '\nEv ID=16: Rápido + Pase - Extremos y Delanteros')
print(Fore.CYAN +str(Partidos_e16), 'partidos, con una media de',Fore.CYAN + str("%.3f" % Jug_partido_e16),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.CYAN + str(Gols16+Fallos16),'eventos. Con', Fore.CYAN + str(Gols16),'goles.')
print('Es decir un',Fore.CYAN + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.CYAN + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=05: Imprevisible PaseLargo - Todos
cur.execute('SELECT count(MatchID) as Partidos_e05 from (select distinct MatchID from alineacion_all where Specialty = 4 and Pos > 99)')
Partidos_e05 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from alineacion_all where Specialty = 4 and Pos > 99) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e05 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 105')
Gols05 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 205')
Fallos05 = cur.fetchone()[0]

if Partidos_e05 == 0:
    App = 0.0
else:
    App = ((Gols05+Fallos05) / (Partidos_e05*Jug_partido_e05)) * 100
if Gols05+Fallos05 == 0:
    Con = 0.0
else:
    Con = ((Gols05) / (Gols05+Fallos05)) * 100

print(Fore.RED + Style.BRIGHT + '\nEv. ID=05: Imprevisible PaseLargo - Todos')
print(Fore.RED +str(Partidos_e05), 'partidos, con una media de',Fore.RED + str("%.3f" % Jug_partido_e05),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.RED + str(Gols05+Fallos05),'eventos. Con', Fore.RED + str(Gols05),'goles.')
print('Es decir un',Fore.RED + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.RED + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=06: Imprevisible Anotacion - Extremos y delanteros
cur.execute('SELECT count(MatchID) as Partidos_e06 from (select distinct MatchID from alineacion_all where Specialty = 4 and (Pos = 106 or Pos > 109))')
Partidos_e06 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from alineacion_all where Specialty = 4 and (Pos = 106 or Pos > 109)) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e06 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 106')
Gols06 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 206')
Fallos06 = cur.fetchone()[0]

if Partidos_e06 == 0:
    App = 0.0
else:
    App = ((Gols06+Fallos06) / (Partidos_e06*Jug_partido_e06)) * 100
if Gols06+Fallos06 == 0:
    Con = 0.0
else:
    Con = ((Gols06) / (Gols06+Fallos06)) * 100

print(Fore.RED + Style.BRIGHT + '\nEv. ID=06: Imprevisible Anotacion - Extremos y delanteros')
print(Fore.RED +str(Partidos_e06), 'partidos, con una media de',Fore.RED + str("%.3f" % Jug_partido_e06),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.RED + str(Gols06+Fallos06),'eventos. Con', Fore.RED + str(Gols06),'goles.')
print('Es decir un',Fore.RED + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.RED + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=08: Imprevisible - Todos menos el portero
cur.execute('SELECT count(MatchID) as Partidos_e08 from (select distinct MatchID from alineacion_all where Specialty = 4 and Pos > 100)')
Partidos_e08 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from alineacion_all where Specialty = 4 and Pos > 100) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e08 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 108')
Gols08 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 208')
Fallos08 = cur.fetchone()[0]

if Partidos_e08 == 0:
    App = 0.0
else:
    App = ((Gols08+Fallos08) / (Partidos_e08*Jug_partido_e08)) * 100
if Gols08+Fallos08 == 0:
    Con = 0.0
else:
    Con = ((Gols08) / (Gols08+Fallos08)) * 100

print(Fore.RED + Style.BRIGHT + '\nEv. ID=08: Imprevisible - Todos menos el portero')
print(Fore.RED +str(Partidos_e08), 'partidos, con una media de',Fore.RED + str("%.3f" % Jug_partido_e08),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.RED + str(Gols08+Fallos08),'eventos. Con', Fore.RED + str(Gols08),'goles.')
print('Es decir un',Fore.RED + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.RED + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=39: Tecnicos - Extremos y delanteros
cur.execute('SELECT count(MatchID) as Partidos_e39 from (select distinct MatchID from alineacion_all_contrarios where (Pos = 106 or Pos > 109) and Specialty = 1 and "Specialty:1" = 5)')
Partidos_e39 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from alineacion_all_contrarios where (Pos = 106 or Pos > 109) and Specialty = 1 and "Specialty:1" = 5) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e39 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 139')
Gols39 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 239')
Fallos39 = cur.fetchone()[0]

if Partidos_e39 == 0:
    App = 0.0
else:
    App = ((Gols39+Fallos39) / (Partidos_e39*Jug_partido_e39)) * 100
if Gols39+Fallos39 == 0:
    Con = 0.0
else:
    Con = ((Gols39) / (Gols39+Fallos39)) * 100

print(Fore.GREEN + Style.BRIGHT + '\nEv. ID=39: Tecnicos - Extremos y delanteros')
print(Fore.GREEN +str(Partidos_e39), 'partidos, con una media de',Fore.GREEN + str("%.3f" % Jug_partido_e39),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.GREEN + str(Gols39+Fallos39),'eventos. Con', Fore.GREEN + str(Gols39),'goles.')
print('Es decir un',Fore.GREEN + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.GREEN + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=37: Lateral + Anotacion - Extremos
cur.execute('SELECT count(MatchID) as Partidos_e37 from (select distinct MatchID from alineacion_all where (Pos = 106 or Pos = 110))')
Partidos_e37 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from alineacion_all where (Pos = 106 or Pos = 110)) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e37 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 137')
Gols37 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 237')
Fallos37 = cur.fetchone()[0]

if Partidos_e37 == 0:
    App = 0.0
else:
    App = ((Gols37+Fallos37) / (Partidos_e37*Jug_partido_e37)) * 100
if Gols37+Fallos37 == 0:
    Con = 0.0
else:
    Con = ((Gols37) / (Gols37+Fallos37)) * 100

print(Fore.WHITE + Style.BRIGHT + '\nEv. ID=37: Lateral + Anotacion - Extremos')
print(Fore.WHITE +str(Partidos_e37), 'partidos, con una media de',Fore.WHITE + str("%.3f" % Jug_partido_e37),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.WHITE + str(Gols37+Fallos37),'eventos. Con', Fore.WHITE + str(Gols37),'goles.')
print('Es decir un',Fore.WHITE + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.WHITE + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=38: Lateral + Cabezón - Extremos
cur.execute('SELECT count(MatchID) as Partidos_e38 from (select distinct MatchID from alineacion_all where (Pos = 106 or Pos = 110))')
Partidos_e38 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from alineacion_all where (Pos = 106 or Pos = 110)) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e38 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 138')
Gols38 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 238')
Fallos38 = cur.fetchone()[0]

if Partidos_e38 == 0:
    App = 0.0
else:
    App = ((Gols38+Fallos38) / (Partidos_e38*Jug_partido_e38)) * 100
if Gols38+Fallos38 == 0:
    Con = 0.0
else:
    Con = ((Gols38) / (Gols38+Fallos38)) * 100

print(Fore.WHITE + Style.BRIGHT + '\nEv. ID=38: Lateral + Cabezon - Extremos')
print(Fore.WHITE +str(Partidos_e38), 'partidos, con una media de',Fore.WHITE + str("%.3f" % Jug_partido_e38),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.WHITE + str(Gols38+Fallos38),'eventos. Con', Fore.WHITE + str(Gols38),'goles.')
print('Es decir un',Fore.WHITE + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.WHITE + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=18: Corner + Anotacion
cur.execute('SELECT count(MatchID) as Partidos_e18 from (select distinct MatchID from alineacion_all)')
Partidos_e18 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 118')
Gols18 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 218')
Fallos18 = cur.fetchone()[0]

if Partidos_e18 == 0:
    App = 0.0
else:
    App = ((Gols18+Fallos18) / (Partidos_e18)) * 100
if Gols18+Fallos18 == 0:
    Con = 0.0
else:
    Con = ((Gols18) / (Gols18+Fallos18)) * 100

print(Fore.YELLOW + Style.BRIGHT + '\nEv. ID=18: Corner + Anotacion')
print(Fore.YELLOW +str(Partidos_e18), 'partidos')
print('Un total de',Fore.YELLOW + str(Gols18+Fallos18),'eventos. Con', Fore.YELLOW + str(Gols18),'goles.')
print('Es decir un',Fore.YELLOW + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.YELLOW + str("%.3f" % Con),'% de conversion global.\n')

# Ev. ID=19: Corner + Cabezon
cur.execute('SELECT count(MatchID) as Partidos_e19 from (select distinct MatchID from (select a.MatchID, a.RoleTeam, a.Pos, a.Player, a.Specialty, a.Minutos from alineacion_all as a left join (select * from alineacion_all where Pos = 18) as b ON a.MatchID=b.MatchID and a.Player=b.Player where b.Pos is null) where Specialty = 5)')
Partidos_e19 = cur.fetchone()[0]
cur.execute('''
            SELECT sum(NumPlayersPond)/count(MatchID)
            from (select a.MatchID,a.RoleTeam,a.NumPlayers,b.MediaHome,b.MediaAway, case when a.RoleTeam = 1 then a.NumPlayers*b.MediaHome/50.0 when a.RoleTeam = 2 then a.NumPlayers*b.MediaAway/50.0 end as NumPlayersPond
            from(select MatchID,RoleTeam,sum(Minutos) as TotalMinutos, sum(Minutos)/90.0 as NumPlayers from (select * from (select a.MatchID, a.RoleTeam, a.Pos, a.Player, a.Specialty, a.Minutos from alineacion_all as a left join (select * from alineacion_all where Pos = 18) as b ON a.MatchID=b.MatchID and a.Player=b.Player where b.Pos is null) where Specialty = 5) group by MatchID,RoleTeam) as a
            left join (select MatchID, (PossessionFirstHalfHome + PossessionSecondHalfHome)/2.0 as MediaHome, (PossessionFirstHalfAway + PossessionSecondHalfAway)/2.0 as MediaAway from partidos) as b ON a.MatchID=b.MatchID)
            ''')
Jug_partido_e19 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 119')
Gols19 = cur.fetchone()[0]
cur.execute('SELECT count(EventTypeID) from eventos where EventTypeID = 219')
Fallos19 = cur.fetchone()[0]

if Partidos_e19 == 0:
    App = 0.0
else:
    App = ((Gols19+Fallos19) / (Partidos_e19*Jug_partido_e19)) * 100
if Gols19+Fallos19 == 0:
    Con = 0.0
else:
    Con = ((Gols19) / (Gols19+Fallos19)) * 100

print(Fore.YELLOW + Style.BRIGHT + '\nEv. ID=19: Corner + Cabezon')
print(Fore.YELLOW +str(Partidos_e19), 'partidos, con una media de',Fore.YELLOW + str("%.3f" % Jug_partido_e19),'jugadores ponderados por possesión y 90min de juego.')
print('Un total de',Fore.YELLOW + str(Gols19+Fallos19),'eventos. Con', Fore.YELLOW + str(Gols19),'goles.')
print('Es decir un',Fore.YELLOW + str("%.3f" % App),'% de aparicion por jugador con 90min y un',Fore.YELLOW + str("%.3f" % Con),'% de conversion global.\n')




cur.close()
