from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from converter import convert_pdf_to_zip
import tempfile
import os
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.post("/convert/upload")
async def convert_uploaded_file(file: UploadFile = File(...)):
    try:
        suffix = ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_file_path = tmp_file.name

        zip_data = convert_pdf_to_zip(tmp_file_path)
        os.unlink(tmp_file_path)

        return StreamingResponse(io.BytesIO(zip_data), media_type="application/zip", headers={
            "Content-Disposition": f"attachment; filename={file.filename.replace('.pdf','')}_sections.zip"
        })

    except Exception as e:
        logging.error(f"Erro na conversão: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/convert/url")
async def convert_from_url(url: str = Form(...)):
    try:
        zip_data = convert_pdf_to_zip(url, is_url=True)

        filename = url.split("/")[-1].replace('.pdf', '')
        return StreamingResponse(io.BytesIO(zip_data), media_type="application/zip", headers={
            "Content-Disposition": f"attachment; filename={filename}_sections.zip"
        })

    except Exception as e:
        logging.error(f"Erro na conversão por URL: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
