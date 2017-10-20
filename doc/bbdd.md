En este documento se define la estructura de datos de la base de datos (bbdd) de la aplicacion.
Se lista la lista de tablas y la lista de los campos de cada una de ellas.

# LISTA DE TABLAS
- info
- partidos
- jugadores
- eventos
- alineacion
- sustituciones

## Tabla info
- [KEY] id (Valor 1 = user, 2 = PrimerEquipo, 3 = SegundoEquipo, 4 = TercerEquipo, etc..)
- type (user/team)
- descripcion

## Tabla "partidos" (matchsarchive.xml para lista de partidos y matchdetails.xml para detalles)
- [KEY] MatchID
- MatchType
- MatchDate (string con datetime.__str__())
- HomeTeamID
- HomeGoals
- AwayTeamID
- AwayGoals
- TacticTypeHome
- TacticSkillHome
- TacticTypeAway
- TacticSkillAway
- expulsiones #valor '1'= si y valor '0'=no
- lesiones #valor '1'= si y valor '0'=no
- PossessionFirstHalfHome
- PossessionFirstHalfAway
- PossessionSecondHalfHome
- PossessionSecondHalfAway
- RatingIndirectSetPiecesDefHome
- RatingIndirectSetPiecesAttHome
- RatingIndirectSetPiecesDefAway
- RatingIndirectSetPiecesAttAway

## Tabla "jugadores" (playerdetails.xml)
- [KEY] PlayerID
- Agreeability
- Aggressiveness
- Honesty
- Leadership
- Specialty

## Tabla tarjetas (matchdetails.xml)
- [KEY] MatchID
- [KEY] IndexTarjeta
- PlayerID
- TeamID
- BookingType
- BookingMinute

## Tabla lesiones (matchdetails.xml)
- [KEY] MatchID
- [KEY] IndexInjury
- PlayerID
- TeamID
- InjuryType
- InjuryMinute

## Tabla "eventos" (matchdetails.xml)
- [KEY] MatchID
- [KEY] IndexEv
- Minute
- EventTypeID
- SubjectTeamID
- SubjectPlayerID
- ObjectPlayerID
- SubPorteria (habilidades de playerdetails.xml)
- SubDefensa
- SubJugadas
- SubLateral
- SubPases
- SubAnotacion
- SubBP
- SubXP
- SubForma
- SubResistencia
- SubSpecialty
- SubLoyalty
- SubMotherClubBonus
- ObjPorteria
- ObjDefensa
- ObjJugadas
- ObjLateral
- ObjPases
- ObjAnotacion
- ObjBP
- ObjXP
- ObjForma
- ObjResistencia
- ObjSpecialty
- ObjLoyalty
- ObjMotherClubBonus

## Tabla "alineacion" (matchlineaup.xml)
- [KEY] MatchID
- [KEY] RoleTeam (Home/Away) (valores 1/2 respectivamente)
- [KEY] RoleID
- PlayerID

Info RoleID:
    POR_ #Contiene el valor del PlayerID con RoleID = 100 de la alineacion. Sino hay jugadores en la posicion toma el valor "0"
    DLD_ #RoleID = 101
    DCD_ #RoleID = 102
    DCC_ #RoleID = 103
    DCI_ #RoleID = 104
    DLI_ #RoleID = 105
    ED_ #RoleID = 106
    ID_ #RoleID = 107
    IC_ #RoleID = 108
    II_ #RoleID = 109
    EI_ #RoleID = 110
    FD_ #RoleID = 111 #F de delantero en ingles forward para diferenciar con defensa(D)
    FC_ #RoleID = 112
    FI_ #RoleID = 113
    Capitan_ #RoleID = 17
    Bepero_ #RoleID = 18

## Tabla "Sustituciones" (matchlineaup.xml)
- [KEY] MatchID
- [KEY] TeamID
- [KEY] SubjectPlayerID
- ObjectPlayerID
- MatchMinute
- NewPositionId
