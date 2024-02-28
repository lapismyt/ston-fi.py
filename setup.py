from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name = "stonfi",
        version = "0.1",
        packages = find_packages(include=["stonfi", "stonfi.*"]),
        install_requires = [
            "requests",
            "tonsdk",
            "tvm_valuetypes"
        ]
    )
