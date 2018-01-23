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

for c in ifile.read():
    i += 1

    if c != '\n' and not p:
        ofile.write('<p>')
        p = True

    if c in ('*', '_'):
        if C:
            ofile.write(c)
            continue
        c = ifile.read()
        if c in ('*', '_'):
            ofile.write(f'<{"/"*B}b>')
            B = not B
        else:
            i -= 1
            ofile.write(f'<{"/"*I}i>')
            I = not I

    elif c == '`':
        c = ifile.read()
        if c == '`':
            c = ifile.read()
            if c == '`':
                ofile.write(f'<{"/"*C}code>')
                C = not C
            else:
                if C:
                    ofile.write('``'+c)
                    continue
                i -= 1
                ofile.write(f'<code></code>')
        else:
            if C:
                ofile.write('`'+c)
                continue
            i -= 1
            ofile.write(f'<{"/"*c}code>')
            c = not c

    elif c == '>':
        ofile.write('<blockquote>')
        Q += 1

    elif c == '\n':
        if not p:
            ofile.write('<br>\n')
        c = ifile.read()
        if c == '\n':
            ofile.write('</blockquote>'*Q)
            ofile.write('</p>\n\n')
            p == False
            B = I = c = S = Q = False
        else:
            ofile.write('<br>\n')
            i -= 1

    else:
        ofile.write(c)

    ifile.seek(i)
