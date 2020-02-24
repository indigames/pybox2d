@echo off

SET LIB_NAME=Box2D

echo COMPILING PC...
SET PROJECT_DIR=%~dp0..

SET BUILD_DIR=%PROJECT_DIR%\build\pc
SET OUTPUT_DIR=%PROJECT_DIR%\igeLibs\%LIB_NAME%
SET OUTPUT_HEADER=%OUTPUT_DIR%\include
SET OUTPUT_LIBS_DEBUG=%OUTPUT_DIR%\libs\Debug\pc
SET OUTPUT_LIBS_RELEASE=%OUTPUT_DIR%\libs\Release\pc

if not exist %OUTPUT_DIR% (
    mkdir %OUTPUT_DIR%
)

echo Cleaning up...
    if exist %OUTPUT_HEADER% (
        rmdir /s /q %OUTPUT_HEADER%
    )
    mkdir %OUTPUT_HEADER%

    if exist %BUILD_DIR% (
        rmdir /s /q %BUILD_DIR%
    )
    mkdir %BUILD_DIR%
    
    if exist %OUTPUT_LIBS_DEBUG% (
        rmdir /s /q %OUTPUT_LIBS_DEBUG%
    )
    mkdir %OUTPUT_LIBS_DEBUG%

    if exist %OUTPUT_LIBS_RELEASE% (
        rmdir /s /q %OUTPUT_LIBS_RELEASE%
    )
    mkdir %OUTPUT_LIBS_RELEASE%

echo Fetching include headers...
    xcopy /h /i /c /k /e /r /y %~dp0..\Box2D\*.h %OUTPUT_HEADER%\Box2D\
   
cd %PROJECT_DIR%
echo Compiling x86...
    if not exist %BUILD_DIR%\x86 (
        mkdir %BUILD_DIR%\x86
    )
    cd %BUILD_DIR%\x86
    echo Generating x86 CMAKE project ...
    cmake %PROJECT_DIR% -A Win32
    if %ERRORLEVEL% NEQ 0 goto ERROR

    echo Compiling x86 - Debug...
    cmake --build . --config Debug -- -m
    if %ERRORLEVEL% NEQ 0 goto ERROR
    xcopy /q /e /y Debug\*.lib %OUTPUT_LIBS_DEBUG%\x86\
    xcopy /q /e /y Debug\*.dll %OUTPUT_LIBS_DEBUG%\x86\

    echo Compiling x86 - Release...
    cmake --build . --config Release -- -m
    if %ERRORLEVEL% NEQ 0 goto ERROR
    xcopy /q /e /y Release\*.lib %OUTPUT_LIBS_RELEASE%\x86\
    xcopy /q /e /y Release\*.dll %OUTPUT_LIBS_RELEASE%\x86\
echo Compiling x86 DONE

cd %PROJECT_DIR%
echo Compiling x64...
    if not exist %BUILD_DIR%\x64 (
        mkdir %BUILD_DIR%\x64
    )
    echo Generating x64 CMAKE project ...
    cd %BUILD_DIR%\x64
    cmake %PROJECT_DIR% -A x64
    if %ERRORLEVEL% NEQ 0 goto ERROR

    echo Compiling x64 - Debug...
    cmake --build . --config Debug -- -m
    if %ERRORLEVEL% NEQ 0 goto ERROR
    xcopy /q /e /y Debug\*.lib %OUTPUT_LIBS_DEBUG%\x64\
    xcopy /q /e /y Debug\*.dll %OUTPUT_LIBS_DEBUG%\x64\

    echo Compiling x64 - Release...
    cmake --build . --config Release -- -m
    if %ERRORLEVEL% NEQ 0 goto ERROR
    xcopy /q /e /y Release\*.lib %OUTPUT_LIBS_RELEASE%\x64\
    xcopy /q /e /y Release\*.dll %OUTPUT_LIBS_RELEASE%\x64\
echo Compiling x64 DONE

goto ALL_DONE

:ERROR
	echo ERROR OCCURED DURING COMPILING

:ALL_DONE
	cd %PROJECT_DIR%
	echo COMPILING PC DONE!