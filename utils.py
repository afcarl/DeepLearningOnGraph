"""
Some utilities functions used in multiple scripts

Use python 3 (but should be working with python 2)
"""

import os, sys
import numpy as np

def extractMesh(meshFilename):
    """
    Extract the mesh informations from the file

    Args:
        meshFilename: path of the mesh file (.off format only !!)
    Returns:
        vertices: Array of the x,y,z position of each mesh points
        faces: Array of the vertex indexes of each triangle
    """
    
    # Open the file
    print('Open file ', meshFilename)
    meshFile = open(meshFilename, 'r')
    lines = meshFile.readlines()
    meshFile.close()

    # Initialisation and global information
    meshCount = lines[1].split()
    vertexCount = int(meshCount[0])
    faceCount = int(meshCount[1])
    edgeCount = int(meshCount[2])
    print('Mesh: ', vertexCount, ' vertices, ', faceCount, ' faces, ', edgeCount, ' edges')
    
    vertices = []
    faces = []
    
    # For each line of the file
    for line in lines[2:]: # Skip the first two lines (OFF and number of vertices)
        words = line.split()
    
        if len(words) == 3: # Read points
            # Save each point coordinates in an array
            vertices.append([float(words[0]), float(words[1]), float(words[2])])
        elif len(words) == 4: # Read triangles >> vertex
            faces.append([int(words[1]), int(words[2]), int(words[3])])
        
    if len(vertices) != vertexCount:
        print('Error: Number of vertices does not matches')
    if len(faces) != faceCount:
        print('Error: Number of faces does not matches')
        
    return vertices, faces
    
def meshToPointCloud(meshVertices, meshFaces):
    """
    Compute the point clouds informations from the mesh informations

    Args:
        vertices: Array of the x,y,z position of each mesh points
        faces: Array of the vertex indexes of each triangle
    Returns:
        A point cloud (list of coordinates)
    """
    
    Xin = np.zeros((len(meshFaces), 3))
    
    for i, face in enumerate(meshFaces):
        # Compute the circumcenter of the triangle
        
        A = np.array(meshVertices[face[0]])
        B = np.array(meshVertices[face[1]])
        C = np.array(meshVertices[face[2]]) # Triangle coordinates
        
        AC = C - A
        AB = B - A
        ABxAC = np.cross(AB, AC)
        
        n = np.cross(ABxAC, AB) * np.linalg.norm(AC)**2  +  np.cross(AC, ABxAC) * np.linalg.norm(AB)**2
        d = 2.0 * np.linalg.norm(ABxAC)**2
        
        center = A + n/d
        
        Xin[i,:] = center
    
    return Xin
