from conans import ConanFile, AutoToolsBuildEnvironment, tools


class Lmdb(ConanFile):
    name = "lmdb"
    version = "0.9.18"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/Parquery/lmdb"
    homepage = "https://symas.com/lmdb/"
    license = "OpenLDAP Public License"
    options = {"shared": [True, False]}
    description = "Lightning Memory-Mapped Database"
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        if tools.os_info.is_linux:
            extension = "tar.gz"
        elif tools.os_info.is_windows:
            extension = "zip"
        else:
            raise RuntimeError("OS {} not supported".format(tools.os_info.os_version_name))

        zip_name = "LMDB_{}.{}".format(self.version, extension)
        zip_url = "https://github.com/LMDB/lmdb/archive/{}".format(zip_name)

        tools.download(url=zip_url, filename=zip_name)
        tools.unzip(filename=zip_name, destination=".")
        tools.replace_in_file(file_path="lmdb-LMDB_{}/libraries/liblmdb/Makefile".format(self.version),
                              search="$(CC) $(LDFLAGS) -pthread -shared -o $@ mdb.lo midl.lo $(SOLIBS)",
                              replace="$(CC) $(LDFLAGS) -pthread -shared -Wl,-soname=liblmdb.so -o $@ mdb.lo midl.lo $(SOLIBS)")

    def build(self):
        with tools.chdir("lmdb-LMDB_{}/libraries/liblmdb".format(self.version)):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.make()

    def package(self):
        self.copy(pattern="*.h*", src=".", dst="include", keep_path=False)
        if self.options.shared:
            self.copy(pattern="*.dll", src="", dst="lib", keep_path=False)
            self.copy(pattern="*.so", src="", dst="lib", keep_path=False)
            self.copy(pattern="*.dylib", src="", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.lib", src="", dst="lib", keep_path=False)
            self.copy(pattern="*.a", src="", dst="lib", keep_path=False)
            self.copy(pattern="*.o", src="", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs.append("lmdb")
        self.cpp_info.includedirs = ['include']


