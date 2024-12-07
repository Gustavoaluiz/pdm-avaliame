import uvicorn
from fastapi import FastAPI, HTTPException
from urllib.parse import unquote
from pydantic import BaseModel
from maps_gustavo import Maps_Scraper

# Modelo de entrada
class ScrapeRequest(BaseModel):
    url: str
    no_interface: bool = False  # Interface gráfica por padrão

# Inicializa o FastAPI
app = FastAPI(debug=True)

@app.post("/scrape")
def scrape(request: ScrapeRequest):
    """
    Endpoint que recebe uma URL do Google Maps e executa o scraping.
    """
    # Decodifica a URL
    url = unquote(request.url)
    no_interface = request.no_interface

    # Valida a URL
    if not url.startswith("https://www.google.com/maps/place"):
        raise HTTPException(
            status_code=400,
            detail="URL inválida. Forneça uma URL válida do Google Maps no formato '/place'.",
        )

    # Inicializa o scraper
    scraper = Maps_Scraper(url=url, no_inteface=no_interface)

    try:
        scraper.start_scrap()
        return {"url": url, "message": "Scraping concluído! Dados salvos em out.csv"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar o scraping: {str(e)}")


@app.get("/")
def home():
    """
    Endpoint básico para verificar se o serviço está funcionando.
    """
    return {"message": "Bem-vindo ao Scraper de Google Maps!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
