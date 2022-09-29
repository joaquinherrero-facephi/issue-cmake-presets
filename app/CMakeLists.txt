cmake_minimum_required(VERSION 3.16)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(TARGET_NAME app)
project(${TARGET_NAME} LANGUAGES C CXX)

list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/build")
list(PREPEND CMAKE_PREFIX_PATH "${CMAKE_CURRENT_SOURCE_DIR}/build")

add_executable(${TARGET_NAME})

file(GLOB_RECURSE TARGET_SOURCES
    "${CMAKE_CURRENT_SOURCE_DIR}/main.cpp")

target_include_directories(${TARGET_NAME}
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}")

target_sources(${TARGET_NAME}
    PRIVATE
        ${TARGET_SOURCES})

find_package(hello REQUIRED)

target_link_libraries(${TARGET_NAME}
    PRIVATE
        hello::hello)
