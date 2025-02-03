# outline_boost

gong1 zhen4
gong kai zhen ming

vs dev-containers: https://code.visualstudio.com/docs/devcontainers/create-dev-container

swift base image: https://github.com/swiftlang/swift-docker/blob/f44060cdf224436060d2df98a5c3f63f2600de63/6.0/ubuntu/24.04/Dockerfile

virtualenv: https://www.geeksforgeeks.org/python-virtual-environment/

scan and transform: https://github.com/docongminh/scan-document/blob/master/README.md

phil_3_vision_mlx docs: https://josefalbers.github.io/Phi-3-Vision-MLX/module.html#functions

azure ai document intelligence sdk: https://learn.microsoft.com/en-us/python/api/azure-ai-documentintelligence/azure.ai.documentintelligence.models?view=azure-python-preview

ollama python examples: https://github.com/ollama/ollama-python/tree/main/examples

nicegui: https://nicegui.io/

### Notes
To run this project end-to-end:
1. Clone this repo and install Docker
2. Add your outline images in the `outlines` folder in numerical order.
3. Run `docker compose up` in the outline_boost directory.
4. json and md artifacts will be generated in `outline_builder`.

If you do not have a dedicated GPU it is recommended to run ollama separately on your host machine with. 

`ollama serve`

`docker compose --profile noGPU build` and 

`docker compose --profile noGPU up`

If you have a GPU, the default configuration is recommended.

`docker compose --profile default build` and

`docker compose --profile default up`

### TODOS:
- [X] Find ocr library/service to use
    - [X] Get raw text from images
    - [X] Extract individual points
- [ ] Create + build json representation of outline
- [X] Create class/tree schema for outline
- [X] Build class/tree structure for outline from images
- [ ] Build class/tree structure for outline from json (allows for editing json before creating final markdown.)
- [ ] Extract verse references for each outline point
    - [ ] Using regex
    - [X] Using SLM (Phi3? Llama 3.1?)
- [ ] Retrieve verses and populate each outline_block (verse_requestor only runs in container with swift compiler, ollama doesn't run in the container. Unable to run build_outline e2e.)
- [ ] Add verses to outline in-line
- [ ] Build docker compose to use ollama in container
- [ ] Add configurability to running ollama in a container or on host machine

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