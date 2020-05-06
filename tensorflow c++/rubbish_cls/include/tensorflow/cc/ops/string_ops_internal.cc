// This file is MACHINE GENERATED! Do not edit.


#include "tensorflow/cc/ops/const_op.h"
#include "tensorflow/cc/ops/string_ops_internal.h"

namespace tensorflow {
namespace ops {
namespace internal {
// NOTE: This namespace has internal TensorFlow details that
// are not part of TensorFlow's public API.

StaticRegexFullMatch::StaticRegexFullMatch(const ::tensorflow::Scope& scope,
                                           ::tensorflow::Input input,
                                           StringPiece pattern) {
  if (!scope.ok()) return;
  auto _input = ::tensorflow::ops::AsNodeOut(scope, input);
  if (!scope.ok()) return;
  ::tensorflow::Node* ret;
  const auto unique_name = scope.GetUniqueNameForOp("StaticRegexFullMatch");
  auto builder = ::tensorflow::NodeBuilder(unique_name, "StaticRegexFullMatch")
                     .Input(_input)
                     .Attr("pattern", pattern)
  ;
  scope.UpdateBuilder(&builder);
  scope.UpdateStatus(builder.Finalize(scope.graph(), &ret));
  if (!scope.ok()) return;
  scope.UpdateStatus(scope.DoShapeInference(ret));
  this->operation = Operation(ret);
  this->output = Output(ret, 0);
}

StaticRegexReplace::StaticRegexReplace(const ::tensorflow::Scope& scope,
                                       ::tensorflow::Input input, StringPiece
                                       pattern, StringPiece rewrite, const
                                       StaticRegexReplace::Attrs& attrs) {
  if (!scope.ok()) return;
  auto _input = ::tensorflow::ops::AsNodeOut(scope, input);
  if (!scope.ok()) return;
  ::tensorflow::Node* ret;
  const auto unique_name = scope.GetUniqueNameForOp("StaticRegexReplace");
  auto builder = ::tensorflow::NodeBuilder(unique_name, "StaticRegexReplace")
                     .Input(_input)
                     .Attr("pattern", pattern)
                     .Attr("rewrite", rewrite)
                     .Attr("replace_global", attrs.replace_global_)
  ;
  scope.UpdateBuilder(&builder);
  scope.UpdateStatus(builder.Finalize(scope.graph(), &ret));
  if (!scope.ok()) return;
  scope.UpdateStatus(scope.DoShapeInference(ret));
  this->operation = Operation(ret);
  this->output = Output(ret, 0);
}

StaticRegexReplace::StaticRegexReplace(const ::tensorflow::Scope& scope,
                                       ::tensorflow::Input input, StringPiece
                                       pattern, StringPiece rewrite)
  : StaticRegexReplace(scope, input, pattern, rewrite, StaticRegexReplace::Attrs()) {}

UnicodeDecode::UnicodeDecode(const ::tensorflow::Scope& scope,
                             ::tensorflow::Input input, StringPiece
                             input_encoding, const UnicodeDecode::Attrs& attrs) {
  if (!scope.ok()) return;
  auto _input = ::tensorflow::ops::AsNodeOut(scope, input);
  if (!scope.ok()) return;
  ::tensorflow::Node* ret;
  const auto unique_name = scope.GetUniqueNameForOp("UnicodeDecode");
  auto builder = ::tensorflow::NodeBuilder(unique_name, "UnicodeDecode")
                     .Input(_input)
                     .Attr("input_encoding", input_encoding)
                     .Attr("errors", attrs.errors_)
                     .Attr("replacement_char", attrs.replacement_char_)
                     .Attr("replace_control_characters", attrs.replace_control_characters_)
  ;
  scope.UpdateBuilder(&builder);
  scope.UpdateStatus(builder.Finalize(scope.graph(), &ret));
  if (!scope.ok()) return;
  scope.UpdateStatus(scope.DoShapeInference(ret));
  this->operation = Operation(ret);
  ::tensorflow::NameRangeMap _outputs_range;
  ::tensorflow::Status _status_ = ::tensorflow::NameRangesForNode(*ret, ret->op_def(), nullptr, &_outputs_range);
  if (!_status_.ok()) {
    scope.UpdateStatus(_status_);
    return;
  }

  this->row_splits = Output(ret, _outputs_range["row_splits"].first);
  this->char_values = Output(ret, _outputs_range["char_values"].first);
}

UnicodeDecode::UnicodeDecode(const ::tensorflow::Scope& scope,
                             ::tensorflow::Input input, StringPiece
                             input_encoding)
  : UnicodeDecode(scope, input, input_encoding, UnicodeDecode::Attrs()) {}

UnicodeDecodeWithOffsets::UnicodeDecodeWithOffsets(const ::tensorflow::Scope&
                                                   scope, ::tensorflow::Input
                                                   input, StringPiece
                                                   input_encoding, const
                                                   UnicodeDecodeWithOffsets::Attrs&
                                                   attrs) {
  if (!scope.ok()) return;
  auto _input = ::tensorflow::ops::AsNodeOut(scope, input);
  if (!scope.ok()) return;
  ::tensorflow::Node* ret;
  const auto unique_name = scope.GetUniqueNameForOp("UnicodeDecodeWithOffsets");
  auto builder = ::tensorflow::NodeBuilder(unique_name, "UnicodeDecodeWithOffsets")
                     .Input(_input)
                     .Attr("input_encoding", input_encoding)
                     .Attr("errors", attrs.errors_)
                     .Attr("replacement_char", attrs.replacement_char_)
                     .Attr("replace_control_characters", attrs.replace_control_characters_)
  ;
  scope.UpdateBuilder(&builder);
  scope.UpdateStatus(builder.Finalize(scope.graph(), &ret));
  if (!scope.ok()) return;
  scope.UpdateStatus(scope.DoShapeInference(ret));
  this->operation = Operation(ret);
  ::tensorflow::NameRangeMap _outputs_range;
  ::tensorflow::Status _status_ = ::tensorflow::NameRangesForNode(*ret, ret->op_def(), nullptr, &_outputs_range);
  if (!_status_.ok()) {
    scope.UpdateStatus(_status_);
    return;
  }

  this->row_splits = Output(ret, _outputs_range["row_splits"].first);
  this->char_values = Output(ret, _outputs_range["char_values"].first);
  this->char_to_byte_starts = Output(ret, _outputs_range["char_to_byte_starts"].first);
}

UnicodeDecodeWithOffsets::UnicodeDecodeWithOffsets(const ::tensorflow::Scope&
                                                   scope, ::tensorflow::Input
                                                   input, StringPiece
                                                   input_encoding)
  : UnicodeDecodeWithOffsets(scope, input, input_encoding, UnicodeDecodeWithOffsets::Attrs()) {}

UnicodeEncode::UnicodeEncode(const ::tensorflow::Scope& scope,
                             ::tensorflow::Input input_values,
                             ::tensorflow::Input input_splits, StringPiece
                             output_encoding, const UnicodeEncode::Attrs&
                             attrs) {
  if (!scope.ok()) return;
  auto _input_values = ::tensorflow::ops::AsNodeOut(scope, input_values);
  if (!scope.ok()) return;
  auto _input_splits = ::tensorflow::ops::AsNodeOut(scope, input_splits);
  if (!scope.ok()) return;
  ::tensorflow::Node* ret;
  const auto unique_name = scope.GetUniqueNameForOp("UnicodeEncode");
  auto builder = ::tensorflow::NodeBuilder(unique_name, "UnicodeEncode")
                     .Input(_input_values)
                     .Input(_input_splits)
                     .Attr("errors", attrs.errors_)
                     .Attr("output_encoding", output_encoding)
                     .Attr("replacement_char", attrs.replacement_char_)
  ;
  scope.UpdateBuilder(&builder);
  scope.UpdateStatus(builder.Finalize(scope.graph(), &ret));
  if (!scope.ok()) return;
  scope.UpdateStatus(scope.DoShapeInference(ret));
  this->operation = Operation(ret);
  this->output = Output(ret, 0);
}

UnicodeEncode::UnicodeEncode(const ::tensorflow::Scope& scope,
                             ::tensorflow::Input input_values,
                             ::tensorflow::Input input_splits, StringPiece
                             output_encoding)
  : UnicodeEncode(scope, input_values, input_splits, output_encoding, UnicodeEncode::Attrs()) {}

}  // namespace internal
}  // namespace ops
}  // namespace tensorflow
