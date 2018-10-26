cp src/main/python/mappings.py src/main/python/fhir-parser/
cp src/main/python/settings.py src/main/python/fhir-parser/
cd src/main/python/fhir-parser/
touch Default/__init__.py
pip install -r requirements.txt
python generate.py
cp -r downloads ../models-full
touch ../models_full/__init__.py