/* Copyright (c) 2015, Julian Straub <jstraub@csail.mit.edu> Licensed
 * under the MIT license. See the license file LICENSE.
 */
#pragma once

#include <vector>
#include <Eigen/Dense>
#include <Eigen/Geometry>
#include "bbTrans/node_R3.h"
#include "bbTrans/numeric_helpers.h"
#include "bbTrans/normal.h"
#include "bbTrans/bound.h"
#include "bbTrans/lower_bound_R3.h"

namespace bb {

class UpperBoundIndepR3 : public Bound<NodeR3> {
 public:
  UpperBoundIndepR3(const std::vector<Normal<3>>& gmm_A, const
      std::vector<Normal<3>>& gmm_B, const Eigen::Quaterniond& q);
  virtual ~UpperBoundIndepR3() = default;
  virtual double Evaluate(const NodeR3& node);
  virtual double EvaluateAndSet(NodeR3& node);
 private:
  std::vector<Normal<3>> gmmT_;
};

Eigen::Vector3d FindMinTranslationInNode(const Eigen::Matrix3d& A, 
    const Eigen::Vector3d& b, const NodeR3& node);

}
