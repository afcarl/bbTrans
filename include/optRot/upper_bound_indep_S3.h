
/* Copyright (c) 2015, Julian Straub <jstraub@csail.mit.edu> Licensed
 * under the MIT license. See the license file LICENSE.
 */
#pragma once

#include <Eigen/Dense>
#include <Eigen/Geometry>
#include "optRot/node_S3.h"
#include "optRot/numeric_helpers.h"
#include "optRot/vmf.h"
#include "optRot/vmf_mm.h"
#include "optRot/bound.h"

namespace OptRot {

class UpperBoundIndepS3 : public Bound<NodeS3> {
 public:
  UpperBoundIndepS3(const vMFMM<3>& vmf_mm_A, const vMFMM<3>& vmf_mm_B);
  virtual double Evaluate(const NodeS3& node);
 private:
  const vMFMM<3>& vmf_mm_A_;
  const vMFMM<3>& vmf_mm_B_;
};

Eigen::Vector3d ClosestPointInTetrahedron(const vMF<3>& vmf_A, const
    vMF<3>& vmf_B, const Tetrahedron4D& tetrahedron, bool
    furthest=false);

Eigen::Vector3d FurthestPointInTetrahedron(const vMF<3>& vmf_A, const
    vMF<3>& vmf_B, const Tetrahedron4D& tetrahedron);

}