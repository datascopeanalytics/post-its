import sys
import json

class JSONable(object):

    def format_for_json(self):
        result = {}
        for name, json_name in self.json_fields:
            value = getattr(self, name)
            if isinstance(value, list):
                if value and hasattr(value[0], 'format_for_json'):
                    value = [i.format_for_json() for i in value]
            result[json_name] = value
        return result

    def to_json(self):
        return json.dumps(self.format_for_json())

    @staticmethod
    def translate(dictionary, key_map):
        result = {}
        for name, json_name in key_map:
            if json_name in dictionary:
                result[name] = dictionary[json_name]
        return result
    
class Board(JSONable):

    json_fields = [
        ('creation_date', 'creationDate'),
        ('uuid', 'UUID'),
        ('name', 'name'),
        ('clusters', 'clusters'),
    ]
    
    def __init__(self, creation_date, uuid, name):
        self.creation_date = creation_date
        self.uuid = uuid
        self.name = name
        self.clusters = []

    def add_cluster(self, *args, **kwargs):
        cluster = Cluster(*args, **kwargs)
        self.clusters.append(cluster)
        return cluster
    
    @classmethod
    def from_json(cls, filename):

        # read json from file into a dictionary
        with open(filename) as infile:
            board_data = json.load(infile)

        # pop 'clusters' from dictionary so that those can be added separately
        cluster_data_list = board_data.pop('clusters')

        # translate JSON variable names to python ones, and then make
        # a Board
        board_kwargs = JSONable.translate(board_data, Board.json_fields)
        board = cls(**board_kwargs)

        for cluster_data in cluster_data_list:

            # same pattern: pop notes so that they can be added
            note_data_list = cluster_data.pop('notes')

            # translate keyword arguments and instantiate Cluster
            cluster_kwargs = \
                JSONable.translate(cluster_data, Cluster.json_fields)
            cluster = board.add_cluster(**cluster_kwargs)

            # same for notes
            for note_data in note_data_list:
                note_kwargs = JSONable.translate(note_data, Note.json_fields)
                cluster.add_note(**note_kwargs)
                
        return board
    
class Cluster(JSONable):

    json_fields = [
        ('width', 'width'),
        ('height', 'height'),
        ('position_x', 'positionX'),
        ('position_y', 'positionY'),
        ('layout_type', 'layoutType'),
        ('name', 'name'),
        ('notes', 'notes'),
    ]
    
    def __init__(self, width, height, position_x, position_y, layout_type, name):
        self.width = width
        self.height = height
        self.position_x = position_x
        self.position_y = position_y
        self.layout_type = layout_type
        self.name = name
        self.notes = []

    def add_note(self, *args, **kwargs):
        note = Note(*args, **kwargs)
        self.notes.append(note)
        return note
        
class Note(JSONable):

    json_fields = [
        ('index', 'index'),
        ('board', 'board'),
        ('uuid', 'UUID'),
        ('content_uuid', 'contentUUID'),
        ('note_uuid', 'noteUUID'),
        ('center_x', 'centerX'),
        ('center_y', 'centerY'),
        ('corners', 'corners'),
        ('background_color', 'backgroundColor'),
        ('layout_index', 'layoutIndex'),
        ('layout_rotation', 'layoutRotation'),
        ('layout_z_order', 'layoutZOrder'),
        ('enhancement_method', 'enhancementMethod'),
        ('position_initialized', 'positionInitialized'),
        ('is_digital', 'isDigitalNote'),
    ]
    
    def __init__(self, is_digital, note_uuid, index, corners, enhancement_method, uuid, board, background_color, center_y, layout_z_order, layout_rotation, center_x, content_uuid, position_initialized, layout_index):

        self.is_digital = is_digital
        self.index = index
        self.note_uuid = note_uuid
        self.center_y = center_y
        self.background_color = background_color
        self.content_uuid = content_uuid
        self.layout_rotation = layout_rotation
        self.center_x = center_x
        self.corners = corners
        self.layout_index = layout_index
        self.enhancement_method = enhancement_method
        self.position_initialized = position_initialized
        self.uuid = uuid
        self.board = board
        self.layout_z_order = layout_z_order

filename = sys.argv[1]
board = Board.from_json(filename)
print board.to_json()
