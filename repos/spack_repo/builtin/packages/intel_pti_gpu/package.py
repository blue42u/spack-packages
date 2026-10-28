# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class IntelPtiGpu(CMakePackage):
    """Intel Profiling Tools Interface (PTI) for GPU: an SDK for tracing and
    profiling applications running on Intel GPUs via Level Zero and SYCL."""

    homepage = "https://github.com/intel/pti-gpu"
    git = "https://github.com/intel/pti-gpu.git"

    license("MIT")

    version("master", branch="master")
    version("1.2.0", commit="fdc44f65ccfc4c75f951a8f01b1ef9326223aaaf")
    version("1.1.0", commit="875cdcde8d0a7ab9efb0c671a6e4f85f0b7384f6")
    version("1.0.1", commit="445c71f0d867c57be25e632d17ffd0ea71a6fcdd")

    root_cmakelists_dir = "sdk"

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.14:", type="build")
    depends_on("python", type="build")

    depends_on("oneapi-level-zero@1.32.0:1.34", when="@1.1:")
    depends_on("oneapi-level-zero@1.28.0:1.34", when="@:1.0")
    depends_on("spdlog@1.17.0:")

    # ITT is linked statically into PTI and is not packaged in Spack
    resource(
        name="ittapi",
        url="https://github.com/intel/ittapi/archive/refs/tags/v3.26.8.tar.gz",
        sha256="0b8b387b02b3ea1111ecb6dcb2295558dccb18dcbb0192d401c9db6a6715b28c",
        destination="resources",
        placement="ittapi",
    )

    def cmake_args(self):
        return [
            self.define("PTI_BUILD_TESTING", False),
            self.define("PTI_BUILD_SAMPLES", False),
            self.define("PTI_BUILD_URGEMM", False),
            self.define("BUILD_TESTING", False),
            self.define("FETCHCONTENT_FULLY_DISCONNECTED", True),
            self.define(
                "FETCHCONTENT_SOURCE_DIR_ITTAPI",
                join_path(self.stage.source_path, "resources", "ittapi"),
            ),
        ]
