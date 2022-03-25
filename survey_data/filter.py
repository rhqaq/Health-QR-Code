import pandas as pd

code_names = ['西安一码通', '随申码', '北京健康宝', '其他', '苏康码', '粤康码']  # 5个文件名


def filter_data(df, filter_dic):
    """filter_dic字典格式为col:val, 过滤选择col对应列值为val的那些样本"""
    for k, v in filter_dic:
        df = df[df[k] == v]
    return df


def split_by_col(df, col):
    """按某一列分开，每个值的样本为一个csv"""
    for val in df[col].unique():
        df_split = df[df[col] == val]
        df_split.to_csv("data/" + val + ".csv")


def filter_valid():
    """过滤有效性"""
    valid_questions = {'西安一码通': '101.西安一码通基本认知情况:问卷有效性测试题：本题请选非常不符合', '随申码': '10.随申码基本认知情况:问卷有效性测试题：本题请选非常不符合', '北京健康宝': '56.北京健康宝基本认知情况:问卷有效性测试题：本题请选非常不符合', '其他': '119.健康码基本认知情况:问卷有效性测试题：本题请选非常不符合', '苏康码': '35.苏康码基本认知情况:问卷有效性测试题：本题请选非常不符合', '粤康码': '77.粤康码各基本认知情况:问卷有效性测试题：本题请选非常不符合'}
    for code, q in valid_questions.items():
        df = pd.read_csv("data/" + code + ".csv")
        df_f = df[df[q] == "E.非常不符合"]
        df_f.to_csv("data/" + code + "valid.csv")


if __name__ == "__main__":
    # df = pd.read_csv("data/survey.csv")

    # split_by_col(df, "7.您使用频率最高的健康码是？")

    filter_valid()