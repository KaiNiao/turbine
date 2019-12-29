'''实现曲线图的自动绘制
支持多个表格的同一列绘制在同一张图片中
https://blog.csdn.net/weixin_42969619/article/details/97654090
https://blog.csdn.net/brink_compiling/article/details/76890198
'''
import xlrd
import os
import random
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class ShowData(object):
    def __init__(self, filepath):
        self.target = ["100级扭矩（N·m）", "100级压降（MPa)", "100级轴向力（N）", "水力效率"]
        self.filepath = filepath
        self.image_path = self.filepath + "\\iamge\\"
        image_is_exists = os.path.exists(self.image_path)
        if not image_is_exists:  # 新建文件夹
            os.makedirs(self.image_path)

    def show_one_data(self, filename):
        for value in self.target:  # 每张表绘制四张图，之后合并
            plt.figure(figsize=(8, 6))
            data_df = pd.read_excel(self.filepath + '\\' + filename)

            # ['转速', '单个叶片扭矩', '单级扭矩', '100级扭矩（N·m）', '进口压力', '出口压力',
            #  '单级压降（Pa）', '100级压降（MPa)', '单个叶片轴向力', '单级转子轴向力',
            #  '100级轴向力（N）', '角速度', '水力效率', 'Unnamed: 13']
            fields = data_df.columns.tolist()

            if data_df.shape[-1] == 14:  # 14列时最后一列是备注，记录是否崩掉
                # data_df = data_df[data_df[fields[-1]] != "崩掉"]
                data_df = data_df.loc[data_df[fields[-1]] != "崩掉"]
            print("{0} 表格有效数据大小为：{1}".format(filename, data_df.shape))
            # print(data_df)
            rotation_rate = data_df["转速"]

            plt.plot(rotation_rate, data_df[value], "bs-", markersize=5, label=filename.split('.')[0])
            plt.xlabel("转速", fontsize=20)
            plt.ylabel(value, fontsize=20)
            # plt.title(value)  # 不需要 title
            plt.legend(loc=0)

            plt.savefig(self.image_path + filename.split('.')[0] + value + ".jpg")
            plt.show()  # show与savefig保存的图片效果一致

        print("绘制完毕，请查看 %s 文件夹" % self.image_path)

    def show_merge_data(self):
        # 修改每条线的颜色和标记符
        color_list = ['r', 'b', 'k', 'g', 'c', 'm']
        mark_list = ['+', '*', '.', 's', '^', 'v', '>']  # '<', 'p', 'h'
        color_mark_list = []
        filename_list = os.listdir(self.filepath)

        if len(filename_list) > len(color_list):
            for color in color_list:
                for mark in mark_list:
                    color_mark_list.append(color + mark + "-")  # "-" 表示实线
            random.shuffle(color_mark_list)            
        else:
            for i in range(len(color_list)):
                color_mark_list.append(color_list[i] + mark_list[i] + "-")
        # print(color_mark_list)

        for value in self.target:  # 每张表绘制四张图，之后合并
            plt.figure(figsize=(8, 6))
            count = 0  # 计数用于选取 mark
            for filename in filename_list:
                if not filename.endswith("xlsx"):  # 跳过新画出来的图片或其他文件
                    continue
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                # 选择线的颜色和标记符
                count += 1
                color_mark = color_mark_list[count % len(color_mark_list)]
                # color_mark = color_mark_list[count]

                data_df = pd.read_excel(self.filepath + '\\' + filename)

                # ['转速', '单个叶片扭矩', '单级扭矩', '100级扭矩（N·m）', '进口压力', '出口压力',
                #  '单级压降（Pa）', '100级压降（MPa)', '单个叶片轴向力', '单级转子轴向力',
                #  '100级轴向力（N）', '角速度', '水力效率', 'Unnamed: 13']
                fields = data_df.columns.tolist()

                if data_df.shape[-1] == 14:  # 14列时最后一列是备注，记录是否崩掉
                    # data_df = data_df[data_df[fields[-1]] != "崩掉"]
                    data_df = data_df.loc[data_df[fields[-1]] != "崩掉"]
                print("{0} 表格有效数据大小为：{1}".format(filename, data_df.shape))
                # print(data_df)
                rotation_rate = data_df["转速"]

                # 修改标签名
                label_filename = '-'.join(filename.split('.xlsx')[0].split('-')[1:-1])  # [1, -2]
                # print(label_filename)
                if 'level' in label_filename or 'mm' in label_filename:
                    label_filename = label_filename.split('-')[0]

                plt.plot(rotation_rate, data_df[value], color_mark, markersize=5, label=label_filename)
                plt.xlabel("转速", fontsize=10)
                plt.ylabel(value, fontsize=10)
                # plt.title(value)  # 不需要 title
                plt.legend(loc=0)

            plt.savefig(self.image_path + value + ".png")
            bottom, top = plt.ylim()
            plt.ylim(bottom/2, top)
            plt.show()  # show与savefig保存的图片效果一致

        print("绘制完毕，请查看文件夹：%s" % self.image_path)

    def show_max_accuracy(self):
        filename_list = os.listdir(self.filepath)
        max_df = pd.DataFrame()

        for value in self.target: 
            # plt.figure(figsize=(16, 12))
            plt.figure(figsize=(8, 6))
            # plt.figure()
            for filename in filename_list:
                if not filename.endswith("xlsx"):  # 跳过新画出来的图片或其他文件
                    continue
                    
                data_df = pd.read_excel(self.filepath + '\\' + filename)

                # ['转速', '单个叶片扭矩', '单级扭矩', '100级扭矩（N·m）', '进口压力', '出口压力',
                #  '单级压降（Pa）', '100级压降（MPa)', '单个叶片轴向力', '单级转子轴向力',
                #  '100级轴向力（N）', '角速度', '水力效率', 'Unnamed: 13']
                fields = data_df.columns.tolist()

                if max_df.empty:
                    max_df = pd.DataFrame(columns=fields)

                if data_df.shape[-1] == 14:  # 14列时最后一列是备注，记录是否崩掉
                    # data_df = data_df[data_df[fields[-1]] != "崩掉"]
                    data_df = data_df.loc[data_df[fields[-1]] != "崩掉"]
                print("{0} 表格有效数据大小为：{1}".format(filename, data_df.shape))
                # print(data_df)

                # 修改标签名
                label_filename = '-'.join(filename.split('.')[0].split('-')[2:-1])  # 记得修改
                if 'level' in label_filename or 'mm' in label_filename:
                    label_filename = label_filename.split('-')[0]

                # 选取指定列最大值所在行
                max_df.loc[label_filename] = data_df.loc[data_df["水力效率"].idxmax()]     

            plt.plot(max_df.index.tolist(), max_df[value], "k.-", markersize=5, label="各方案最高"+value)
            plt.xlabel("方案名", fontsize=10)
            plt.ylabel(value, fontsize=10)
            bottom, top = plt.ylim()
            plt.ylim(bottom/2, top)
            # plt.title(value)  # 不需要 title
            # 图例的字体格式在prop中进行设置，赋值font1可以是一个字典，包含各个属性及其对应值，
            # 属性包括family（字体）、size（字体大小）等常用属性
            plt.legend(loc=0, prop={'size': 15})

            plt.savefig(self.image_path + "最高" + value + ".png")
            plt.show()  # show与savefig保存的图片效果一致
        print("绘制完毕，请查看文件夹：%s" % self.image_path)


if __name__ == "__main__":
    # filepath = r"E:\20190908\A-A-8mm\A-8mm-1-level"
    # show = ShowData(filepath)
    # filename = r"73mm-A-8mm.csv"
    # show.show_one_data(filename)

    filepath = r"E:\20191226\compare" + '\\'
    show = ShowData(filepath)
    show.show_merge_data()
    show.show_max_accuracy()