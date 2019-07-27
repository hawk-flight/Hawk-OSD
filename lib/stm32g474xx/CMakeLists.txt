cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

add_library(stm32g474xx STATIC)

target_include_directories(stm32g474xx PUBLIC .)
target_sources(stm32g474xx PRIVATE
  font12.c
  font16.c
  font20.c
  font24.c
  font8.c
  startup_stm32g474xx.S
  system_stm32g4xx.c)
