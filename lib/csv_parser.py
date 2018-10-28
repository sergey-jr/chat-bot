import copy
import json
import re
import urllib.request

from kutana import logger


def parse_pair(pair):
    subject, room = pair, ''
    if ',' in pair and '/' in pair:
        res = pair.split('/')
        has_not_pair = ['None', 'пары нет']
        if any([i in pair for i in has_not_pair]):
            if res[0] in has_not_pair:
                res[1] = res[1].split(',')
                subject = '/'.join([res[0], res[1][0]])
                room = '/'.join([res[0], res[1][1]])
            if res[1] in has_not_pair:
                res[0] = res[0].split(',')
                subject = '/'.join([res[0][0], res[1]])
                room = '/'.join([res[0][1], res[1]])
        else:
            res = [item.split(',') for item in res]
            subject = '/'.join([res[0][0], res[1][0]])
            room = '/'.join([res[0][1], res[1][1]])
    elif ',' in pair:
        subject, room = pair.split(',')
    return {"subject": subject, "room": room}


def parse_row(high, low, day):
    time = high[0]
    res = None
    low, high = low[day], high[day]
    if high or low:
        if low and high and high != low:
            res = [{'time': time}, {'time': time}]
            res[0].update(parse_pair(high))
            res[1].update(parse_pair(low))
        elif low and not high:
            res = [{}, {'time': time}]
            res[1].update(parse_pair(low))
        elif high == low:
            res = {'time': time}
            res.update(parse_pair(high))
        elif high and not low:
            res = [{'time': time}, {}]
            res[0].update(parse_pair(high))
    return res


class CsvParser:
    def __init__(self, **kwargs):
        url = kwargs.get('url', None)
        file_path = kwargs.get('path', None)
        if url is None and file_path is None:
            logger.error('URL of file and file path not given')
        if url:
            try:
                file = urllib.request.urlopen(url)
                self.data = file.read().decode('windows-1251')
            except Exception as err:
                logger.error('Error occurred: {}({})'.format(err, type(err)))
        elif file_path:
            try:
                file = open(file_path, encoding='windows-1251')
                self.data = file.read()
            except FileNotFoundError:
                logger.error('File with path={} not found'.format(file_path))

    def parse(self):
        if self.data:
            data_to_write = self.data
            data_to_write = re.sub('\r', '', data_to_write).split('\n')
            data_to_write = [i.split(';') for i in data_to_write]
            n = (len(data_to_write) - 1) // 2
            res = {}
            for i in range(len(data_to_write[0]) - 1):
                res[str(i + 1)] = {}

            for i in range(n):
                high = data_to_write[i * 2 + 1]
                low = data_to_write[(i + 1) * 2]
                if any(high[1:]) or any(low[1:]):
                    for k in range(1, len(high)):
                        row = parse_row(high, low, k)
                        if row is not None:
                            res[str(k)][str(i + 1)] = row
            res_1 = copy.deepcopy(res)
            for k in res:
                if not res[k]:
                    res_1.pop(k)
            res = res_1
            return json.dumps(res, ensure_ascii=False)