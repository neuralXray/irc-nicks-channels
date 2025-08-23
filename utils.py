from os import listdir
from os.path import isdir
from re import search
from datetime import datetime


date_time_format = '%Y %b %d %H:%M:%S'
len_date_time = 21
user_regex = '[^!]+![^@]+@[^ ]+'

ast_tab_regex = r'^\*\t'
len_ast_tab = 2
join_regex = ast_tab_regex + user_regex + ' ((has)|(was)) joined\n$'
nick_change_regex = ast_tab_regex + '[^ ]+ is now known as [^\n]+\n$'


def find_nicks(nick, ident, ip, chat, log_directory, months):
    nick = nick.lower()
    log_directories = [d + '/' for d in listdir(log_directory) if isdir(log_directory + d)]
    log_directories.sort()

    if len(log_directories) > months:
        log_directories = log_directories[-months:]

    if ip.endswith('.79j.0Ar7OI.virtual') and (chat == 'irc.chathispano.com') :
        if ident == 'irccloud':
            match_case = -1
        else:
            match_case = 1
    elif (ident == '_') or (ident == '-') or (ident == '.') or (ident == '...') or \
       (ident == 'kiwiirccom') or (ident == 'KiwiIRC') or (ident == 'kvirc') or \
       (ident == 'opirc') or (ident == 'x-cript51') or (ident == 'igloo') or \
       (ident.lower() == 'irc') or (ident.lower() == 'ircap') or (ident == 'irccloud') or \
       (ident == 'yaaic') or (ident == 'androirc') or (ident == 'android') or \
       (ident == 'Username') or ip.endswith('.matrix.chathispano.com'):
        match_case = 0
    else:
        match_case = 2

    first_seen = ''
    last_seen = ''
    nick_history = {}
    ident_history = {}
    channel_history = []
    for log_dir in log_directories:
        channels = [channel for channel in listdir(log_directory + log_dir) if (channel[0] == '#')]
        channels.sort()
        for channel in channels:
            data = open(log_directory + log_dir + channel)
            channel = channel[:channel.rindex('.')]
            for line in data:
                clean_line = line[len_date_time:]

                if search(join_regex, clean_line):
                    i = clean_line.find('!')
                    j = clean_line.find('@')
                    nick_check = clean_line[len_ast_tab:i]
                    ip_check = clean_line[j + 1:]
                    k = ip_check.find(' ')
                    ip_check = ip_check[:k]
                    ident_check = clean_line[i + 1:j]

                    if match_case == 0:
                        match = (ip_check == ip) or (nick_check.lower() == nick)
                    elif match_case == 1:
                        match = (ident_check == ident) or (nick_check.lower() == nick)
                    elif match_case == -1:
                        match = nick_check.lower() == nick
                    else:
                        match = (ip_check == ip) or (ident_check == ident) or \
                                (nick_check.lower() == nick)

                    if match:
                        #print(line[:-1])
                        possible_last_seen = line[:len_date_time - 1]
                        possible_last_seen_datetime = datetime.strptime(possible_last_seen,
                                                                        date_time_format)

                        if last_seen:
                            if (possible_last_seen_datetime > last_seen_datetime):
                                last_seen = possible_last_seen
                                last_seen_datetime = possible_last_seen_datetime
                        else:
                            last_seen = possible_last_seen
                            last_seen_datetime = possible_last_seen_datetime

                        if (not first_seen) or (possible_last_seen_datetime < first_seen_datetime):
                            first_seen = possible_last_seen
                            first_seen_datetime = possible_last_seen_datetime
                        if (nick_check not in nick_history.keys()) or \
                           (nick_history[nick_check] > possible_last_seen_datetime):
                            nick_history[nick_check] = possible_last_seen_datetime
                        if nick_check in ident_history.keys():
                            if ident_check not in ident_history[nick_check]:
                                ident_history[nick_check].append(ident_check)
                        else:
                            ident_history[nick_check] = [ident_check]
                        if channel not in channel_history:
                            channel_history.append(channel)

                elif search(nick_change_regex, clean_line):
                    nick_check = clean_line[len_ast_tab:clean_line.find(' ')]
                    nick_check_new = clean_line[clean_line.rindex(' ') + 1:-1]

                    if (nick_check.lower() == nick) or (nick_check_new.lower() == nick):
                        #print(line[:-1])
                        possible_last_seen = line[:len_date_time - 1]
                        possible_last_seen_datetime = datetime.strptime(possible_last_seen,
                                                                        date_time_format)

                        if last_seen:
                            if (possible_last_seen_datetime > last_seen_datetime):
                                last_seen = possible_last_seen
                                last_seen_datetime = possible_last_seen_datetime
                        else:
                            last_seen = possible_last_seen
                            last_seen_datetime = possible_last_seen_datetime

                        if (not first_seen) or (possible_last_seen_datetime < first_seen_datetime):
                            first_seen = possible_last_seen
                            first_seen_datetime = possible_last_seen_datetime
                        if (nick_check not in nick_history.keys()) or \
                           (nick_history[nick_check] > possible_last_seen_datetime):
                            nick_history[nick_check] = possible_last_seen_datetime
                        if (nick_check_new not in nick_history) or \
                           (nick_history[nick_check_new] > possible_last_seen_datetime):
                            nick_history[nick_check_new] = possible_last_seen_datetime
                        if channel not in channel_history:
                            channel_history.append(channel)
            data.close()

    nick_history_sorted = sorted(nick_history.keys(), key=lambda n: nick_history[n])
    #for nick in nick_history_sorted:
    #    print(nick_history[nick], nick)
    #print(nick_history_sorted)
    return channel_history, nick_history_sorted, ident_history, first_seen, last_seen


def printout_nick_history(nick_history, ident_history, nick='', ident='', ip=''):
    if bool(nick) & bool(ident) & bool(ip):
        printout = f'*\t[{nick}!{ident}@{ip}] '
    else:
        printout = '*\t'

    list_ident_history = sum(ident_history.values(), [])
    if (len(set(list_ident_history)) == 1) and \
       (len(nick_history) == len(list_ident_history)) and \
       (len(nick_history) > 1):
        nick_history[-1] = f'{nick_history[-1]} ! {list_ident_history[0]}'
    else:
        nick_history = \
        [f'{nick}!{",".join(ident_history[nick])}' if nick in ident_history.keys()
         else nick for nick in nick_history]

    printout = printout + 'Nick(s): ' + ', '.join(nick_history)

    return printout


def printout_channel_history(channel_history, nick='', ident='', ip=''):
    if bool(nick) & bool(ident) & bool(ip):
        printout = f'*\t[{nick}!{ident}@{ip}] '
    else:
        printout = '*\t'

    printout = printout + 'Channel(s): ' + ', '.join(channel_history)

    return printout


def printout_first_seen(first_seen, nick=''):
    if nick:
        printout = f'*\t[{nick}] '
    else:
        printout = '*\t'

    printout = printout + f'First seen: {first_seen}'

    return printout


def printout_last_seen(last_seen, nick=''):
    if nick:
        printout = f'*\t[{nick}] '
    else:
        printout = '*\t'

    printout = printout + f'Last seen: {last_seen}'

    return printout


def printout_first_and_last_seen(first_seen, nick=''):
    if nick:
        printout = f'*\t[{nick}] '
    else:
        printout = '*\t'

    printout = printout + f'First and Last seen: {first_seen}'

    return printout

