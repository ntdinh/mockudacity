from flask import Flask
import os
from glob import glob
import importlib


def registerRoutes(app: Flask):
    rootPkgPath = 'src/features'
    for pkgPath in glob(f'{rootPkgPath}/*'):
        if os.path.isdir(pkgPath):
            pkgUri = pkgPath.replace('/', '.')
            pkg = importlib.import_module(pkgUri)
            app.register_blueprint(pkg.feature)
