En este documento se define la estructura de datos de la base de datos (bbdd) de la aplicacion.
Se lista la lista de tablas y la lista de los campos de cada una de ellas.

# LISTA DE TABLAS
- partidos
- jugadores
- eventos
- alineacion
- sustituciones

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
- tarjetas #valor '1'= si y valor '0'=no
- lesiones #valor '1'= si y valor '0'=no
- SUS_Home #valor '1'= si y valor '0'=no
- SUS_Away #valor '1'= si y valor '0'=no
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

## Tabla "eventos" (matchdetails.xml)
- [KEY] MatchID
- [KEY] Index
- Minute
- EventTypeID
- SubjectTeamID
- SubjectPlayerID
- ObjectPlayerID
- SubPorteria
- SubDefensa
- SubJugadas
- SubLateral
- SubPases
- SubAnotacion
- SubXP
- SubFidelidad
- SubForma
- SubResistencia
- ObjPorteria
- ObjDefensa
- ObjJugadas
- ObjLateral
- ObjPases
- ObjAnotacion
- ObjXP
- ObjFidelidad
- ObjForma
- ObjResistencia

## Tabla "alineacion" (matchlineaup.xml)
- [KEY] MatchID
- TeamIDHome
- TeamIDAway
- POR_Home #Contiene el valor del PlayerID con RoleID = 100 de la alineacion. Sino hay jugadores en la posicion toma el valor "0"
- DLD_Home #RoleID = 101
- DCD_Home #RoleID = 102
- DCC_Home #RoleID = 103
- DCI_Home #RoleID = 104
- DLI_Home #RoleID = 105
- ED_Home #RoleID = 106
- ID_Home #RoleID = 107
- IC_Home #RoleID = 108
- II_Home #RoleID = 109
- EI_Home #RoleID = 110
- FD_Home #RoleID = 111 #F de delantero en ingles forward para diferenciar con defensa(D)
- FC_Home #RoleID = 112
- FI_Home #RoleID = 113
- Capitan_Home #RoleID = 17
- Bepero_Home #RoleID = 18
- POR_Away #RoleID = 100
- DLD_Away #RoleID = 101
- DCD_Away #RoleID = 102
- DCC_Away #RoleID = 103
- DCI_Away #RoleID = 104
- DLI_Away #RoleID = 105
- ED_Away #RoleID = 106
- ID_Away #RoleID = 107
- IC_Away #RoleID = 108
- II_Away #RoleID = 109
- EI_Away #RoleID = 110
- FD_Away #RoleID = 111
- FC_Away #RoleID = 112
- FI_Away #RoleID = 113
- Capitan_Away #RoleID = 17
- Bepero_Away #RoleID = 18

## Tabla "Sustituciones" (matchdetails.xml)
- [KEY] MatchID
- SubjectPlayerID_S1_Home #Sino hay Sustituciones toma el valor "0"
- ObjectPlayerID_S1_Home
- MatchMinute_S1_Home
- NewPositionId_S1_Home
- SubjectPlayerID_S2_Home
- ObjectPlayerID_S2_Home
- MatchMinute_S2_Home
- NewPositionId_S2_Home
- SubjectPlayerID_S3_Home
- ObjectPlayerID_S3_Home
- MatchMinute_S3_Home
- NewPositionId_S3_Home
- SubjectPlayerID_S1_Away
- ObjectPlayerID_S1_Away
- MatchMinute_S1_Away
- NewPositionId_S1_Away
- SubjectPlayerID_S2_Away
- ObjectPlayerID_S2_Away
- MatchMinute_S2_Away
- NewPositionId_S2_Away
- SubjectPlayerID_S3_Away
- ObjectPlayerID_S3_Away
- MatchMinute_S3_Away
- NewPositionId_S3_Away
