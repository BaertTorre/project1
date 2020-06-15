from .Database import Database

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def make_time_event(error_id):
        sql = f"INSERT INTO `time` (`error codes_id error code`) VALUES ({error_id});"
        return Database.execute_sql(sql)

    @staticmethod
    def add_ultrasone_waarde(ultrasone_data_rechts, ultrasone_data_links, id_time):
        sql = f"INSERT INTO `ultrasonic data` (`ultrasonic data rechts`,`ultrasonic data links`,`time_id time`) VALUES ({ultrasone_data_rechts},{ultrasone_data_links},{id_time});"
        return Database.execute_sql(sql)

    @staticmethod
    def add_ldr_waarde(ldr_value, id_time):
        sql = f"INSERT INTO `LDR data` (`LDR data`, `time_id time`) VALUES ({ldr_value},{id_time});"
        return Database.execute_sql(sql)

    @staticmethod
    def add_led_waarde(led_value, id_time):
        sql = f"INSERT INTO `LED data` (`led aan uit`, `time_id time`) VALUES ({led_value},{id_time});"
        return Database.execute_sql(sql)

    @staticmethod
    def add_gps_data(coordinaat_lengte, coordinaat_breedte, speed, id_time):
        sql = f"INSERT INTO `GPS data` (`coordinaat lengte`, `coordinaat breedte`, `speed`,`time_id time`) VALUES ({coordinaat_lengte},{coordinaat_breedte},{speed},{id_time});"
        return Database.execute_sql(sql)

    @staticmethod
    def give_last_gps_rows(rows):
        sql = f"SELECT GPS.`coordinaat lengte`, GPS.`coordinaat breedte`, GPS.speed, T.`time stamp` FROM `GPS data` as GPS INNER JOIN time as T ON GPS.`time_id time` = T.`id time` order by T.`time stamp` desc limit {rows};"
        return Database.get_rows(sql)