#!/usr/bin/env python3
from db import Dictionary
import sys

word = '_'.join(sys.argv[1:]).lower()

dic = Dictionary()
meaning = list(dic.get_meaning(word))
meaning = meaning[:min(len(meaning),5)]

if meaning:
    print(meaning[0])
    print('\n'.join(meaning[1:]))
else:
    print('Result Not Found!!!')
dic.close()
