/* Copyright (c) 2015, Julian Straub <jstraub@csail.mit.edu> Licensed
 * under the MIT license. See the license file LICENSE.
 */

namespace OptRot {

template <class Node>
BranchAndBound<Node>::BranchAndBound(Bound<Node>& lower_bound,
    Bound<Node>& upper_bound)
  : lower_bound_(lower_bound), upper_bound_(upper_bound)
{}

template <class Node>
uint32_t BranchAndBound<Node>::BoundAndPrune(std::list<Node>& nodes, double& lb,
    double& ub, double eps) {

  lb = -1e40; ub = -1e40; 
  for (auto& node : nodes) {
//    lower_bound_.EvaluateAndSet(node);
//    upper_bound_.EvaluateAndSet(node);
    // Because of numerics...
    if (node.GetUB() < node.GetLB()) {
      std::cout << " ub < lb: " << node.GetUB() << " < " <<
        node.GetLB() << " - " << node.GetUB() - node.GetLB()
        << " lvl " << node.GetLevel()
        << std::endl;
      node.SetUB(node.GetLB()+eps); 
    }
    lb = std::max(lb, node.GetLB());
    ub = std::max(ub, node.GetUB());
  }
  // Prune
  nodes.remove_if(IsPrunableNode<Node>(lb));
  return std::distance(nodes.begin(), nodes.end());
}

template <class Node>
Node BranchAndBound<Node>::Compute(std::list<Node>& nodes, double eps,
    uint32_t max_it) {
  double lb = -1.e6;
  double ub = -1.e6;
  uint32_t it = 0;
  uint32_t n_nodes = 0;
  for (auto& node : nodes) {
    lower_bound_.EvaluateAndSet(node);
    upper_bound_.EvaluateAndSet(node);
    // Because of numerics in S3 case...
    if (node.GetUB() < node.GetLB()) {
      std::cout << " ub < lb: " << node.GetUB() << " < " <<
        node.GetLB() << " - " << node.GetUB() - node.GetLB()
        << " lvl " << node.GetLevel()
        << std::endl;
      node.SetUB(node.GetLB()+eps); 
    }
  }
  bool write_stats = true;
  std::ofstream out;
  if (write_stats) {
    double V = 0.; // Volume that trhe nodes explain
    for (auto& node : nodes) {
      V += node.GetVolume(); 
    }
    std::stringstream ss;
    ss << "./bb_iteration_stats_" << nodes.begin()->GetSpace() << ".csv";
    out.open(ss.str());
    if (write_stats) 
      out << lb << " " << ub << " " << n_nodes << " " << V << std::endl;
  }

  n_nodes = BoundAndPrune(nodes, lb, ub, eps);

//  Node node_star = *std::max_element(nodes.begin(), nodes.end(),
//        LessThanNodeLB<Node>());
//  nodes.remove_if(IsPrunableNode<Node>(lb));
//  n_nodes = std::distance(nodes.begin(), nodes.end());

  do  {
    // Find node with the biggest upper bound (the most promising node)
    // to explore further.
    auto node_i = std::max_element(nodes.begin(), nodes.end(),
        LessThanNodeUB<Node>());
    if (node_i == nodes.end()) {
      // We removed all nodes.
      break;
    }
    // Find the node with the biggest lower bound (the most
    // conservative node to return).
    if (it%(max_it/10) == 0)
      std::cout << "@" << it << " # " << n_nodes 
        << ": cur " << node_i->GetLB() << " < " << node_i->GetUB() 
        << " lvl " << node_i->GetLevel()
        << "\t global "
        << lb << " < " << ub << " " << " |.| " << (ub - lb)/lb
        << std::endl;
      // Branch and check resulting nodes.
      std::vector<Node> new_nodes = node_i->Branch();
      for (auto& node : new_nodes) {
        upper_bound_.EvaluateAndSet(node);
        lower_bound_.EvaluateAndSet(node);
        // Because of numerics in S3 case...
        if (node.GetUB() < node.GetLB()) {
          if (node.GetLevel() < 8) 
            std::cout << " ub < lb: " << node.GetUB() << " < " <<
              node.GetLB() << " - " << node.GetUB() - node.GetLB() 
              << " lvl " << node.GetLevel() //<< " \t" << node.ToString()
              << "@" << it << " # " << n_nodes 
              << ": cur " << node_i->GetLB() << " < " << node_i->GetUB() 
              << " lvl " << node_i->GetLevel()
              << "\t global "
              << lb << " < " << ub << " " << " |.| " << (ub - lb)/lb
              << std::endl;
//          upper_bound_.ToggleVerbose();
//          upper_bound_.EvaluateAndSet(node);
//          upper_bound_.ToggleVerbose();
//          std::cout << "lower bound ----------- " << std::endl;
//          lower_bound_.ToggleVerbose();
//          lower_bound_.EvaluateAndSet(node);
//          lower_bound_.ToggleVerbose();
          node.SetUB(node.GetLB()+10*eps); 
        }
        if (node.GetUB() > lb) {
          // Remember this node since we cannot prune it.
          nodes.push_back(node);
          ++n_nodes;
        }
      }

//    // Copy the best node to return here since the next operation might
//    // remove all nodes.
//    node_star = *std::max_element(nodes.begin(), nodes.end(),
//        LessThanNodeLB<Node>())
//    if (n_nodes == 1) break;
    // Pop the examined node since we are branching here
    nodes.erase(node_i); 
//    nodes.remove_if(IsPrunableNode<Node>(lb));

    n_nodes =BoundAndPrune(nodes, lb, ub, eps);

//    n_nodes = 0; lb = -1e40; ub = -1e40; 
//    for (auto& node : nodes) {
//      lb = std::max(lb, node.GetLB());
//      ub = std::max(ub, node.GetUB());
//      ++n_nodes;
//    }
    if (write_stats) {
      double V = 0.;
      for (auto& node : nodes) {
        V += node.GetVolume(); 
      }
      out << lb << " " << ub << " " << n_nodes << " " << V << std::endl;
    }
  } while (it++ < max_it && (ub - lb)/lb > eps && n_nodes >= 1);

  Node node_star = *std::max_element(nodes.begin(), nodes.end(),
      LessThanNodeLB<Node>());

  std::cout << "@" << it << " # " << n_nodes << ": global " 
    << lb << " < " << ub << " " << " |.| " << fabs(ub - lb)/lb << "\t selected "
    << node_star.GetLB() << " < " << node_star.GetUB() << " lvl "
    << node_star.GetLevel() << " " //<< node_star.GetIds()[0] << "\t" 
    << std::endl;
  if (write_stats) 
    out.close();
  return node_star;
}

}
