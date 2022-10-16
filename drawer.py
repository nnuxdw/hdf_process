from pylab import *




def drawLineChart(title, xLabel, yLabel, xAxis, yAxis, legend, file):
    plt.title(title, fontsize=20)  # 折线图标题
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文
    # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
    plt.plot(xAxis, yAxis, 'ro-', color='#4169E1', alpha=0.8, linewidth=2, label=legend)

    # 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
    plt.legend(loc="lower right", fontsize=14)
    plt.xlabel(xLabel, fontsize=18)
    plt.ylabel(yLabel, fontsize=18)
    # 设置x轴刻度变化步长为1
    x_major_locator = MultipleLocator(1)
    plt.gca().xaxis.set_major_locator(x_major_locator)
    plt.gca().tick_params(labelsize='10')
    plt.show()
    plt.savefig(file)  # 保存该图片

def drawBarChart(title, xLabel, yLabel, xAxis, yAxis, legend, file):
    plt.title(title, fontsize=20)  # 折线图标题
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文
    # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
    plt.bar(xAxis, yAxis, color='#4169E1', alpha=0.8,  label=legend)

    # 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
    plt.legend(loc="upper right", fontsize=14)
    plt.xlabel(xLabel, fontsize=18)
    plt.ylabel(yLabel, fontsize=18)
    # 设置x轴刻度变化步长为1
    x_major_locator = MultipleLocator(1)
    y_major_locator = MultipleLocator(10)
    # 设置y轴刻度范围
    plt.ylim(290,370)

    plt.gca().xaxis.set_major_locator(x_major_locator)
    plt.gca().yaxis.set_major_locator(y_major_locator)
    plt.gca().tick_params(labelsize='10')
    plt.show()
    plt.savefig(file)  # 保存该图片


def drawMultiLineChart(title, xLabel, yLable, xAxis, yAxis, legends, file):
    gradientColorArr = ['#0099cc', '#33cccc', '#00ff99', '#00ff00', '#33cc33', '#1e9600', '#ffff99', '#ffff00',
                        '#fff200', '#ff9900', '#ff3300', '#ff0000']
    plt.title(title, fontsize=20)  # 折线图标题
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
    plt.xlabel(xLabel, fontsize=18)  # x轴标题
    plt.ylabel(yLable, fontsize=18)  # y轴标题
    for i in range(len(yAxis)):
        plt.plot(xAxis, yAxis[i], 'ro-', color=gradientColorArr[i], marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
    # 设置x轴刻度变化步长为1
    x_major_locator = MultipleLocator(1)
    plt.gca().xaxis.set_major_locator(x_major_locator)
    plt.gca().tick_params(labelsize='10')
    # 显示数值
    # for i in range(len(yAxis)):
    #     for a, b in zip(xAxis, yAxis[i]):
    #         plt.text(a, b, b, ha='center', va='bottom', fontsize=10)  # 设置数据标签位置及大小

    plt.legend(legends, fontsize=12)  # 设置折线名称
    plt.show()  # 显示折线图
    plt.savefig(file)  # 保存该图片


