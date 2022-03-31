# Install script for directory: /home/naman/Documents/ROSProjects/shepherd_ws/src/multi_robot

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/naman/Documents/ROSProjects/shepherd_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_robot/action" TYPE FILE FILES "/home/naman/Documents/ROSProjects/shepherd_ws/src/multi_robot/action/goto.action")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_robot/msg" TYPE FILE FILES
    "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/multi_robot/msg/gotoAction.msg"
    "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/multi_robot/msg/gotoActionGoal.msg"
    "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/multi_robot/msg/gotoActionResult.msg"
    "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/multi_robot/msg/gotoActionFeedback.msg"
    "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/multi_robot/msg/gotoGoal.msg"
    "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/multi_robot/msg/gotoResult.msg"
    "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/multi_robot/msg/gotoFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_robot/cmake" TYPE FILE FILES "/home/naman/Documents/ROSProjects/shepherd_ws/build/multi_robot/catkin_generated/installspace/multi_robot-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/naman/Documents/ROSProjects/shepherd_ws/devel/include/multi_robot")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/roseus/ros/multi_robot")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/common-lisp/ros/multi_robot")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/naman/Documents/ROSProjects/shepherd_ws/devel/share/gennodejs/ros/multi_robot")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/naman/Documents/ROSProjects/shepherd_ws/devel/lib/python3/dist-packages/multi_robot")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/naman/Documents/ROSProjects/shepherd_ws/devel/lib/python3/dist-packages/multi_robot")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/naman/Documents/ROSProjects/shepherd_ws/build/multi_robot/catkin_generated/installspace/multi_robot.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_robot/cmake" TYPE FILE FILES "/home/naman/Documents/ROSProjects/shepherd_ws/build/multi_robot/catkin_generated/installspace/multi_robot-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_robot/cmake" TYPE FILE FILES
    "/home/naman/Documents/ROSProjects/shepherd_ws/build/multi_robot/catkin_generated/installspace/multi_robotConfig.cmake"
    "/home/naman/Documents/ROSProjects/shepherd_ws/build/multi_robot/catkin_generated/installspace/multi_robotConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/multi_robot" TYPE FILE FILES "/home/naman/Documents/ROSProjects/shepherd_ws/src/multi_robot/package.xml")
endif()

