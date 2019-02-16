## Set up


- `python -m virtualenv .venv`
- `source .venv/bin/activate`
- `mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS && cd ..`
- `pip install -r requirements.txt`
- `python server.py`
- In another terminal session: `python client.py`