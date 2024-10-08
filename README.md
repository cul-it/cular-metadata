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

A manifest is a JSON document which includes specific details at the collection, package, and item level for digital asssets deposited into CULAR. At the top-level it is an array of collection objects, each of which has one or more package objects, each of which has one or more file objects.

The manifest is created in two stages. The first stage, the "ingest manifest" lists all of the files being furnished; optionally, fixity information for those files; how files are arranged into packages; and basic collection identification information. At this stage, the CULAR application ensure that all the files in the source directory are referenced in the "ingest manifest", only the files referenced in the "ingest manifest" exist in the source directory, and updates the `source_path` field so that the absolute path for each file can be determined for transfer. The requirements for this stage of the manifest are listed in the table below, under the column labeled "Ingest Requirements".

The CULAR application generates a "storage manifest" from the "ingest manifest" after the ingest (transfer, fixity check) is complete. For each file referenced in the "ingest manifest", the "storage manifest" populates the `ingest_date`, `tool_version`, and `media_type`. Any field listed as optional or not-allowed under "Ingest Requirements" and required under "Storage Requirements" will be filled in during this stage. The requirements for the "storage manifest" are listed in the table below, under the column labeled "Storage Requirements". 

For examples, see [example manifest JSON for ingest](manifest_ingest.json) and [example manifest JSON for storage](manifest_storage.json).

### Collection properties

| Property       | Ingest Requirements | Storage Requirements | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `collection_id`   | required          | required          | The intellectual aggregation as assembled by the steward acting as depositor.  In the case of RMC entities, use Archival Collection IDs. If collection is not archival, but cataloged, use BibID. Must be provided if available. Examples: `RMM06885` (Bolivian Pamphlets), `RMA03590` (Cornell Hockey Films), `5780-156` (Kheel). Primarily letters and numbers, case sensitive, may contain a space, dash or underscore, must not contain a `/`. |
| `depositor`       | required          | required          | The subject area designation driven off the area list and Archival units (`RMC/RMM`, `RMC/RMA`, `Kheel`, `ILR`, `Music`, etc). |
| `steward`         | required          | required          | The netID of the Digital Collection steward. String must match netID pattern. |
| `documentation`          | required          | required          | A pointer to where to find collection-level documentation (i.e., CULAR PID). |
| `packages`        | required         | required            | Array of package objects |
| `number_packages` | optional         | required            | The number of entries in the `packages` array, allows self-checking for consistency if present. An integer. |


### Package properties

Each object in the `packages` array may have the following properties:

| Property       | Required/Optional for Ingest | Required/Optional for Storage | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `package_id`   | required          | required          | URI identifier for the package. MUST be unique within Cornell collections so that it can be used as the primary key for access to packages. Use UUID in URI form, e.g. `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6` (following [RFC4122](https://tools.ietf.org/html/rfc4122) and [IANA](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml)) for all packages. |
| `source_path`  | required         | not-allowed       | Must be left blank in ingest manifest and is used by ingest code. Value not retained in storage manifest. |
| `bibid`        | optional          | optional          | Bibliographic record id this package is associated with, SHOULD be provided if available. (Note that this value is intended for identifying the bibliographic record of the assets specific to this package, rather than for the collection as a whole.) |
| `local_id`   | optional          | optional            | Physical item identifier, SHOULD be provided by depositor, if available. |
| `files`        | required          | required          | An array of objects describing each file/object in the manifest. We use `files` even though they are `objects/resources` in some storage technologies like AWS S3. |
| `number_files` | optional          | required          | The number of entries in the `files` array, allows self-checking for consistency if present. An integer.|


### File properties

Each object in the `files` array may have the following properties:

| Property       | Required/Optional for Ingest | Required/Optional for Storage | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `filepath`     | required          | required          | Path and filename of the file within the package. The character `/` MUST be used as a path separator (not `\` as is used on Windows systems). Following Bagit, if a `filepath` includes a Line Feed (LF), a Carriage Return (CR), a Carriage-Return Line Feed (CRLF), or a percent sign (%), those characters (and only those) MUST be percent-encoded following [RFC3986] |
| `sha1`         | optional          | required          | SHA-1 hash of data (hex encoded using lowercase alphas, same as output from `sha1sum`, e.g. `021ea82f0468043e81a734b1342b1e64904672b0`). If present for ingest, it will be verified; otherwise it will be calculated by ingest code. |
| `md5`          | optional          | optional          | MD5 hash of data (hex encoded using lowercase alphas, same as output from `md5sum`, e.g. `d41d8cd98f00b204e9800998ecf8427e`). May or may not be present on ingest, will be verified and retained if present |
| `size`         | optional          | required          | Size of the file in bytes, an integer value. If not present for ingest, will be calculated by ingest code. |
| `ingest_date`  | not-allowed       | required          | Date of ingest of the file. |
| `tool_version` | required       | required          | Must be left blank in ingest manifest. String representing the tool and version of the file identification utility run. (e.g., `tika-2.1.0`) |
| `media_type`   | required       | required          | Must be left blank in ingest manifest. The media type of the file referenced by `filepath` using the tool referenced in `tool_version`. |
