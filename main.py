from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI(title="Chan Song API")

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("file_chan_song_cho_mua_mua.xlsx")

df["Ngày"] = pd.to_datetime(df["Ngày"])
df["Ngày tạo đỉnh"] = pd.to_datetime(df["Ngày tạo đỉnh"])


# =========================
# REQUEST MODEL (GIỐNG STOCKTRADERS)
# =========================
class ChanSongRequest(BaseModel):
    account: str
    from_date: str = None
    to_date: str = None


class RequestBody(BaseModel):
    ChanSongRequest: ChanSongRequest


# =========================
# HELPER FORMAT
# =========================
def format_df(data):
    data = data.copy()
    data["Ngày"] = data["Ngày"].dt.strftime("%Y-%m-%d")
    data["Ngày tạo đỉnh"] = data["Ngày tạo đỉnh"].dt.strftime("%Y-%m-%d")
    return data.to_dict(orient="records")


# =========================
# POST API (GIỐNG STOCKTRADERS)
# =========================
@app.post("/service/data/getChanSong")
def get_chan_song(req: RequestBody):

    from_date = req.ChanSongRequest.from_date
    to_date = req.ChanSongRequest.to_date

    result = df.copy()

    # lọc theo ngày nếu có
    if from_date:
        result = result[result["Ngày"] >= pd.to_datetime(from_date)]

    if to_date:
        result = result[result["Ngày"] <= pd.to_datetime(to_date)]

    return {
        "account": req.ChanSongRequest.account,
        "total_rows": len(result),
        "data": format_df(result)
    }
