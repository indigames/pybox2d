cmake_minimum_required(VERSION 2.8.12)

project(Box2D)
set (CMAKE_CXX_STANDARD 14)

# [IGE]: tweaks for platforms
if(DEFINED ANDROID_PLATFORM)
    set (ANDROID 1)
    if(ANDROID_ABI STREQUAL "armeabi-v7a")
        add_compile_options(-marm -march=armv7-a -mtune=cortex-a15 -mfpu=neon-fp16 -mfloat-abi=softfp)
    elseif(ANDROID_ABI STREQUAL "x86")
        add_compile_options(-march=atom -m32 -msse -msse2 -msse3 -mssse3 -mfpmath=sse -mstackrealign)
    elseif(ANDROID_ABI STREQUAL "arm64-v8a")
        add_compile_options(-march=armv8-a+simd+sve -mtune=cortex-a53 -D__ARM_NEON -D__ARM_NEON__)
    elseif(ANDROID_ABI STREQUAL "x86_64")
        add_compile_options(-march=atom -m64 -msse -msse2 -msse3 -mssse3 -msse4.1 -msse4.2 -mfpmath=sse)
    endif()
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
        add_compile_options(-g0 -Ofast)
    else(CMAKE_BUILD_TYPE STREQUAL "Debug")
        add_compile_options(-Og)
    endif()
elseif(MSVC)
    add_compile_options(/MP /MD)
elseif(IOS)
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
        add_compile_options(-g0 -Ofast)
    endif()
endif()
# [/IGE]

# [IGE]: try include conan build config
if(EXISTS ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
endif()
# [/IGE]

set(PYTHON_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS}")

file(GLOB SRC
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Collision/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Collision/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Collision/Shapes/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Collision/Shapes/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Common/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Common/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Dynamics/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Dynamics/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Dynamics/Contacts/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Dynamics/Contacts/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Dynamics/Joints/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Dynamics/Joints/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Particle/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Particle/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Rope/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Rope/*.cpp"
)

if(ANDROID_ABI STREQUAL "armeabi-v7a")
  enable_language(ASM)
  set(SRC ${SRC}
      "${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Particle/b2ParticleAssembly.neon.s"
  )
  set_source_files_properties(${CMAKE_CURRENT_SOURCE_DIR}/Box2D/Particle/b2ParticleAssembly.neon.s PROPERTIES COMPILE_FLAGS "${CMAKE_ASM_FLAGS} ${CMAKE_CXX_FLAGS} -x assembler-with-cpp")
endif()

add_definitions(-DLIQUIDFUN_EXTERNAL_LANGUAGE_API=1 -D_LIBCPP_ENABLE_CXX17_REMOVED_FEATURES)

add_library(Box2D STATIC ${SRC})

target_include_directories(Box2D PRIVATE . ${PYTHON_INCLUDE_DIRS}
)
