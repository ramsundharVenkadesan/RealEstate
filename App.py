# File: app.py (Modified Version)
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from Pipeline import run_full_pipeline

# 1. Setup FastAPI
app = FastAPI(
    title="Real Estate Data Pipeline API",
    description="A service to scrape, analyze, and plot real estate data based on an input area."
)


# 2. Define Request Body Model
class AreaRequest(BaseModel):
    area: str = "tempe"  # Default example area


# 3. Define the directory to store/retrieve generated files
FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


# 4. API Endpoint: Run the Pipeline and Return File
@app.post("/run-pipeline/download-plot")
def run_pipeline_and_download(request: AreaRequest):
    """
    Triggers the full data pipeline (Scrape -> Analyze -> Plot) synchronously.
    Returns the generated JPEG plot file as a direct download response upon completion.
    """
    area_name = request.area.lower().strip()

    if not area_name:
        raise HTTPException(status_code=400, detail="Area name cannot be empty.")

    print(f"\n[API] Starting synchronous pipeline for area: {area_name}")

    # --- Execute the Pipeline ---
    # Call the synchronous pipeline function from pipeline.py
    result = run_full_pipeline(area_name)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    # The pipeline was successful, now prepare to return the file
    plot_filename = result["plot_file"]
    file_path = os.path.join(FILE_DIRECTORY, plot_filename)

    # Final check for the file
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline succeeded, but generated file '{plot_filename}' was not found at expected path."
        )

    print(f"[API] Pipeline finished. Returning file: {plot_filename}")

    # FileResponse handles setting the correct headers for download
    return FileResponse(
        path=file_path,
        media_type="image/jpeg",
        filename=plot_filename,
        # The 'Content-Disposition: attachment' header forces a download dialog
    )


