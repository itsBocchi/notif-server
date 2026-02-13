#!/usr/bin/env python
"""
Script para ejecutar las pruebas unitarias del sistema
"""
import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notif_server.settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    print("🧪 Ejecutando pruebas unitarias del sistema de alertas...")
    print("=" * 60)
    
    failures = test_runner.run_tests(["api.tests"])
    
    if failures:
        print(f"\n❌ {failures} prueba(s) fallaron")
        sys.exit(1)
    else:
        print("\n✅ Todas las pruebas pasaron exitosamente!")
        print("🎉 El sistema está funcionando correctamente")