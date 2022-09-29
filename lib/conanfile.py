from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from configparser import ConfigParser
from os import path, remove
from shutil import which
from platform import system
import json

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class ConanFileClass(ConanFile):
    name = "hello"
    version = "1.0.0"
    license = "none"
    author = "none"
    url = "none"
    description = "none"
    topics = ("")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        toolchain_path = path.join(self.build_folder, "conan_toolchain.cmake")
        if path.exists(toolchain_path):
            remove(toolchain_path)
        generator = self.conf.get("tools.cmake.cmaketoolchain:generator", default="Ninja Multi-Config")
        tc = CMakeToolchain(self, generator=generator)
        tc.generate()

    def export_sources(self):
        self.copy("hello.h")
        self.copy("hello.cpp")
        self.copy("CMakeLists.txt")

    def build(self):
        # For environment management see:
        # https://docs.conan.io/en/1.52/migrating_to_2.0/recipes.html#the-environment-management
        cmake = CMake(self)
        print(f"GENERATOR: {cmake._generator}")
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include")
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        libname = self.name
        self.cpp_info.libs = [libname]
        self.cpp_info.set_property("cmake_find_mode", "both")
