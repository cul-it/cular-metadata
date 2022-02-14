# Cornell University Library Archival Repository Storage Manifest Specification

## Purpose

The CULAR manifest specification primarily supports workflows that verify the fixity and completeness of packages (and the files that comprise them) within collections: `filepath`, `sha1`, `md5`, `size`, `number_files`, `number_packages`

The manifest also enables select management tasks; data from the manifest is aggregated and stored in an administrative system to support collection-, depositor-, and system-wide querying.

At the collection level, this includes:
* Identification of collection in both CULAR and other library systems: `collection_id`, `collection_ref_bibid`, `collection_ref_aspace`
* Storage locations for packages in the collection: `locations`
* Pointer to collection documentation (i.e., non-asset) packages: `documentation`
* Identification of key roles for the collection, including depositor, stewardship, and technical administrative responsibility: `depositor`, `collection_steward`, `depositor_admin`

At the package level, this includes:
* The unique identification of the package within the CULAR system: `package_id`
* Identifiers that link the package to descriptive, administrative, and/or technical metadata in other library systems: `package_ref_bibid`, `package_ref_barcode`, `package_ref_medianum`


At the file level, this includes:
* The date the file within the package was ingested into the CULAR system: `ingest_date`
* Basic file identification for the file in the package: `media_type`, `tool_version`

### Not Included

The CULAR manifest itself does not include any descriptive metadata, access, or usage rights information.

This information will either be found in the collection level documentation, exist in the package (in some way that we can find by inspecting the package --> [require local standard](https://github.com/cul-it/cular-metadata/issues/13)), or linked through the system identifiers listed above.

## Manifest Specification

### A note about the manifest workflow

The manifest is created in two stages. The first stage "ingest manifest" has slightly different requirements which will be described at the end of this document. The specification below outlines the requirements for the "storage manifest", which populates the CULAR administrative interface (AS-IF).

### Collection

| Property  | Requirements | Description | JSON Data Type |
| --------- | ------------ | ----------- | -------------- |
| `collection_id` | required | The intellectual aggregation as assembled by the collection steward and/or depositor manager. This name is typically human-readable, with underscores in place of spaces. | string |
| `collection_ref_bibid` | required | The collection-level BibID assigned to the collection. For `MultiSteward/Items`, it will be assigned the value "N/A". | string |
| `collection_ref_aspace` | optional | The archival collection ID assigned to the collection (e.g., `RMM06885` or `RMA03590`.) | string |
 | `depositor` | required | The depositor is a conceptual entity that alignes with the functional collecting areas of the library (e.g., Fine Arts, Rare and Manuscript Collections, Mann Special Collections, Music, Veterinary School, Africana, etc). The depositor will be encoded in the manifest in a consistent, agreed-upon way as designated by the CULAR admins (e.g., FineArts, RMC/RMA, RMC/RMM, MannSpecColl, Music, Vet, Africana, etc). | string |
 | `depositor_admin` | optional | A depositor may identify an individual who provides technical and administrative management of all of the collections under its purview. If identified, this value stores the netid of the individual in this role. | string (must match netID pattern) |
 | `collection_steward` | required | The collection steward provides information and consultation about the content of the collection. This value stores the netid of the individual in this role. | string (must match netID pattern) |
 | `documentation` | required | The CULAR PID of the package that contains collection-level documentation. | string |
 | `locations` | required | An array of base URI locations where every package in this manifest is stored. | array |
 | `number_pacakges` | required | The number of entries in the `packages` array; allows self-checking for consistency if present. | integer |
 | `packages` | required | An array of package objects (see Package properties, below). | array |
 

### Package

The following defines the package object properties:

| Property | Requirements | Description | JSON Data Type |
| -------- | ------------ | ----------- | -------------- |
| `package_id` | required | Unique URI identifier for the package. Use UUID in URI form, e.g., `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6` (following [RFC4122](https://tools.ietf.org/html/rfc4122) and [IANA](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml)) for all packages. | string |
| `package_ref_bibid` | optional | Bibliographic record ID this package is associated with, which should be provided if available. (Note that this is not the BibID for the collection as a whole.) | string |
| `package_ref_barcode` | optional | Barcode assigned to the physical manifestation or the physical media carrier of the assets referenced in this package, which should be provided if available. | string |
| `package_ref_medianum` | optional | Media Number assigned to the physical manifestation or the physical media carrier of the assets referenced in this package, which should be provided if available. (Note that this field is primarily associated with the "RMC Media Number".) | string |
| `number_files` | required | The number of entries in the `files` array, allows self checking for consistency of present. | integer |
| `files` | required | An array of file objects describing each file/object in the manifest. We use `files` even though they are `objects/resources` in some storage technologies. | array | 

### File

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


## Manifest Workflow

Since the manifest is generated in two stages, there are slightly different requirements for the first stage "ingest manifest" that is supplied for the initial stages of the ingest workflow. Note that some fields required in the "ingest manifest" are not allowed once the deposit has completed and the "storage manifest" has been generated. 

The "ingest manifest" provides detail for what is being furnished for deposit: what files are included, how files are arranged into packages, optional fixity information, and collection metadata. The CULAR application ensures that all files in the source directory are referenced in the "ingest manifest", and only the files referenced in the "ingest manifest" exist in the source directory. The CULAR application generates the "storage manifest" from the "ingest manifest" after the ingest (transfer, fixity check) is complete. For each file referenced in the "ingest manifest", the "storage manifest" populates the `ingest_date`, `tool_version`, and `media_type`. For new collections, the `location` field is added; for existing collections, the `location` field is appended to when appropriate.

### Collection (Ingest)

| Property | Requirements | Description (if different from storage manifest) | JSON Data Type |
| -------- | ------------ | -- | -------------- |
| `collection_id` | required |  | string | 
| `collection_ref_bibid` | required |  | string | 
| `collection_ref_aspace` | optional |  | string | 
| `depositor` | required |  | string | 
| `depositor_admin` | optional |  | string |
| `collection_steward` | required |  | string | 
| `documentation` | required |  | string |
| `number_pacakges` | optional |  | integer |
| `packages` | required |  | array |

### Package (Ingest)
| Property | Requirements | Description (if different from storage manifest) | JSON Data Type |
| -------- | ------------ | -- | -------------- |
| `package_id` | required |  | string |
| `source_path` | required | The CULAR application uses this field to determine the absolute path for each file for transfer | null |
| `package_ref_bibid` | optional |  | string |
| `package_ref_barcode` | optional |  | string |
| `package_ref_medianum` | optional |  | string | 
| `number_files` | optional |  | integer |
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
