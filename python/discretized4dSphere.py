import numpy as np
from scipy.linalg import svd, det, eig
from rotations import *
from itertools import combinations, permutations

def normed(a):
  return a/np.sqrt((a**2).sum())

class Tetrahedron(object):
  def __init__(self, vertices, lvl, ids):
    self.vertices = vertices
    self.tetra = np.arange(4)
    self.lvl = lvl
    self.ids = [i for i in ids]
  def Center(self):
    center = 0.25*self.vertices[self.tetra[0]] \
      + 0.25*self.vertices[self.tetra[1]] + \
      0.25*self.vertices[self.tetra[2]] + 0.25*self.vertices[self.tetra[3]]
    return normed(center)

  def GeMinMaxVertexDotProduct(self):
    dots = np.zeros(6)
    for i, p in enumerate(combinations(range(4), 2)):
      print i,p, p[0], p[1]
      print self.vertices[p[0]]
      dots[i] = self.vertices[p[0]].dot(self.vertices[p[1]])
    return np.min(dots), np.max(dots)

  def Volume(self):
    A = np.zeros((4,3))
    for i in range(3):
      A[:,i] = self.vertices[i] - self.vertices[3]
#    print A
    U,S,Vt = svd(A)
#    print U
#    print S
#    print Vt
#    print det(U)
#    print det(Vt)
    return S.prod()
#    print " reducing dim" 
#    print U[:,:3]
#    print np.diag(S[:3])
#    print Vt[:3,:]
#    A_ = U[:,:3].dot(np.diag(S[:3])).dot(Vt[:3,:])
#    print A_
#    print det(A_)
#    A_ = U[:3,:].dot(A).dot(Vt[:,:3])
#    print A_
#    print det(A_)
#    A_ = U[:3,:].dot(np.diag(S)).dot(Vt[:,:3])
#    print A_
#    print det(A_)
    # http://mathworld.wolfram.com/Cayley-MengerDeterminant.html
#    B = np.zeros((4,4))
#    for i in range(4):
#      for j in range(4):
#        B[i,j] = ((self.vertices[i]-self.vertices[j])**2).sum()
#    B_ = np.ones((5,5))
#    B_[0,0] = 0.
#    B_[1:,1:] = B
#    print B_
#    print det(B_)
#    print det(B_)/(-9216.)
    
    V = 0;
    return V;

  def Subdivide(self):
    '''
    Subdivide the tetraheadron 
    8 tetrahedra and pop out the inner corners of
    the new tetrahedra to the S3 sphere.
    http://www.ams.org/journals/mcom/1996-65-215/S0025-5718-96-00748-X/S0025-5718-96-00748-X.pdf
    '''
    tetrahedra = []
    vertices = np.zeros((6, 4))
    vertices[0, :] = normed(self.vertices[0] + self.vertices[1]) 
    vertices[1, :] = normed(self.vertices[1] + self.vertices[2]) 
    vertices[2, :] = normed(self.vertices[2] + self.vertices[0]) 
    vertices[3, :] = normed(self.vertices[0] + self.vertices[3]) 
    vertices[4, :] = normed(self.vertices[1] + self.vertices[3]) 
    vertices[5, :] = normed(self.vertices[2] + self.vertices[3]) 
    # Corner tetrahedron at 0th corner of parent.
    tetrahedra.append(Tetrahedron([
      self.vertices[0],
      vertices[0,:],
      vertices[2,:],
      vertices[3,:]], self.lvl+1, self.ids + [0]))
    # Corner tetrahedron at 1th corner of parent.
    tetrahedra.append(Tetrahedron([
      self.vertices[1],
      vertices[0,:],
      vertices[1,:],
      vertices[4,:]], self.lvl+1, self.ids + [1]))
    # Corner tetrahedron at 2th corner of parent.
    tetrahedra.append(Tetrahedron([
      self.vertices[2],
      vertices[1,:],
      vertices[2,:],
      vertices[5,:]], self.lvl+1, self.ids + [2]))
    # Corner tetrahedron at 3th corner of parent.
    tetrahedra.append(Tetrahedron([
      self.vertices[3],
      vertices[3,:],
      vertices[4,:],
      vertices[5,:]], self.lvl+1, self.ids + [3]))
    # Check which skew edge is the shortest.
    dots = np.zeros(3)
    dots[0] = vertices[0,:].dot(vertices[5,:])
    dots[1] = vertices[2,:].dot(vertices[4,:])
    dots[2] = vertices[3,:].dot(vertices[1,:])
    skewEdgeId = np.argmax(dots)
    if skewEdgeId == 0:
      tetrahedra.append(Tetrahedron([
        vertices[0,:], 
        vertices[5,:],
        vertices[3,:],
        vertices[2,:]], self.lvl+1, self.ids + [4]))
      tetrahedra.append(Tetrahedron([
        vertices[0,:], 
        vertices[5,:],
        vertices[4,:],
        vertices[3,:]], self.lvl+1, self.ids + [5]))
      tetrahedra.append(Tetrahedron([
        vertices[5,:], 
        vertices[0,:],
        vertices[1,:],
        vertices[4,:]], self.lvl+1, self.ids + [6]))
      tetrahedra.append(Tetrahedron([
        vertices[5,:], 
        vertices[0,:],
        vertices[1,:],
        vertices[2,:]], self.lvl+1, self.ids + [7]))
    elif skewEdgeId == 1:
      tetrahedra.append(Tetrahedron([
        vertices[0,:], 
        vertices[4,:],
        vertices[3,:],
        vertices[2,:]], self.lvl+1, self.ids + [4]))
      tetrahedra.append(Tetrahedron([
        vertices[0,:], 
        vertices[1,:],
        vertices[4,:],
        vertices[2,:]], self.lvl+1, self.ids + [5]))
      tetrahedra.append(Tetrahedron([
        vertices[5,:], 
        vertices[2,:],
        vertices[1,:],
        vertices[4,:]], self.lvl+1, self.ids + [6]))
      tetrahedra.append(Tetrahedron([
        vertices[5,:], 
        vertices[3,:],
        vertices[2,:],
        vertices[4,:]], self.lvl+1, self.ids + [7]))
    elif skewEdgeId == 2:
      tetrahedra.append(Tetrahedron([
        vertices[3,:], 
        vertices[1,:],
        vertices[0,:],
        vertices[2,:]], self.lvl+1, self.ids + [4]))
      tetrahedra.append(Tetrahedron([
        vertices[3,:], 
        vertices[1,:],
        vertices[4,:],
        vertices[0,:]], self.lvl+1, self.ids + [5]))
      tetrahedra.append(Tetrahedron([
        vertices[3,:], 
        vertices[1,:],
        vertices[5,:],
        vertices[4,:]], self.lvl+1, self.ids + [6]))
      tetrahedra.append(Tetrahedron([
        vertices[1,:], 
        vertices[3,:],
        vertices[2,:],
        vertices[5,:]], self.lvl+1, self.ids + [7]))
    return tetrahedra

class S3Grid(object):
  def __init__(self, depth):
    self.depth = depth
    self.vertices = np.zeros((120,4))
    self.tetra = np.zeros((600, 4), dtype = np.int)
    self.InitGrid()
    for lvl in range(self.depth):
      self.SubdivideOnce()
  def InitGrid(self):
    # The vertices of a 600-cell 
    vs = np.zeros((120,4))
    # https://en.wikipedia.org/wiki/600-cell
    # http://eusebeia.dyndns.org/4d/600-cell
    i=0
    for a in [-1.,1.]:
      for b in [-1.,1.]:
        for c in [-1.,1.]:
          for d in [-1.,1.]:
            vs[i,:] = [a,b,c,d]
            i+=1
    for j in range(4):
      vs[i,j] = 2.
      i+=1
      vs[i,j] = -2.
      i+=1
    # Golden Ratio
    phi = (1 + np.sqrt(5)) * 0.5
    # iterate over all *even* permutations
    # http://mathworld.wolfram.com/EvenPermutation.html
    for perm in [ [0,1,2,3], [0,2,3,1], [0,3,1,2], [1,0,3,2],
        [1,2,0,3], [1,3,2,0], [2,0,1,3], [2,1,3,0], [2,3,0,1],
        [3,0,2,1], [3,1,0,2], [3,2,1,0]]:
      for a in [-1.,1.]:
        for b in [-1.,1.]:
          for c in [-1.,1.]:
            vs[i,perm[0]] = a*phi
            vs[i,perm[1]] = b
            vs[i,perm[2]] = c/phi
            vs[i,perm[3]] = 0.
            i+=1
    vs *= 0.5
    # Filter out half the sphere
    north = np.array([1.,0.,0.,0.])
    j = 0
    for i in range(vs.shape[0]):
      if np.arccos(vs[i,:].dot(north)) <= 120*np.pi/180.:
        vs[j,:] = vs[i,:]
        j+=1
    self.vertices = np.copy(vs[:j,:])
    n_vertices = self.vertices.shape[0]
    print self.vertices.shape
    print "# north-filtered vertices:", n_vertices
      
    # Tada: all of the vertices are unit length and hence \in S^3
#    print np.sqrt((self.vertices**2).sum(axis=1))
    if False:
      import mayavi.mlab as mlab
      figm = mlab.figure()
      for i in range(n_vertices):
        qi = Quaternion(vec=self.vertices[i])
        qi.plot(figm)
      mlab.show(stop=True)

    G = np.ones((n_vertices, n_vertices)) * 99
    for i in range(n_vertices):
      for j in range(n_vertices):
        if j != i:
          qi = Quaternion(vec=self.vertices[i])
          qj = Quaternion(vec=self.vertices[j])
          G[i,j] = qi.angleTo(qj)

    print np.unique(G) *180./np.pi
    GSorted = np.sort(G, axis=1)
#    print GSorted[0,:] * 180. / np.pi

    minAngle = GSorted[0, 1] 
    G[G < minAngle - 1e-6] = -1.
    G[G > minAngle + 1e-6] = -1.

    print "Min angle for tetrahedra construction: ", minAngle * 180./np.pi
    print "# edges:", G[G>0.].shape

    if False:
      import matplotlib.pyplot as plt
      plt.figure()
      plt.imshow(G, interpolation="nearest")
      plt.show()

    tetra = []
    for p in combinations(range(n_vertices), 4):
      if G[p[0], p[1]] > 0 and G[p[0], p[2]] > 0 and G[p[0], p[3]] > 0 and  \
        G[p[1], p[2]] > 0 and G[p[1], p[3]] > 0 and G[p[2], p[3]] > 0:
        tetra.append(p)
    print len(tetra)
#    if len(tetra) == 600:
#      print "Yeaha the 600 cell"
    self.tetra_levels = [0, len(tetra)]
    self.tetra = np.array(tetra)
          

  def SubdivideOnce(self):
      '''
      Subdivide each of the existing tetraheadra of the current
      S3Grid into 4 triangles and pop out the inner corners of
      the new triangles to the S3 sphere.
      http://www.ams.org/journals/mcom/1996-65-215/S0025-5718-96-00748-X/S0025-5718-96-00748-X.pdf
      '''
      n_vertices = self.vertices.shape[0]
      n_tetra = self.tetra.shape[0]
      print n_tetra, n_vertices
      self.vertices.resize((n_vertices + n_tetra * 6, 4), refcheck=False)
      self.tetra.resize((n_tetra * (8 + 1), 4))
      self.tetra_levels.append(n_tetra * (8 + 1))
      for i in range(n_tetra):
          i0 = self.tetra[i, 0]
          i1 = self.tetra[i, 1]
          i2 = self.tetra[i, 2]
          i3 = self.tetra[i, 3]
          i01 = n_vertices + i*6 
          i12 = n_vertices + i*6 + 1
          i20 = n_vertices + i*6 + 2
          i03 = n_vertices + i*6 + 3
          i13 = n_vertices + i*6 + 4
          i23 = n_vertices + i*6 + 5
          self.vertices[i01, :] = 0.5 * (self.vertices[i0, :] + self.vertices[i1, :]) 
          self.vertices[i12, :] = 0.5 * (self.vertices[i1, :] + self.vertices[i2, :]) 
          self.vertices[i20, :] = 0.5 * (self.vertices[i2, :] + self.vertices[i0, :]) 
          self.vertices[i03, :] = 0.5 * (self.vertices[i0, :] + self.vertices[i3, :]) 
          self.vertices[i13, :] = 0.5 * (self.vertices[i1, :] + self.vertices[i3, :]) 
          self.vertices[i23, :] = 0.5 * (self.vertices[i2, :] + self.vertices[i3, :]) 
          self.tetra[n_tetra + i*8, :]     = [i0, i01, i20, i03]
          self.tetra[n_tetra + i*8 + 1, :] = [i01, i1, i12, i13]
          self.tetra[n_tetra + i*8 + 2, :] = [i12, i2, i20, i23]
          self.tetra[n_tetra + i*8 + 3, :] = [i03, i13, i23, i3]
          self.tetra[n_tetra + i*8 + 4, :] = [i01, i13, i03, i20]
          self.tetra[n_tetra + i*8 + 5, :] = [i01, i12, i13, i20]
          self.tetra[n_tetra + i*8 + 6, :] = [i23, i20, i12, i13]
          self.tetra[n_tetra + i*8 + 7, :] = [i23, i03, i20, i13]
      print np.sqrt((self.vertices[n_vertices::,:]**2).sum(axis=1))
      self.vertices[n_vertices::, :] /= np.sqrt((self.vertices[n_vertices::,:]**2).sum(axis=1))[:, np.newaxis]
  def GetTetras(self, level):
    return self.tetra[self.tetra_levels[level]: \
        self.tetra_levels[level+1]]
  def GetVertex(self, id):
    return self.vertices[id,:]
  def GetTetrahedra(self, level):
    tetras = self.GetTetras(level)
    tetrahedra = []
    for i,tetra in enumerate(tetras):
      tetrahedra.append(Tetrahedron([
        self.vertices[tetra[0],:],
        self.vertices[tetra[1],:],
        self.vertices[tetra[2],:],
        self.vertices[tetra[3],:]
        ], level, [i]))
    return tetrahedra

if __name__ == "__main__":
  s3 = S3Grid(4)
  Vs = np.zeros((4,100))
  for lvl in range(4):
    tetras = s3.GetTetrahedra(lvl)
    ids = np.arange(len(tetras))
    np.random.shuffle(ids)
    for i,id in enumerate(ids[:100]):
      Vs[lvl,i] = tetras[id].Volume()
  print "mean", np.mean(Vs, axis=1)
  print np.cov(Vs[0,:].T)
  print np.cov(Vs[1,:].T)
  print np.cov(Vs[2,:].T)
  print np.cov(Vs[3,:].T)
  raw_input()
  lvls = 4
  s3 = S3Grid(lvls)
  print s3.tetra_levels

  for lvl in range(lvls):
    print " --- {} ---".format(lvl)
    tetras = s3.GetTetras(lvl)
    dAng = np.zeros((tetras.shape[0], 6))
    for i, tetra in enumerate(tetras):
      dAng[i, 0] = Quaternion(vec = s3.GetVertex(tetra[0])).angleTo(
              Quaternion(vec = s3.GetVertex(tetra[1])))
      dAng[i, 1] = Quaternion(vec = s3.GetVertex(tetra[1])).angleTo(
              Quaternion(vec = s3.GetVertex(tetra[2])))
      dAng[i, 2] = Quaternion(vec = s3.GetVertex(tetra[0])).angleTo(
              Quaternion(vec = s3.GetVertex(tetra[2])))
      dAng[i, 3] = Quaternion(vec = s3.GetVertex(tetra[0])).angleTo(
              Quaternion(vec = s3.GetVertex(tetra[3])))
      dAng[i, 4] = Quaternion(vec = s3.GetVertex(tetra[1])).angleTo(
              Quaternion(vec = s3.GetVertex(tetra[3])))
      dAng[i, 5] = Quaternion(vec = s3.GetVertex(tetra[2])).angleTo(
              Quaternion(vec = s3.GetVertex(tetra[3])))
    print dAng.mean(axis=0) * 180. / np.pi
