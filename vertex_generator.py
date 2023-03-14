from math import sqrt

def cuboid(length,center):
    x, y, z = center
    vertex_list = []
    l1, l2, l3 = length
    l1 = l1 // 2
    l2 = l2 // 2
    l3 = l3 // 2

    for i in (-l1, l1):
        for j in (-l2, l2):
            for k in (-l3, l3):
                vertex_list.append((x + i, y + j, z + k))

    edge_list = ((0, 2), (2, 3), (3, 7), (5, 7), (1, 5), (1, 3), (2, 6), (6, 7), (4, 6), (4, 5), (0, 4), (0, 1))
    return vertex_list, edge_list, list(center)


def equilateral_triangular_pyramid(length,center):
    unit_vertices=((-0.5,-1/3,-(sqrt(3)-1)/3),(0.5,-1/3,-(sqrt(3)-1)/3),(0,2/3,-(sqrt(3)-1)/2),(0,0,2*(sqrt(3)-1)/3))

    scaled_vertices=[]

    cx,cy,cz=center

    for vertex in unit_vertices:
        x,y,z=vertex
        scaled_vertices.append((x*length+cx,y*length+cy,z*length+cz))

    edges=((0,1),(1,2),(2,0),(0,3),(1,3),(2,3))

    return scaled_vertices,edges,list(center)



def square_pyramid(base_length,height,center):
    unit_vertices=((.5,.5,-1/3),(.5,-.5,-1/3),(-.5,-.5,-1/3),(-.5,.5,-1/3),(0,0,2/3))

    scaled_vertices=[]

    cx,cy,cz=center

    for vertex in unit_vertices:
        x,y,z=vertex
        scaled_vertices.append((x*base_length+cx,y*base_length+cy,z*height+cz))

    edges=((0,1),(1,2),(2,3),(3,0),(0,4),(1,4),(2,4),(3,4))

    return scaled_vertices,edges,list(center)
