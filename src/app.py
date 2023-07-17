import logging
import os

import numpy as np
import uvicorn
from fastapi import Body, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from prometheus_metric import count_language, language_metrics

log = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
app = FastAPI()


@app.get('/')
async def default():
    """
    Returns a 200 to signal that the server is up.
    """
    return {"status": "ok"}


@app.post("/work/{language}")
@count_language(language_metrics)
async def work(
        language: str,
        body: str = Body(..., media_type='text/plain')
):
    try:
        if not language or language is None:
            language = "en"
        print(language)
        if body:
            zeros = np.zeros((10, 10))
            for i in range(2):
                np.dot(zeros, zeros)
        response = Response(content="calculation successful", status_code=200)
        return response
    except Exception as e:
        return_message = f"Failed with error: {e}"
        raise HTTPException(
            status_code=404, detail=return_message)


def main() -> None:
    log.info(
        f"********************* Ready to Serve on port 8080 ********************")
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
