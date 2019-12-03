

class AnnotationModel:

    def __init__(self, filename, folder, path, size, objects):
        self.filename = filename
        self.folder = folder
        self.path = path
        self.size: AnnotationSize = size
        self.objects = objects

    def dict(self):
        return {
            'filename': self.filename,
            'folder': self.folder,
            'path': self.path,
            'size': self.size.dict(),
            'objects': [x.dict() for x in self.objects]
        }


class AnnotationObjectModel:

    def __init__(self, name, bndbox):
        self.name = name
        self.bndbox = bndbox

    def dict(self):
        return {
            'name': self.name,
            'bndbox': self.bndbox
        }


class AnnotationSize:

    def __init__(self, width, height, depth):
        self.width: int = width
        self.height: int = height
        self.depth: int = depth

    def dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'depth': self.depth
        }