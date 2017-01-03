Just dumping for now the full template to be made into a profile doc:


{
    "Collection Name": {
        "phys_coll_id": "bib|archival|other", (required if available)
        "number_files": int, (required if available)
        "steward": "netID", (required if available)
        "date_s3_ingest": YYYY-MM-DD, (auto-generated)
        "date_s3_update": YYYY-MM-DD, (auto-generated)
        "items": {
            "item_subdir": {
                "filename" : {
                    "video_number": "video id", (required if available)
                    "bib_id": "bibliographic record id", (required if available)
                    "part_num": int, (if applicable)
                    "md5": hash (strongly recommended when available)
                    "size": int (strongly recommended when available)
                    }
            }
        }
    }
}