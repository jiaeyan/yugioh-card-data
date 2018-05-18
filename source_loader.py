import re


# parse a sql file
def read_cdb(sql_f):
    with open(sql_f, 'r') as f:
        cards = {}
        for line in f:
            if line.startswith('INSERT'):
                values = re.findall(r'VALUES\((.+)\)', line.strip())[0]
                fields = values.split(',')
                if "''" in fields:
                    cards[fields[0]] = list(map(lambda x: re.findall(r'\'(.+?)\'', x)[0], fields[1:3]))
                else:
                    cards[fields[0]] += list(map(lambda x: int(x), fields[1:]))
    return cards


# parse a strings.conf file
def read_conf(conf_f):
    attributes = []
    races = []
    types = []
    categories = []
    setnames = {}
    ot = {1: 'OCG', 2: 'TCG', 3: 'OCG & TCG'}
    with open(conf_f, 'r') as f:
        for line in f:
            if re.match(r'!system 101\d', line):
                attributes.append(line.strip().split()[2])
            elif re.match(r'!system 10[234]\d', line):
                races.append(line.strip().split()[2])
            elif re.match(r'!system 10[5678]\d', line):
                types.append(line.strip().split()[2])
            elif re.match(r'!system 11[0123]\d', line):
                categories.append(line.strip().split()[2])
            elif line.startswith('!setname'):
                k, v = line.strip().split('\t')[0].split(maxsplit=2)[1:]
                setnames[int(k, 16)] = v
    return attributes, races, types, categories, setnames, ot
