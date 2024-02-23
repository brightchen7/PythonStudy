import datetime
import time
from itertools import product
from client_examples.client_example import Client
import cx_Oracle
import pandas as pd
import requests

print("===正在生成Excel表")
start_time = time.process_time()
# DataService接口
base_url = "http://10.110.13.221:8061"
headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}
# WindDB接口
winddb_url = "RSWINDDB/Abc123@192.168.142.83:1521/van"
conn = cx_Oracle.connect(winddb_url)

def QueryTradingDay(exact_day, offset):
    # exact_day是标准日，offset是偏置，求偏置的交易日
    url = base_url + "/calendar/trading_day_query/ml"
    body = {"base_day": exact_day, "offset": offset}
    response = requests.get(url=url, headers=headers, params=body)
    return response.json()["message"]

def QueryIndustry(list_tickers_code):
    url = base_url + "/data_service/get_citics_industry"
    body = {"tickers": list_tickers_code}
    response = requests.post(url, headers=headers, data=body)
    return {
        item["S_INFO_WINDCODE"]: item["CITICS_IND_NAME"]
        for item in response.json()
        if item is not None
    }

def Wind2Code(wind):
    if "." in wind:
        number, market = wind.split(".")
        code = market + number
        return code
    else:
        return wind

def QuerySector(code):
    if code.startswith("60"):
        return "上交所主板"
    elif code.startswith("688"):
        return "上交所科创板"
    elif code.startswith("00"):
        return "深交所主板"
    elif code.startswith("30"):
        return "深交所创业板"
    elif code.startswith("8") or code.startswith("4"):
        return "北交所"
    else:
        return "未知板块"

def get_trade_days(exact_day, day_nums):
    # 返回exact_day开始往前推共day_nums天(包含exact_day)的收盘价
    query = f"""
        SELECT * FROM (
            SELECT DISTINCT TRADE_DAYS
            FROM WINDDF.ASHARECALENDAR
            WHERE TRADE_DAYS <= '{exact_day}'
            ORDER BY TRADE_DAYS DESC
        ) WHERE ROWNUM <= {day_nums}
    """
    return pd.read_sql(query, conn)

def get_period_close_price(trade_days_series, stock_list_base_date):
    # 返回stock_list_base_date的各股票在trade_days_series的收盘价
    query = f"""
        SELECT TRADE_DT, S_INFO_WINDCODE, S_DQ_CLOSE
        FROM WINDDF.ASHAREEODPRICES
        WHERE TRADE_DT 
        IN ({",".join(["'" + date + "'" for date in trade_days_series])})
    """
    df = pd.read_sql(query, conn)
    dit = df.set_index(["TRADE_DT", "S_INFO_WINDCODE"])["S_DQ_CLOSE"].to_dict()
    query = f"""
        SELECT S_INFO_WINDCODE
        FROM WINDDF.AShareEODPrices
        WHERE TRADE_DT = '{stock_list_base_date}'
    """
    stock_df = pd.read_sql(query, conn)
    stock_date_combination = list(product(stock_df["S_INFO_WINDCODE"], trade_days_series))
    df = pd.DataFrame(stock_date_combination, columns=["S_INFO_WINDCODE", "TRADE_DAYS"])
    df = df.sort_values(["S_INFO_WINDCODE", "TRADE_DAYS"]).reset_index(drop=True)
    df["close"] = df.set_index(["TRADE_DAYS", "S_INFO_WINDCODE"]).index.map(dit)
    return df

if __name__ == "__main__":
    print("-->获取交易日信息")
    url = base_url + "/calendar/trading_day_check/ml"
    today = datetime.datetime.now().strftime("%Y%m%d")
    body = {"base_day": today}
    response = requests.get(url, headers=headers, params=body)
    if response.json()["message"]:
        if datetime.datetime.now().time() < datetime.time(hour=15, minute=41, second=0):
            url = base_url + "/calendar/trading_day_query/ml"
            body = {"base_day": today, "offset": -1, }
            response = requests.get(url, headers=headers, params=body)
            curr_trade_date = response.json()["message"]
        else:
            curr_trade_date = today
    prev_trade_date = QueryTradingDay(curr_trade_date, -1)
    next_trade_date = QueryTradingDay(curr_trade_date, 1)

    print("-->获取股票代码和简称")
    query = "SELECT S_INFO_WINDCODE, S_INFO_NAME FROM WINDDF.AShareDescription"
    code_name_df = pd.read_sql(query, conn)
    name_dict = code_name_df.set_index("S_INFO_WINDCODE")["S_INFO_NAME"].to_dict()

    print("-->获取收盘价")
    query = f"""
        SELECT S_INFO_WINDCODE, S_DQ_CLOSE
        FROM WINDDF.AShareEODPrices
        WHERE TRADE_DT = '{curr_trade_date}'
    """
    new_df = pd.read_sql(query, conn)
    new_df = new_df.rename(columns={"S_INFO_WINDCODE": "万得代码", "S_DQ_CLOSE": "现价(元)"})

    print("-->获取MA, EMA, 距离目标价等衍生行情数据")
    print("   注: 非空样本占比大于1/3的才计算移动平均")
    trade_days = get_trade_days(curr_trade_date, 11)
    df = get_period_close_price(trade_days['TRADE_DAYS'], curr_trade_date)
    df["MA10"] = (df.groupby("S_INFO_WINDCODE")["close"]
             .rolling(window=10, min_periods=10//3).mean().values)
    close = (df.loc[df.TRADE_DAYS==curr_trade_date]
             .set_index("S_INFO_WINDCODE")["close"].to_dict())
    ma_today = (df.loc[df.TRADE_DAYS==curr_trade_date]
             .set_index("S_INFO_WINDCODE")["MA10"].to_dict())
    ma_yes = (df.loc[df.TRADE_DAYS==prev_trade_date]
             .set_index("S_INFO_WINDCODE")["MA10"].to_dict())
    ma_next = {key: (ma_today[key] - ma_yes[key]) * 2 + ma_today[key] for key in ma_today}
    距离目标价1 = {key: (1 - ma_next[key]) / close[key] for key in ma_today}
    trade_days = get_trade_days(curr_trade_date, 20)
    df = get_period_close_price(trade_days['TRADE_DAYS'], curr_trade_date)
    df["EMA20"] = (df.groupby("S_INFO_WINDCODE")["close"]
            .transform(lambda x: x.ewm(span=20, min_periods=20//3).mean()))
    expma_today = (df.loc[df.TRADE_DAYS==curr_trade_date]
             .set_index("S_INFO_WINDCODE")["EMA20"].to_dict())
    距离目标价2 = {key: (1 - expma_today[key]) / close[key] for key in ma_today}
    trade_days = get_trade_days(curr_trade_date, 110)
    trade_days["TRADE_DAYS"] = pd.to_datetime(trade_days["TRADE_DAYS"])
    trade_days = trade_days.sort_values("TRADE_DAYS").reset_index(drop=True)
    trade_days = trade_days.set_index("TRADE_DAYS").resample("W-Fri").last().reset_index()
    week_date_series = (trade_days['TRADE_DAYS'].dt
             .strftime("%Y%m%d")[-20:].reset_index(drop=True))
    df = get_period_close_price(week_date_series, curr_trade_date)
    df["EMA20_weekly"] = (df.groupby("S_INFO_WINDCODE")["close"]
             .transform(lambda x: x.ewm(span=20, min_periods=20//3).mean()))
    expma_weekly = df.groupby("S_INFO_WINDCODE")["EMA20_weekly"].last().to_dict()
    距离目标价3 = {key: (1 - expma_weekly[key]) / close[key] for key in ma_today}

    new_df["股票简称"] = new_df["万得代码"].map(name_dict)
    new_df = new_df[["万得代码", "股票简称", "现价(元)"]]
    new_df[prev_trade_date+"(MA10)"] = new_df["万得代码"].map(ma_yes).round(2)
    new_df[curr_trade_date+"(MA10)"] = new_df["万得代码"].map(ma_today).round(2)
    new_df[next_trade_date+"(MA10)"] = new_df["万得代码"].map(ma_next).round(2)
    new_df["距离目标价1"] = new_df["万得代码"].map(距离目标价1).round(4)
    new_df[curr_trade_date+"(EMA20)"] = new_df["万得代码"].map(expma_today).round(2)
    new_df["距离目标价2"] = new_df["万得代码"].map(距离目标价2).round(4)
    new_df[curr_trade_date+"(EMA20_weekly)"] = new_df["万得代码"].map(expma_weekly).round(2)
    new_df["距离目标价3"] = new_df["万得代码"].map(距离目标价3).round(4)
    
    print("-->获取行业, 代码, 板块")
    dict_industry = QueryIndustry(list(new_df.万得代码))
    df_industry = pd.DataFrame(list(dict_industry.items()), columns=["万得代码", "所属行业"])
    industry_dict = df_industry.set_index("万得代码")["所属行业"].to_dict()
    new_df["所属行业"] = new_df["万得代码"].map(industry_dict)
    new_df["Code"] = new_df.apply(lambda row: Wind2Code(row["万得代码"]), axis=1)
    new_df["Sector"] = new_df.apply(lambda row: QuerySector(row["万得代码"]), axis=1)
    
    print("-->获取5/10/20/30日涨跌幅")
    trade_days = get_trade_days(curr_trade_date, 31)
    for i in [5, 10, 20, 30]:
        query = f"""
            SELECT S_INFO_WINDCODE, S_DQ_CLOSE
            FROM WINDDF.AShareEODPrices
            WHERE TRADE_DT = '{trade_days["TRADE_DAYS"][i]}'
        """
        df = pd.read_sql(query, conn)
        dit = df.set_index("S_INFO_WINDCODE").to_dict()["S_DQ_CLOSE"]
        new_df[f"{i}D涨跌幅"] = new_df["万得代码"].map(dit)
        new_df[f"{i}D涨跌幅"] = ((new_df["现价(元)"] - new_df[f"{i}D涨跌幅"]) 
                 / new_df[f"{i}D涨跌幅"]).round(4)

    print("-->数据存入excel")
    new_df.to_excel(f"股票汇总数据_{curr_trade_date}.xlsx", index=False)
    end_time = time.process_time()
    print(f"===总耗时: {round(end_time-start_time, 2)}s")

    client = Client()
    relative_url = "/mail"
    user = "EQD_EDS_Notice"
    credential = "cIccBJhello2023!"
    sender = "EQD_EDS_Notice@cicc.com.cn"
    address = "Xiaorui.Dong@cicc.com.cn"

    attach_path = f".//股票汇总数据_{curr_trade_date}.xlsx"

    res = client.post(
        relative_url,
        data={
            "user": user,
            "credential": credential,
            "to": address,
            "subject": f"股票汇总数据-{curr_trade_date}",
            "html_body": '',
            "from": sender,
            "cc": address,
            "attach_path": attach_path
        },
    )
