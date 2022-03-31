import pandas as pd

code_names = ['西安一码通', '随申码', '北京健康宝', '其他', '苏康码', '粤康码']  # 5个文件名


def filter_data(df, filter_dic):
    """filter_dic字典格式为col:val, 过滤选择col对应列值为val的那些样本"""
    for k, v in filter_dic:
        df = df[df[k] == v]
    return df


def split_by_col(df, col, f_prefix="data/"):
    """按某一列分开，每个值的样本为一个csv"""
    for val in df[col].unique():
        df_split = df[df[col] == val]
        df_split.to_csv(f_prefix + val[2:] + ".csv")


def filter_valid():
    """过滤有效性"""
    valid_questions = {'西安一码通': '101.西安一码通基本认知情况:问卷有效性测试题：本题请选非常不符合', '随申码': '10.随申码基本认知情况:问卷有效性测试题：本题请选非常不符合', '北京健康宝': '56.北京健康宝基本认知情况:问卷有效性测试题：本题请选非常不符合', '其他': '119.健康码基本认知情况:问卷有效性测试题：本题请选非常不符合', '苏康码': '35.苏康码基本认知情况:问卷有效性测试题：本题请选非常不符合', '粤康码': '77.粤康码各基本认知情况:问卷有效性测试题：本题请选非常不符合'}
    for code, q in valid_questions.items():
        df = pd.read_csv("data/" + code + ".csv")
        df_f = df[df[q] == "E.非常不符合"]
        df_f.to_csv("data/" + code + "valid.csv")


def filter_education(df, f_prefix="data/valid_samples/随申码_有效_"):
    col = "3.到目前为止，您的最高学历(包括在读)是？"
    picked = ["E.硕士及以上", "D.大学本科"]
    for val in picked:
        df_split = df[df[col] == val]
        df_split.to_csv(f_prefix + val[2:] + ".csv")
    df_remain = df[(df[col]!=picked[0]) & (df[col]!=picked[1])]
    df_remain.to_csv(f_prefix + "本科以下" + ".csv")


def filter_age(df, f_prefix="data/valid_samples/随申码_有效_"):
    """
    20周岁-39周岁为青年。 40周岁-59周岁为中年。 60周岁以上为老年。
    """
    col = "2.您的出生年份是？"
    df_old = df[df[col].str[-5:-1]<= "1962"]
    df_old.to_csv(f_prefix + "老年" + ".csv")
    df_young = df[df[col].str[-5:-1]> "1982"]
    df_young.to_csv(f_prefix + "青年" + ".csv")
    df_middle = df[(df[col].str[-5:-1] > "1962") & (df[col].str[-5:-1]<= "1982")]
    df_middle.to_csv(f_prefix + "中年" + ".csv")


def filter_pudong(df, f_prefix="data/valid_samples/随申码_有效_"):
    col = "5.您常住地所在的地区是？:区"
    df_pudong = df[df[col] == "浦东新区"]
    df_pudong.to_csv(f_prefix + "浦东" + ".csv")
    df_puxi = df[df[col] != "浦东新区"]
    df_puxi.to_csv(f_prefix + "浦东以外" + ".csv")


if __name__ == "__main__":
    df = pd.read_csv("data/valid_samples/随申码valid.csv")

    # split_by_col(df, "7.您使用频率最高的健康码是？")

    # filter_valid()

    # split_by_col(df, "1.您的性别是？", "data/valid_samples/随申码_有效_")
    # filter_education(df)
    # filter_age(df)
    # split_by_col(df, "11.您是否有健康码由绿色转变为其他颜色的经历？", "data/valid_samples/随申码_有效_")
    filter_pudong(df)