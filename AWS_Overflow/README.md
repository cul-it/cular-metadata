# CULAR AWS Punting Plan

## JSON Model / Profile for the AWS Overflow Plan

### Collection

field                   | definition | external mapping | obligation | notes
---                     | ---        | ---              | ---        | ---
Collection Name         | Name of the _Digital Collection_ being preserved. | dcterms:title | {1,1} | Take from consistent source. Digitization spreadsheet? MARC Bib title?
Physical Collection ID  | Name of the _Analog Collection_ that was the source of the Digital Collection being preserved. | dcterms:source | {0,1} | Take from consistent source. MARC Bib title preferred.
Number of Files         | Number of files (not items, files) in the Digital Collection. | dcterms:extent | {1,1} | Used primarily for verification purposes of data consistency.
Collection Steward      | netID of the Digital Collection steward. | marcrel: ?? | {1,1} | Should be decided pre-digitization or pre-preservation.
Date of AWS Ingest      | Date when the Digital Collection was loaded into AWS. | ?? | {1,1} |
Date of Last AWS Update | Date when the Digital Collection was last updated in AWS. | ?? | {0,1} |
Items                   | Items (map to analog items conceptual level) contained in the Digital Collection. | dcterms:hasPart | {1,n} | More structural than anything else.

### Items (Item Subdirectories)

Items is a holder dictionary/wrapper for all items in a collection. Item Subdirectories are dictionaries that represent the item itself, which may be captured in multiple binary forms (i.e. an Item could be represented by multiple files).

field               | definition | external mapping | obligation | notes
---                 | ---        | ---              | ---        | ---
Item Subdirectory   | The identifier / base of the filename for the item at the discrete, analog item level or at the descriptive metadata (MARC Bibliographic Record) conceptualization. | dcterms:identifier | {1,1} | Note, this conceptualization does vary. Make best efforts at capturing what is meant by item, and document in the project documentation where this varies significantly.
Filename            | The filename for each file that is a representation of the item. Includes the filename with extension. | dcterms:title | {1,1} |

### Files / Filename-level

field            | definition                     | external mapping    | obligation | notes
---              | ---                            | ---                 | ---        | ---
Video Identifier | Identifier for the video file. | dcterms:identifier? | {1,1}      | Make more generic identifier than just for videos?
Bibliographic ID | Analog bibliographic record ID | dcterms:source      | {0,1}  | Ignore "e-bibs" for now? Not always present?
Part Number      | If the Item is represented by multiple parts (reels of a recording, for example), capture the part number here. | find the ons:number pred. | {0,1} | Required if used.
MD5              | MD5 hash of data.              | ??                  | {1,1}      |
Size             | Size of the file in bytes.     | ebucore:fileSize    | {1,1}      | Capture the integer alone (no units).

### Sample:

```json
{
    "Collection Name": {
        "phys_coll_id": "bib|archival|other (required if available)",
        "number_files": "int (required if available)",
        "steward": "netID (required if available)",
        "date_s3_ingest": "YYYY-MM-DD (auto-generated)",
        "date_s3_update": "YYYY-MM-DD (auto-generated)",
        "items": {
            "item_subdir": {
                "filename" : {
                    "video_number": "video id (required if available)",
                    "bib_id": "bibliographic record id (required if available)",
                    "part_num": "int (if applicable)",
                    "md5": "hash (strongly recommended when available)",
                    "size": "int (strongly recommended when available)"
                    }
            }
        }
    }
}
```

## JSON Manifest File Generation
In this subdirectory are attempts at generation scripts of JSON manifests for collections being prepped for AWS CULAR Overflow from hashdeep manifest files.

Included in this folder are:
* `hashdeep_to_json.py`: python script that generates JSON from hashdeep and user-supplied input
* `mathtest.txt`: dummy hashdeep file for testing purposes
* `math_json_draft.txt`: sample output from `hashdeep_to_json.py` and `mathtest.txt`
* `previous_drafts`: older attempts, kept for historical purposes only

