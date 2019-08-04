cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

if(NOT CMAKE_BUILD_TYPE)
    message(STATUS "CMAKE_BUILD_TYPE not set, defaulting to RELEASE")
    set(CMAKE_BUILD_TYPE RELEASE)
else()
    message(STATUS "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")
endif()

message(STATUS "CMAKE_TOOLCHAIN_FILE: ${CMAKE_TOOLCHAIN_FILE}")

project(hawk-osd VERSION 1.0
  LANGUAGES C CXX ASM)

include(cmake/utils.cmake)

file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.h
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.hxx
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.c
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cxx
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.s
)

add_executable(${PROJECT_NAME})

target_include_directories(${PROJECT_NAME}
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_sources(${PROJECT_NAME}
    PRIVATE
        ${SOURCES}
)

set_target_properties(${PROJECT_NAME}
    PROPERTIES
        SUFFIX ".elf"
        C_STANDARD 11
        C_EXTENSIONS ON
        CMAKE_C_STANDARD_REQUIRED ON
        CXX_STANDARD 17
        CXX_EXTENSIONS ON
        CMAKE_CXX_STANDARD_REQUIRED ON
)

target_compile_options(${PROJECT_NAME}
    PRIVATE
        -Wall
        -Wextra
        -Wpedantic
#        -Werror
        -Wstrict-prototypes
        -Wmissing-prototypes
        -Wduplicated-cond
        -Wduplicated-branches
        -Wlogical-op
        -Wnull-dereference
        -Wshadow
        -Wconversion
        -Wsign-conversion
)

target_link_libraries(${PROJECT_NAME}
    PRIVATE stm32g474
)

target_link_options(${PROJECT_NAME}
    PRIVATE
        -Wl,-Map=${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.map,--cref
)

utils_target_generate_bin(${PROJECT_NAME})
utils_target_print_size(${PROJECT_NAME})

add_subdirectory(lib)
