ukpd_metadata
=============

Metadata for my UK Power Dataset

The data itself can be found at http://www.doc.ic.ac.uk/~dk3810/data

There are three files in this repository:

* **ukpd_ukerc_edc_metadata.yaml** is the metdata for the UK Energy
  Research Council (UKERC)
  [Energy Data Centre](http://ukedc.rl.ac.uk/) (EDC).
  The schema for this metadata can be found
  [here](http://ukedc.rl.ac.uk/format.html).
* **ukpd_nilm_metadata.yaml** is the detailed metadata describing each
  appliance and meter using the schema defined by the
  [nilm_metadata](https://github.com/nilmtk/nilm_metadata) project.
  This file is the 'minimal' version which has not been merged
  ('concatenated') with the objects stored in the
  [nilm_metadata](https://github.com/nilmtk/nilm_metadata) project.
* **ukpd_nilm_metadata_concatenated.yaml** contains all the info from
  the file above as well as all the related info from the
  [nilm_metadata](https://github.com/nilmtk/nilm_metadata) project.
