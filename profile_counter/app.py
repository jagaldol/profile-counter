from xml.sax.saxutils import escape

import redis
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

redis_client = redis.Redis(host="profile-counter-redis", port=6379, decode_responses=True)


PLACES = 7

SVG_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}px" height="30px" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <title>Count</title>
    <defs>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        {parts}
    </g>
</svg>"""


DIGIT_TEMPLATE = """
<rect fill="#000000" x="{x}" width="29" height="29"></rect>
<text font-family="Courier" font-size="24" fill="#00FF13" filter="url(#glow)">
    <tspan x="{text_x}" y="22">{digit}</tspan>
</text>"""


def make_svg(count: int) -> str:
    count_array = str(count).zfill(PLACES)
    parts = "".join(
        DIGIT_TEMPLATE.format(x=index * 32, text_x=index * 32 + 7, digit=escape(d))
        for index, d in enumerate(count_array)
    )
    return SVG_TEMPLATE.format(width=PLACES * 32, parts=parts)


@app.get("/{key}/count.svg")
def get_svg(key: str):
    try:
        count = redis_client.get(key)
        if count is None:
            count = "1"
        else:
            count = str(int(count) + 1)

        redis_client.set(key, count)
        svg = make_svg(int(count))

        return Response(
            content=svg,
            media_type="image/svg+xml",
            headers={"Cache-Control": "max-age=0, no-cache, no-store, must-revalidate"},
        )
    except Exception as e:
        print("Error:", e)
        return Response(content="Internal Server Error", status_code=500)


@app.get("/{key}/")
def get_count(key: str):
    try:
        count = redis_client.get(key)
        if count is None:
            count = "0"

        return JSONResponse(content={"key": key, "count": count})
    except Exception as e:
        print("Error:", e)
        return Response(content="Internal Server Error", status_code=500)


if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
