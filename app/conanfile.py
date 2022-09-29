from conans import ConanFile, tools
from conan.tools.cmake import CMakeToolchain, cmake_layout
from configparser import ConfigParser
from os import path, remove
from shutil import which
from platform import system
import json

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class ConanFileClass(ConanFile):
    name = "app"
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
    generators = ["CMakeDeps"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def requirements(self):
        self.requires("hello/1.0.0@")

    def generate(self):
        toolchain_path = path.join(self.build_folder, "conan_toolchain.cmake")
        if path.exists(toolchain_path):
            remove(toolchain_path)

        tc = CMakeToolchain(self)
        tc.generate()

    def layout(self):
        cmake_layout(self)

    def export_sources(self):
        self.copy("*.h")
        self.copy("*.cpp")
        self.copy("CMakeLists.txt")

    def build(self):
        generator = self.conf.get("tools.cmake.cmaketoolchain:generator", default="Ninja Multi-Config")
        lower_build_type = str(self.settings.build_type).lower()

        env_vars = {}

        # Explicitly add vcvars to the environment. Do not known why is automatically done before calling build() on conan side
        if self.settings.os == "Windows":
            env_vars = tools.vcvars_dict(self)

        with tools.environment_append(env_vars):
            with tools.chdir(self.source_folder):
                cmd_cmake_config = f"cmake --preset {lower_build_type}" if generator == "Unix Makefiles" else "cmake --preset default"
                self.run(cmd_cmake_config)
                self.run(f"cmake --build --preset {lower_build_type}")

    def package(self):
        self.copy("app", dst="bin", src=str(self.settings.build_type), keep_path=False)

    def package_info(self):
        libname = self.name
        self.cpp_info.libs = [libname]
        self.cpp_info.set_property("cmake_find_mode", "both")
