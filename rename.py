#! /usr/bin/python

import re
from collections import defaultdict

def main():
    file1 = open("Naruto Shippuuden.txt").read()
    names = file1.split('\n')

    # Naruto Shippuuden - 1x01 - Homecoming
    r=re.compile('(Naruto Shippuuden) - ([0-9]{1,2}x[0-9]{2}) - (.*)')

    count = 0
    details = {}
    for name in names:
        match = r.search(name)
        if match:
            count += 1
            season, episode = match.group(2).split('x')
            title = match.group(3)
            details[count] = ( int(season), int(episode), title )

    file2 = open("list.txt").read()

    f_names = file2.split('\n')

    # [Taka]_Naruto_Shippuuden_230_[720p][4EC3BBF6].mp4
    r=re.compile('(Naruto[_\-. ]Shippuuden)[^0-9]*([0-9]{3})-?([0-9]{3})?[^.]*.(.*)')
    file_names = []
    for f in f_names:
        match = r.search(f)
        if match:
            _, first, second, suff = match.groups()
            file_names.append((int(first), f, suff))
            if second is not None:
                file_names.append((int(second), f, suff))

    matched = [ (x[1], details[x[0]], x[2], x[0]) for x in file_names ]

    d = defaultdict(list)
    for file, title, suff, num in matched:
        d[file].append((title,suff,num))

    for key, values in d.items():
        format = {}

        ((season, episode, name), suff, num) = values[0]
        season = str(season)
        season_pad = season.zfill(2)
        episode = str(episode).zfill(2)

        if len(values) == 2:
            ((_, episode2, title2),_,_) = values[1]
            episode += "-" + str(episode2).zfill(2)
            name = name + " & " + title2


        format['src'] = key
        format['season'] = season
        format['season_pad'] = season_pad
        format['episode'] = episode
        format['name'] = name
        format['suff'] = suff
        format['num'] = str(num).zfill(3) 

        print ('mv "%(src)s" "Season %(season)s/Naruto Shippuuden - %(season_pad)sx%(episode)s - %(name)s (%(num)s).%(suff)s"') % (format)


if __name__ == "__main__":
    main()
