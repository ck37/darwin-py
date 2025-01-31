import csv
from pathlib import Path
from typing import List, Optional

import darwin.datatypes as dt
from darwin.path_utils import deconstruct_full_path


def parse_path(path: Path) -> Optional[List[dt.AnnotationFile]]:
    if path.suffix != ".csv":
        return None

    files = []
    with path.open() as f:
        reader = csv.reader(f)
        for row in reader:
            filename, *tags = map(lambda s: s.strip(), row)
            if filename == "":
                continue
            annotations = [dt.make_tag(tag) for tag in tags if len(tag) > 0]
            annotation_classes = set([annotation.annotation_class for annotation in annotations])
            remote_path, filename = deconstruct_full_path(filename)
            files.append(dt.AnnotationFile(path, filename, annotation_classes, annotations, remote_path=remote_path))
    return files
