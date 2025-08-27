@echo off
echo =====================================================
echo   INSTALACION DEL ENTORNO - CLASIFICADOR DE DOCS
echo =====================================================

echo.
echo Creando entorno virtual...
python -m venv .venv

echo.
echo Activando entorno virtual...
call .venv\Scripts\activate

echo.
echo Actualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando dependencias...
pip install fastapi uvicorn[standard] transformers torch PyMuPDF docx2txt sqlite-utils pandas numpy scikit-learn nltk python-multipart pydantic

echo.
echo =====================================================
echo   INSTALACION COMPLETADA
echo =====================================================
echo.
echo Para activar el entorno virtual en el futuro:
echo   .venv\Scripts\activate
echo.
echo Para ejecutar la aplicacion:
echo   cd app
echo   python main.py
echo   o
echo   uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
pause
