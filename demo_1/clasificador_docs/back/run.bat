@echo off
echo =====================================================
echo   EJECUTANDO CLASIFICADOR DE DOCUMENTOS
echo =====================================================

echo.
echo Activando entorno virtual...
call .venv\Scripts\activate

echo.
echo Ejecutando servidor FastAPI...
echo Servidor disponible en: http://localhost:8000
echo Documentacion API: http://localhost:8000/docs
echo.

cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
