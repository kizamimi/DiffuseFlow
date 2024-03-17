if not exist "venv" (
    python -m venv venv
    copy init_requirements.txt requirements.txt
)
call venv\\Scripts\\activate.bat

pip freeze > dependencies.txt
fc requirements.txt dependencies.txt
if %errorlevel% == 0 (
    echo OK
) else if %errorlevel% == 1 (
    pip install --upgrade pip
    choice /c ab /m "Select cuda version to use (a: cuda11.8, b: cuda12.1)"
    if %errorlevel% == 1 (
        pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        pip3 install -U xformers --index-url https://download.pytorch.org/whl/cu118
    ) else if %errorlevel% == 2 (
        pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        pip3 install -U xformers --index-url https://download.pytorch.org/whl/cu121
    ) else (
        del dependencies.txt
        call venv\\Scripts\\deactivate.bat
        exit /b 2
    )
    pip install -r requirements.txt
    pip install streamdiffusion[tensorrt]
    
    choice /c yn /m "Do you use TensorRT? (y: yes, n: no)"
    if %errorlevel% == 1 (
        python -m streamdiffusion.tools.install-tensorrt
    )
    pip install --force-reinstall pywin32
    pip freeze > requirements.txt
) else (
    del dependencies.txt
    call venv\\Scripts\\deactivate.bat
    exit /b 1
)
del dependencies.txt

python basic.py

call venv\\Scripts\\deactivate.bat
@REM pause