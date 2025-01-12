# outline_boost

vs dev-containers: https://code.visualstudio.com/docs/devcontainers/create-dev-container

swift base image: https://github.com/swiftlang/swift-docker/blob/f44060cdf224436060d2df98a5c3f63f2600de63/6.0/ubuntu/24.04/Dockerfile

virtualenv: https://www.geeksforgeeks.org/python-virtual-environment/

scan and transform: https://github.com/docongminh/scan-document/blob/master/README.md

phil_3_vision_mlx docs: https://josefalbers.github.io/Phi-3-Vision-MLX/module.html#functions

azure ai document intelligence sdk: https://learn.microsoft.com/en-us/python/api/azure-ai-documentintelligence/azure.ai.documentintelligence.models?view=azure-python-preview

Plan:
1. retrieval all paragraphs in the outline
2. for all paragraphs (starting from roman numeral 1)
    1. take last verse in previous paragraph if first verse in current paragraph has no book or chapter
    2. extract all verse references
    3. remember the last verse reference in the paragraph


Features
1. Scan images and save to a folder. Create outline from images.
2. Generates json representation of outline
3. Can edit and load json outline to generate markdown outline