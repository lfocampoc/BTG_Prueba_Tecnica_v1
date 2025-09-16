#!/usr/bin/env python3
"""
Script para ejecutar pruebas unitarias
"""
import subprocess
import sys
import os

def run_tests():
    """Ejecuto todas las pruebas"""
    print("🧪 Ejecutando pruebas unitarias...")
    
    # Cambio al directorio del proyecto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Comando para ejecutar pytest
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-fail-under=80"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Todas las pruebas pasaron exitosamente!")
        print("📊 Reporte de cobertura generado en htmlcov/index.html")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Algunas pruebas fallaron. Código de salida: {e.returncode}")
        return False

def run_specific_test(test_file):
    """Ejecuto una prueba específica"""
    print(f"🧪 Ejecutando {test_file}...")
    
    cmd = ["python", "-m", "pytest", f"tests/{test_file}", "-v"]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ {test_file} pasó exitosamente!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {test_file} falló. Código de salida: {e.returncode}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Ejecutar prueba específica
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        # Ejecutar todas las pruebas
        success = run_tests()
    
    sys.exit(0 if success else 1)
