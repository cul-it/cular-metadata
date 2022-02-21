# Cornell University Library Archival Repository Storage Manifest Specification

## Purpose

The CULAR manifest specification consists of two separate files that work in concert to enable collection management tasks and to support workflows that verify the fixity and completeness of packages (and the files that comprise them) within collections.
 
A top-level record uniquely identifies the collection in the CULAR system, links to collection-level identifiers in other library systems, provides a pointer to collection documentation (i.e., non-asset) packages, and specifies key roles for the collection.

A package inventory record links packages with their CULAR collection, uniquely identifies that package within the CULAR system, specifies identifiers that link the package to descriptive, administrative, and/or technical metadata in other library systems. Within each package, file-level metadata provides the date the file was ingested into the CULAR system, basic file identification, filepath, and fixity information.


### Not Included

The CULAR manifests do not include any descriptive metadata, access, or usage rights information.

This information will either be found in the collection level documentation, exist in the package (in some way that we can find by inspecting the package --> [require local standard](https://github.com/cul-it/cular-metadata/issues/13)), or linked through the system identifiers listed above.

## Manifest Specification

### Collection Manifest

| Property  | Requirements | Description | JSON Data Type |
| --------- | ------------ | ----------- | -------------- |
| `collection_id` | required | An identifier that uniquely identifies the collection in the CULAR system. | string |
| `collection_name` | required | A human-readable string representing the name of the collection. | string |
| `collection_bibid` | ????? | The collection-level BibID assigned to the collection. For `MultiSteward/Items`, it will be assigned the value "N/A". | string |
| `collection_archcollnum` | optional | The archival collection number assigned to the collection. | string |
| `collection_documentation` | required | The identifier of the package that contains collection-level documentation. | string |
| `depositing_unit` | required | The depositing unit aligns with the functional collecting areas of the library (e.g., Fine Arts, Rare and Manuscript Collections, Mann Special Collections, Music, Veterinary School, Africana, etc). The depositing unit will be encoded in the manifest in a consistent, agreed-upon way as designated by the CULAR admins (e.g., FineArts, RMC/RMA, RMC/RMM, MannSpecColl, Music, Vet, Africana, etc). | string |
 
### Package Manifest

| Property | Requirements | Description | JSON Data Type |
| -------- | ------------ | ----------- | -------------- |
| `collection_id` | required | The CULAR identifier that is associated with this package. |
| `package_locations` | required | An array of base URI locations where this package is stored. | 
| `package_id` | required | Unique URI identifier for the package. Use UUID in URI form, e.g., `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6` (following [RFC4122](https://tools.ietf.org/html/rfc4122) and [IANA](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml)) for all packages. | string |
| `package_bibid` | optional | Bibliographic record ID this package is associated with, which should be provided if available. (Note that this is not the BibID for the collection as a whole.) | string |
| `package_barcode` | optional | Barcode assigned to the physical manifestation or the physical media carrier of the assets referenced in this package, which should be provided if available. | string |
| `package_medianum` | optional | Media Number assigned to the physical manifestation or the physical media carrier of the assets referenced in this package, which should be provided if available. (Note that this field is primarily associated with the "RMC Media Number".) | string |
| `files` | required | An array of file objects describing each file/object in the manifest. We use `files` even though they are `objects/resources` in some storage technologies. | array | 

#### File Objects

The following defines the file object properties:

| Property | Requirements | Description | JSON Data Type |
| -------- | ------------ | ----------- | -------------- |
| `filepath` | required | Path and filename of the file within the package. The `/` character MUST be used as a path separator (not `\` as it is used on Windows systems). Following [BagIt](https://datatracker.ietf.org/doc/html/rfc8493), if a `filepath` includes a Line Feed (LF), a Carriage Return (CR), a Carriage-Return Line Feed (CRLF), or a percent sign (%), those characters (and only those) MUST be percent-encoded following [RFC3986](https://datatracker.ietf.org/doc/html/rfc3986/). | string | 
| `sha1` | required | SHA-1 hash of data (hex encoded using lowercase alphas, same as output from `sha1sum`, e.g. `021ea82f0468043e81a734b1342b1e64904672b0`). | string |
| `md5` | optional | MD5 hash of data (hex encoded using lowercase alphas, same as output from `md5sum`, e.g. `d41d8cd98f00b204e9800998ecf8427e`), only present if furnished at ingest. | string | 
| `size` | required | Size of the file in bytes. | integer |
| `ingest_date` | required | Date of ingest of the file, expressed as YYYY-MM-DD. | string | 
| `tool_version` | required | String representation of the tool and version of the file identification utility run (e.g., `tika-2.1.0`). | string | 
| `media_type`   | required | The media type of the file referenced by `filepath` using the tool referenced in `tool_version`. | string |



## A note about the manifest workflow

The package manifest is created in two stages. The first stage "ingest manifest" has slightly different requirements which will be described at the end of this document. The specification below outlines the requirements for the "storage manifest", which populates the CULAR administrative interface (AS-IF).

Since the manifest is generated in two stages, there are slightly different requirements for the first stage "ingest manifest" that is supplied for the initial stages of the ingest workflow. Note that some fields required in the "ingest manifest" are not allowed once the deposit has completed and the "storage manifest" has been generated. 

The "ingest manifest" provides detail for what is being furnished for deposit: what files are included, how files are arranged into packages, optional fixity information, and linking collection id. The CULAR application ensures that all files in the source directory are referenced in the "ingest manifest", and only the files referenced in the "ingest manifest" exist in the source directory. The CULAR application generates the "storage manifest" from the "ingest manifest" after the ingest (transfer, fixity check) is complete. For each file referenced in the "ingest manifest", the "storage manifest" populates the `ingest_date`, `tool_version`, and `media_type`. For new collections, the `location` field is added; for existing collections, the `location` field is appended to when appropriate.


### Package (Ingest)
| Property | Requirements | Description (if different from storage manifest) | JSON Data Type |
| -------- | ------------ | -- | -------------- |
| `collection_id` | required | | string |
| `package_locations` | ????? | | null |
| `package_id` | required |  | string |
| `source_path` | required | The CULAR application uses this field to determine the absolute path for each file for transfer | null |
| `package_bibid` | optional |  | string |
| `package_barcode` | optional |  | string |
| `package_medianum` | optional |  | string | 
| `files` | required |  | array |

### File (Ingest)
| Property | Requirements | Description (if different from storage manifest) | JSON Data Type |
| -------- | ------------ | -- | -------------- |
| `filepath` | required |  | string |
| `sha1` | optional |  | string |
| `md5` | optional |  | string |
| `size` | optional |  | string |
| `tool_version` | required | The CULAR application fills in this field during the ingest process | null | 
| `media_type` | required | The CULAR application fills in this field during the ingest process | null |
