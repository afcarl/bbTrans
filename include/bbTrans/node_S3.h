/* Copyright (c) 2015, Julian Straub <jstraub@csail.mit.edu> Licensed
 * under the MIT license. See the license file LICENSE.
 */
#pragma once

#include <stdint.h>
#include <vector>
#include <list>
#include <sstream>
#include <string>
#include "bbTrans/node.h"
#include "bbTrans/tetrahedron.h"
#include "bbTrans/s3_tessellation.h"

namespace bb {

class NodeS3 : public BaseNode {
 public:
  NodeS3(const Tetrahedron4D& tetrahedron, std::vector<uint32_t> ids);
  NodeS3(const NodeS3& node);
  virtual ~NodeS3() = default;
  virtual std::vector<NodeS3> Branch() const;
  const Tetrahedron4D& GetTetrahedron() const { return tetrahedron_;}
  void SetLbArgument(const Eigen::Quaterniond& q) {q_lb_ = q;}
  Eigen::Quaterniond GetLbArgument() const {return q_lb_;}
  virtual uint32_t GetBranchingFactor(uint32_t i) const { return i==0? 600 : 8;}
  virtual std::string ToString() const;
  virtual std::string Serialize() const;
  std::string GetSpace() const { return "S3"; }
 protected:
  Tetrahedron4D tetrahedron_;
  Eigen::Quaterniond q_lb_;
  virtual double GetVolume_() const { return tetrahedron_.GetVolume();}
};

std::list<NodeS3> GenerateNotesThatTessellateS3();
}
