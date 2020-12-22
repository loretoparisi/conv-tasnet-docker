# conv-tasnet-docker
This code is an adaption of [JusperLee's Conv-Tasnet Code](https://github.com/JusperLee/Conv-TasNet) to run over CPU in a Docker container.

## Build docker
```
docker build -f Dockerfile -t conv-tasnet .
docker run --rm -it -d -v `pwd`/src:/app -v /root:/root --name conv-tasnet-test conv-tasnet
docker exec -it conv-tasnet-test bash
```

## Run docker image
```
python Separation_wav.py -mix_scp /root/test.wav -yaml options/train/train.yml -model /root/best.pt -save_path ./checkpoint
```

### Requirement
- **Pytorch 1.3.0**
- **TorchAudio 0.3.1**
- **PyYAML 5.1.2**
- **tqmd**

### References
- [JusperLee's Conv-Tasnet Code](https://github.com/JusperLee/Conv-TasNet)
- [Luo Yi's Conv-Tasnet Code](https://github.com/naplab/Conv-TasNet)

