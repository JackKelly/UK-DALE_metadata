#!/bin/sh

cp ~/workspace/schemas/nilm_metadata/examples/UK-DALE_dataset.yaml UK-DALE_nilm_metadata.yaml

~/workspace/schemas/nilm_metadata/scripts/process.py UK-DALE_nilm_metadata.yaml -o UK-DALE_nilm_metadata_concatenated.yaml

echo "Done"
