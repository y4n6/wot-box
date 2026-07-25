# -*- coding: utf-8 -*-
import os
root = r'D:\06.source\MyProject\wot-xvm\src\res\scripts\client\gui\mods'
for name in sorted(os.listdir(root)):
    if not name.endswith('.py'):
        continue
    path = os.path.join(root, name)
    with open(path, 'rb') as f:
        data = f.read()
    text = data.decode('utf-8', 'replace')
    lines = text.splitlines()
    if lines and lines[-1].strip() == 'return':
        print(name)
