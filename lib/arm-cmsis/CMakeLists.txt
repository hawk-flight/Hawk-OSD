cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

add_library(arm-cmsis INTERFACE)

target_include_directories(arm-cmsis INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/CMSIS_5/CMSIS/Core/Include/)

file(GLOB_RECURSE ARM_CMSIS_SOURCES CONFIGURE_DEPENDS
    ${CMAKE_CURRENT_SOURCE_DIR}/CMSIS_5/CMSIS/Core/Include/*.h
)

target_sources(arm-cmsis INTERFACE ${ARM_CMSIS_SOURCES})