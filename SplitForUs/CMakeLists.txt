cmake_minimum_required(VERSION 3.19)
project(SplitForUs LANGUAGES CXX)

find_package(Qt6 6.5 REQUIRED COMPONENTS Core Widgets LinguistTools)
find_package(Qt6 REQUIRED COMPONENTS Widgets Network)

qt_standard_project_setup()

qt_add_executable(SplitForUs
    WIN32 MACOSX_BUNDLE
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
    startdialog.h startdialog.cpp startdialog.ui
    splashscreen.h splashscreen.cpp splashscreen.ui
    resources.qrc
)

qt_add_translations(
    TARGETS SplitForUs
    TS_FILES SplitForUs_tr_TR.ts
)


target_link_libraries(SplitForUs PRIVATE Qt6::Widgets Qt6::Network)
include(GNUInstallDirs)

install(TARGETS SplitForUs
    BUNDLE  DESTINATION .
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

qt_generate_deploy_app_script(
    TARGET SplitForUs
    OUTPUT_SCRIPT deploy_script
    NO_UNSUPPORTED_PLATFORM_ERROR
)
install(SCRIPT ${deploy_script})
