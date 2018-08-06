# New Archival Storage Manifest Proposal

See [example manifest JSON](new_manifest_proposal.json).

A manifest is a JSON document, at the top-level it is an array of collection objects, each of which has one or more package objects, each of which has one or more file objects. 

## Collection properties

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `collection_id`   | required          | The intellectual aggregation as assembled by the steward acting as depositor.  In the case of RMC entities, use Archival Collection IDs. If collection is not archival, but cataloged, use BibID. Must be provided if available. Examples: `RMM06885` (Bolivian Pamphlets), `RMA03590` (Cornell Hockey Films), `5780-156` (Kheel). Primarily letters and numbers, case sensitive, may contain a space, dash or underscore, must not contain a `/`. |
| `depositor`    | required          | The subject area designation driven off the area list and Archival units (`RMC` (`RMA` is not a separate depositor), `Kheel`, `ILR`, `Music`). Letters and numbers only, must not contain a `/`. |
| `steward`      | optional          | The netID of the Digital Collection steward. Must be provided if available and is expected in most cases. [Policy describing items without formal collection affiliation](https://confluence.cornell.edu/x/rRI2FQ) is the only situation where a steward would not be identified at this level |
| `locations` | optional             | An array of base URI locations where every package in this collection is stored or to be stored. There may be additional `locations` specified at the package level. May not be present when assembling a manifest for ingest. |
| `packages` | required         | Array of package objects |
| `number_packages` | optional         | The number of entries in the `packages` array, allows self-checking for consistency if present. An integer. |


## Package properties

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `package_id`   | required          | URI-like identifier for the package. Must be unique within Cornell collections and is the primary key for access to packages. |
| `bibid`        | optional          | Bibliographic record id this package is associated with, SHOULD be provided if available. |
| `rmcmediano`   | optional          | RMC media number, SHOULD be provided if available. |
| `locations`    | optional          | An array of base URI locations where every file in this package is stored or to be stored. May not be present when assembling a manifest for ingest. |
| `files`        | required          | An array of objects describing each file/object in the manifest. We use `files` even though they are `objects/resources` in some storage technologies like AWS S3. |
| `number_files` | optional          | The number of entries in the `files` array, allows self-checking for consistency if present. An integer. |

## File properties

Inside the `files` array, each object may have the following properties:

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `filename`     | required          | Name of the file/object. MUST not contain `/` (FIXME - define other illegal chars) |
| `path`         | required          | Path of item within package. The filepath within the package is constructed by appending the filename to the path with an appropriate path separator. |

| `sha1`         | required          | SHA-1 hash of data (hex encoded using lowercase alphas, same as output from sha1sum, e.g. "021ea82f0468043e81a734b1342b1e64904672b0"). We require this for every item. |
| `md5`          | optional          | MD5 hash of data (hex encoded using lowercase alphas, same as output from md5sum, e.g. `d41d8cd98f00b204e9800998ecf8427e`) |
| `size`         | required          | Size of the file in bytes, an integer value. |

For any item the set of locations where it is stored is determined by the union of the `locations` for the collection and the `locations` for the specific package.

