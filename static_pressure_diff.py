'''计算转子叶片静压分布曲线的总面积
'''

import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sympy import integrate, symbols

matplotlib.use('TkAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class StaticPressureDiff():
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename_list = os.listdir(filepath)

        for filename in self.filename_list:
            if 'NormalizedArclength' not in filename:
                self.filename_list.remove(filename)
        # print(self.filename_list)

    def fit_pressure(self):
        # columns = ['ps-x', 'ps-y', 'ss-x', 'ss-y']
        # pressure_df = pd.DataFrame(columns=columns)
        ps_df = pd.DataFrame()
        ss_df = pd.DataFrame()
        for filename in self.filename_list:
            # file_source = '.'.join(filename.split('-')[:-1])  # 去掉后缀
            # file_source = filename.split('.')[:-1]  # 去掉后缀
            # print(file_source)
            file_source = filename

            if 'ps' in file_source:
                data_df = pd.read_csv(self.filepath + filename, sep=' ')
                # print(data_df.columns.tolist())  # 1       1.1  37  ||
                # print(file_source, data_df.shape)

                data_df = data_df[[data_df.columns.tolist()[0], data_df.columns.tolist()[1]]]
                # print(data_df.shape)
                # pressure_df[['ps-x', 'ps-y']] = data_df

                ps_df = data_df
                ps_df.columns = ['ps-x', 'ps-y']

            if 'ss' in file_source:
                data_df = pd.read_csv(self.filepath + filename, sep=' ')
                data_df = data_df[[data_df.columns.tolist()[0], data_df.columns.tolist()[1]]]
                # pressure_df[['ss-x', 'ss-y']] = data_df
                # print(pressure_df.head())
                # print(pressure_df['ps-x'])

                ss_df = data_df
                ss_df.columns = ['ss-x', 'ss-y']


        # print(pressure_df)
        ps_func = np.polyfit(ps_df['ps-x'], ps_df['ps-y'], 12)  # 多项式拟合，指定自由度，计算系数
        ps_formula = np.poly1d(ps_func, variable='x')  # 生成多项式对象，多项式。指定未知数的字母
        x = np.arange(0, 1, 0.001)
        ps_new_values = np.polyval(ps_func, x)  # 多项式曲线求值，<class 'numpy.ndarray'>

        ss_func = np.polyfit(ss_df['ss-x'], ss_df['ss-y'], 12)  # 多项式拟合，指定自由度
        ss_formula = np.poly1d(ss_func, variable='x')
        # p_ps = np.poly1d(ps_func)  # 生成多项式对象
        x = np.arange(0, 1, 0.001)
        ss_new_values = np.polyval(ss_func, x)  # 多项式曲线求值

        plt.figure(figsize=(8, 6))
        plt.plot(ps_df['ps-x'], ps_df['ps-y'], 'm', label='ps original values')
        plt.plot(x, ps_new_values, 'r', label='ps polyfit values')
        plt.plot(ss_df['ss-x'], ss_df['ss-y'], 'b', label='ss original values')
        plt.plot(x, ss_new_values, 'k', label='ss polyfit values')
        plt.xlabel('Normalized Arc Length', fontsize=10)
        plt.ylabel('Static Pressure Difference', fontsize=10)
        plt.legend()
        # plt.show()

        # np.poly1d + sympy.integrate 报错
        # AttributeError: 'poly1d' object has no attribute 'atoms'
        # x = symbols('x')
        # pressure_diff_formula = ps_formula - ss_formula
        # print('formula:\n', pressure_diff_formula)
        # pressure_diff = integrate(pressure_diff_formula, (x, 0, 1))
        # print("压差为：", pressure_diff)
        
        # 解决办法：stackoverflow: Calculating the area underneath a mathematical function
        # https://stackoverflow.com/questions/2352499/calculating-the-area-underneath-a-mathematical-function
        # numpy.poly1d.integ([m,k])表示积分，参数m表示积几次分，k表示积分后的常数项的值
        # Return an antiderivative (indefinite integral) of this polynomial. 返回此多项式的不定积分
        # print('ps:\n', ps_formula)
        # print('ss:\n', ss_formula)
        # print('formula:', pressure_diff_formula)
        pressure_diff_formula = ps_formula - ss_formula
        Antiderivative_factor = pressure_diff_formula.integ(m=1, k=0)
        pressure_diff = Antiderivative_factor[1] - Antiderivative_factor[0] # The area under the curve from 0 to 1
        print("压差为：", pressure_diff)


if __name__ == '__main__':
    # filepath = input("请输入文件路径，结尾不需要添加分号：") + '\\'
    # pressure = StaticPressureDiff(filepath)
    # pressure.fit_pressure()

    diff_y = [2577.314997980022, 2573.6749591886473, 1885.5174831432814, 1803.6101913737657, 
    1569.8250404101564, 1567.1165026536328, 1439.753581258352]

    diff_x = ['65°', '66°', '67°', '67.5°', '68°', '69°', '70°']

    plt.figure(figsize=(8, 6))
    plt.plot(diff_x, diff_y, "k.-")
    plt.xlabel('转子安装角', fontsize=10)
    plt.ylabel('转子叶片静压分布曲线面积', fontsize=10)
    # plt.show()
    plt.savefig(r'E:\20191101\angle\compare\rotor\4\3level\figure\static_pressure_regre\\' + 'pressure_difference.png')