from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

LOTTO_API_URL_LOTTO = "https://www.lotto.pl/api/lotteries/draw-results/by-gametype?game=Lotto&index=1&size=100&sort=drawDate&order=DESC"
LOTTO_API_URL_EUROJACKPOT = "https://www.lotto.pl/api/lotteries/draw-results/by-gametype?game=EuroJackpot&index=1&size=100&sort=drawDate&order=DESC"

@app.get("/", response_class=HTMLResponse)
async def get_lotto_results(request: Request):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        response_lotto = requests.get(LOTTO_API_URL_LOTTO, headers=headers)
        response_eurojackpot = requests.get(LOTTO_API_URL_EUROJACKPOT, headers=headers)

        response_lotto.raise_for_status()
        response_eurojackpot.raise_for_status()

        data_lotto = response_lotto.json()
        data_eurojackpot = response_eurojackpot.json()

        lotto_results = []
        for item in data_lotto.get("items", []):
            draw_date = datetime.strptime(item.get("drawDate"), "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y")
            draw_results = []
            for draw in item.get("results", []):
                game_type = draw.get("gameType")
                numbers = sorted(draw.get("resultsJson", []))
                draw_results.append({"gameType": game_type, "numbers": numbers})
            lotto_results.append({"drawDate": draw_date, "drawResults": draw_results})

        eurojackpot_results = []
        for item in data_eurojackpot.get("items", []):
            draw_date = datetime.strptime(item.get("drawDate"), "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y")
            draw_results = []
            for draw in item.get("results", []):
                game_type = draw.get("gameType")
                numbers = sorted(draw.get("resultsJson", []))
                special_numbers = sorted(draw.get("specialResults", []))
                draw_results.append({"gameType": game_type, "numbers": numbers, "specialNumbers": special_numbers})
            eurojackpot_results.append({"drawDate": draw_date, "drawResults": draw_results})

        return templates.TemplateResponse("lotto_results.html", {"request": request,
                                                                 "lotto_results": lotto_results,
                                                                 "eurojackpot_results": eurojackpot_results})

    except requests.exceptions.RequestException as e:
        print("Wystąpił błąd podczas pobierania danych Lotto:", e)
        raise HTTPException(status_code=500, detail="Error fetching lotto results") from e
