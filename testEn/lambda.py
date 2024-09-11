# Numbers with their names in English, German, Mandarin, and Spanish:
number_names = [[1, 'one',   'eins',   '一', 'uno'],
                [2, 'two',   'zwei',   '二',  'dos'],
                [3, 'three', 'drei',   '三',  'tres'],
                [4, 'four',  'vier',   '四',  'quatro'],
                [5, 'five',  'fünf',   '五',  'cinco'],
                [6, 'six',   'sechs',  '六',  'seis'],
                [7, 'seven', 'sieben', '七',  'siete'],
                [8, 'eight', 'acht',   '八',  'ocho'],
                [9, 'nine',  'neun',   '九',  'nueve'],
                [10, 'ten',  'zehn',   '十',  'diez']]

sorted(number_names, key=lambda w: w[3])
print(number_names)