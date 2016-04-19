/* Copyright (c) 2015, Julian Straub <jstraub@csail.mit.edu> Licensed
 * under the MIT license. See the license file LICENSE.
 */
#pragma once

#include <stdint.h>
#include <iostream>
#include <vector>
#include <list>
#include <string>
#include "bbTrans/node.h"
#include "bbTrans/box.h"

namespace bb {

class NodeR3 : public BaseNode {
 public:
  NodeR3(const Box& box, std::vector<uint32_t> ids);
  NodeR3(const NodeR3& node);
  virtual ~NodeR3() = default;
  virtual std::vector<NodeR3> Branch() const;
  const Box& GetBox() const { return box_;}
  const Eigen::Vector3d& GetLbArgument() const {return t_lb_;}
  void SetLbArgument(const Eigen::Vector3d& t) {t_lb_ = t;}
  virtual uint32_t GetBranchingFactor(uint32_t i) const { return 8;}
  virtual std::string ToString() const;
  virtual std::string Serialize() const;
  std::string GetSpace() const { return "R3"; }
 protected:
  Box box_;
  Eigen::Vector3d t_lb_;
  virtual double GetVolume_() const { return box_.GetVolume();}
};

std::list<NodeR3> GenerateNotesThatTessellateR3(const Eigen::Vector3d&
    min, const Eigen::Vector3d& max, double max_side_len); 
}
