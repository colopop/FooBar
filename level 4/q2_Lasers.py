def answer(dimensions, captain_position, badguy_position, distance):
   from math import ceil, sqrt, pow, copysign
   from fractions import gcd

   def getSmallestVector(vec):
      if vec[0] == 0:
         if vec[1] == 0:
            return (0,0)
         return (0,int(copysign(1,vec[1])))
      
      if vec[1] == 0:
            return (int(copysign(1,vec[0])),0)

      div = gcd(vec[0], vec[1]) * copysign(1,vec[1]) #gcd in python27 is incorrect
      return (int(vec[0]/div), int(vec[1]/div))
           
   def newpos(base_pos, frame_pos):
      new_x = int(pow(-1, frame_pos[0])) * base_pos[0] +  dimensions[0] * (frame_pos[0]+(1 if frame_pos[0] % 2 == 1 else 0))
      new_y = int(pow(-1, frame_pos[1])) * base_pos[1] + dimensions[1] * (frame_pos[1]+(1 if frame_pos[1] % 2 == 1 else 0))
      return (new_x, new_y)


   def samevector(v1, v2):
      #print v1, v2
      if v1[0] == 0:
         return v2[0] == 0 and copysign(v1[1], v2[1]) == v1[1]
      if v1[1] == 0:
         return v2[1] == 0 and copysign(v1[0], v2[0]) == v1[0]
      if v2[0] == 0:
         return v1[0] == 0 and copysign(v1[1], v2[1]) == v1[1]
      if v2[1] == 0:
         return v1[1] == 0 and copysign(v1[0], v2[0]) == v1[0]
      div1 = gcd(v1[0], v1[1])
      if div1 < 0: div1 *= -1
      div2 = gcd(v2[0], v2[1])
      if div2 < 0: div2 *= -1
      
      return (v1[0]/div1, v2[1]/div1) == (v2[0]/div2, v2[1]/div2)
      

   max_x = int ( ceil( float(distance) / dimensions[0] ) )
   max_y = int( ceil( float(distance) / dimensions[1] ) )
   f = max(max_x, max_y)

   dont_hit_me = set([])
   base_solution = getSmallestVector((badguy_position[0]-captain_position[0],badguy_position[1]-captain_position[1]))
   hit_me = set([])
   
   #generate all possible positions
   for xval in range(f):
      for yval in range(f):
         def getVector(x, y, bp):
            return (newpos(bp,(x, y))[0] - captain_position[0], newpos(bp,(x, y))[1] - captain_position[1])       
         
         toBadGuy = [getVector(xval, yval, badguy_position), getVector(-xval, yval, badguy_position), \
                     getVector(xval, -yval, badguy_position), getVector(-xval, -yval, badguy_position)]
         toCaptain = [getVector(xval, yval, captain_position), getVector(-xval, yval, captain_position), \
                      getVector(xval, -yval, captain_position), getVector(-xval, -yval, captain_position)]
         
         #locations that are too far away and duplicates will be weeded out
         for vc in toCaptain:
            if sqrt(vc[0]**2 + vc[1]**2) > distance: continue
            dont_hit_me.add(getSmallestVector(vc))         
         for vc in toBadGuy:
            if sqrt(vc[0]**2 + vc[1]**2) > distance: continue
            hit_me.add(getSmallestVector(vc))


   cpy = hit_me - dont_hit_me
   
   rejected = set([])

   #print "entering loop..."
   for solution in (hit_me & dont_hit_me):

#      # if a vector hits both the captain and the guard, see which one it hits first
      frame = (0,0) #current frame that laser is in
      frame_LR_border = (0, dimensions[0]) #left/right borders of current frame
      frame_BT_border = (0, dimensions[1]) #bottom/top borders of current frame
      laser_pos = (captain_position[0]+solution[0], captain_position[1]+solution[1])
#      print solution
      while True:
#         #follow the path of the laser. stop when we hit a target. hitting a target is guaranteed.
#         #update frame#
         

         if laser_pos == newpos(captain_position, frame):
            rejected.add(solution)
            break
         if laser_pos == newpos(badguy_position, frame):
            cpy.add(solution)
            break


         #if laser_pos[0] == frame_LR_border[0] or laser_pos[0] == frame_LR_border[1]:
            #if laser_pos[1] == frame_BT_border[0] or laser_pos[1] == frame_BT_border[1]:
             #  rejected.add(solution)
              # break

         
         if laser_pos[0] <= frame_LR_border[0]:
            gap = int ( ceil ( (frame_LR_border[0] - laser_pos[0]) / float(dimensions[0]) )) 
#            #out of bounds to the left
            frame = (frame[0] - gap, frame[1])
            frame_LR_border = (frame_LR_border[0] - gap*dimensions[0], frame_LR_border[1] - gap*dimensions[0])
#         
         elif laser_pos[0] >= frame_LR_border[1]:
            gap = int ( ceil ( -(frame_LR_border[1] - laser_pos[0]) / float(dimensions[0]) ))
#            #out of bounds to the right
            frame = (frame[0] + gap, frame[1])
            frame_LR_border = (frame_LR_border[0] + gap*dimensions[0], frame_LR_border[1] + gap*dimensions[0])
#         
         if laser_pos[1] <= frame_BT_border[0]:
            gap = int ( ceil ( (frame_BT_border[0] - laser_pos[1]) / float(dimensions[1]) ))
#            #out of bounds to the bottom
            frame = (frame[0], frame[1] - gap)
            frame_BT_border = (frame_BT_border[0] - gap*dimensions[1], frame_BT_border[1] - gap*dimensions[1])
#         
         elif laser_pos[1] >= frame_BT_border[1]:
            gap = int ( ceil ( -(frame_BT_border[1] - laser_pos[1]) / float(dimensions[1]) ))
#            #out of bounds to the top
            frame = (frame[0], frame[1] + gap)
            frame_BT_border = (frame_BT_border[0] + gap*dimensions[1], frame_BT_border[1] + gap*dimensions[1])
#
         #if (dimensions == [42,59] and solution == (51,38)):
            #print frame, frame_LR_border, frame_BT_border, laser_pos
#         #print frame
#         #print laser_pos, newpos(captain_position, frame), newpos(badguy_position, frame)
         if laser_pos == newpos(captain_position, frame):
            rejected.add(solution)
            break
         if laser_pos == newpos(badguy_position, frame):
            cpy.add(solution)
            break
#         for x in [-5,-4,-3,-2,-1,0,1,2,3,4,5]:
 #           for y in [-5,-4,-3,-2,-1,0,1,2,3,4,5]:
  #             if laser_pos == newpos(captain_position, (frame[0]+x, frame[1]+y)):
   #               rejected.add(solution)
    #              break
      #         if laser_pos == newpos(badguy_position, (frame[0]+x, frame[1]+y)):
     #             cpy.add(solution)
       #           break
#         #update laser
         laser_pos = (laser_pos[0] + solution[0], laser_pos[1] + solution[1])

   if len(cpy) == 0:
      return 0

   cpy.add(base_solution)
   #print rejected
   #print (hit_me - cpy) - rejected
   #print cpy
   return len(cpy)
   
   print answer([3,2],[1,1],[2,1],4)
   print answer([300,275],[150,150],[185,100],500)
   print answer([2,5],[1,2],[1,4],11)
   print answer([10,10],[4,4],[3,3],5000)
   print answer([23,10],[6,4],[3,2],23)
   print answer([42,59],[39,44],[6,34],5000)
