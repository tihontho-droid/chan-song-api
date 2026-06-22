from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI(title="Lịch sử Chân Sóng API")

# =========================
# LOAD DATA (Render: load 1 lần khi start)
# =========================
df = pd.read_excel("file_chan_song_cho_mua_mua.xlsx")

df["Ngày"] = pd.to_datetime(df["Ngày"])
df["Ngày tạo đỉnh"] = pd.to_datetime(df["Ngày tạo đỉnh"])


# =========================
# HELPER FORMAT
# =========================
def format_df(data: pd.DataFrame):
    data = data.copy()

    data["Ngày"] = data["Ngày"].dt.strftime("%Y-%m-%d")
    data["Ngày tạo đỉnh"] = data["Ngày tạo đỉnh"].dt.strftime("%Y-%m-%d")

    return data.to_dict(orient="records")


# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {"message": "API Lịch sử Chân Sóng đang chạy"}


# =========================
# GET ALL DATA
# =========================
@app.get("/chan-song")
def get_all():
    return format_df(df)


# =========================
# FILTER THEO NGÀY
# =========================
@app.get("/chan-song/ngay/{ngay}")
def get_by_date(ngay: str):

    ngay = pd.to_datetime(ngay)

    result = df[df["Ngày"] == ngay]

    if result.empty:
        return {"message": "Không có dữ liệu"}

    return format_df(result)


# =========================
# FILTER THEO TÍN HIỆU
# =========================
@app.get("/chan-song/tin-hieu/{tin_hieu}")
def get_by_signal(tin_hieu: str):

    result = df[
        df["Tín hiệu"].str.contains(tin_hieu, case=False, na=False)
    ]

    return format_df(result)


# =========================
# FILTER THEO KHOẢNG NGÀY
# =========================
@app.get("/chan-song/khoang-ngay")
def get_by_range(
    from_date: str = Query(...),
    to_date: str = Query(...)
):

    from_date = pd.to_datetime(from_date)
    to_date = pd.to_datetime(to_date)

    result = df[
        (df["Ngày"] >= from_date) &
        (df["Ngày"] <= to_date)
    ]

    return format_df(result)
