from setuptools import setup, find_packages

setup(
    name="golf_society_backend",
    version="1.0.0",
    packages=find_packages(include=["backend", "backend.*"]),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
    ],
    entry_points={
        "console_scripts": [
            "golf-backend = backend.main:app",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

