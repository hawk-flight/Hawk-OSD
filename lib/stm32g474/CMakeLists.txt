cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

add_library(stm32g474 STATIC)

target_include_directories(stm32g474 PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_sources(stm32g474 
    PRIVATE
        font12.c
        font16.c
        font20.c
        font24.c
        font8.c
        startup_stm32g474xx.S
        system_stm32g4xx.c
    PUBLIC
        stm32g4xx.h
        stm32g474xx.h
        system_stm32g4xx.h
 )

 target_compile_definitions(stm32g474 PUBLIC STM32G474xx)

utils_target_set_linker_script(${CMAKE_PROJECT_NAME}
  ${CMAKE_CURRENT_SOURCE_DIR}/stm32g474.ld
)

target_link_libraries(stm32g474
    arm-cmsis
)
