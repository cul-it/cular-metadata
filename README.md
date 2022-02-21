# Cornell University Library Archival Repository Storage Manifest Specification

## Purpose

The CULAR manifest specification consists of two separate files that work in concert to enable collection management tasks and to support workflows that verify the fixity and completeness of packages (and the files that comprise them) within collections.
 
A top-level record uniquely identifies the collection in the CULAR system, links to collection-level identifiers in other library systems, provides a pointer to collection documentation (i.e., non-asset) packages, and specifies key roles for the collection.

A package inventory record links packages with their CULAR collection, uniquely identifies that package within the CULAR system, specifies identifiers that link the package to descriptive, administrative, and/or technical metadata in other library systems. Within each package, file-level metadata provides the date the file was ingested into the CULAR system, basic file identification, filepath, and fixity information.


### Not Included

The CULAR manifests do not include any descriptive metadata, access, or usage rights information. This information will either be found in the collection level documentation or exist in the package (in some way that we can find by inspecting the package --> [require local standard](https://github.com/cul-it/cular-metadata/issues/13)). [Fields proposed for local standard](LocalStandard.md)

# Manifest Specification
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
| `package_physical_media_type` | optional | For items digitized or copied from a physical media object. Uses controlled vocabulary. |
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

The package manifest is created in two stages. The CULAR application ensures that all files in the source directory are referenced in the "ingest manifest", and only the files referenced in the "ingest manifest" exist in the source directory. The CULAR application generates the finalized manifest from the "ingest manifest" after the ingest (transfer, fixity check) is complete. For each package referenced in the "ingest manifest", the CULAR application will populate `package_locations`. For each file referenced in the "ingest manifest", the CULAR application will populate `ingest_date`, `tool_version`, and `media_type`.

### Elements required for the "ingest manifest"
* `collection_id`
* `source_path` (package); set to null
* `filepath`
* `tool_version` (file); set to null
* `media_type` (file); set to null

