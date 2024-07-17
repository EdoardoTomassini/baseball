from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(year)
                        from teams a
                        where year > 1979
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from teams a
                    where year = %s
                """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryOfTeamOfYear(year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select t.teamCode, t.ID, sum(tb.salary) as totSalary
                    from(
                    SELECT a.playerID , a.teamID, s.salary 
                    FROM appearances a , salaries s
                    where a.playerID = s.playerID 
                    and a.`year` = s.`year`
                    and s.`year` = %s
                    ) as tb, teams t
                    where tb.teamID = t.ID 
                    GROUP by teamID
                """

        cursor.execute(query, (year,))

        # FACCIAMO UN DIZIONARIO
        result = {}

        for row in cursor:
            result[idMap[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return result
