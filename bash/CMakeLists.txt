cmake_minimum_required(VERSION 2.8)
project($project_name)
set(CMAKE_MODULE_PATH \${CMAKE_MODULE_PATH} \${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules/ \${CMAKE_CURRENT_SOURCE_DIR}/SdlGui/MwLibrary2/cmake/Modules/)

if (MSVC)
	# Exception handler model.
	set(CMAKE_CXX_FLAGS_DEBUG \${CMAKE_CXX_FLAGS_DEBUG} /EHsc)
	set(CMAKE_CXX_FLAGS_RELEASE \${CMAKE_CXX_FLAGS_RELEASE} /EHsc)
	
	add_definitions(-D_CRT_SECURE_NO_WARNINGS -D_SCL_SECURE_NO_WARNINGS -DWIN32)
else ()
	set(CMAKE_CXX_FLAGS \"-std=c++14\")
	option(Debug \"Set projects to debug mode.\")
	if (Debug)
		set(CMAKE_BUILD_TYPE \"Debug\" CACHE INTERNAL \"Build type.\")
		add_definitions(-D_DEBUG)
	else ()
		set(CMAKE_BUILD_TYPE \"Release\" CACHE INTERNAL \"Build type.\")
	endif ()
endif ()

# Source files.
set(SOURCES
	main.cpp
)
	
# End of source files.

find_package(SDL2 REQUIRED)
find_package(SDL2_image REQUIRED)
find_package(SDL2_mixer REQUIRED)
find_package(SDL2_ttf REQUIRED)
find_package(SDL2_net REQUIRED)
find_package(GLEW REQUIRED)
find_package(OpenGL REQUIRED)

if (CMAKE_COMPILER_IS_GNUCXX)
	find_package(Threads REQUIRED) # Due to a bug, which forces the user to link to Threads when using #include <thread>.
endif (CMAKE_COMPILER_IS_GNUCXX)

add_subdirectory(SdlGui)
add_subdirectory(Signal)

file(COPY data/. DESTINATION \${CMAKE_CURRENT_BINARY_DIR}) # Copy data to build folder.

include_directories(
	\${SDL2_INCLUDE_DIRS} 
	\${SDL2_TTF_INCLUDE_DIRS}
	\${SDL2_MIXER_INCLUDE_DIRS} 
	\${SDL2_IMAGE_INCLUDE_DIRS}
	\${SDL2_NET_INCLUDE_DIRS}
	\${GLEW_INCLUDE_DIRS}
	SdlGui/src
	SdlGui/MwLibrary2/src
	SdlGui/Signal/src
)

add_executable($project_name \${SOURCES})

if (MSVC)
	set_target_properties($project_name PROPERTIES LINK_FLAGS_DEBUG \"/NODEFAULTLIB:msvcrt\")
	set_target_properties($project_name PROPERTIES LINK_FLAGS_RELEASE \"/SUBSYSTEM:windows\")
endif ()

target_link_libraries($project_name
	MwLibrary2
	Signal
	SdlGui	
	\${GLEW_LIBRARIES}
	\${OPENGL_LIBRARIES}
	\${SDL2_LIBRARIES}
	\${SDL2_TTF_LIBRARIES}
	\${SDL2_MIXER_LIBRARIES}
	\${SDL2_IMAGE_LIBRARIES}
	\${SDL2_NET_LIBRARIES}
	\${CMAKE_THREAD_LIBS_INIT})
