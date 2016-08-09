# CULAR

## Scope

CULAR Metadata stuff. Primarily a place for [Christina](mailto:cmh329@cornell.edu) to dump metadata documentation, data, and code (or other) before pushing to the CULAR team for ingest into their documentation/application/etc.

# CULAR Structure Presently (Metadata viewpoint)

See the CULAR IT documentation [on their Cornell Confluence Wiki (CUL staff only)](https://confluence.cornell.edu/pages/viewpage.action?pageId=109222702). CULAR pushes to a Fedora 3 repository (and then has other backups, copies, storage options triggered - this is out of scope for these metadata notes). You can see the proposed 2012 CULAR Data Model (as of 2012, seems still relevant) on [this internal documentation page](https://confluence.cornell.edu/display/CULREPO/CULAR+Data+Model). This seems to have not been followed.

## CULAR Object Structure

### Resource == Digital Assets to be Archived (usually collection of resources)

The resource as a whole being pushed to CULAR. It appears resources are pushed to CULAR as 'collections' in a broad sense. Resources could also be files within a 'collection', but minimal level descriptive/administrative/structural metadata is captured about these files (we just know that file/resource belongs to this other collection/resource through Fedora 3 RELS-EXT predicates).

### Resource DC/XML Datastream == Basic CULAR Metadata

The basic DC metadata captured for the resource going into CULAR. May or may not be derived from the Descriptive Metadata File linked to the Resource. Validated against OAI-DC XSD, meaning it just checks if it is a bunch of simple DC elements in a OAI-DC:DC wrapper record (no obligation checks or datapoint validations done).

Need to pull out fields to see what is captured where/what is auto-generated from Fedora 3.


### Bitstream == Descriptive Metadata File (usually at the digital assets collection level)

EAD XML file of some sort, usually. Not validated, parsed, checked, etc. May also be a collection-level MARC record (or could be?).

### File Technical (PREMIS/XML) Datastream == Technical Metadata from various Tools (DROID, JHove?, Other?)

The technical metadata for the file as harvested from various preservation or repository file-check tools. Primarily pulled from DROID. Not the DROID output as XML (though that may be captured elsewhere?). The fields captured:

Field | DROID Property | DROID Definition | CULAR PREMIS Property | CULAR PREMIS Definition
--- | --- | --- | --- | --- | ---
Filename | ?? | The name of a file, folder or archival file is its name, independent of its location on a disk or inside an archival file. It includes any file name extension as part of its name. DROID treats all filenames as case-sensitive. For example, “MYDOCUMENT.DOC” and “mydocument.doc” are regarded as different file names. | dc:title {1,1} or premis:originalName | The name of the object as submitted to or harvested by the repository, before any renaming by the repository.
Alternative Filename | ?? | n/a | 
Identifier |
Repository |
Collection |
Extension |
MIME Type |
File size |
PUID |
DROID Provenance |
Signature File Provenance |
Format Information |
Method |
