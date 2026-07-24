# Cornell University Library Archival Repository Storage Manifest Specification

## Overview
This document is part of the publicly available documentation for the Cornell University Library Archival Repository (CULAR). This documentation describes the technical structure the Cornell University Library (CUL) team has chosen to represent the collection material preserved in CULAR. This documentation is aimed at external developers who are interested in understanding the metadata structure developed to represent digital assets in CULAR storage, as well as internal CUL developers who are writing integrations with systems to organize and arrange collection material for deposit. CUL stakeholders directly preparing collections for ingest will want to consult internal documentation to supplement the technical detail offered here. 

All collections in CULAR are represented by a storage manifest. The manifest is a JSON document that includes specific details at the collection, package, and item level for all digital assets deposited into CULAR, independent of the storage that contains them. Various workflows (e.g., fixity, retrieval, administration, analysis, etc.) are supported by this manifest.

The storage manifest includes the following:
* Collection-level properties: Collection level identifier, depositor, steward, and pointer to documentation package
* Package-level properties: Identifiers from a system of record (e.g., FOLIO or ASpace) that pertain to the package
* File-level properties: Fixity value(s), filesize in bytes, date of ingest in CULAR, file identification information

The metadata contained in the storage manifest is indexed and represented in a PostgreSQL database, available to CULAR administrators, select depositors, and select developers assisting in preparing collections for ingest into CULAR.

## Technical detail
The storage manifest is created in two stages. In the first stage, an intermediate form of the manifest, known as the "ingest manifest", lists all the files being furnished for deposit, with optional fixity information for those files (see note in table below); how files are arranged into packages; and basic collection information. The CULAR application ensures that all files in the source directory (as specified in the configuration file for the ingest) are referenced in the ingest manifest and only the files referenced in the ingest manifest exist in the source directory. The CULAR application then updates the `source_path` field so that the absolute path for each file can be determined for transfer. The requirements for this stage of the manifest are listed in the table below, under the column labeled “Ingest Requirements.”

In the second phase, the CULAR application generates the storage manifest from the ingest manifest after the ingest (i.e., transfer and fixity check) is complete. For each file referenced, the CULAR application populates the `ingest_date`, `tool_version`, and `media_type` fields in the storage manifest.

## Examples and schemas
* [Example ingest manifest](examples/INGEST_Depositor_Collection_name.json)
* [Example storage manifest](examples/INGEST_Depositor_Collection_name.json)
* [Ingest manifest schema](schema_ingest_manifest.json)
* [Storage manifest schema](schema_storage_manifest.json)

## Detailed specifications

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

| Property       | Ingest Requirements | Storage Requirements | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `package_id`   | required          | required          | URI identifier for the package. MUST be unique within Cornell collections so that it can be used as the primary key for access to packages. Use UUID in URI form, e.g. `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6` (following [RFC4122](https://tools.ietf.org/html/rfc4122) and [IANA](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml)) for all packages. |
| `source_path`  | required         | not-allowed       | Must be left blank in ingest manifest and is used by ingest code. Value not retained in storage manifest. |
| `bibid`        | optional          | optional          | Bibliographic record id this package is associated with, SHOULD be provided if available. (Note that this value is intended for identifying the bibliographic record of the assets specific to this package, rather than for the collection as a whole.) |
| `local_id`   | optional          | optional            | Physical item identifier, SHOULD be provided by depositor, if available. |
| `files`        | required          | required          | An array of objects describing each file/object in the manifest. We use `files` even though they are `objects/resources` in some storage technologies like AWS S3. |
| `number_files` | optional          | required          | The number of entries in the `files` array, allows self-checking for consistency if present. An integer.|


### File properties

Each object in the `files` array may have the following properties:

| Property       | Ingest Requirements | Storage Requirements | Description | 
|----------------|------------------------------|-------------------------------|-------------|
| `filepath`     | required          | required          | Path and filename of the file within the package. The character `/` MUST be used as a path separator (not `\` as is used on Windows systems). Following Bagit, if a `filepath` includes a Line Feed (LF), a Carriage Return (CR), a Carriage-Return Line Feed (CRLF), or a percent sign (%), those characters (and only those) MUST be percent-encoded following [RFC3986] |
| `sha1`         | optional          | required          | SHA-1 hash of data (hex encoded using lowercase alphas, same as output from `sha1sum`, e.g. `021ea82f0468043e81a734b1342b1e64904672b0`). If present for ingest, it will be verified; otherwise it will be calculated by ingest code. |
| `md5`          | optional          | optional          | MD5 hash of data (hex encoded using lowercase alphas, same as output from `md5sum`, e.g. `d41d8cd98f00b204e9800998ecf8427e`). May or may not be present on ingest, will be verified and retained if present. |
| `size`         | optional          | required          | Size of the file in bytes, an integer value. If not present for ingest, will be calculated by ingest code. |
| `ingest_date`  | not-allowed       | required          | Date of ingest of the file. |
| `tool_version` | required       | required          | Must be left blank in ingest manifest. String representing the tool and version of the file identification utility run. (e.g., `tika-2.1.0`) |
| `media_type`   | required       | required          | Must be left blank in ingest manifest. The media type of the file referenced by `filepath` using the tool referenced in `tool_version`. |


