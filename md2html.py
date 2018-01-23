import os
import sys
import re

if len(sys.argv) == 1:
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    sys.exit(2)

ifile = sys.argv[1]
ofile = re.sub('\.(md|markdown)$', '', ifile)+'.html'

ifile = open(ifile, 'r')
ofile = open(ofile, 'w')

B = False
I = False
S = False
c = False
C = False
Q = 0
p = False
i = 0

for ch in ifile.read():
    i += 1

    if ch != '\n' and not p:
        ofile.write('<p>')
        p = True

    if ch in ('*', '_'):
        if C:
            ofile.write(ch)
            continue
        ch = ifile.read()
        if ch in ('*', '_'):
            ofile.write(f'<{"/"*B}b>')
            B = not B
        else:
            i -= 1
            ofile.write(f'<{"/"*I}i>')
            I = not I

    elif ch == '`':
        ch = ifile.read()
        if ch == '`':
            ch = ifile.read()
            if ch == '`':
                ofile.write(f'<{"/"*C}code>')
                C = not C
            else:
                if C:
                    ofile.write('``'+ch)
                    continue
                i -= 1
                ofile.write(f'<code></code>')
        else:
            if C:
                ofile.write('`'+ch)
                continue
            i -= 1
            ofile.write(f'<{"/"*c}code>')
            c = not c

    elif ch == '>':
        ofile.write('<blockquote>')
        Q += 1

    elif ch == '\n':
        if not p:
            ofile.write('<br>\n')
        ch = ifile.read()
        if ch == '\n':
            ofile.write('</blockquote>'*Q)
            ofile.write('</p>\n\n')
            p == False
            B = I = c = S = Q = False
        else:
            ofile.write('<br>\n')
            i -= 1

    else:
        ofile.write(ch)

    ifile.seek(i)
