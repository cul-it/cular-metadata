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

Field | DROID Property | DROID Definition | CULAR PREMIS Property | CULAR PREMIS Definition/Notes
--- | --- | --- | --- | --- | ---
Filename | IdentificationFile/FilePath [text after last \ or /] | The name of a file, folder or archival file is its name, independent of its location on a disk or inside an archival file. It includes any file name extension as part of its name. DROID treats all filenames as case-sensitive. For example, “MYDOCUMENT.DOC” and “mydocument.doc” are regarded as different file names. | dc:title {1,1} or premis:originalName | The name of the object as submitted to or harvested by the repository, before any renaming by the repository.
Alternative Filename | n/a | n/a | dct:alternative {0,n} or ?? (separate PREMIS record) | The object may have other names in different contexts. When two repositories are exchanging content, it would be important for the receiving repository to know and record the name of the Intellectual Entity or Representation at the originating repository. In the case of IEs or representations, this may be a directory name.
Identifier | n/a | n/a | dc:identifier or premis:objectIdentifier/[premis:objectIdentifierType {1,n} | premis:objectIdentifierValue] | A designation used to identify the Object uniquely within the preservation repository system in which it is stored.
Repository | n/a | n/a | dc:relation or premis:storage/premis:contentLocation/premis:contentLocationValue | The reference to the location of the content used by the storage system.
Collection | n/a | n/a | n/a | captured through Fedora RELS-EXT
Extension | n/a | File extensions are a convention to indicate the broad type of a file (or archival file) by appending a short string to a file name, separated by a full stop. DROID converts all file extensions it extracts to lower case, to facilitate sorting, reporting and filtering. | dc:format or premis:objectCharacteristics/premis:format/premis:formatName | A commonly accepted name for the format of the file or bitstream.
MIME Type | IdentificationFile/MimeType | The mime-type is another scheme for identifying broad types of files in use on the internet. They are assigned by a body called the Internet Assigned Numbers Authority. Mime-types are quite broad classifications, so many different file formats will have the same mime-type. | dc:type or premis:objectCharacteristics/premis:format/premis:formatDesignation/[formatName='value' & formatVersion='IANA MIME Type'] | A commonly accepted name for the format of the file or bitstream. And the version of the format named in formatName. (here, just MIME Type)
File size | n/a | The size of a file or archival file is recorded as the number of bytes used by the file. Files can have a size of zero (no content, just a record in the file system). Folders do not have a size. The size of an archival file is the size of the archival file itself, not the sum of the sizes of its contents. For example, zip files compress their contents, so the sum of the sizes of the files inside a zip file will be bigger than the size of the archival file itself. | dct:extent or premis:objectCharacteristics/premis:size | The size in bytes of the file or bitstream stored in the repository.
PUID | IdentificationFile/PUID | The PUID is a globally unique, persistent identifier for a file format and version, assigned by the National Archives through its PRONOM file format registry. | premis:objectCharacteristics/premis:format/premis:formatDesignation/[formatName='value' & formatVersion='PUID'] | N/A
DROID Provenance |  n/a | n/a | dc:note or getting into premis:agents +linking/relationships | A commonly accepted name for the format of the file or bitstream. And the version of the format named in formatName. 
Signature File Provenance | ?? | ?? | dct:provenance or premis:signatureInformation/premis:signature/premis:signatureProperties | Additional information about the generation of the signature.
Format Information | ?? | ?? | dct:provenance or premis:objectcharacteristics/premis:format/premis:formatNote | Additional information about format.
Method | ?? | ?? | dc:source | method of technical metadata information?
