from setuptools import setup, find_packages

setup(
    name="edge_learner",
    version="1.0.0",
    description="Continuous self-learning pipeline for YOLOv8 on RK3588",
    author="Akhil B",
    author_email="akhil@edgeble.ai",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "torch>=2.1.0",
        "torchvision>=0.16.0",
        "ultralytics>=8.0.0",
        "onnx>=1.14.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "scikit-learn>=1.3.0",
        "Pillow>=10.0.0",
        "opencv-python>=4.8.0",
        "pyyaml>=6.0",
        "apscheduler>=3.10.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": ["pytest>=7.4.0", "pytest-cov>=4.1.0", "black>=23.0.0", "ruff>=0.1.0"],
        "cloud": ["boto3>=1.28.0", "github3.py>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "edge-learner-infer=edge_learner.inference.frame_pipeline:main",
            "edge-learner-run=edge_learner.orchestrator.pipeline_runner:main",
            "edge-learner-monitor=edge_learner.orchestrator.health_monitor:main",
        ]
    },
)
