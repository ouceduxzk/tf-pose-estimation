# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: shape.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='shape.proto',
  package='proto',
  syntax='proto2',
  serialized_pb=_b('\n\x0bshape.proto\x12\x05proto\"7\n\x05Shape\x12\n\n\x02\x64\x31\x18\x01 \x02(\r\x12\n\n\x02\x64\x32\x18\x02 \x02(\r\x12\n\n\x02\x64\x33\x18\x03 \x02(\r\x12\n\n\x02\x64\x34\x18\x04 \x02(\r')
)




_SHAPE = _descriptor.Descriptor(
  name='Shape',
  full_name='proto.Shape',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='d1', full_name='proto.Shape.d1', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='d2', full_name='proto.Shape.d2', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='d3', full_name='proto.Shape.d3', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='d4', full_name='proto.Shape.d4', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=77,
)

DESCRIPTOR.message_types_by_name['Shape'] = _SHAPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Shape = _reflection.GeneratedProtocolMessageType('Shape', (_message.Message,), dict(
  DESCRIPTOR = _SHAPE,
  __module__ = 'shape_pb2'
  # @@protoc_insertion_point(class_scope:proto.Shape)
  ))
_sym_db.RegisterMessage(Shape)


# @@protoc_insertion_point(module_scope)
