# New Archival Storage Manifest Proposal

See [example manifest JSON](new_manifest_proposal.json).

A manifest is a JSON document, at the top-level it is an array of collection objects, each of which has one or more package objects, each of which has one or more file objects. 

## Collection properties

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `collection_id`   | required          | The intellectual aggregation as assembled by the steward acting as depositor.  In the case of RMC entities, use Archival Collection IDs. If collection is not archival, but cataloged, use BibID. Must be provided if available. Q - what are formatting restrictions? Can this include `/` as in [`RMM/RMM01234` example](https://confluence.cornell.edu/display/CULREPO/Archival+Storage+Collection+Manifests)? |
| `depositor`    | required          | The subject area designation driven off the area list and Archival units (`RMC`, `Kheel`). Letters and numbers only, must not contain a `/`. Q - is depositor the right name? |
| `steward`      | optional          | The netID of the Digital Collection steward. Must be provided if available and is expected in most cases. [Policy describing items without formal collection affiliation](https://confluence.cornell.edu/x/rRI2FQ) is the only situation where a steward would not be identified at this level |
| `packages` | required         | Array of package objects |
| `number_packages` | optional         | The number of entries in the `packages` array, allows self-checking for consistency if present. An integer. |


## Package properties

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `package_id`   | required          | URI-like identifier for the package |
| `locations`    | optional          | An array of base URI locations where every item in this section of the manifest is stored or to be stored. May not be present when assembling a manifest for ingest. |
| `files`        | required          | An array of objects describing each file/object in the manifest. Q - would `items` be better if we are talking about both files on SFS and objects in S3? Then `number_files` would presumably become `number_items` too. |
| `number_files` | optional          | The number of entries in the `files` array, allows self-checking for consistency if present. An integer. |

## File properties

Inside the `files` array, each object may have the following properties:

| Property       | Required/Optional | Description | 
|----------------|-------------------|-------------|
| `filename`     | required          | Name of the file/object. Q - what restrictions do we place on the name? No '/' at least? |
| `path`         | required          | Path of item within package. The filepath within the package is constructed by appending the filename to the path with an appropriate path separator. |
| `locations`    | optional          | Specific base URI locations where this item is stored. |
| `bibid`        | optional          | Bibliographic record id this item is associated with. Rrequired if available. |
| `rmcmediano`   | optional          | RMC media number. Required if available. Q - Can this be generalized? It seems unfortunate to have a field specific to one depositor. Are there likely to be other similar ids? |
| `sha1`         | required          | SHA-1 hash of data (hex encoded using lowercase alphas, same as output from sha1sum, e.g. "021ea82f0468043e81a734b1342b1e64904672b0"). We require this for every item. |
| `md5`          | optional          | MD5 hash of data (hex encoded using lowercase alphas, same as output from md5sum, e.g. `d41d8cd98f00b204e9800998ecf8427e`) |
| `size`         | required          | Size of the file in bytes, an integer value. |

The combination of (`depositor`,`collection`,`path`,`filename`) provides a unique identity for an item within CUL Archival Storage.

For any item the set of locations where it is stored is determined by the union of the `locations` for the collection and the `locations` for the specific item.

