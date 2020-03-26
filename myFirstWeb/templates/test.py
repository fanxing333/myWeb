

'''def zuoye():
    if input('是否继续') == 'Y':
        str = input('请输入字符')
        for s in str:
            print('这是第字符' + s)
    else:return

    return zuoye()'''
'''t=True
while t==True:
    str = input('请输入字符')
    for s in str:
        print('这是第字符' + s)

    if input('是否继续') == 'Y':
        t=True
    else:
        t=False'''
print('{:-^60}'.format('微实例3+3 while+try+重复.py'))
print()
str1=input('请输入一个字符串：')
no1 = 1
no2 = 1
for s in str1:
    print('字符串“{}”的第{}个数是：{}'.format(str1,no1,str1[no1-1]))
    no1+=1
else:
    r=input('还要继续吗（Y/N）：')
while r=='Y':
    str2 = input('请输入一个字符串：')
    for s in str1:
        print('字符串“{}”的第{}个数是：{}'.format(str2,no2,str2[no2-1]))
        no2+=1
    else:
        r=input('还要继续吗（Y/N）：')
else:
    print('此次拆分字符串完毕，下次再见！')
print()
print('{:-^60}'.format('微实例3+3 while+try+重复.py'))