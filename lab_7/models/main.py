from AOIS.lab_7.diagonal_matrix import *

if __name__ == '__main__':
    dm = DiagonalMatrix(16, 16)

    print('ЗАПИСЬ СЛОВ:')
    word1 = [1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
    dm.write_word(3, word1)

    word2 = [0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0]
    dm.write_word(7, word2)

    word3=[1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
    dm.write_word(11, word3)

    word4=[0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1,0]
    dm.write_word(4, word4)
    print(dm)

    print('\nЗАПИСЬ РАЗРЯДНОГО СТОЛБЦА')
    dm.write_address_column(2,[1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1])
    print(dm)


    print("\nЧТЕНИЕ СЛОВ И РАЗРЯДНЫХ СТОЛБЦОВ")
    print("Слово №3: ",dm.read_word(3))
    print("Разрядный столбец №4: ",dm.read_address_column(4))

    print("\nЛОГИЧЕСКИЕ ФУНКЦИИ")
    print('f7 - дизъюнкция (ИЛИ) для слова 1 и 4 и запись в 15')
    word1=dm.read_word(1)
    print('Word1:  ',word1)
    word4=dm.read_word(4)
    print('Word4:  ',word4)
    result=dm.logic_disjunction(word1,word4)
    print('Result: ',result)
    dm.write_word(15,result)
    print(dm)

    print('f8 - операция Пирса (ИЛИ-НЕ) для слова 2 и 7 и запись в 13')
    word2=dm.read_word(2)
    print('Word2:  ',word2)
    word7=dm.read_word(7)
    print('Word7:  ',word7)
    result=dm.logic_disjunction_negation(word2,word7)
    print('Result: ',result)
    dm.write_word(13,result)
    print(dm)


    print('f2 - запрет 1-го аргумента (НЕТ) для слова 5 и 3 и запись в 10')
    word5=dm.read_word(5)
    print('Word5:  ',word5)
    word3=dm.read_word(3)
    print('Word3:  ',word3)
    result=dm.logic_first_arg_ban(word5,word3)
    print('Result: ',result)
    dm.write_word(10,result)
    print(dm)


    print('f13 - импликация от 1-го элемента ко 2-му (НЕТ-НЕ) для слова 8 и 2 и запись в 11')
    word8=dm.read_word(8)
    print('Word8:  ',word8)
    word2=dm.read_word(2)
    print('Word2:  ',word2)
    result=dm.logic_implic_from1_to2(word8,word2)
    print('Result: ',result)
    dm.write_word(11,result)
    print(dm)


    print('\n\nПоиск величин, заключенных в заданном интервале [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] - [0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0]:')
    dm.search_in_range([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0])


    print("\n\nCложение полей по заданному V=011")
    dm.add_fields_by_key('011')
    print(dm)
