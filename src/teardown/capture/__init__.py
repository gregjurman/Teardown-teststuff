import importlib
import teardown.settings as settings

class CaptureEngineError(Exception):
    pass

def load_capture_engine(capture_engine_name):
    module = importlib.import_module(".base", 'teardown.capture.%s' % capture_engine_name)
    return module

class CaptureHandler(object):
    def __init__(self):
        self.backend = load_capture_engine(settings.CAPTURE_ENGINE)
        self.detectors = self.backend.detectors
    
    def load_image(self, file_name):
        self.image = self.backend.load_image(file_name)