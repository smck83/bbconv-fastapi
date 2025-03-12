## bbenv-fastapi

A fastAPI endpoint to convert B1 codes to B0.

This is useful for Sonos RF Bridge with Tasmota and portisch on it.

Take the B1 code captured via

````
rfaw 177
````

Run via docker;

````
docker run -it -p 8000:8000 smck83/bbconv-fastapi
````

Pass just the code to this API

````
http://localhost:8000/convert?b1_signal=<B1_SIGNAL>
````

Response:

````
{
  "b0_signal": "AA B0 21 03 08 01A4 0492 30B6 28181908181819081819090908190819090909081818181909 55"
}
````
