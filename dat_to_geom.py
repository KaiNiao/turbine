'''实现dat文件向geom文件数据的自动拷贝，同时比较大小，1最大，5最小
数据分两部分，行列数固定。第一部分215行一列，第二部分209行三列。比较第二列的数据
行数异常时报错，表明dat提取出错
dat文件中以“Curve SISL lofted”开头的数据为需要向geom中拷贝的数据，从小到大共5部分
'''

import os


def replace_data_in_geom(dat, geom, base_path, row_sorted):
    with open(base_path  + '\\dat\\' + dat, 'r') as f1, open(base_path + '\\geo\\' +  geom, 'r+') as f2:
        # 读取数据
        f1_line = f1.readlines()
        f1_line = [x.replace('\n', '') for x in f1_line]

        f2_line = f2.readlines()
        f2_line = [x.replace('\n', '') for x in f2_line]
        
        f2.seek(0)  # seek()手动定位指针，否则write时文件追加内容 len(f2_line)
        # https://segmentfault.com/a/1190000016579093
        
        # 分别记录吸力面与压力面数据的开始行数
        global start_row  # UnboundLocalError： local variable 'xxx' referenced before assignment
        if dat.split('.')[0].endswith("ss"):
            for row, line in enumerate(f2_line):
                if line == "suction":
                    start_row = row
                    # print(start_row)
                    break
        elif dat.split('.')[0].endswith("ps"):
            for row, line in enumerate(f2_line):
                if line == "pressure":
                    start_row = row
                    # print(start_row)
                    break
        
        # print(start_row)
        copy_count = 0
        for row, line in enumerate(f2_line):
            # line = line.rstrip()  # 去掉字符串右边的空格
            # 但是，这种去掉空格只是临时操作，原字符串没有任何改变。如果想要永久去掉字符串中的空格，一定要对字符串变量进行重新赋值。

            if row < start_row:
                continue
            
            # 实现替换
            if line.endswith("section 1"):
                f2_line[row+3: row+3+209] = f1_line[row_sorted[0]: row_sorted[0]+209]
                copy_count += 1
            elif line.endswith("section 2"):
                f2_line[row+3: row+3+209] = f1_line[row_sorted[1]: row_sorted[1]+209]
                copy_count += 1
            elif line.endswith("section 3"):
                f2_line[row+3: row+3+209] = f1_line[row_sorted[2]: row_sorted[2]+209]
                copy_count += 1
            elif line.endswith("section 4"):
                f2_line[row+3: row+3+209] = f1_line[row_sorted[3]: row_sorted[3]+209]
                copy_count += 1
            elif line.endswith("section 5"):
                f2_line[row+3: row+3+209] = f1_line[row_sorted[4]: row_sorted[4]+209]
                copy_count += 1

            if copy_count == 5:  # 拷贝完成
                break
        
        # print("274: ", f2_line[274], len(f2_line))
        # print(f2_line[-1])  # NI_END   GEOMETRYYY
        f2.write('\n'.join(f2_line))
        # print(f2_line[-1])


def test(geom1, geom2):
    with open(geom1, 'r') as f1, open(geom2, 'r') as f2:
        f1_line = f1.readlines()
        f1_line = [x.replace('\n', '') for x in f1_line]
        f2_line = f2.readlines()
        f2_line = [x.replace('\n', '') for x in f2_line]
        print(len(f1_line), len(f2_line))

        error_num = 0
        for row in range(62, len(f2_line)):
            if f1_line[row] != f2_line[row]:
                # 出现了两种报错
                print(row, "wrong")  # NI_END   GEOMETRYYY
                print(f1_line[row], len(f1_line[row]))  # 行末多了个空格。可以忽略
                print(f2_line[row], len(f2_line[row]))
                error_num += 1
        
        if error_num == 0:
            print("success")


def dat_to_geom(dat_list, geom, base_path):
    '''ss、ps没有顺序。dat_list中包含两个元素，分别为ss、ps
    '''
    for dat in dat_list:
        copy_count = 0  # 记录已拷贝的次数
        row_data = []  # 存储行数与数字，根据数字大小决定行数存储的顺序

        with open(base_path + '\\dat\\' + dat, 'r') as f1:
            # 读取数据
            info = f1.readlines()
            # info = f.readlines -> <class 'builtin_function_or_method'>
            # print(type(info))  # list

            for row, line in enumerate(info):
                if line.startswith("Curve SISL lofted"):
                    if ( copy_count < 5 ):
                        # 读取成功
                        row_data.append(( (row + 215 + 1), float(info[row + 215 + 1].split(' ')[1]) ))
                        copy_count += 1
                        # print(copy_count)

                    if (copy_count == 5 ):
                        # 实现拷贝
                        # print(row_data)
                        row_data.sort(key=lambda x: x[1])  # 排序
                        # print(row_data)
                        break

                    if ( len(info[row+200]) > 60 ):
                        print("DAT 文件读取失败，请重新读取")
                        # print(row, line)
                        return

        print("%s 文件拷贝完毕，请查看文件 %s" % (dat, geom))
        # print(row_data)
        row_sorted = [x[0] for x in row_data]
        replace_data_in_geom(dat, geom, base_path, row_sorted)


def path_classification(dat_path, geo_path):
    dat_files = os.listdir(dat_path)
    dat_files = [x for x in dat_files if x.endswith(".dat")]
    geo_files = os.listdir(geo_path)
    geo_files = [x for x in geo_files]

    # print(dat_files)
    # print(geo_files)

    # 单级、三级分类。定转子分类
    # 一级一个列表，定转子各一个字典
    files_list = []
    for i in range(1, 4):
        count = 0
        for geo in geo_files:
            if geo.startswith('%d' % i):  # 一级只创建一个列表
                if count == 0:
                    files_list.insert(i-1, [])
                    # print(files_list)
                    count += 1

                geo_dat_dict = {geo: []}
                for dat in dat_files:
                    # 同级、同叶片类型
                    if dat.split('-')[:-1] == geo.split('-')[:-1]:
                        geo_dat_dict[geo].append(dat)
                files_list[i-1].append(geo_dat_dict)
    
    # print(files_list)
    print("\n1. 文件结构如下：")
    for files in files_list:
        print(files)

    return files_list


if __name__ == "__main__":
    # 每次只需要修改 base_path 即可
    # base_path = r"C:\Users\HMZ\Desktop\dat"
    # base_path = r"E:\20191101\angle\AB-2-2\AB-2-2-1level"
    base_path = input("请输入文件路径，结尾不需要添加分号：")  # 用户手动输入路径

    dat_path = base_path + "\\dat"
    geo_path = base_path + "\\geo"
    files_list = path_classification(dat_path, geo_path)

    print("\n2. 开始拷贝 -_- -_- -_- -_-\n")

    for level_files in files_list:  # 每级一个列表
        for turbine_dict in level_files:  # 每种叶片一个字典
            for geo, dat in turbine_dict.items():
                dat_to_geom(dat, geo, base_path)

    print("\n3. 请核对定转子叶片个数、叶片编号、叶片尺寸范围！")

    # 用于测试
    # dat_ss = r"C:\Users\HMZ\Desktop\dat\1-staor-ss.dat"
    # dat_ps = r"C:\Users\HMZ\Desktop\dat\1-staor-ps.dat"
    # geom = r"C:\Users\HMZ\Desktop\dat\geo\1-stator-73mm.geomTurbo"

    # dat_ss = r"C:\Users\HMZ\Desktop\dat\1-rotor-ss.dat"
    # dat_ps = r"C:\Users\HMZ\Desktop\dat\1-rotor-ps.dat"
    # geom = r"C:\Users\HMZ\Desktop\dat\geo\1-rotor-73mm.geomTurbo"

    # dat_to_geom(dat_ss, dat_ps, geom)
    # replace_data_in_geom(dat_ps, geom, [222, 1126, 1552, 1978, 648])
    # test(geom, r"C:\Users\HMZ\Desktop\dat\1-stator-73mm - 副本.geomTurbo")
    # test(geom, r"C:\Users\HMZ\Desktop\dat\1-rotor-73mm - 副本.geomTurbo")


'''
stator:
#Curve 282492768
Curve SISL lofted_3#2 -> 5

#Curve 282491424
Curve SISL lofted_3#6 -> 1 

#Curve 282492096
Curve SISL cspline_5#2

#Curve 282494112
Curve SISL cspline_5#3

#Curve 282494336
Curve SISL lofted_3#3 -> 4

#Curve 282487168
Curve SISL lofted_3#4 -> 3

#Curve 282488064
Curve SISL lofted_3#5 -> 2

#Curve 282492992
Curve SISL lofted_3#0

#Curve 282489856
Curve SISL lofted_3#1


rotor:
#Curve 282488368
Curve SISL lofted_4#2 -> 1

#Curve 282489712
Curve SISL lofted_4#6 -> 5

#Curve 282485008
Curve SISL cspline_9#2

#Curve 282485456
Curve SISL cspline_9#3

#Curve 282491728
Curve SISL lofted_4#3 -> 2

#Curve 282486128
Curve SISL lofted_4#4 -> 3

#Curve 282490832
Curve SISL lofted_4#5 -> 4

#Curve 282485680
Curve SISL lofted_4#0

#Curve 282491280
Curve SISL lofted_4#1
'''