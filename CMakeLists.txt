set (CMAKE_CXX_STANDARD 14)

file(GLOB SRC
    "Box2D/*.h"
    "Box2D/*.cpp"
    "Box2D/Collision/*.h"
    "Box2D/Collision/*.cpp"
    "Box2D/Collision/Shapes/*.h"
    "Box2D/Collision/Shapes/*.cpp"
    "Box2D/Common/*.h"
    "Box2D/Common/*.cpp"
    "Box2D/Dynamics/*.h"
    "Box2D/Dynamics/*.cpp"
    "Box2D/Dynamics/Contacts/*.h"
    "Box2D/Dynamics/Contacts/*.cpp"
    "Box2D/Dynamics/Joints/*.h"
    "Box2D/Dynamics/Joints/*.cpp"
    "Box2D/Particle/*.h"
    "Box2D/Particle/*.cpp"
    "Box2D/Rope/*.h"
    "Box2D/Rope/*.cpp"
)

if(ANDROID_ABI STREQUAL "armeabi-v7a")
  enable_language(ASM)
  set(SRC ${SRC}
      "Box2D/Particle/b2ParticleAssembly.neon.s"
  )
  set_source_files_properties(Box2D/Particle/b2ParticleAssembly.neon.s PROPERTIES COMPILE_FLAGS "${CMAKE_ASM_FLAGS} ${CMAKE_CXX_FLAGS} -x assembler-with-cpp")
endif()

add_definitions(-DLIQUIDFUN_EXTERNAL_LANGUAGE_API=1 -D_LIBCPP_ENABLE_CXX17_REMOVED_FEATURES)

add_library(_Box2D STATIC ${SRC}) 

target_include_directories(_Box2D PRIVATE 
.
${PYTHON_INCLUDE_DIRS}
)
