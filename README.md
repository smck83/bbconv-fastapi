## bbenv-fastapi

A fastAPI endpoint to convert B1 codes to B0.

This is useful for Sonos RF Bridge with Tasmota and portisch on it.

Take the B1 code captured via

````
rfaw 177
````

Pass just the code to this API

````
http://localhost:8000/convert?b1_signal=<B1_SIGNAL>
````
