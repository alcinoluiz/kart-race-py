import unittest
import log


class TestLogMethods(unittest.TestCase):

    def test_get_list_from_file(self):
        self.assertIsNotNone(log.get_list_from_file(
            'corridas.log'), 'Arquivo não existe.')

    def test_parse_to_list(self):
        line = '23:49:08.277      038 – F.MASSA                           1		1:02.852                        44,275'
        self.assertEqual(log.parse_to_list(line), [
                         '23:49:08.277', '038 – F.MASSA', '1', '1:02.852', '44,275'])

    def test_file_to_list(self):
        log_file = log.read_file('corridas.log')
        self.assertEqual(type(log.file_to_list(log_file)), type(list()))
        log_file.close()

    def test_clean_log(self):
        list_lap = [['Hora', 'Piloto', 'Nº Volta', 'Tempo Volta', 'Velocidade média da volta\n'], [
            '23:49:08.277', '038 – F.MASSA', '1', '1:02.852', '44,275\n']]
        self.assertEqual(log.clean_log(list_lap), [
                         ['23:49:08.277', '038 – F.MASSA', '1', '1:02.852', '44,275']])

    def test_sort_lap_time(self):
        laps_list = [['23:49:11.075', '002 – K.RAIKKONEN', '1', '1:04.108', '43,408'], [
            '23:49:08.277', '038 – F.MASSA', '1', '1:02.852', '44,275'], ['23:49:10.858', '033 – R.BARRICHELLO', '1', '1:04.352', '43,243']]

        self.assertEqual(log.sort_lap_time(laps_list), [['23:49:08.277', '038 – F.MASSA', '1', '1:02.852', '44,275'],  [
                         '23:49:11.075', '002 – K.RAIKKONEN', '1', '1:04.108', '43,408'], ['23:49:10.858', '033 – R.BARRICHELLO', '1', '1:04.352', '43,243']])

    def test_sort_ranking(self):
        laps_list = [['23:49:11.075', '002 – K.RAIKKONEN', '2', '1:04.108', '43,408'], ['23:49:08.277', '038 – F.MASSA',                                                                               '1', '1:02.852', '44,275'], ['23:49:10.858', '033 – R.BARRICHELLO', '2', '1:04.352', '43,243']]

        self.assertEqual(log.sort_lap_time(laps_list), [['23:49:08.277', '038 – F.MASSA', '1', '1:02.852', '44,275'],  [
                         '23:49:11.075', '002 – K.RAIKKONEN', '2', '1:04.108', '43,408'], ['23:49:10.858', '033 – R.BARRICHELLO', '2', '1:04.352', '43,243']])

    def test_time_to_miliseconds(self):
        self.assertEqual(log.time_to_miliseconds('1:04.352'), 64352)

    def test_time_to_seconds(self):
        self.assertEqual(log.time_to_seconds(64352), 64.352)

    def test_get_pilot_code(self):
        self.assertEqual(log.get_pilot_code('038 – F.MASSA'), '038')

    def test_get_pilot_name(self):
        self.assertEqual(log.get_pilot_name('038 – F.MASSA'), 'F.MASSA')

    def test_get_pilots_last_lap(self):
        laps_list = [['23:49:11.075', '002 – K.RAIKKONEN', '1', '1:04.108', '43,408'], [
            '23:49:08.277', '002 – K.RAIKKONEN', '2', '1:02.852', '44,275'], ['23:49:10.858', '002 – K.RAIKKONEN', '3', '1:04.352', '43,243']]

        self.assertEqual(log.get_pilots_last_lap(laps_list), {
                         '002': ['23:49:10.858', '002 – K.RAIKKONEN', '3', '1:04.352', '43,243']})


if __name__ == '__main__':
    unittest.main()
