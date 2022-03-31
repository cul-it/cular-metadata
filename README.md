# Cornell University Library Archival Repository Storage Manifest Specification

## Purpose

The CULAR manifest specification enables collection management tasks and supports workflows that verify the fixity and completeness of packages (and the files that comprise them) within collections.
 
The manifest uniquely identifies the collection in the CULAR system, links to collection-level identifiers in other library systems, provides a pointer to collection documentation (i.e., non-asset) packages, and identifies the depositor of the collection. The manifest additionally uniquely identifies collection packages within the CULAR system, and specifies identifiers that link the package to descriptive, administrative, and/or technical metadata in other library systems. Within each package, file-level metadata provides the date the file was ingested into the CULAR system, basic file identification, filepath, and fixity information.


### Not Included

The CULAR manifest does not include any descriptive metadata, access, or usage rights information. This information will be found in collection-level documentation or [structured within the package itself](https://github.com/cul-it/cular-metadata/issues/13). (See also [fields proposed for local standard](LocalStandard.md)

# Manifest Specification

| Property  | Requirements | Description | JSON Data Type |
| --------- | ------------ | ----------- | -------------- |
| `collection_id` | required | With `depositor`, this uniquely identifies a collection in the CULAR system. This string should be meaningful within the depositor's context. (e.g., an archival collection number or a shortname encoded in an 899 field.) | string |
| `collection_name` | required | The title of the collection, as entered into a system of record. (e.g., the 245 field in the catalog or the collection name in ASpace) Intended for human readability when looking up collections in AS-IF. | string |
| `collection_bibid` | optional | The collection-level BibID assigned to the collection. | string |
| `documentation` | required | The identifier (`package_id`) of the package that contains collection-level documentation. | string |
| `depositor` | required | The depositor aligns with the functional collecting areas of the library (e.g., Fine Arts, Rare and Manuscript Collections, Mann Special Collections, Music, Veterinary School, Africana, etc). The depositor will be encoded in the manifest in a consistent, agreed-upon way as designated by the CULAR admins (e.g., FineArts, RMC/RMA, RMC/RMM, MannSpecColl, Music, Vet, Africana, etc). With `collection_id`, must be a unique value in the CULAR system. | string |
| `locations` | required | An array of base URI locations where this package is stored. | 
| `packages` | required | An array of package objects. |

## Package properties

Each object in the `packages` array may have the following properties:

| Property  | Requirements | Description | JSON Data Type |
| --------- | ------------ | ----------- | -------------- |
| `package_id` | required | Unique URI identifier for the package. Use UUID in URI form, e.g., `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6` (following [RFC4122](https://tools.ietf.org/html/rfc4122) and [IANA](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml)). | string |
| `package_bibid` | optional | Bibliographic record ID this package is associated with, which should be provided if it exists. (This value connects to the package, and not for the collection as a whole.) |
| `package_barcode` | optional | When this package consists of digitized material (defined by the [SAA Dictionary of Archives Terminology](https://dictionary.archivists.org/entry/digitize.html) of a physical item that has a barcode affixed to it (e.g., a book from the circulating collection), supply the barcode value for this field. | string |
| `rmc_media_number` | optional | When this package consists of material digitized from a physical item or transferred from fixed or removable media that is associated with an RMC Media Number, supply that value for this field. | string |
| `physical_media_type` | optional | When this package consists of material digitized from a physical item or transferred from fixed or removable media, this field can capture the physical media format. Should use controlled vocabulary. | string |
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
| `media_type`   | required | The media type (equivalently, the MIME type) of the file referenced by `filepath` using the tool referenced in `tool_version`. | string |



## A note about the manifest workflow

The package manifest is created in two stages. The CULAR application ensures that all files in the source directory are referenced in the "ingest manifest", and only the files referenced in the "ingest manifest" exist in the source directory. The CULAR application generates the finalized manifest from the "ingest manifest" after the ingest (transfer, fixity check) is complete. For each package referenced in the "ingest manifest", the CULAR application will populate `package_locations`. For each file referenced in the "ingest manifest", the CULAR application will populate `ingest_date`, `tool_version`, and `media_type`.

### Elements required for the "ingest manifest"
* `collection_id`
* `source_path` (package); set to null
* `filepath`
* `tool_version` (file); set to null
* `media_type` (file); set to null

