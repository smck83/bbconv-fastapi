from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="RF Signal Converter",
    description="API for converting B1 RF signals to B0 format for SonOff bridges",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class B1Signal(BaseModel):
    signal: str
    repeats: Optional[int] = 8

def convert_b1_to_b0(b1_input: str, repeats: int = 8) -> str:
    """
    Efficiently convert a B1 RF signal to B0 format.
    
    Args:
        b1_input: A string containing the B1 format RF signal
        repeats: Number of times to repeat the signal (default: 8)
        
    Returns:
        A string containing the B0 format RF signal
    """
    # Clean input by removing spaces and extracting just the relevant part
    clean_input = b1_input.replace(' ', '')
    
    # Find the start and end positions of the B1 data
    start_pos = clean_input.find('AAB1')
    end_pos = clean_input.rfind('55')
    
    if start_pos == -1 or end_pos == -1:
        raise ValueError("Invalid B1 signal format. Must contain 'AAB1' and end with '55'")
    
    # Extract the relevant B1 data
    b1_data = clean_input[start_pos:end_pos+2]
    
    # Get the number of buckets
    num_buckets = int(b1_data[4:6], 16)
    
    # Start building the B0 output
    bucket_info = f"{num_buckets:02X} {repeats:02X} "
    
    # Extract the bucket values
    for i in range(num_buckets):
        start_idx = 6 + i * 4
        end_idx = 10 + i * 4
        bucket_info += b1_data[start_idx:end_idx] + " "
    
    # Extract the data portion (after the bucket definitions)
    data_start_idx = 6 + num_buckets * 4
    data_portion = b1_data[data_start_idx:-2]
    
    # Combine all parts to form the B0 command
    data_str = (bucket_info + data_portion).replace(" ", "")
    length = len(data_str) // 2
    
    # Format the final B0 output
    b0_output = f"AA B0 {length:02X} {bucket_info}{data_portion} 55"
    
    return b0_output

@app.get("/")
async def root():
    return {
        "message": "RF Signal Converter API",
        "usage": {
            "GET /convert": "Convert B1 to B0 using query parameters",
            "POST /convert": "Convert B1 to B0 using JSON body",
            "GET /convert-plain": "Convert B1 to B0 and return plain text"
        }
    }

@app.get("/convert")
async def convert_get(b1_signal: str, repeats: int = 8):
    """
    Convert a B1 signal to B0 format using GET method
    """
    try:
        b0_signal = convert_b1_to_b0(b1_signal, repeats)
        return {"b0_signal": b0_signal}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing signal: {str(e)}")

@app.post("/convert")
async def convert_post(request: B1Signal):
    """
    Convert a B1 signal to B0 format using POST method
    """
    try:
        b0_signal = convert_b1_to_b0(request.signal, request.repeats)
        return {"b0_signal": b0_signal}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing signal: {str(e)}")

@app.get("/convert-plain")
async def convert_plain(b1_signal: str, repeats: int = 8):
    """
    Convert a B1 signal to B0 format and return as plain text
    """
    try:
        return convert_b1_to_b0(b1_signal, repeats)
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error: {str(e)}"

