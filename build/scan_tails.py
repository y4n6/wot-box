import os
root = r'D:\06.source\MyProject\wot-xvm\src\res\scripts\client\gui\mods'
for name in sorted(os.listdir(root)):
    if not name.endswith('.py'):
        continue
    path = os.path.join(root, name)
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    tail = lines[-8:]
    if any(line.strip() == 'return' for line in tail):
        print('--- %s ---' % name)
        print('\n'.join(tail))
