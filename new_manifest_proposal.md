# New Archival Storage Manifest Proposal

## Purpose

The primary purpose is to support workflows that move and copy packages (and the files that comprise them), replicate them, and verify their fixity and completeness.

The secondary purpose is to enable some very basic management tasks, for which we need to know ownership/stewardship information (see `collection_id`, `depository`, `steward`), and links to external descriptions and rights information (see `bibid`, `rmcmediano`, `rights`). More sophisticated management tasks will rely on other services and on descriptive and technical metadata not included in the manifest.

## Descriptive and technical metadata

Manifests will not include descriptive and technical metadata, this will be either:
  
  1. in the package (in some way that we can find by inspecting the package --> [require local standard](https://github.com/cul-it/cular-metadata/issues/13))
  2. in a linked reference system (connected via `bibid`, `rmcmediano` and/or `package_id`)

Other services (e.g. disovery, dissemination) will need to extract/access this information to understand the item type, its metadata, etc..

## Access and usage rights information

Manifests will not include access and usage rights information, they will link to such information via the collection level `rights` property. We expect this information to change more frequently than the packages themselves. It may be managed as a separate package, or in another system (for example, the archival collection management system is expected to be the authoritative source of such information for RMC content).

## Manifest format

A manifest is a JSON document. At the top-level it is an array of collection objects, each of which has one or more package objects, each of which has one or more file objects. See [example manifest JSON](new_manifest_proposal.json).

### Collection properties

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `collection_id`   | required          | The intellectual aggregation as assembled by the steward acting as depositor.  In the case of RMC entities, use Archival Collection IDs. If collection is not archival, but cataloged, use BibID. Must be provided if available. Examples: `RMM06885` (Bolivian Pamphlets), `RMA03590` (Cornell Hockey Films), `5780-156` (Kheel). Primarily letters and numbers, case sensitive, may contain a space, dash or underscore, must not contain a `/`. |
| `depositor`    | required          | The subject area designation driven off the area list and Archival units (`RMC` (`RMA` is not a separate depositor), `Kheel`, `ILR`, `Music`). Letters and numbers only, must not contain a `/`. |
| `steward`      | optional          | The netID of the Digital Collection steward. Must be provided if available and is expected in most cases. [Policy describing items without formal collection affiliation](https://confluence.cornell.edu/x/rRI2FQ) is the only situation where a steward would not be identified at this level |
| `rights`       | required          | A pointer to where to find access and usage rights information. For RMC material where information is held in the archival collection management system the value will be `archival_cms`, other values might be a `package_id`. We may want to add extra special values in the future. |
| `locations` | optional             | An array of base URI locations where every package described in this manifest in this collection is stored or to be stored. There may be additional `locations` specified at the package level. Specification at the collection level is essentially a short-hand to avoid repetition for every package. May not be present when assembling a manifest for ingest. |
| `packages` | required         | Array of package objects |
| `number_packages` | optional         | The number of entries in the `packages` array, allows self-checking for consistency if present. An integer. |


### Package properties

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `package_id`   | required          | URI identifier for the package. MUST be unique within Cornell collections so that it can be used as the primary key for access to packages. Current proposal is to use UUID in URI form, e.g. `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6` (following [RFC4122](https://tools.ietf.org/html/rfc4122) and [IANA](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml)) for all packages. [Need to validate this choice](https://github.com/cul-it/cular-metadata/issues/14) |
| `bibid`        | optional          | Bibliographic record id this package is associated with, SHOULD be provided if available. |
| `rmcmediano`   | optional          | RMC media number, SHOULD be provided if available. |
| `locations`    | optional          | An array of base URI locations where every file in this package is stored or to be stored. May not be present when assembling a manifest for ingest. |
| `files`        | required          | An array of objects describing each file/object in the manifest. We use `files` even though they are `objects/resources` in some storage technologies like AWS S3. |
| `number_files` | optional          | The number of entries in the `files` array, allows self-checking for consistency if present. An integer. |

### File properties

Inside the `files` array, each object may have the following properties:

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `filename`     | required          | Name of the file/object. MUST not contain `/` (FIXME - define other illegal chars) |
| `path`         | required          | Path of item within package. The filepath within the package is constructed by appending the filename to the path with an appropriate path separator. |
| `sha1`         | required          | SHA-1 hash of data (hex encoded using lowercase alphas, same as output from `sha1sum`, e.g. `021ea82f0468043e81a734b1342b1e64904672b0`). We require this for every item. |
| `md5`          | optional          | MD5 hash of data (hex encoded using lowercase alphas, same as output from `md5sum`, e.g. `d41d8cd98f00b204e9800998ecf8427e`) |
| `size`         | required          | Size of the file in bytes, an integer value. |

For any package, the set of locations where it is stored is determined by the union of the set of `locations` for the collection and the set of `locations` for the specific package.
