from sys import argv
from utils import find_nicks, printout_nick_history, printout_channel_history, \
                  printout_first_seen, printout_last_seen, printout_first_and_last_seen


chat = argv[1]
nick = argv[2]
ident = argv[3]
ip = argv[4]

if len(argv) == 6:
    months = int(argv[5])
else:
    months = 1

print(f'Searching {nick}!{ident}@{ip} in {chat}...')


script = argv[0]
if '/' in script:
    script_path = script[:script.rindex('/') + 1]
else:
    script_path = ''

config = {}
file = open(f'{script_path}nicks_channels.config')
for line in file:
    key, value = line.strip().split(',')
    config[key] = value
file.close()

log_directory = config['logs'] + chat + '/'


channel_history, nick_history, ident_history, first_seen, last_seen = \
find_nicks(nick, ident, ip, chat, log_directory, months)


if nick_history:
    printout = printout_nick_history(nick_history, ident_history, nick, ident, ip)
    print(printout)
    printout = printout_channel_history(channel_history)
    print(printout)
    if first_seen == last_seen:
        printout = printout_first_and_last_seen(first_seen)
        print(printout)
    else:
        printout = printout_first_seen(first_seen)
        print(printout)
        printout = printout_last_seen(last_seen)
        print(printout)
else:
    print(f'*\t[{nick}!{ident}@{ip}] Not seen')

