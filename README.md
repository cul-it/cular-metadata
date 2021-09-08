# Cornell University Library Archival Repository Storage Manifest Specification

## Purpose

The primary purpose is to support workflows that move and copy packages (and the files that comprise them), replicate them, and verify their fixity and completeness.

The secondary purpose is to enable some very basic management tasks, for which we need to know ownership/stewardship information (see `collection_id`, `depository`, `steward`), links to system identifiers and collection documentation (see `bibid`, `local_id`, `documentation`), and basic file information (see `size`, `ingest_date`, `filetype`). More sophisticated management tasks will rely on other services and on descriptive and technical metadata not included in the manifest.

## Descriptive and technical metadata

Manifests will not include descriptive and certain technical metadata, this will be either:
  
  1. in the package (in some way that we can find by inspecting the package --> [require local standard](https://github.com/cul-it/cular-metadata/issues/13))
  2. in a linked reference system (connected via `bibid`, `local_id` and/or `package_id`)

Other services (e.g. disovery, dissemination) will need to extract/access this information to understand more extensive item and file metadata.

## Access and usage rights information

Manifests will not include access and usage rights information, they will link to such information via the collection level `documentation` property. At this point, we are not providing machine-actionable, item-level or package-level rights information for collection assets. 

## Manifest format

A manifest is a JSON document. At the top-level it is an array of collection objects, each of which has one or more package objects, each of which has one or more file objects. See [example manifest JSON for ingest](manifest_ingest.json) and [example manifest JSON for storage](manifest_storage.json).

### Collection properties

| Property       | Required/Optional for Ingest | Required/Optional for Storage | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `collection_id`   | required          | required          | The intellectual aggregation as assembled by the steward acting as depositor.  In the case of RMC entities, use Archival Collection IDs. If collection is not archival, but cataloged, use BibID. Must be provided if available. Examples: `RMM06885` (Bolivian Pamphlets), `RMA03590` (Cornell Hockey Films), `5780-156` (Kheel). Primarily letters and numbers, case sensitive, may contain a space, dash or underscore, must not contain a `/`. |
| `depositor`       | required          | required          | The subject area designation driven off the area list and Archival units (`RMC/RMM`, `RMC/RMA`, `Kheel`, `ILR`, `Music`, etc). |
| `steward`         | required          | required          | The netID of the Digital Collection steward. |
| `documentation`          | required          | required          | A pointer to where to find collection-level documentation (i.e., CULAR PID). |
| `locations`       | not-allowed             | required             | An array of base URI locations where every package described in this manifest in this collection is stored or to be stored. There may be additional `locations` specified at the package level. Specification at the collection level is essentially a short-hand to avoid repetition for every package.|
| `packages`        | required         | required            | Array of package objects |
| `number_packages` | optional         | required            | The number of entries in the `packages` array, allows self-checking for consistency if present. An integer. If not present for ingest, will be filled in before storage |


### Package properties

Each object in the `packages` array may be the following properties:

| Property       | Required/Optional for Ingest | Required/Optional for Storage | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `package_id`   | required          | required          | URI identifier for the package. MUST be unique within Cornell collections so that it can be used as the primary key for access to packages. Use UUID in URI form, e.g. `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6` (following [RFC4122](https://tools.ietf.org/html/rfc4122) and [IANA](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml)) for all packages. |
| `source_path`  | required         | not-allowed       | Must be left blank in ingest manifest and is used by ingest code. Value not retained in storage manifest. |
| `bibid`        | optional          | optional          | Bibliographic record id this package is associated with, SHOULD be provided if available. (Note that this value is intended for identifying the bibliographic record of the assets specific to this package, rather than for the collection as a whole. Records identified in MARC as collection records are highly discouraged at this level.) |
| `local_id`   | optional          | optional            | Physical item identifier, SHOULD be provided by depositor, if available. |
| `files`        | required          | required          | An array of objects describing each file/object in the manifest. We use `files` even though they are `objects/resources` in some storage technologies like AWS S3. |
| `number_files` | optional          | required          | The number of entries in the `files` array, allows self-checking for consistency if present. An integer. If not present for ingest, will be filled in before storage |

### File properties

Each object in the `files` array may have the following properties:

| Property       | Required/Optional for Ingest | Required/Optional for Storage | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `filepath`     | required          | required          | Path and filename of the file within the package. The character `/` MUST be used as a path separator (not `\` as is used on Windows systems). Following Bagit, if a `filepath` includes a Line Feed (LF), a Carriage Return (CR), a Carriage-Return Line Feed (CRLF), or a percent sign (%), those characters (and only those) MUST be percent-encoded following [RFC3986] |
| `sha1`         | optional          | required          | SHA-1 hash of data (hex encoded using lowercase alphas, same as output from `sha1sum`, e.g. `021ea82f0468043e81a734b1342b1e64904672b0`). We require this for every item. If present for ingest, it will be verified; otherwise it will be calculated by ingest code |
| `md5`          | optional          | optional          | MD5 hash of data (hex encoded using lowercase alphas, same as output from `md5sum`, e.g. `d41d8cd98f00b204e9800998ecf8427e`). May or may not be present on ingest, will be verified and retained if present |
| `size`         | optional          | required          | Size of the file in bytes, an integer value. If not present for ingest, will be filled in before storage |
| `ingest_date`  | not-allowed       | required          | Date of ingest of the file |
| `filetype`     | not-allowed       | required          | An array supplying file identification information for each file object.|

### Filetype properties

Each object in the `filetype` array may have the following properties:
| Property       | Required/Optional for Ingest | Required/Optional for Storage | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `id_tool`      | not-allowed  | required | The name and version of the tool supplying the MIME/Media Type for the file|
| `media_type`   | not-allowed | required | The Media Type (MIME Type) of the file, as determined by the tool referenced in `id_tool` |


For any package, the set of locations where it is stored is determined by the union of the set of `locations` for the collection and the set of `locations` for the specific package.
