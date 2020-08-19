# -*-coding:utf-8-*-
import pandas as pd

from talib import func
import baostock as bs
import tushare as ts


class Macd:
    @staticmethod
    def _format(df):
        df.rename(
            columns={
                'date': 'Date',
                'code': 'Code',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close'
            },
            inplace=True)
        # 转换为日期格式
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
        # 将日期列作为行索引
        df.set_index(['Date'], inplace=True)
        return df

    @staticmethod
    def get_data_from_tushare(code, freq="M"):
        token = "ff8d8b472dec1fbe4d332a2e2e0898aefdd50a502e7bac35f2d411d1"
        ts.set_token(token)
        df = ts.pro_bar(ts_code=code, adj='qfq', freq=freq, start_date='20150101', end_date='20200710')
        print(df)
        # return df

    @staticmethod
    def calculate_macd(df):
        """
        DIFF: macd = 12 天 EMA - 26 天 EMA
        DEA:  macdsignal = 9 天 MACD的EMA
        MACD: macdhist = MACD - MACD signal
        #todo 需要修正 前复权
        ts.get_hist_data('600848', ktype='W') #获取周k线数据
        ts.get_hist_data('600848', ktype='M') #获取月k线数据
        """
        df['close'] = df['close'].apply(lambda x: round(float(x), 4))
        close = df.close.values
        try:
            df['dif'], df['dea'], df['macd'] = func.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
            return df[['date', 'close', 'dif', 'dea', 'macd']]
        except:
            return pd.DataFrame()

    @staticmethod
    def get_daily_macd(code):
        bs.login()
        rs = bs.query_history_k_data_plus(code,
                                          "date,code,open,high,low,close",
                                          frequency="d",
                                          adjustflag="2")

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        daily = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        d_df = Macd.calculate_macd(daily)
        if not d_df.empty:
            return d_df.tail(7)
        else:
            return pd.DataFrame()

    @staticmethod
    def get_monthly_data(code, frequency="m", adjustflag="2"):
        lg = bs.login()
        rs = bs.query_history_k_data_plus(code,
                                          "date,code,open,high,low,close",
                                          # start_date=start_date,
                                          # end_date=end_date,
                                          frequency=frequency,
                                          adjustflag=adjustflag)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        monthly = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        d_df = Macd.calculate_macd(monthly)
        return d_df.tail(7)


if __name__ == '__main__':
    df = Macd.get_monthly_data('sh.600760')
    print(df)
