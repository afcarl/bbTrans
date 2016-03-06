/* Copyright (c) 2015, Julian Straub <jstraub@csail.mit.edu> Licensed
 * under the MIT license. See the license file LICENSE.
 */

namespace bb {

template<class NodeLin>
LowerBoundLin<NodeLin>::LowerBoundLin(LowerBoundS3& boundS3) 
  : boundS3_(boundS3)
{ }

template<class NodeLin>
double LowerBoundLin<NodeLin>::Evaluate(const NodeLin& node) {
  Eigen::Matrix<double,5,1> lbs;
  for (uint32_t i=0; i<5; ++i)
    lbs(i) = boundS3_.Evaluate(node.GetNodeS3(i));
  return lbs.minCoeff();
}

template<class NodeLin>
double LowerBoundLin<NodeLin>::EvaluateAndSet(NodeLin& node) {
  Eigen::Matrix<double,5,1> lbs;
  uint32_t id = 0;
  for (uint32_t i=0; i<5; ++i)
    lbs(i) = boundS3_.Evaluate(node.GetNodeS3(i));
  double lb = lbs.minCoeff(&id);
//  Eigen::Matrix<double,3,9> xs;
//  Eigen::Matrix<double,9,1> lbs;
//  Evaluate(node, xs, lbs);
//  uint32_t id_max = 0;
////  double lb = lbs.maxCoeff(&id_max);
//  double lb = lbs(id_max);
//  node.SetLbArgument(xs.col(id_max));
  node.SetLB(lb);
  // Set the LB argument in the S3 node
  boundS3_.EvaluateAndSet(node.GetNodeS3(id));
  // Copy the LB argument over to the Lin node
  node.SetLbArgument(node.GetNodeS3(id).GetLbArgument());
  return lb;
}

}