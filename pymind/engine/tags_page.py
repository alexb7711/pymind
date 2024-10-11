"""!
@file tags_page.py
@package Tags Page

This module generates the file that groups and links to all of the tags found. The file structure will be created as
follows:

├── tag1
│   ├── file1.md
│   └── file2.md
├── tag2
│   └── file1.md
└── tag3
    ├── file1.md
    ├── file2.md
    └── file3.md
"""

import pymind


##======================================================================================================================
#
def run(in_d: str) -> bool:
    """!
    @brief Executes the tag page creation engine.

    @param in_d Input directory path

    @return True if creation was successful, False if creation failed
    """
    # Create an instance of PyMind
    pm = pymind.PyMind({"input": in_d, "force": True, "dry_run": True})
    return True
