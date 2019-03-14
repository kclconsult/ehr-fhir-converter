cp src/mappings.py src/fhir-parser/
cp src/settings.py src/fhir-parser/
cd src/fhir-parser/
touch Default/__init__.py
pip install -r requirements.txt
python generate.py
cp -r downloads ../models-full
touch ../models_full/__init__.py
