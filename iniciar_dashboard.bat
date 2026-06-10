@echo off
echo ========================================================
echo  Iniciando o Servidor Local para o Dashboard de Treino
echo ========================================================
echo.
echo Tentando abrir no navegador em http://localhost:8000...
start http://localhost:8000

echo.
echo Tentando usar o Python...
python -m http.server 8000
if %errorlevel% equ 0 exit

echo.
echo Python falhou. Tentando usar o Node.js (npx)...
call npx http-server -p 8000 -c-1
if %errorlevel% equ 0 exit

echo.
echo [ERRO] Nao foi possivel iniciar o servidor.
echo Para rodar localmente, instale o Python ou o Node.js, 
echo ou utilize a extensao "Live Server" no VS Code.
pause
