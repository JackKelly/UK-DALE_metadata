#!/bin/sh

cp ~/workspace/schemas/nilm_metadata/examples/ukpd_dataset.yaml ukpd_nilm_metadata.yaml

~/workspace/schemas/nilm_metadata/scripts/process.py ukpd_nilm_metadata.yaml -o ukpd_nilm_metadata_concatenated.yaml

echo "Done"
