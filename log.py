import re
import sys
import os
import datetime


def read_file(path):
    if os.path.isfile(path):
        log_file = open(path, 'r')
        return log_file
    raise_exception('Arquivo não existe.')


def parse_to_list(line):
    return re.split(r'\s{2,}', line)


def file_to_list(log_file):
    lines = []
    for line in log_file:
        lines.append(parse_to_list(line))
    return lines

def get_list_from_file(path):
    log_file = read_file(path)
    laps_list = file_to_list(log_file)
    log_file.close()
    return laps_list


def raise_exception(msg):
    raise Exception(msg)


def sort_lap_time(laps_list):
    laps = laps_list
    laps.sort(key=lambda lap: (lap[3]))
    return laps


def sort_ranking(ranking_list):
    ranking = ranking_list
    ranking.sort(key=lambda racer: (-int(racer[2]), racer[3]))
    return ranking


def delete_header(laps_list):
    laps = laps_list
    laps.pop(0)
    return laps


def fix_pilot_name():
    pass


def clean_log(laps_list):
    laps = delete_header(laps_list)
    for lap in laps:
        lap[4] = lap[4].replace('\n', '')
    return laps


def time_to_miliseconds(value):
    minutes = value.replace('.', ':')
    miliseconds = sum(x * int(t)
                      for x, t in zip([60000, 1000, 1], minutes.split(':')))
    return miliseconds


def time_to_seconds(value):
    return value / 1000


def get_pilots_last_lap(laps_list):
    last_laps = {}
    for lap in laps_list[::-1]:
        pilot_code = get_pilot_code(lap[1])

        if not pilot_code in last_laps:
            last_laps[pilot_code] = lap
            pass

        if lap[2] > last_laps[pilot_code][2]:
            last_laps[pilot_code] = lap
    return last_laps


def get_ranking(laps_list, pilots_total_times):
    ranking_list = []
    pilots_laps = get_pilots_last_lap(laps_list)

    for code, lap in pilots_laps.items():
        lap = list(lap)
        lap.append(get_pilot_total_time(code, pilots_total_times))
        lap.append(get_pilot_mean_time_format(code, laps_list))
        lap.append(get_pilot_mean_speed(code, laps_list))
        ranking_list.append(lap)
    return sort_ranking(ranking_list)


def get_pilot_mean_speed(pilot_code, laps_list):
    mean = get_mean_value(pilot_code, laps_list, 4)
    return mean


def get_pilot_mean_time_format(pilot_code, laps_list):
    mean = get_pilot_mean_time(pilot_code, laps_list)
    return str(datetime.timedelta(seconds=mean))


def get_mean_value(pilot_code, laps_list, index):
    sum_value = 0
    pilots_laps = get_pilot_laps(pilot_code, laps_list)
    for lap in pilots_laps:
        pilot_lap_value = float(lap[index].replace(',', '.'))
        sum_value += pilot_lap_value
    mean = sum_value / len(pilots_laps)
    return mean


def get_pilot_mean_time(pilot_code, laps_list):
    sum_value = 0
    pilots_laps = get_pilot_laps(pilot_code, laps_list)
    for lap in pilots_laps:
        pilot_lap_time = lap[3]
        sum_value += get_lap_seconds(pilot_lap_time)
    mean = sum_value / len(pilots_laps)
    return mean


def get_pilot_code(pilot):
    return re.split(r'\s', pilot)[0]


def get_pilot_name(pilot):
    return re.split(r'\s', pilot)[2]


def get_pilot_total_time(code, pilots_total_times):
    return pilots_total_times[code]


def get_lap_seconds(value):
    miliseconds = time_to_miliseconds(value)
    return time_to_seconds(miliseconds)


def get_pilots_total_time(laps_list):
    pilots_total_times = {}

    for lap in laps_list:
        pilot_code = get_pilot_code(lap[1])
        pilot_lap_time = lap[3]

        if pilot_code not in pilots_total_times:
            pilots_total_times[pilot_code] = get_lap_seconds(pilot_lap_time)
            pass
        pilots_total_times[pilot_code] += get_lap_seconds(pilot_lap_time)
    return pilots_total_times


def get_pilot_laps(pilot_code, laps_list):
    return list(filter(lambda lap: pilot_code in lap[1], laps_list))


def get_best_lap(laps_list):
    laps = laps_list
    laps.sort(key=lambda lap: (lap[3]))
    return laps[0]


def get_pilot_best_lap(pilot_code, laps_list):
    pilot_laps = get_pilot_laps(pilot_code, laps_list)
    return get_best_lap(pilot_laps)


def format_ranking_line(index, pilot, first_pilot_time):
    position = index + 1
    name = get_pilot_name(pilot[1])
    code = get_pilot_code(pilot[1])
    laps_completed = pilot[2]
    total_time = str(datetime.timedelta(seconds=pilot[5]))
    mean_lap_time = pilot[6][:-3]
    mean_speed = str(pilot[7])[:6]
    
    if laps_completed == '4':
        seconds = pilot[5] - first_pilot_time
        if seconds == 0:
            seconds_behind_first = '-'
        else:
            seconds_behind_first = str(datetime.timedelta(seconds=(pilot[5] - first_pilot_time)))[:-3]

    else:
        seconds_behind_first = 'Não completou'

    if len(name) < 7:
        name += '  '

    total_time = total_time[:-3]
    return '	{0}		    {1}   		{2}		{3}		   {4}            {5}           {6}         {7}'.format(position, code, name, laps_completed, total_time, mean_lap_time, mean_speed, seconds_behind_first)


def format_best_lap_line(lap, best_lap):
    pilot = lap[1]
    time = lap[3]
    best = '*' if best_lap else ''

    print('{0} | Tempo: {1}  {2}'.format(pilot, time, best))


def display_ranking(ranking):
    first_pilot_time = ranking[0][5]
    display_ranking = ranking
    title = 'Posição Chegada		Código Piloto 		Nome Piloto 	Voltas Completadas	Tempo Total de Prova      Tempo médio        Vel. média     Tempo após o 1º'
    print(title)
    for index, pilot in enumerate(display_ranking):
        print(format_ranking_line(index, pilot, first_pilot_time))


def display_best_laps(laps_list, ranking):
    pilot_codes = list(map(lambda pilot: get_pilot_code(pilot[1]), ranking))
    best_pilots_laps = []

    for code in pilot_codes:
        best_pilots_laps.append(get_pilot_best_lap(code, laps_list))

    print('Melhores voltas por piloto')

    for index, lap in enumerate(best_pilots_laps):
        format_best_lap_line(lap, index == 0)
    print('\n* melhor volta da corrida')


def main(path):
    laps_list = get_list_from_file(path)
    laps_list_clean = clean_log(laps_list)
    pilots_total_times = get_pilots_total_time(laps_list_clean)
    ranking = get_ranking(laps_list_clean, pilots_total_times)
    display_ranking(ranking)
    print('')
    display_best_laps(laps_list, ranking)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
