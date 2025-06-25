from collections import defaultdict

from database.DB_connect import DBConnect


class DAO():

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select  distinct s.`year` from seasons s """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRacesofYear(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select r.raceId as rId
                        from races r 
                        where year=%s """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(row["rId"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(raceId1, raceId2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select res.raceId , res.raceId , count(*) as Peso
            from results res, results res2
            where res.raceId = %s
            and res2.raceId = %s
            and res2.driverId =res.driverId
            and res.statusId=1 and res2.statusId=1  """

        race1, race2 = sorted([raceId1, raceId2])
        cursor.execute(query, (race1, race2))

        for row in cursor:
            result.append(row["Peso"])

        cursor.close()
        conn.close()
        return result


    #non usato
    @staticmethod
    def getNumMaxGiriRace(raceId1):
        conn = DBConnect.get_connection()

        result = -999999
        cursor = conn.cursor(dictionary=True)
        query = """SELECT max(`position`) as Mp
                    FROM laptimes l 
                    where raceId = %s"""

        cursor.execute(query, (raceId1,))

        for row in cursor:
            result = row["Mp"]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPilotiRace(raceId1):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct driverId as driverId
                FROM formula1.laptimes l 
                where raceId = 900 """

        cursor.execute(query, (raceId1,))

        for row in cursor:
            result.append(row["driverId"])

        cursor.close()
        conn.close()
        return result

    #usato
    @staticmethod
    def getDatiRace(raceId1):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT driverId, lap, milliseconds
            FROM laptimes
            WHERE raceId = %s
            ORDER BY lap ASC
        """

        cursor.execute(query, (raceId1,))
        rows = cursor.fetchall()

        tempi = defaultdict(dict) # È un dizionario (dict) che per ogni driverId contiene un altro dizionario.

        piloti = set()
        numero_giri = 0

        for row in rows:
            driverId = row['driverId']
            lap = row['lap']
            milliseconds = row['milliseconds']

            tempi[driverId][lap] = milliseconds
            piloti.add(driverId)
            numero_giri = max(numero_giri, lap)

        cursor.close()
        conn.close()

        # Restituisci i dati utili per la simulazione
        return tempi, piloti, numero_giri
