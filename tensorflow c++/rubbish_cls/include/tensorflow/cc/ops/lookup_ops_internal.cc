// This file is MACHINE GENERATED! Do not edit.


#include "tensorflow/cc/ops/const_op.h"
#include "tensorflow/cc/ops/lookup_ops_internal.h"

namespace tensorflow {
namespace ops {
namespace internal {
// NOTE: This namespace has internal TensorFlow details that
// are not part of TensorFlow's public API.

LookupTableRemove::LookupTableRemove(const ::tensorflow::Scope& scope,
                                     ::tensorflow::Input table_handle,
                                     ::tensorflow::Input keys) {
  if (!scope.ok()) return;
  auto _table_handle = ::tensorflow::ops::AsNodeOut(scope, table_handle);
  if (!scope.ok()) return;
  auto _keys = ::tensorflow::ops::AsNodeOut(scope, keys);
  if (!scope.ok()) return;
  ::tensorflow::Node* ret;
  const auto unique_name = scope.GetUniqueNameForOp("LookupTableRemove");
  auto builder = ::tensorflow::NodeBuilder(unique_name, "LookupTableRemoveV2")
                     .Input(_table_handle)
                     .Input(_keys)
  ;
  scope.UpdateBuilder(&builder);
  scope.UpdateStatus(builder.Finalize(scope.graph(), &ret));
  if (!scope.ok()) return;
  scope.UpdateStatus(scope.DoShapeInference(ret));
  this->operation = Operation(ret);
  return;
}

}  // namespace internal
}  // namespace ops
}  // namespace tensorflow
