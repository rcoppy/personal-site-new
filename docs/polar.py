#----------------------------------------------------------
# File polar.py
# Graph a polar curve by creating vertices in a mesh 
# Alex Rupp-Coppi, 5/11/2016
#----------------------------------------------------------

import bpy 
import math
import pdb #; pdb.set_trace() 
import mathutils
from mathutils import Vector
 
def createMeshFromData(name, origin, verts, edges, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
 
    # Link object to scene and make active
    scn = bpy.context.scene
    scn.objects.link(ob)
    scn.objects.active = ob
    ob.select = True
 
    # Create mesh from given verts, faces.
    me.from_pydata(verts, edges, faces)
    # Update mesh with new data
    me.update()    
    return ob


#by 7:00 -- vertices rendered from path 

def getVerts(res, tMin, tMax, curveXY, curveZ): 
    #res: resolution, basically a step size; higher value, greater precision. Don't set to 0. 
    #vary t from min to max 
    
    #error check res
    res = abs(res)

    if res == 0: 
        res = 1

    verts = ()
    
    for t in range(int(tMin*res), int(tMax*res)): #range(0,3) counts 0, 1, 2 
        
        #Old method (polar coords: 
        #2D base 
        #r = curveXYToGraph(t/res)
        #x = r * math.cos(t/res)
        #y = r * math.sin(t/res)

        #scale factor 
        s = 3

        #2D base from parametric 
        coords = curveXY(t/res)
        x = s*coords[0]
        y = s*coords[1]

        #Z-height
        z = s*rollerHeight(t/res)    

        #Add vertices 
        verts = verts + ( (x,y,z), )
        
        #faces = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))

        print("\n"+str(t)+","+str(t/res))

    #print("verts:\n"+str(verts)+"\n")

    return verts

# edges for straight path, super simple 
def getEdges(verts):
    edges = ()
    l = len(verts) #how many vertices 
    for i in range(0,l-1): 
        edges = edges + ( (i,i+1), ) #connect the vertices tip-to-tail

    #close loop 
    edges = edges + ( (l,0), ) 
    #print("edges:\n"+str(edges)+"\n")

    return edges 

def cloverCurve(t):
    r = 4 * math.sin(t) * math.cos(t)
    return r

def cloverZ(t): 
    return 0 #math.sin(t)

def rollerHeight(t): 
    #set period to half of length of base interval
    p = rollerBase(0)[2]/2 #should be roughly 5pi/2
    b = 2*math.pi/p

    return ((1-math.sin(-1*b*t)+math.sin(-1*b*t)*math.sin(-1*b*t)) * (1+math.cos(b*t)) * (1+math.cos(b*t)) * (math.sin(-1*b*t)*math.sin(-1*b*t)+1))

def rollerBase(t):
    #returns a tuple containing x, y, and the interval length of the domain 
    #to get length of interval of function to use in code: 
    # length = rollerBase(0)[2] <-- returns i6
    
    # parametric - returns x and y 
    coords = ()
    x = 0
    y = 0

    #constants 
    z = 1.8
    a = 0.9
    b = 0.3
    q = 6.2
    n = 9
    m = 2 

    #intervals
    pi = math.pi 

    i1 = pi/4
    i2 = i1 + 2*pi
    i3 = i2 + pi/4
    i4 = i3 + pi/4
    i5 = i4 + 2*pi 
    i6 = i5 + pi/4

    # constrain t to positive values, values on domain 
    t = abs(t) 
    t = t % i6

    #piecewise function
    if t < i1: 
        x = -1 * math.cos(i1-t) * math.sqrt(n * math.cos(m * (i1-t)))
        y = -1 * math.sin(i1-t) * math.sqrt(n * math.cos(m * (i1-t)))
        print("i1: "+","+str(x)+","+str(y))
    elif t < i2: 
        x = -1 * (b + a*math.cos(t-i1)) * math.cos(t-i1) - z
        y = (b + a*math.cos(t-i1)) * math.sin(t-i1)
        print("i2: "+","+str(x)+","+str(y))
    elif t < i3: 
        x = -1 * math.cos(t-i2) * math.sqrt(n * math.cos(m * (t-i2)))
        y = math.sin(t-i2) * math.sqrt(n * math.cos(m * (t-i2)))
        print("i3: "+","+str(x)+","+str(y))
    elif t < i4: 
        x = math.cos(i4-t) * math.sqrt(n * math.cos(m * (i4-t)))
        y = -1 * math.sin(i4-t) * math.sqrt(n * math.cos(m * (i4-t)))
        print("i4: "+","+str(x)+","+str(y))
    elif t < i5: 
        x = (b + a*math.cos(t-i4)) * math.cos(t-i4) + z
        y = (b + a*math.cos(t-i4)) * math.sin(t-i4)
        print("i5: "+","+str(x)+","+str(y))
    else:
        x = math.cos(t-i5) * math.sqrt(n * math.cos(m * (t-i5)))
        y = math.sin(t-i5) * math.sqrt(n * math.cos(m * (t-i5)))
        print("i6: "+","+str(x)+","+str(y))

    #return coords 
    coords = (x,y,i6)
    return coords 

 
def run(origo):
    origin = Vector(origo)
    #(x,y,z) = (0.707107, 0.258819, 0.965926)
    verts = getVerts(100,0,rollerBase(0)[2], rollerBase, cloverZ)
    edges = getEdges(verts)
    faces = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))
 
    curveObject = createMeshFromData('Curve', origin, verts, edges, [])

    setCameraKeyframes(verts, 20, 1, bpy.data.objects["Camera"])

    #cone2 = createMeshFromOperator('OpsCone', origin+Vector((0,2,0)), verts, faces)
    #cone3 = createMeshFromPrimitive('PrimCone', origin+Vector((0,4,0)))
 
    #rig1 = createArmatureFromData('DataRig', origin+Vector((0,6,0)))
    #rig2 = createArmatureFromOperator('OpsRig', origin+Vector((0,8,0)))
    #rig3 = createArmatureFromPrimitive('PrimRig', origin+Vector((0,10,0)))


def setCameraKeyframes(verts, pointsAhead, timeStep, obj_camera): 
    
    # rotation 
    frame = 1
    l = len(verts)

    # prepare a scene
    scn = bpy.context.scene
    scn.frame_start = frame
    scn.frame_end = frame + l*timeStep

    for i in range(l):
        frame += timeStep 
        if i < l-pointsAhead:
            

            # move to frame 17
            #bpy.ops.anim.change_frame(frame=frame)
            scn.frame_set(frame=frame)
        
            # select the created object -- broken 
            #bpy.ops.object.select_name(name=obj_camera.name)

            # do something with the object. A rotation, in this case
            #bpy.ops.transform.rotate(value=(-0.5*pi, ), axis=(-1, 0, 0))
            #bpy.ops.transform.translate(value=(-0.5*pi, ), axis=(-1, 0, 0))
            
            # update position, then from new position, rotation 
            obj_camera.select = True
            obj_camera.location = verts[i]
            look_at(obj_camera, verts[i+pointsAhead])

            # create keyframe
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')

            #create a point lights at intervals to illuminate tunnel 
            if frame % (3 * pointsAhead) == 0: 
                #addLamp(verts[i])


# http://blender.stackexchange.com/questions/5210/pointing-the-camera-in-a-particular-direction-programmatically
def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = Vector(point) - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()

#http://stackoverflow.com/questions/17355617/can-you-add-a-light-source-in-blender-using-python
def addLamp(point):

    scene = bpy.context.scene

    # Create new lamp datablock
    lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
    lamp_data.distance = 0.1
    
    # Create new object with our lamp datablock
    lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)

    # Link lamp object to the scene so it'll appear in this scene
    scene.objects.link(lamp_object)

    # Place lamp to a specified location
    lamp_object.location = point

    # And finally select it make active
    lamp_object.select = True
    scene.objects.active = lamp_object


"""def setCamera
# Test
obj_camera = bpy.data.objects["Camera"]
obj_other = bpy.data.objects["Cube"]

obj_camera.location = (5.0, 2.0, 3.0)
look_at(obj_camera, obj_other.matrix_world.to_translation())
"""

def initKeyframes():
    # prepare a scene
    scn = bpy.context.scene
    scn.frame_start = 1
    scn.frame_end = 101

    # move to frame 17
    bpy.ops.anim.change_frame(frame = 17)

    # select the created object
    bpy.ops.object.select_name(name="myTriangle")

    # do something with the object. A rotation, in this case
    bpy.ops.transform.rotate(value=(-0.5*pi, ), axis=(-1, 0, 0))

    # create keyframe
    bpy.ops.anim.keyframe_insert_menu(type='Rotation')


if __name__ == "__main__":
    run((0,0,0))


